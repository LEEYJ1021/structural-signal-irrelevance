#!/usr/bin/env python3
# =====================================================================
# research_wide_audit_core.py  [CROSS-CUTTING]
#
# Single-file, simplified reproduction of the two audit results cited in
# the root README:
#   PART A — pooled multiplicity audit across all 25 officially-reported
#            p-values in the repository (root README §7, Figure 14)
#   PART B — H1c core-model influence diagnostic: DFBETA + leave-k-out,
#            run for the first time directly on the confirmatory model
#            rather than a Level 2 sub-analysis (root README §5.3)
#
# This script omits the broader internal audit (cluster-SE validity
# checks across sub-samples, unexplored-moderator scan, spec-curve
# selective-reporting review, temporal-precedence check, merge-point
# coverage audit). Those are narrated in docs/METHODOLOGY_NOTES.md; none
# of them changed the two headline results reproduced here.
#
# Usage:
#   python research_wide_audit_core.py --panel-csv /path/to/panel.csv --out-dir ./detail
# =====================================================================

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ALPHA = 0.05
CORE_COLS = ["spend_z", "size_z"]

# Hard-coded list of every p-value officially reported in the repository,
# sourced from docs/RESULTS_SUMMARY.md. Family labels match the root
# README's terminology so the pooled table can be cross-referenced directly.
ALL_REPORTED_TESTS = [
    {"family": "H1c(6-cell)", "test": "approval_full", "p": 0.251},
    {"family": "H1c(6-cell)", "test": "approval_exspike", "p": 0.357},
    {"family": "H1c(6-cell)", "test": "cpc_full", "p": 0.756},
    {"family": "H1c(6-cell)", "test": "cpc_exspike", "p": 0.073},
    {"family": "H1c(6-cell)", "test": "adrank_full", "p": 0.481},
    {"family": "H1c(6-cell)", "test": "adrank_exspike", "p": 0.937},
    {"family": "H2(joint+3-term)", "test": "joint_wald_H2_legacy", "p": 0.023},
    {"family": "H2_continuous(3-term)", "test": "share2_shopping", "p": 0.306785},
    {"family": "H2_continuous(3-term)", "test": "share3_powercontent", "p": 0.004339},
    {"family": "H2_continuous(3-term)", "test": "share6_localbiz", "p": 0.099387},
    {"family": "RDD(5-candidate)", "test": "rdd_logsize_1.386", "p": 0.79},
    {"family": "RDD(5-candidate)", "test": "rdd_logsize_2.092", "p": 0.40},
    {"family": "RDD(5-candidate)", "test": "rdd_logsize_2.515", "p": 0.048},
    {"family": "RDD(5-candidate)", "test": "rdd_spend_11.515", "p": 0.86},
    {"family": "RDD(5-candidate)", "test": "rdd_spend_11.912", "p": 0.21},
    {"family": "policy_change(5-candidate)", "test": "policy_0203", "p": 0.58},
    {"family": "policy_change(5-candidate)", "test": "policy_0218", "p": 0.41},
    {"family": "policy_change(5-candidate)", "test": "policy_0305", "p": 0.23},
    {"family": "policy_change(5-candidate)", "test": "policy_0320", "p": 0.58},
    {"family": "policy_change(5-candidate)", "test": "policy_0404", "p": 0.34},
    {"family": "H3", "test": "h1c_full_vs_exlocalbiz", "p": 0.0060},
    {"family": "H3", "test": "random_placebo_empirical_p", "p": 0.009},
    {"family": "H3", "test": "size_matched_placebo_empirical_p", "p": 0.004},
    {"family": "keyword_review(exploratory)", "test": "restricted_def", "p": 0.016},
    {"family": "keyword_review(exploratory)", "test": "combined_def", "p": 0.016},
]


def cluster_ols(df, y, x_cols, cluster_col="customer_id"):
    X = sm.add_constant(df[x_cols])
    return sm.OLS(df[y], X).fit(cov_type="cluster", cov_kwds={"groups": df[cluster_col]})


def bh_fdr(pvals, alpha=ALPHA):
    p = np.asarray(pvals)
    order = np.argsort(p)
    ranked = p[order]
    m = len(p)
    thresh = (np.arange(1, m + 1) / m) * alpha
    passed = ranked <= thresh
    sig = np.zeros(m, dtype=bool)
    if passed.any():
        max_i = np.max(np.where(passed)[0])
        sig[order[: max_i + 1]] = True
    return sig


# ---------------------------------------------------------------------
# PART A — pooled multiplicity audit
# ---------------------------------------------------------------------
def run_multiplicity_audit():
    df = pd.DataFrame(ALL_REPORTED_TESTS)
    m = len(df)
    bonf_alpha = ALPHA / m
    df["bonferroni_sig"] = df["p"] < bonf_alpha
    df["bh_sig"] = bh_fdr(df["p"].values)
    return {
        "m_total": int(m),
        "bonferroni_alpha": float(bonf_alpha),
        "n_bonferroni_survive": int(df["bonferroni_sig"].sum()),
        "n_bh_survive": int(df["bh_sig"].sum()),
        "surviving_bonferroni": df.loc[df["bonferroni_sig"], "test"].tolist(),
        "surviving_bh": df.loc[df["bh_sig"], "test"].tolist(),
        "table": df.sort_values("p").to_dict(orient="records"),
    }


# ---------------------------------------------------------------------
# PART B — H1c core-model influence diagnostic
# ---------------------------------------------------------------------
def run_h1c_influence(panel: pd.DataFrame):
    panel = panel.dropna(subset=["log_cpc"] + CORE_COLS).reset_index(drop=True)
    cust_agg = panel.groupby("customer_id")[["log_cpc"] + CORE_COLS].mean().reset_index()
    X = sm.add_constant(cust_agg[CORE_COLS])
    ols_fit = sm.OLS(cust_agg["log_cpc"], X).fit()
    infl = ols_fit.get_influence()
    focal_idx = list(X.columns).index("size_z")
    dfbeta = infl.dfbetas[:, focal_idx]

    n_cust = len(cust_agg)
    threshold = 2 / np.sqrt(n_cust)
    cust_agg["dfbeta_size_z"] = dfbeta
    ranked = cust_agg.reindex(cust_agg["dfbeta_size_z"].abs().sort_values(ascending=False).index)
    n_exceed = int((cust_agg["dfbeta_size_z"].abs() > threshold).sum())

    model_full = cluster_ols(panel, "log_cpc", CORE_COLS)
    beta_full, p_full = float(model_full.params["size_z"]), float(model_full.pvalues["size_z"])

    leave_k = []
    ranked_ids = ranked["customer_id"].tolist()
    for k in [1, 3, 5, 10]:
        excluded = set(ranked_ids[:k])
        sub = panel[~panel["customer_id"].isin(excluded)]
        m = cluster_ols(sub, "log_cpc", CORE_COLS)
        beta_k, p_k = float(m.params["size_z"]), float(m.pvalues["size_z"])
        leave_k.append({
            "k_removed": k, "beta": beta_k, "p": p_k,
            "sign_flip": bool(np.sign(beta_k) != np.sign(beta_full)),
            "significance_flip": bool((p_k < ALPHA) != (p_full < ALPHA)),
        })

    return {
        "n_customers": int(n_cust),
        "dfbeta_threshold": float(threshold),
        "n_customers_exceeding_threshold": n_exceed,
        "top10_influence": ranked.head(10)[["customer_id", "dfbeta_size_z"]].to_dict(orient="records"),
        "baseline_beta": beta_full, "baseline_p": p_full,
        "leave_k_out": leave_k,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel-csv", type=Path, required=True,
                     help="Customer-level panel with log_cpc, spend_z, size_z, customer_id")
    ap.add_argument("--out-dir", type=Path, default=Path("./detail"))
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print("[A] Running pooled multiplicity audit (25 reported p-values)...")
    multiplicity = run_multiplicity_audit()
    print(f"    Bonferroni survivors: {multiplicity['n_bonferroni_survive']}/25 | "
          f"BH-FDR survivors: {multiplicity['n_bh_survive']}/25")

    print("[B] Running H1c core-model influence diagnostic...")
    panel = pd.read_csv(args.panel_csv, dtype={"customer_id": str})
    influence = run_h1c_influence(panel)
    print(f"    {influence['n_customers_exceeding_threshold']} customers exceed the DFBETA threshold")

    report = {"multiplicity_audit": multiplicity, "h1c_core_influence": influence}
    with open(args.out_dir / "research_wide_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nSaved: {args.out_dir / 'research_wide_audit_report.json'}")


if __name__ == "__main__":
    main()
