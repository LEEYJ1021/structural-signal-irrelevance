"""
Pipeline v4, Step 3 -- churn-prediction benchmark appendix.

Not part of the coldstart_v5 confirmatory design; kept as a
supplementary appendix benchmarking how predictable *ad-group-level*
churn (inactivity for `churn_inactive_days` or more, with no
subsequent activity before the observation-end date) is from the same
family of early-window operating signals used in RQ2, using
spike-account-excluded data so that the mass-deletion event does not
get misread as organic churn.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from src.pipeline_v4.step0_data_prep_v4 import run as step0
from src.utils.io import load_config


FEATURE_COLS = ["coverage_30d", "mean_cost_30d", "std_cost_30d", "active_days_total"]


def build_churn_labels_and_features(panel: pd.DataFrame, adgroup_dim: pd.DataFrame, spike_ids: set,
                                     obs_end, churn_inactive_days: int) -> pd.DataFrame:
    panel = panel[~panel["customer_id"].isin(spike_ids)]
    first_last = panel.groupby("ad_group_id")["date"].agg(first="min", last="max")
    active_days_total = panel.groupby("ad_group_id")["date"].nunique().rename("active_days_total")

    rows = []
    for adg_id, row in first_last.iterrows():
        window_end = row["first"] + pd.Timedelta(days=29)
        early = panel[(panel["ad_group_id"] == adg_id) & (panel["date"] >= row["first"]) & (panel["date"] <= window_end)]
        daily = early.set_index("date")["cost"].reindex(pd.date_range(row["first"], window_end), fill_value=0.0)
        churned = (obs_end - row["last"]).days >= churn_inactive_days
        rows.append({
            "ad_group_id": adg_id,
            "customer_id": panel.loc[panel["ad_group_id"] == adg_id, "customer_id"].iloc[0],
            "coverage_30d": (daily > 0).mean(), "mean_cost_30d": daily.mean(), "std_cost_30d": daily.std() or 0.0,
            "active_days_total": active_days_total.get(adg_id, 0), "churned": int(churned),
        })
    return pd.DataFrame(rows)


def run(cfg: dict):
    ctx = step0(cfg)
    panel, adgroup_dim, spike_ids = ctx["panel"], ctx["adgroup_dim"], ctx["spike_ids"]
    ccfg = cfg["pipeline_v4"]["churn_appendix"]
    seed = cfg["random_seed"]
    obs_end = panel["date"].max()

    df = build_churn_labels_and_features(panel, adgroup_dim, spike_ids, obs_end, ccfg["churn_inactive_days"])
    print(f"[step3_v4] churn appendix sample: n={len(df)}, churn rate={df['churned'].mean():.1%}")

    if df["churned"].nunique() < 2 or len(df) < 30:
        print("[step3_v4] insufficient class balance / sample size for churn benchmark -- skipping model fit")
        return None

    groups = df["customer_id"].values
    X, y = df[FEATURE_COLS].values, df["churned"].values
    gkf = GroupKFold(n_splits=min(5, df["customer_id"].nunique()))

    results = {}
    for model_name in ccfg["benchmark_models"]:
        aucs = []
        for tr, te in gkf.split(X, y, groups=groups):
            scaler = StandardScaler().fit(X[tr])
            Xtr, Xte = scaler.transform(X[tr]), scaler.transform(X[te])
            if model_name == "logistic_baseline":
                clf = LogisticRegression(max_iter=1000, random_state=seed)
            else:
                clf = GradientBoostingClassifier(random_state=seed)
            if len(np.unique(y[tr])) < 2:
                continue
            clf.fit(Xtr, y[tr])
            if len(np.unique(y[te])) < 2:
                continue
            proba = clf.predict_proba(Xte)[:, 1]
            aucs.append(roc_auc_score(y[te], proba))
        results[model_name] = {"mean_auc": float(np.mean(aucs)) if aucs else np.nan, "n_folds_valid": len(aucs)}
        print(f"[step3_v4] {model_name}: mean group-CV AUC = {results[model_name]['mean_auc']:.3f} "
              f"({len(aucs)} valid folds)")

    out_dir = Path(cfg["paths"]["v4_intermediate_dir"]).parent / "_v4_churn_appendix"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "churn_benchmark.json").write_text(json.dumps(results, indent=2))
    print(f"[step3_v4] wrote {out_dir / 'churn_benchmark.json'}")
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
