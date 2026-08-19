"""
supplementary_robustness/04_design_artifact_future_work.py

Formalizes the early-flagging decision rule implied by the within-customer
result in root README Section 3.3 as an explicit design artifact, then
backtests it against (a) a naive account size/tenure rule and (b) random
flagging, across a grid of sample-definition specifications.

Supports: root README.md Section 3.4.

Key methodological point demonstrated by this script (not just described):
account maturity is a customer-level constant, so within-customer demeaning
of any prediction built purely from it collapses to floating-point zero.
early_warning_flag_backtest() detects this degeneracy explicitly rather than
silently producing an uninterpretable "naive wins/loses" comparison -- see
04_design_artifact_future_work.md for why this matters and how it changes
the reported conclusion (own-signal vs. random baseline, not own-signal vs.
naive, once naive is confirmed to carry no within-customer information).

Expected inputs (see data/README.md for schema):
  - adgroup_dim.tsv    (customer_id, ad_group_id, regTm, ...)
  - ad_performance.tsv (date, customer_id, ad_group_id, cost, ...)

Output:
  - supplementary_robustness/outputs/04_design_artifact_future_work.json
  - supplementary_robustness/outputs/04_backtest_grid.csv
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path("data")
ADGROUP_DIM_PATH = DATA_DIR / "adgroup_dim.tsv"
PERF_PANEL_PATH = DATA_DIR / "ad_performance.tsv"
OUTPUT_JSON_PATH = Path("supplementary_robustness/outputs/04_design_artifact_future_work.json")
OUTPUT_GRID_PATH = Path("supplementary_robustness/outputs/04_backtest_grid.csv")

RANDOM_STATE = 2026
EXCLUDE_TEST_ACCOUNTS: set[str] = set()  # populate with known non-representative test-account IDs, if any

FEATURE_COLS = ["coverage", "mean_cost", "std_cost", "early_slope"]
FLAG_THRESHOLD = 0.30
N_BOOT = 2000
MIN_CUSTOMERS_FOR_SPEC = 20
MIN_ADGROUPS_FOR_SPEC = 60
MIN_OBS_PER_CUSTOMER_FOR_WITHIN = 2
NAIVE_DEGENERATE_STD_THRESHOLD = 1e-6

# (min_active_days, early_window_days, later_window_days)
BACKTEST_GRID = [
    (7, 14, 14), (5, 14, 14), (5, 10, 10), (5, 7, 14),
    (7, 10, 10), (7, 7, 14), (10, 14, 14), (5, 14, 21), (7, 14, 21),
]


# ---------------------------------------------------------------------------
# The design artifact itself
# ---------------------------------------------------------------------------
def early_warning_flag(predicted_growth_rank_percentile: float, day_since_registration: int,
                        flag_threshold: float = FLAG_THRESHOLD, min_day: int = 7, max_day: int = 21) -> dict:
    """Ad-Group Early Warning Flagging Rule.

    Design principles:
      DP1. Base flagging solely on the ad group's own early-period signal
           (coverage, spend trend, CTR/CVR) -- never on account-level history.
      DP2. Evaluate at any point within a bounded window (day 7-21) rather
           than committing to a single fixed day.
      DP3. Threshold on relative rank (percentile) within the observed
           cohort, not on an absolute growth value.

    This rule is grounded in the *continuous-scale* within-customer result
    (root README Section 3.3). Its binary-flagging empirical backtest below
    did not produce a confirmed advantage at the sample sizes available here
    -- see the module docstring and 04_design_artifact_future_work.md.
    """
    if not (min_day <= day_since_registration <= max_day):
        return {"flag": False, "reason": f"outside observation window ({min_day}-{max_day} days)"}
    if predicted_growth_rank_percentile <= flag_threshold:
        return {"flag": True, "reason": f"bottom {flag_threshold:.0%} predicted growth -- review candidate",
                "confidence_note": ("Equal confidence across day 7-21 (no single day is "
                                     "statistically distinguishable as optimal, per RQ3). The "
                                     "binary-flagging empirical backtest is future work, not a "
                                     "confirmed result -- see supplementary_robustness/"
                                     "04_design_artifact_future_work.md.")}
    return {"flag": False, "reason": "predicted growth at or above threshold -- normal range"}


# ---------------------------------------------------------------------------
# Trajectory-feature construction (mirrors the coldstart_v5 pipeline's
# early/later window feature builder, kept self-contained here)
# ---------------------------------------------------------------------------
def clean_id(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)


def load_and_prepare() -> tuple[pd.DataFrame, pd.DataFrame, pd.Timestamp, pd.Timestamp]:
    adgroup_dim = pd.read_csv(ADGROUP_DIM_PATH, sep="\t", low_memory=False)
    adgroup_dim = adgroup_dim.rename(columns={c: "regTm" for c in adgroup_dim.columns if c.lower().startswith("reg")
                                               and "regTm" not in adgroup_dim.columns})
    adgroup_dim["customer_id"] = clean_id(adgroup_dim["customer_id"])
    adgroup_dim["ad_group_id"] = clean_id(adgroup_dim["ad_group_id"])
    adgroup_dim["regTm"] = pd.to_datetime(adgroup_dim["regTm"], errors="coerce")
    adgroup_dim = adgroup_dim.dropna(subset=["regTm"])

    panel = pd.read_csv(PERF_PANEL_PATH, sep="\t", low_memory=False, dtype={"customer_id": str})
    panel["customer_id"] = clean_id(panel["customer_id"])
    panel["ad_group_id"] = clean_id(panel["ad_group_id"])
    panel["date"] = pd.to_datetime(panel["date"], errors="coerce").dt.normalize()
    panel["cost"] = pd.to_numeric(panel["cost"], errors="coerce").fillna(0)
    panel = panel.dropna(subset=["date"])
    panel_cost = panel.groupby(["ad_group_id", "customer_id", "date"], as_index=False)["cost"].sum()

    obs_start, obs_end = panel_cost["date"].min(), panel_cost["date"].max()

    adgroup_dim = adgroup_dim.merge(
        panel_cost.groupby("ad_group_id")["date"].agg(perf_first_active="min", perf_last_active="max"),
        on="ad_group_id", how="inner")

    return adgroup_dim, panel_cost, obs_start, obs_end


def build_usable_sample(adgroup_dim: pd.DataFrame, obs_start: pd.Timestamp, obs_end: pd.Timestamp,
                         min_active_days: int) -> pd.DataFrame:
    """Ad groups registered strictly within the observation window
    (genuine cold-start), with at least `min_active_days` of activity."""
    is_true_coldstart = (adgroup_dim["regTm"] >= obs_start + pd.Timedelta(days=1)) & \
                         (adgroup_dim["regTm"] <= obs_end)
    coldstart = adgroup_dim.loc[is_true_coldstart].copy()
    coldstart["active_days"] = (coldstart["perf_last_active"] - coldstart["perf_first_active"]).dt.days + 1
    usable = coldstart[coldstart["active_days"] >= min_active_days].copy()
    usable = usable[~usable["customer_id"].isin(EXCLUDE_TEST_ACCOUNTS)]

    alltime_count = adgroup_dim.groupby("customer_id").size().rename("all_time_count")
    usable = usable.merge(alltime_count, on="customer_id", how="left")
    return usable


def build_window_features(usable: pd.DataFrame, panel_cost: pd.DataFrame, obs_end: pd.Timestamp,
                           early_days: int, later_days: int) -> pd.DataFrame:
    rows = []
    for _, row in usable.iterrows():
        adg_id, first_active = row["ad_group_id"], row["perf_first_active"]
        early_end = first_active + pd.Timedelta(days=early_days - 1)
        later_start = early_end + pd.Timedelta(days=1)
        later_end = later_start + pd.Timedelta(days=later_days - 1)
        if later_end > obs_end:
            continue
        sub = panel_cost[panel_cost["ad_group_id"] == adg_id]
        early = sub[(sub["date"] >= first_active) & (sub["date"] <= early_end)]
        later = sub[(sub["date"] >= later_start) & (sub["date"] <= later_end)]

        early_daily = early.set_index("date")["cost"].reindex(
            pd.date_range(first_active, early_end), fill_value=0.0)
        day_idx = np.arange(len(early_daily))
        coverage = (early_daily > 0).mean()
        mean_cost = early_daily.mean()
        std_cost = early_daily.std()
        slope = (np.polyfit(day_idx, early_daily.values, 1)[0]
                 if early_daily.sum() > 0 and len(day_idx) >= 2 else 0.0)
        growth_target = np.log1p(later["cost"].sum()) - np.log1p(early["cost"].sum())

        rows.append({
            "ad_group_id": adg_id, "customer_id": row["customer_id"],
            "coverage": coverage, "mean_cost": mean_cost,
            "std_cost": std_cost if not np.isnan(std_cost) else 0.0,
            "early_slope": slope, "growth_target": growth_target,
            "all_time_count": row["all_time_count"],
        })
    return pd.DataFrame(rows)


def compute_loco_predictions(feat_df: pd.DataFrame, feature_cols: list[str],
                              target_col: str = "growth_target") -> np.ndarray:
    """Leave-one-customer-out Ridge predictions -- guards against
    within-customer information leakage across train/test splits."""
    groups = feat_df["customer_id"].values
    X = feat_df[feature_cols].values
    y = feat_df[target_col].values
    logo = LeaveOneGroupOut()
    y_pred = np.full(len(feat_df), np.nan)
    for train_idx, test_idx in logo.split(feat_df, groups=groups):
        scaler = StandardScaler().fit(X[train_idx])
        model = Ridge(alpha=1.0, random_state=RANDOM_STATE).fit(scaler.transform(X[train_idx]), y[train_idx])
        y_pred[test_idx] = model.predict(scaler.transform(X[test_idx]))
    return y_pred


def precision_recall(flag: np.ndarray, actual: np.ndarray) -> tuple[float, float]:
    flag, actual = np.asarray(flag, dtype=bool), np.asarray(actual, dtype=bool)
    tp = int((flag & actual).sum())
    fp = int((flag & ~actual).sum())
    fn = int((~flag & actual).sum())
    precision = tp / (tp + fp) if (tp + fp) > 0 else np.nan
    recall = tp / (tp + fn) if (tp + fn) > 0 else np.nan
    return precision, recall


def within_customer_demean(feat_df: pd.DataFrame, col: str) -> pd.Series:
    return feat_df[col] - feat_df.groupby("customer_id")[col].transform("mean")


# ---------------------------------------------------------------------------
# Backtest for a single (min_active_days, early_days, later_days) spec
# ---------------------------------------------------------------------------
def run_backtest_spec(usable: pd.DataFrame, panel_cost: pd.DataFrame, obs_end: pd.Timestamp,
                       spec_label: str, early_days: int, later_days: int,
                       flag_threshold: float = FLAG_THRESHOLD, n_boot: int = N_BOOT) -> dict:
    feat = build_window_features(usable, panel_cost, obs_end, early_days, later_days)
    n_rows, n_cust = len(feat), feat["customer_id"].nunique() if len(feat) else 0
    if n_rows < MIN_ADGROUPS_FOR_SPEC or n_cust < MIN_CUSTOMERS_FOR_SPEC:
        return {"spec_label": spec_label, "note": f"insufficient sample (n={n_rows}, customers={n_cust})"}

    alltime_map = usable.drop_duplicates("customer_id").set_index("customer_id")["all_time_count"]
    log_maturity = np.log1p(alltime_map)
    if log_maturity.std() == 0 or np.isnan(log_maturity.std()):
        return {"spec_label": spec_label, "note": "zero variance in account maturity"}
    maturity_z_map = (log_maturity - log_maturity.mean()) / log_maturity.std()
    feat["maturity_z"] = feat["customer_id"].map(maturity_z_map)
    feat = feat.dropna(subset=["maturity_z"] + FEATURE_COLS + ["growth_target"]).reset_index(drop=True)

    obs_per_cust = feat.groupby("customer_id")["ad_group_id"].transform("count")
    feat_wc = feat[obs_per_cust >= MIN_OBS_PER_CUSTOMER_FOR_WITHIN].copy()
    n_cust_wc = feat_wc["customer_id"].nunique()
    if len(feat_wc) < 30 or n_cust_wc < 5:
        return {"spec_label": spec_label,
                "note": f"insufficient within-customer comparison sample (n={len(feat_wc)}, customers={n_cust_wc})"}

    feat["own_pred"] = compute_loco_predictions(feat, FEATURE_COLS)
    feat["naive_pred"] = compute_loco_predictions(feat, ["maturity_z"])
    feat_wc = feat.loc[feat_wc.index].copy()
    feat_wc["growth_target_wc"] = within_customer_demean(feat_wc, "growth_target")
    feat_wc["own_pred_wc"] = within_customer_demean(feat_wc, "own_pred")
    feat_wc["naive_pred_wc"] = within_customer_demean(feat_wc, "naive_pred")

    n_wc = len(feat_wc)
    actual_pct = rankdata(feat_wc["growth_target_wc"].values, method="average") / n_wc
    own_pct = rankdata(feat_wc["own_pred_wc"].values, method="average") / n_wc
    actual_low = actual_pct <= flag_threshold
    own_flag = own_pct <= flag_threshold
    own_p, own_r = precision_recall(own_flag, actual_low)
    random_baseline_p = float(actual_low.mean())
    own_vs_random = own_p - random_baseline_p

    # Structural check: is the naive (account-maturity) prediction degenerate
    # after within-customer demeaning? It is a customer-level constant, so
    # this is expected to be true in every spec -- see module docstring.
    naive_wc_std = float(feat_wc["naive_pred_wc"].std())
    naive_is_degenerate = naive_wc_std < NAIVE_DEGENERATE_STD_THRESHOLD

    result = {
        "spec_label": spec_label, "n_adgroups": int(n_wc), "n_customers": int(n_cust_wc),
        "flag_threshold": flag_threshold,
        "naive_pred_wc_std": naive_wc_std, "naive_is_degenerate": bool(naive_is_degenerate),
        "own_precision": float(own_p), "own_recall": float(own_r),
        "random_baseline_precision": random_baseline_p,
        "own_vs_random_baseline": float(own_vs_random),
    }

    if naive_is_degenerate:
        result["comparison"] = ("naive is a customer-level constant and carries no "
                                 "within-customer predictive content by construction; "
                                 "own-signal is evaluated against random baseline only.")
        return result

    naive_pct = rankdata(feat_wc["naive_pred_wc"].values, method="average") / n_wc
    naive_flag = naive_pct <= flag_threshold
    naive_p, naive_r = precision_recall(naive_flag, actual_low)

    customer_ids_wc = feat_wc["customer_id"].values
    unique_custs = feat_wc["customer_id"].unique()
    rng = np.random.default_rng(RANDOM_STATE)
    diffs = []
    for _ in range(n_boot):
        sampled = rng.choice(unique_custs, size=len(unique_custs), replace=True)
        idx = np.concatenate([np.where(customer_ids_wc == c)[0] for c in sampled])
        if len(idx) < 20:
            continue
        o_p, _ = precision_recall(own_flag[idx], actual_low[idx])
        n_p, _ = precision_recall(naive_flag[idx], actual_low[idx])
        if not (np.isnan(o_p) or np.isnan(n_p)):
            diffs.append(o_p - n_p)
    diffs = np.array(diffs)

    if len(diffs) >= 30:
        ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])
        ci_excludes_zero = not (ci_low <= 0 <= ci_high)
    else:
        ci_low, ci_high, ci_excludes_zero = None, None, None

    result.update({
        "naive_precision": float(naive_p), "naive_recall": float(naive_r),
        "precision_diff_ci_low": float(ci_low) if ci_low is not None else None,
        "precision_diff_ci_high": float(ci_high) if ci_high is not None else None,
        "ci_excludes_zero": ci_excludes_zero,
    })
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> dict:
    adgroup_dim, panel_cost, obs_start, obs_end = load_and_prepare()

    grid_results = []
    for min_active_days, early_days, later_days in BACKTEST_GRID:
        spec_label = f"active{min_active_days}_{early_days}-{later_days}"
        usable = build_usable_sample(adgroup_dim, obs_start, obs_end, min_active_days)
        res = run_backtest_spec(usable, panel_cost, obs_end, spec_label, early_days, later_days)
        grid_results.append(res)
        print(f"[{spec_label}] {res.get('note', res.get('comparison', 'ok'))}")

    valid = [r for r in grid_results if "note" not in r]
    n_degenerate = sum(1 for r in valid if r.get("naive_is_degenerate"))
    n_comparable = len(valid) - n_degenerate

    summary = {
        "n_specs_total": len(grid_results), "n_specs_valid": len(valid),
        "n_specs_naive_degenerate": n_degenerate, "n_specs_naive_comparable": n_comparable,
        "interpretation": (
            "Account maturity is a customer-level constant, so within-customer demeaning of a "
            "naive prediction built from it is expected to collapse to numerical zero in every "
            "specification -- this is the correct, structural result, not a bug (see "
            "04_design_artifact_future_work.md). Where this holds, own-signal precision is "
            "compared against a random flagging baseline instead of against naive. Design "
            "principles DP1-DP3 are grounded in the continuous-scale within-customer result "
            "(RQ2/Section 3.3), not in this binary-flagging backtest; the backtest is reported "
            "as future work, not a confirmed empirical advantage."
        ),
    }
    if valid:
        own_beats_random = np.mean([r["own_vs_random_baseline"] > 0 for r in valid])
        summary["own_beats_random_baseline_share"] = float(own_beats_random)

    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "grid_results": grid_results}, f, ensure_ascii=False, indent=2)
    pd.DataFrame(grid_results).to_csv(OUTPUT_GRID_PATH, index=False, encoding="utf-8-sig")
    print(f"Wrote {OUTPUT_JSON_PATH} and {OUTPUT_GRID_PATH}")
    return {"summary": summary, "grid_results": grid_results}


if __name__ == "__main__":
    main()
