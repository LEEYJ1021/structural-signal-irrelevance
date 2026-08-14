"""
Step M -- Pre-registration diagnostic for RQ3 (at what point after
registration is it most efficient to flag a low-growth ad group for
intervention?).

This is a *diagnostic*, not the confirmatory RQ3 result: it exists to
establish, before committing to a single "optimal decision day" claim,
(1) how accurately an early-signal model actually discriminates
eventual low-growth ad groups at each candidate decision cutoff --
measured directly, no assumptions required -- and (2) whether an
"expected uplift" ranking across cutoffs is robust to the intervention-
effect assumptions it necessarily depends on, since this dataset
contains no record of an actual intervention ever being applied.

Historical finding (kept here as a comment, not a hard-coded
assumption): the first two uplift-simulation designs tried here were
both found to be mathematically incapable of producing a different
optimal-cutoff ranking regardless of the assumed effect size --
because the assumed per-unit effect (delta) and its probability of
success (efficacy) entered the expected-uplift formula as constants
multiplying every (cutoff, threshold) combination identically, so the
argmax could never move. The precision/recall/lift table (Step M3) is
therefore the only part of this diagnostic reported as a *measured*
result; everything downstream of an assumed delta/efficacy is reported
as an illustrative what-if, never as a policy conclusion. See
docs/METHODOLOGY_NOTES.md for the full trace of this correction.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.coldstart_v5._sample_construction import apply_maturity_metrics
from src.coldstart_v5.step_l_rq2_feature_engineering import load_perf_detail, FEATURE_COLS_BASE
from src.utils.io import load_config


def build_decision_window_features(sample: pd.DataFrame, perf: pd.DataFrame, obs_end,
                                     cutoff_days: int, total_horizon_days: int) -> pd.DataFrame:
    """Build early-window (0..cutoff_days) operating-signal features and
    a matched later-window (cutoff_days..total_horizon_days) growth
    target, holding the *total* horizon fixed across all candidate
    cutoffs so that comparisons across cutoffs are never confounded by
    a shifting ad-group population (see Step M1's cross-cutoff sample
    check)."""
    later_days = total_horizon_days - cutoff_days
    first_active_map = sample.set_index("ad_group_id")["perf_first_active"]
    customer_map = sample.set_index("ad_group_id")["customer_id"]

    rows = []
    for adg_id, first_active in first_active_map.items():
        early_end = first_active + pd.Timedelta(days=cutoff_days - 1)
        later_start, later_end = early_end + pd.Timedelta(days=1), early_end + pd.Timedelta(days=later_days)
        if later_end > obs_end:
            continue  # keeps every cutoff's sample restricted to fully-elapsed windows

        sub = perf[perf["ad_group_id"] == adg_id]
        early = sub[(sub["date"] >= first_active) & (sub["date"] <= early_end)]
        later = sub[(sub["date"] >= later_start) & (sub["date"] <= later_end)]

        early_daily = early.set_index("date")["cost"].reindex(
            pd.date_range(first_active, early_end), fill_value=0.0
        )
        day_idx = np.arange(len(early_daily))
        coverage = (early_daily > 0).mean()
        slope = np.polyfit(day_idx, early_daily.values, 1)[0] if early_daily.sum() > 0 and len(day_idx) >= 2 else 0.0

        impr, click = early["impression"].sum(), early["click"].sum()
        conv = early.get("conversion_count", pd.Series(dtype=float)).sum()
        cost_sum = early["cost"].sum()
        ctr = click / impr if impr > 0 else np.nan
        cvr = conv / click if click > 0 else np.nan
        roas = early.get("sales", pd.Series(dtype=float)).sum() / cost_sum if cost_sum > 0 else np.nan

        growth_target = np.log1p(later["cost"].sum()) - np.log1p(cost_sum)
        rows.append({
            "ad_group_id": adg_id, "customer_id": customer_map.get(adg_id), "coverage": coverage,
            "mean_cost": early_daily.mean(), "std_cost": early_daily.std() or 0.0, "early_slope": slope,
            "ctr": ctr, "cvr": cvr, "roas": roas, "growth_target": growth_target,
        })

    feat_df = pd.DataFrame(rows)
    if len(feat_df) == 0:
        return feat_df
    for col in ["ctr", "cvr", "roas"]:
        feat_df[f"{col}_missing"] = feat_df[col].isna().astype(int)
        feat_df[col] = feat_df[col].fillna(feat_df[col].median())
    return feat_df


def loco_predict(feat_df: pd.DataFrame, feature_cols: list[str], seed: int) -> np.ndarray:
    """Out-of-fold Leave-One-Customer-Out predictions -- the same
    information-leakage-safe design used throughout Step L, so that
    Step M's precision/recall diagnostics are never inflated by a
    customer appearing in both its own train and test fold."""
    groups = feat_df["customer_id"].values
    X, y = feat_df[feature_cols].values, feat_df["growth_target"].values
    logo = LeaveOneGroupOut()
    preds = np.full(len(feat_df), np.nan)
    for tr, te in logo.split(feat_df, groups=groups):
        scaler = StandardScaler().fit(X[tr])
        model = Ridge(alpha=1.0, random_state=seed).fit(scaler.transform(X[tr]), y[tr])
        preds[te] = model.predict(scaler.transform(X[te]))
    return preds


def run(cfg: dict):
    ctx = step_a(cfg)
    adgroup_dim, coldstart, usable, obs_end = ctx["adgroup_dim"], ctx["coldstart"], ctx["usable"], ctx["obs_end"]
    icfg = cfg["coldstart_diagnostics"]["intervention"]
    seed = cfg["random_seed"]

    excl = set(cfg["sample_definition"].get("known_test_account_ids", []))
    usable_m = apply_maturity_metrics(usable, adgroup_dim, coldstart)
    sample = usable_m[~usable_m["customer_id"].isin(excl)].copy()
    print(f"[step_m] sample after test-account exclusion: {len(sample)} ad groups, "
          f"{sample['customer_id'].nunique()} customers")

    perf = load_perf_detail(cfg, set(sample["ad_group_id"]))

    total_horizon = icfg["total_horizon_days"]
    cutoffs = icfg["decision_cutoffs_days"]
    thresholds = icfg["flag_thresholds"]
    reliable_thresholds = icfg.get("reliable_flag_thresholds", thresholds)

    # --- M1/M2: build datasets per cutoff on a fixed total horizon, predict ---
    datasets = {}
    adg_id_sets = []
    for cutoff in cutoffs:
        feat_df = build_decision_window_features(sample, perf, obs_end, cutoff, total_horizon)
        if len(feat_df) >= 20 and feat_df["customer_id"].nunique() >= 5:
            feat_df["pred_growth"] = loco_predict(feat_df, FEATURE_COLS_BASE, seed)
        datasets[cutoff] = feat_df
        adg_id_sets.append(set(feat_df.get("ad_group_id", pd.Series(dtype=str))))
        rho = (stats.spearmanr(feat_df["growth_target"], feat_df["pred_growth"])[0]
               if "pred_growth" in feat_df.columns else np.nan)
        print(f"[step_m] cutoff={cutoff}d: n={len(feat_df)}, out-of-fold rho={rho:.3f}")

    if len(set(map(frozenset, adg_id_sets))) != 1:
        print("[step_m] WARNING: cutoffs do not share an identical ad-group set -- "
              "cross-cutoff comparisons may be confounded by sample drift")

    # --- M3: precision/recall/lift -- the only *measured* (assumption-free) result ---
    m3_rows = []
    for cutoff, feat_df in datasets.items():
        if "pred_growth" not in feat_df.columns:
            continue
        for th in thresholds:
            pred_cut, true_cut = feat_df["pred_growth"].quantile(th), feat_df["growth_target"].quantile(th)
            flagged, true_low = feat_df["pred_growth"] <= pred_cut, feat_df["growth_target"] <= true_cut
            n_flagged, n_true_low, n_tp = flagged.sum(), true_low.sum(), (flagged & true_low).sum()
            precision = n_tp / n_flagged if n_flagged else np.nan
            recall = n_tp / n_true_low if n_true_low else np.nan
            m3_rows.append({
                "cutoff": cutoff, "threshold": th, "n_flagged": int(n_flagged),
                "precision": precision, "recall": recall, "lift": precision / th if th else np.nan,
                "reliable": th in reliable_thresholds,
            })
    m3 = pd.DataFrame(m3_rows)
    print(f"[step_m] precision/recall/lift (measured, no intervention-effect assumption):\n"
          f"{m3.to_string(index=False)}")
    print("[step_m] use only rows with reliable=True in reported results -- unreliable rows correspond "
          "to threshold bands narrow enough to be dominated by ties in growth_target (zero-spend ad groups).")

    # --- M4/M5: illustrative what-if uplift, explicitly labeled as non-causal ---
    print("\n[step_m] NOTE: the following expected-uplift figures assume an intervention effect "
          "(delta, efficacy) never observed in this data -- they are what-if illustrations, not results.")
    delta, efficacy = icfg["baseline_delta"], icfg["baseline_efficacy"]
    m4_rows = []
    for cutoff, feat_df in datasets.items():
        if "pred_growth" not in feat_df.columns:
            continue
        for th in reliable_thresholds:
            pred_cut, true_cut = feat_df["pred_growth"].quantile(th), feat_df["growth_target"].quantile(th)
            flagged, true_low = feat_df["pred_growth"] <= pred_cut, feat_df["growth_target"] <= true_cut
            n_flagged, n_tp = flagged.sum(), (flagged & true_low).sum()
            uplift = n_tp * efficacy * delta
            m4_rows.append({"cutoff": cutoff, "threshold": th, "n_flagged": int(n_flagged),
                             "expected_uplift": uplift, "uplift_per_flag": uplift / n_flagged if n_flagged else np.nan})
    m4 = pd.DataFrame(m4_rows)
    print(f"[step_m] illustrative what-if uplift (delta={delta}, efficacy={efficacy}):\n"
          f"{m4.to_string(index=False)}")
    print("[step_m] WARNING: because uplift = n_true_positive * efficacy * delta and (efficacy, delta) "
          "multiply every (cutoff, threshold) cell identically, the argmax over cutoff/threshold is "
          "*mathematically incapable* of changing across any efficacy/delta assumption -- do not report "
          "an 'optimal' cutoff from this table alone. See docs/METHODOLOGY_NOTES.md.")

    out_dir = Path(cfg["paths"]["intermediate_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    m3.to_csv(out_dir / "step_m_precision_recall_lift.csv", index=False)
    m4.to_csv(out_dir / "step_m_illustrative_uplift.csv", index=False)
    print(f"[step_m] wrote outputs to {out_dir}")

    return {"per_cutoff_datasets": datasets, "precision_recall_lift": m3, "illustrative_uplift": m4}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
