"""
Step L -- RQ2 feature design: build early-window operating-signal features
(coverage, mean spend, spend trend/slope, CTR/CVR/ROAS) and a later-window
growth target, then validate predictive value with two independently
information-leakage-checked designs:

  (1) Repeated, customer-grouped train/test splits (GroupShuffleSplit),
      base features vs. base+account-maturity, paired per split, tested
      with a Wilcoxon signed-rank test on the improvement.
  (2) Leave-One-Customer-Out (LOCO) cross-validation, decomposed into a
      between-customer component (captures customer-level maturity effects
      "leaking in") and a within-customer component (the actual ad-group-
      level predictive signal RQ2 is meant to measure).

This decomposition is the key methodological safeguard in this file: a
naive pooled LOCO improvement can look positive purely because maturity
re-derives the RQ1 (customer-level) signal, not because it improves
ad-group-level prediction. See `src/analysis/rq2_prediction_validation.py`
for the confirmatory run on the full sample.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit, LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import find_column, read_perf_panel_columns_only
from src.utils.identifiers import clean_id
from src.utils.io import load_config

FEATURE_COLS_BASE = ["coverage", "mean_cost", "std_cost", "early_slope",
                      "ctr", "cvr", "roas", "ctr_missing", "cvr_missing", "roas_missing"]
FEATURE_COLS_PLUS = FEATURE_COLS_BASE + ["log_all_time_count", "coldstart_ratio"]


def load_perf_detail(cfg: dict, target_ids: set) -> pd.DataFrame:
    path = cfg["paths"]["perf_panel"]
    header = pd.read_csv(path, sep="\t", nrows=5) if str(path).endswith(".tsv") else pd.read_csv(path, nrows=5)
    cols = {
        "date": find_column(header, ["date"]), "ad_group_id": find_column(header, ["ad_group_id"]),
        "impression": find_column(header, ["impression"]), "click": find_column(header, ["click"]),
        "cost": find_column(header, ["cost"]), "conversion_count": find_column(header, ["conversion_count"]),
        "sales": find_column(header, ["sales_by_conversion"]),
    }
    usecols = [v for v in cols.values() if v]
    accum = []
    for chunk in read_perf_panel_columns_only(path, usecols=usecols, dtype={cols["ad_group_id"]: str}, chunksize=2_000_000):
        chunk = chunk.rename(columns={v: k for k, v in cols.items() if v})
        chunk["ad_group_id"] = clean_id(chunk["ad_group_id"])
        chunk = chunk[chunk["ad_group_id"].isin(target_ids)]
        if len(chunk):
            accum.append(chunk)
    perf = pd.concat(accum, ignore_index=True)
    perf["date"] = pd.to_datetime(perf["date"], errors="coerce").dt.normalize()
    perf = perf.dropna(subset=["date"])
    for c in ["impression", "click", "cost", "conversion_count", "sales"]:
        if c in perf.columns:
            perf[c] = pd.to_numeric(perf[c], errors="coerce").fillna(0)
    return perf.groupby(["ad_group_id", "date"], as_index=False)[
        [c for c in ["impression", "click", "cost", "conversion_count", "sales"] if c in perf.columns]
    ].sum()


def build_window_features(sample: pd.DataFrame, perf: pd.DataFrame, obs_end, early_days: int, later_days: int) -> pd.DataFrame:
    first_active_map = sample.set_index("ad_group_id")["perf_first_active"]
    customer_map = sample.set_index("ad_group_id")["customer_id"]
    maturity_by_cust = sample.drop_duplicates("customer_id").set_index("customer_id")

    rows = []
    for adg_id, first_active in first_active_map.items():
        early_end = first_active + pd.Timedelta(days=early_days - 1)
        later_start, later_end = early_end + pd.Timedelta(days=1), early_end + pd.Timedelta(days=later_days)
        if later_end > obs_end:
            continue  # keeps the sample free of look-ahead artifacts

        sub = perf[perf["ad_group_id"] == adg_id]
        early = sub[(sub["date"] >= first_active) & (sub["date"] <= early_end)]
        later = sub[(sub["date"] >= later_start) & (sub["date"] <= later_end)]

        early_daily = early.set_index("date")["cost"].reindex(pd.date_range(first_active, early_end), fill_value=0.0)
        day_idx = np.arange(len(early_daily))
        coverage = (early_daily > 0).mean()
        slope = np.polyfit(day_idx, early_daily.values, 1)[0] if early_daily.sum() > 0 and len(day_idx) >= 2 else 0.0

        impr, click, conv, cost_sum = early["impression"].sum(), early["click"].sum(), early.get("conversion_count", pd.Series(dtype=float)).sum(), early["cost"].sum()
        ctr = click / impr if impr > 0 else np.nan
        cvr = conv / click if click > 0 else np.nan
        roas = early.get("sales", pd.Series(dtype=float)).sum() / cost_sum if cost_sum > 0 else np.nan

        growth_target = np.log1p(later["cost"].sum()) - np.log1p(cost_sum)
        rows.append({"ad_group_id": adg_id, "customer_id": customer_map.get(adg_id), "coverage": coverage,
                     "mean_cost": early_daily.mean(), "std_cost": early_daily.std() or 0.0, "early_slope": slope,
                     "ctr": ctr, "cvr": cvr, "roas": roas, "growth_target": growth_target})

    feat_df = pd.DataFrame(rows)
    if len(feat_df) == 0:
        return feat_df
    feat_df["log_all_time_count"] = feat_df["customer_id"].map(np.log1p(maturity_by_cust["all_time_count"]))
    feat_df["coldstart_ratio"] = feat_df["customer_id"].map(maturity_by_cust["coldstart_ratio"])
    for col in ["ctr", "cvr", "roas"]:
        feat_df[f"{col}_missing"] = feat_df[col].isna().astype(int)
        feat_df[col] = feat_df[col].fillna(feat_df[col].median())
    return feat_df


def spearman_metric(y_true, y_pred):
    if len(y_true) < 3 or np.std(y_pred) == 0:
        return np.nan
    return stats.spearmanr(y_true, y_pred)[0]


def repeated_group_split_eval(feat_df: pd.DataFrame, n_splits: int, test_size: float, seed: int) -> dict:
    groups = feat_df["customer_id"].values
    gss = GroupShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=seed)
    base_rhos, plus_rhos = [], []
    for tr, te in gss.split(feat_df, groups=groups):
        for cols, sink in [(FEATURE_COLS_BASE, base_rhos), (FEATURE_COLS_PLUS, plus_rhos)]:
            X = feat_df[cols].values
            y = feat_df["growth_target"].values
            scaler = StandardScaler().fit(X[tr])
            model = Ridge(alpha=1.0, random_state=seed).fit(scaler.transform(X[tr]), y[tr])
            sink.append(spearman_metric(y[te], model.predict(scaler.transform(X[te]))))
    base_rhos, plus_rhos = np.array(base_rhos), np.array(plus_rhos)
    diff = plus_rhos - base_rhos
    p = stats.wilcoxon(diff)[1] if len(diff) >= 10 and np.any(diff != 0) else np.nan
    return {"rho_base_mean": base_rhos.mean(), "rho_plus_mean": plus_rhos.mean(), "wilcoxon_p": p}


def loco_within_between_eval(feat_df: pd.DataFrame, seed: int) -> dict:
    groups = feat_df["customer_id"].values
    logo = LeaveOneGroupOut()
    y = feat_df["growth_target"].values
    preds = {}
    for cols, key in [(FEATURE_COLS_BASE, "base"), (FEATURE_COLS_PLUS, "plus")]:
        X = feat_df[cols].values
        pred = np.full(len(feat_df), np.nan)
        for tr, te in logo.split(feat_df, groups=groups):
            scaler = StandardScaler().fit(X[tr])
            model = Ridge(alpha=1.0, random_state=seed).fit(scaler.transform(X[tr]), y[tr])
            pred[te] = model.predict(scaler.transform(X[te]))
        preds[key] = pred

    def decompose(y_true, y_pred):
        df = pd.DataFrame({"customer_id": feat_df["customer_id"].values, "y_true": y_true, "y_pred": y_pred})
        cm = df.groupby("customer_id")[["y_true", "y_pred"]].mean()
        between = stats.spearmanr(cm["y_true"], cm["y_pred"])[0] if len(cm) >= 3 and cm["y_pred"].std() > 0 else np.nan
        df["yt_c"] = df["y_true"] - df.groupby("customer_id")["y_true"].transform("mean")
        df["yp_c"] = df["y_pred"] - df.groupby("customer_id")["y_pred"].transform("mean")
        multi = df.groupby("customer_id").filter(lambda g: len(g) >= 2)
        within = stats.spearmanr(multi["yt_c"], multi["yp_c"])[0] if len(multi) >= 3 and multi["yp_c"].std() > 0 else np.nan
        return between, within

    btw_b, win_b = decompose(y, preds["base"])
    btw_p, win_p = decompose(y, preds["plus"])
    return {"between_base": btw_b, "between_plus": btw_p, "within_base": win_b, "within_plus": win_p,
            "between_improvement": btw_p - btw_b, "within_improvement": win_p - win_b}


def run(cfg: dict):
    ctx = step_a(cfg)
    adgroup_dim, coldstart, usable, obs_end = ctx["adgroup_dim"], ctx["coldstart"], ctx["usable"], ctx["obs_end"]

    from src.coldstart_v5._sample_construction import apply_maturity_metrics
    usable_m = apply_maturity_metrics(usable, adgroup_dim, coldstart)

    excl = set(cfg["sample_definition"].get("known_test_account_ids", []))
    sample = usable_m[~usable_m["customer_id"].isin(excl)].copy()

    perf = load_perf_detail(cfg, set(sample["ad_group_id"]))

    for early_d, later_d in cfg["rq2_prediction"]["window_pairs"]:
        feat_df = build_window_features(sample, perf, obs_end, early_d, later_d)
        print(f"[step_l] early={early_d}d/later={later_d}d -> n={len(feat_df)}, "
              f"customers={feat_df['customer_id'].nunique() if len(feat_df) else 0}")
        if len(feat_df) < 20 or feat_df["customer_id"].nunique() < 5:
            continue
        split_result = repeated_group_split_eval(feat_df, cfg["rq2_prediction"]["n_repeated_splits"],
                                                   cfg["rq2_prediction"]["test_size"], cfg["random_seed"])
        loco_result = loco_within_between_eval(feat_df, cfg["random_seed"])
        print(f"[step_l]   repeated-split: {split_result}")
        print(f"[step_l]   LOCO within/between decomposition: {loco_result}")
        print("[step_l]   Interpretation rule: trust the within-customer LOCO improvement and the "
              "repeated-split Wilcoxon result over the pooled LOCO number -- pooled LOCO gains that "
              "are concentrated in the between-customer component reflect RQ1 signal leaking in, "
              "not genuine ad-group-level predictive improvement.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
