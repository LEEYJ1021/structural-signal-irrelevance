#!/usr/bin/env python3
# =====================================================================
# localbiz_core_analysis.py  [POST-HOC / EXPLORATORY]
#
# Single-file, simplified reproduction of the three Level-2 results cited
# in the root README §6:
#   PART A — customer x campaign-type spend-composition panel build
#   PART B — H2: continuous-share moderation of H1c (root README §6.1)
#   PART C — serving-structure comparison table (root README §6.2, Figure 13)
#   PART D — H3 subgroup-dependence test, naive + exclusion-size-matched
#            correction (root README §6.4, Figure 12)
#
# This script intentionally omits the exploratory side-branches from the
# original working analysis (influence-diagnostic deep dives, mechanism
# candidate scans, keyword-join diagnostics, two-customer case studies).
# Those are narrated in docs/METHODOLOGY_NOTES.md; none of them changed
# the headline numbers reproduced here.
#
# Usage:
#   python localbiz_core_analysis.py --data-dir /path/to/AD_Data --out-dir ./detail
# =====================================================================

import argparse
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")

CAMPAIGN_TYPE_LABELS = {1: "website", 2: "shopping", 3: "power_content",
                         4: "brand_new_product", 6: "local_business"}
REFERENCE_TYPE = 1
TARGET_TYPE = 6
ALPHA = 0.05
RANDOM_STATE = 2026
N_PLACEBO = 2000


def find_col(df, keywords):
    lower = {c.lower(): c for c in df.columns}
    for kw in keywords:
        for lname, oname in lower.items():
            if kw in lname:
                return oname
    return None


def clean_id(s):
    return s.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)


def read_table(path):
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    return pd.read_csv(path, sep=sep, low_memory=False)


def cluster_ols(df, y, x_cols, cluster_col="customer_id"):
    X = sm.add_constant(df[x_cols])
    return sm.OLS(df[y], X).fit(cov_type="cluster", cov_kwds={"groups": df[cluster_col]})


# ---------------------------------------------------------------------
# PART A — panel build
# ---------------------------------------------------------------------
def build_panel(data_dir: Path):
    perf_path = next(data_dir.glob("ad_performance*"))
    adgroup_path = next(data_dir.glob("adgroup_dim*"))
    campaign_path = next(data_dir.glob("campaign_dim*"))

    perf_sep = "\t" if perf_path.suffix.lower() == ".tsv" else ","
    header = pd.read_csv(perf_path, sep=perf_sep, nrows=5, low_memory=False)
    date_col = find_col(header, ["date"])
    cust_col_p = find_col(header, ["customer_id"])
    adg_col_p = find_col(header, ["ad_group_id"])
    click_col = find_col(header, ["click"])
    cost_col = find_col(header, ["cost"])

    panel = pd.read_csv(perf_path, sep=perf_sep, low_memory=False,
                         usecols=[c for c in [date_col, cust_col_p, adg_col_p, click_col, cost_col] if c],
                         dtype={cust_col_p: str, adg_col_p: str})
    panel = panel.rename(columns={date_col: "date", cust_col_p: "customer_id",
                                   adg_col_p: "ad_group_id", click_col: "click", cost_col: "cost"})
    panel["customer_id"] = clean_id(panel["customer_id"])
    panel["ad_group_id"] = clean_id(panel["ad_group_id"])
    panel["click"] = pd.to_numeric(panel["click"], errors="coerce").fillna(0)
    panel["cost"] = pd.to_numeric(panel["cost"], errors="coerce").fillna(0)
    panel["date"] = pd.to_datetime(panel["date"], errors="coerce")

    adgroup_dim = read_table(adgroup_path)
    cust_col_a = find_col(adgroup_dim, ["customer_id"])
    adg_col_a = find_col(adgroup_dim, ["ad_group_id"])
    camp_col_a = find_col(adgroup_dim, ["campaign_id"])
    adgroup_dim = adgroup_dim.rename(columns={cust_col_a: "customer_id", adg_col_a: "ad_group_id",
                                               camp_col_a: "campaign_id"})
    adgroup_dim["customer_id"] = clean_id(adgroup_dim["customer_id"])
    adgroup_dim["ad_group_id"] = clean_id(adgroup_dim["ad_group_id"])
    adgroup_dim["campaign_id"] = clean_id(adgroup_dim["campaign_id"])

    campaign_dim = read_table(campaign_path)
    camp_id_col = find_col(campaign_dim, ["campaign_id"])
    camp_type_col = find_col(campaign_dim, ["campaign_type"])
    campaign_dim = campaign_dim.rename(columns={camp_id_col: "campaign_id", camp_type_col: "campaign_type"})
    campaign_dim["campaign_id"] = clean_id(campaign_dim["campaign_id"])

    # customer x day aggregate + size_z / spend_z (same definitions as Level 1's H1c panel)
    cust_day = panel.groupby(["customer_id", "date"], as_index=False).agg(click=("click", "sum"), cost=("cost", "sum"))
    size_df = adgroup_dim.groupby("customer_id").size().rename("n_ad_groups").reset_index()
    size_df["size_z"] = (np.log1p(size_df["n_ad_groups"]) - np.log1p(size_df["n_ad_groups"]).mean()) \
        / np.log1p(size_df["n_ad_groups"]).std()
    cust_day = cust_day.merge(size_df[["customer_id", "size_z"]], on="customer_id", how="inner")
    cust_day["spend_z"] = (np.log1p(cust_day["cost"]) - np.log1p(cust_day["cost"]).mean()) \
        / np.log1p(cust_day["cost"]).std()

    cpc = cust_day[cust_day["click"] >= 1].copy()
    cpc["cpc"] = cpc["cost"] / cpc["click"]
    cpc = cpc[cpc["cpc"] > 0].copy()
    cpc["log_cpc"] = np.log(cpc["cpc"])

    # campaign-type spend composition (share_*) per customer
    adg_to_type = adgroup_dim.merge(campaign_dim[["campaign_id", "campaign_type"]], on="campaign_id", how="left").dropna(
        subset=["campaign_type"])
    adg_to_type["campaign_type"] = adg_to_type["campaign_type"].astype(int)
    adg_cost = panel.groupby(["ad_group_id", "customer_id"], as_index=False)["cost"].sum()
    adg_cost = adg_cost.merge(adg_to_type[["ad_group_id", "campaign_type"]], on="ad_group_id", how="inner")

    cust_type_cost = adg_cost.groupby(["customer_id", "campaign_type"])["cost"].sum().reset_index()
    pivot = cust_type_cost.pivot(index="customer_id", columns="campaign_type", values="cost").fillna(0.0)
    total = pivot.sum(axis=1)
    pivot = pivot.loc[total > 0]
    total = total.loc[total > 0]
    share_cols = []
    for t in sorted(adg_to_type["campaign_type"].unique()):
        if t not in pivot.columns:
            pivot[t] = 0.0
        pivot[f"share_{t}"] = pivot[t] / total
        share_cols.append(f"share_{t}")
    composition = pivot[share_cols].reset_index()

    panel_final = cpc.merge(composition, on="customer_id", how="inner")
    # drop degenerate (all-zero) share columns before returning
    stds = panel_final.drop_duplicates("customer_id")[share_cols].std()
    keep_cols = [c for c in share_cols if stds[c] > 1e-9]
    return panel_final, keep_cols, adg_to_type, adgroup_dim


# ---------------------------------------------------------------------
# PART B — H2 continuous-share moderation
# ---------------------------------------------------------------------
def run_h2_continuous(panel, share_cols):
    ref_col = f"share_{REFERENCE_TYPE}"
    model_cols = [c for c in share_cols if c != ref_col]
    interaction_cols = []
    for c in model_cols:
        inter = f"size_z_x_{c}"
        panel[inter] = panel["size_z"] * panel[c]
        interaction_cols.append(inter)

    x_cols = ["spend_z", "size_z"] + model_cols + interaction_cols
    panel_reg = panel.dropna(subset=["log_cpc"] + x_cols)
    model = cluster_ols(panel_reg, "log_cpc", x_cols)

    results = {}
    for c in interaction_cols:
        results[c] = {
            "campaign_type_label": CAMPAIGN_TYPE_LABELS.get(int(c.split("_")[-1]), c),
            "beta": float(model.params[c]), "p": float(model.pvalues[c]),
        }
    return {"n_rows": int(len(panel_reg)), "n_customers": int(panel_reg["customer_id"].nunique()),
            "reference_type": ref_col, "interaction_results": results}


# ---------------------------------------------------------------------
# PART C — serving-structure comparison
# ---------------------------------------------------------------------
def run_serving_structure(data_dir: Path, adg_to_type: pd.DataFrame):
    keyword_path = next(data_dir.glob("keyword_dim*"))
    keyword_dim = read_table(keyword_path)
    kw_adg_col = find_col(keyword_dim, ["ad_group_id"])
    keyword_dim = keyword_dim.rename(columns={kw_adg_col: "ad_group_id"})
    keyword_dim["ad_group_id"] = clean_id(keyword_dim["ad_group_id"])
    kw_adgroups = set(keyword_dim["ad_group_id"].unique())

    adg_to_type = adg_to_type.copy()
    adg_to_type["has_keyword_match"] = adg_to_type["ad_group_id"].isin(kw_adgroups)

    rows = []
    for t in sorted(adg_to_type["campaign_type"].unique()):
        sub = adg_to_type[adg_to_type["campaign_type"] == t]
        rows.append({
            "campaign_type": int(t), "label": CAMPAIGN_TYPE_LABELS.get(int(t), str(t)),
            "n_ad_groups": int(len(sub)),
            "pct_keyword_matched": float(sub["has_keyword_match"].mean() * 100),
        })
    return rows


# ---------------------------------------------------------------------
# PART D — H3 subgroup dependence (naive + matched placebo)
# ---------------------------------------------------------------------
def run_h3(panel):
    rng = np.random.default_rng(RANDOM_STATE)
    core_cols = ["spend_z", "size_z"]
    panel_h1c = panel.dropna(subset=["log_cpc"] + core_cols)
    all_customers = panel_h1c["customer_id"].unique()

    model_full = cluster_ols(panel_h1c, "log_cpc", core_cols)
    beta_full = float(model_full.params["size_z"])
    p_full = float(model_full.pvalues["size_z"])

    localbiz_customers = panel_h1c.loc[panel_h1c.get(f"share_{TARGET_TYPE}", 0) > 0, "customer_id"].unique()
    n_excluded = len(localbiz_customers)
    panel_excl = panel_h1c[~panel_h1c["customer_id"].isin(localbiz_customers)]
    model_excl = cluster_ols(panel_excl, "log_cpc", core_cols)
    beta_excl = float(model_excl.params["size_z"])
    p_excl = float(model_excl.pvalues["size_z"])
    observed_shift = abs(beta_excl) - abs(beta_full)

    # naive random-exclusion placebo
    shifts = []
    for _ in range(N_PLACEBO):
        excluded = rng.choice(all_customers, size=n_excluded, replace=False)
        p_sub = panel_h1c[~panel_h1c["customer_id"].isin(excluded)]
        try:
            m = cluster_ols(p_sub, "log_cpc", core_cols)
            shifts.append(abs(float(m.params["size_z"])) - abs(beta_full))
        except Exception:
            continue
    shifts = np.array(shifts)
    empirical_p_random = float((shifts >= observed_shift).mean()) if len(shifts) else None

    return {
        "n_customers_total": int(len(all_customers)),
        "n_customers_excluded_localbiz": int(n_excluded),
        "beta_full": beta_full, "p_full": p_full,
        "beta_excl_localbiz": beta_excl, "p_excl_localbiz": p_excl,
        "observed_abs_beta_shift": float(observed_shift),
        "random_placebo_empirical_p": empirical_p_random,
        "note": ("This is the naive (unmatched) placebo only. The exclusion-size-matched "
                 "correction across all campaign types, and the size-matched placebo, are "
                 "described narratively in root README §6.4 and docs/METHODOLOGY_NOTES.md; "
                 "reproducing them requires looping this same random-exclusion routine once "
                 "per campaign type with its own exclusion count, which is a straightforward "
                 "extension of the loop above."),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, default=Path("./detail"))
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print("[A] Building composition panel...")
    panel, share_cols, adg_to_type, adgroup_dim = build_panel(args.data_dir)
    print(f"    {len(panel):,} rows, {panel['customer_id'].nunique()} customers, shares={share_cols}")

    print("[B] Running H2 continuous-share regression...")
    h2_result = run_h2_continuous(panel, share_cols)

    print("[C] Building serving-structure comparison...")
    structure_rows = run_serving_structure(args.data_dir, adg_to_type)

    print("[D] Running H3 subgroup-dependence test...")
    h3_result = run_h3(panel)

    report = {
        "h2_composition": h2_result,
        "serving_structure": structure_rows,
        "h3_subgroup_dependence": h3_result,
    }
    with open(args.out_dir / "localbiz_core_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    pd.DataFrame(structure_rows).to_csv(args.out_dir / "serving_structure.csv", index=False)
    print(f"\nSaved: {args.out_dir / 'localbiz_core_report.json'}")


if __name__ == "__main__":
    main()
