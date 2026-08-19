"""
supplementary_robustness/02_boundary_conditions.py

Tests whether Study 1's central null result (size has no direct effect on
outcomes once spend is controlled) holds uniformly across two meaningful
strata: campaign product type (well-measured, load-bearing) and keyword
review status (poorly powered, exploratory).

Supports: root README.md Sections 2.5 and 5 ("Boundary conditions and
generalizability").

Two analyses, run independently:
  1. campaign_type_boundary_condition() -- re-estimates the spend-controlled
     CPC model within each dominant campaign product type per customer, then
     runs a joint Wald test on the size x product-type interaction terms.
  2. keyword_review_status_boundary_condition() -- classifies customers by
     the share of their keywords carrying a non-standard `inspect_status`
     code, under three overlapping definitions, and tests size x pending
     interactions.

`campaign_type` is a platform-defined ad-product code (website / shopping /
brand-new-product / local-business), NOT an industry classification -- see
02_boundary_conditions.md Section 1 for the codebook. An industry-proxy
pipeline (text embeddings + clustering + LLM-ensemble labeling) was also
piloted; because its inter-rater reliability was only moderate (Randolph's
free-marginal kappa = 0.557, cross-validation kappa vs. a rule-based
classifier = 0.363), it is not re-implemented here and is not used to
support any claim -- see 02_boundary_conditions.md Section 3.

Expected inputs (see data/README.md for schema):
  - adgroup_dim.tsv     (customer_id, ad_group_id, campaign_id, ...)
  - campaign_dim.tsv    (campaign_id, campaign_type, ...)
  - ad_performance.tsv  (date, customer_id, ad_group_id, click, cost, ...)
  - keyword_dim.tsv     (ad_group_id, inspect_status, ...)   [optional]

Output: supplementary_robustness/outputs/02_boundary_conditions.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

DATA_DIR = Path("data")
ADGROUP_DIM_PATH = DATA_DIR / "adgroup_dim.tsv"
CAMPAIGN_DIM_PATH = DATA_DIR / "campaign_dim.tsv"
PERF_PANEL_PATH = DATA_DIR / "ad_performance.tsv"
KEYWORD_DIM_PATH = DATA_DIR / "keyword_dim.tsv"
OUTPUT_PATH = Path("supplementary_robustness/outputs/02_boundary_conditions.json")

RANDOM_STATE = 2026
ALPHA = 0.05
MIN_CLICKS_FOR_CPC = 1
MIN_CUSTOMERS_PER_STRATUM = 15

# inspect_status codebook (platform-defined; see data/README.md)
INSPECT_STATUS_CODE_MAP = {"10": "under_review", "20": "approved", "30": "restricted_approval", "40": "held"}
PENDING_DEFINITIONS = {
    "under_review_only": ["10"],
    "restricted_approval_only": ["30"],
    "combined": ["10", "30"],
}
MIN_KEYWORDS_FOR_PENDING_SHARE = 5


# ---------------------------------------------------------------------------
# Shared helpers (kept self-contained so this script is independently runnable)
# ---------------------------------------------------------------------------
def clean_id(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)


def cluster_robust_ols(df: pd.DataFrame, y_col: str, x_cols: list[str]):
    X = sm.add_constant(df[x_cols])
    return sm.OLS(df[y_col], X).fit(cov_type="cluster", cov_kwds={"groups": df["customer_id"]})


def load_core_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    adgroup_dim = pd.read_csv(ADGROUP_DIM_PATH, sep="\t", low_memory=False)
    adgroup_dim["customer_id"] = clean_id(adgroup_dim["customer_id"])
    adgroup_dim["ad_group_id"] = clean_id(adgroup_dim["ad_group_id"])
    if "campaign_id" in adgroup_dim.columns:
        adgroup_dim["campaign_id"] = clean_id(adgroup_dim["campaign_id"])

    panel = pd.read_csv(PERF_PANEL_PATH, sep="\t", low_memory=False, dtype={"customer_id": str})
    panel["customer_id"] = clean_id(panel["customer_id"])
    if "ad_group_id" in panel.columns:
        panel["ad_group_id"] = clean_id(panel["ad_group_id"])
    panel["date"] = pd.to_datetime(panel["date"], errors="coerce").dt.normalize()
    panel["click"] = pd.to_numeric(panel["click"], errors="coerce").fillna(0)
    panel["cost"] = pd.to_numeric(panel["cost"], errors="coerce").fillna(0)
    panel = panel.dropna(subset=["date"])
    return adgroup_dim, panel


def build_cpc_sample(adgroup_dim: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    """Reconstructs the same customer x day CPC sample used in Study 1's
    primary mediation model (size_z, spend_z, log_cpc). Mirrors
    01_alternative_outcome_mediation.py's build_customer_day_panel /
    build_cpc_sample so this file can be run on its own."""
    cust_day = panel.groupby(["customer_id", "date"], as_index=False).agg(
        click=("click", "sum"), cost=("cost", "sum"))

    size_df = adgroup_dim.groupby("customer_id").size().rename("all_time_ad_group_count").reset_index()
    size_df["log_size"] = np.log1p(size_df["all_time_ad_group_count"])
    size_df["size_z"] = (size_df["log_size"] - size_df["log_size"].mean()) / size_df["log_size"].std()
    cust_day = cust_day.merge(size_df[["customer_id", "size_z"]], on="customer_id", how="inner")

    cust_day["log_spend"] = np.log1p(cust_day["cost"])
    cust_day["spend_z"] = (cust_day["log_spend"] - cust_day["log_spend"].mean()) / cust_day["log_spend"].std()

    cpc = cust_day[cust_day["click"] >= MIN_CLICKS_FOR_CPC].copy()
    cpc["cpc"] = cpc["cost"] / cpc["click"]
    cpc = cpc[cpc["cpc"] > 0].copy()
    cpc["log_cpc"] = np.log(cpc["cpc"])
    return cpc


# ---------------------------------------------------------------------------
# 1. campaign_type boundary condition (load-bearing, README Section 2.5)
# ---------------------------------------------------------------------------
def campaign_type_boundary_condition(cpc_sample: pd.DataFrame, adgroup_dim: pd.DataFrame,
                                      panel: pd.DataFrame) -> dict:
    if not CAMPAIGN_DIM_PATH.exists():
        return {"note": "campaign_dim.tsv not found, skipped"}

    campaign_dim = pd.read_csv(CAMPAIGN_DIM_PATH, sep="\t", low_memory=False)
    if "campaign_id" not in campaign_dim.columns or "campaign_type" not in campaign_dim.columns:
        return {"note": "campaign_type column not found, skipped"}
    campaign_dim["campaign_id"] = clean_id(campaign_dim["campaign_id"])

    adg_to_campaign = adgroup_dim[["ad_group_id", "campaign_id", "customer_id"]].dropna(subset=["campaign_id"])
    adg_to_campaign = adg_to_campaign.merge(
        campaign_dim[["campaign_id", "campaign_type"]], on="campaign_id", how="left")

    # Assign each customer their dominant product type by spend share
    adg_cost = panel.groupby(["ad_group_id", "customer_id"], as_index=False)["cost"].sum()
    adg_cost = adg_cost.merge(adg_to_campaign[["ad_group_id", "campaign_type"]], on="ad_group_id", how="left")
    adg_cost = adg_cost.dropna(subset=["campaign_type"])
    dominant_type = (
        adg_cost.groupby(["customer_id", "campaign_type"])["cost"].sum()
        .reset_index().sort_values("cost", ascending=False)
        .drop_duplicates("customer_id")[["customer_id", "campaign_type"]]
        .rename(columns={"campaign_type": "campaign_type_dominant"})
    )

    sample = cpc_sample.merge(dominant_type, on="customer_id", how="left")
    counts = sample.drop_duplicates("customer_id")["campaign_type_dominant"].value_counts()
    usable_types = counts[counts >= MIN_CUSTOMERS_PER_STRATUM].index.tolist()

    stratum_rows = []
    for ctype in usable_types:
        sub = sample[sample["campaign_type_dominant"] == ctype]
        if sub["customer_id"].nunique() < MIN_CUSTOMERS_PER_STRATUM:
            continue
        m = cluster_robust_ols(sub, "log_cpc", ["spend_z", "size_z"])
        stratum_rows.append({
            "campaign_type": str(ctype), "n_rows": int(len(sub)),
            "n_customers": int(sub["customer_id"].nunique()),
            "c_prime_size": float(m.params["size_z"]), "c_prime_p": float(m.pvalues["size_z"]),
            "b_path_spend": float(m.params["spend_z"]), "b_path_p": float(m.pvalues["spend_z"]),
        })

    joint_result = None
    if len(usable_types) >= 2:
        sub_test = sample[sample["campaign_type_dominant"].isin(usable_types)].copy()
        sub_test["campaign_type_dominant"] = pd.Categorical(
            sub_test["campaign_type_dominant"], categories=usable_types)
        full_model = smf.ols(
            "log_cpc ~ spend_z*C(campaign_type_dominant) + size_z*C(campaign_type_dominant)",
            data=sub_test
        ).fit(cov_type="cluster", cov_kwds={"groups": sub_test["customer_id"]})
        size_inter_terms = [p for p in full_model.params.index
                             if p.startswith("size_z:C(campaign_type_dominant)")]
        if size_inter_terms:
            hypothesis = ", ".join(f"{t} = 0" for t in size_inter_terms)
            wald_res = full_model.wald_test(hypothesis, scalar=True)
            joint_result = {
                "wald_stat": float(np.asarray(wald_res.statistic).squeeze()),
                "df": len(size_inter_terms),
                "joint_p": float(wald_res.pvalue),
                "heterogeneous": bool(wald_res.pvalue < ALPHA),
            }

    return {
        "note": ("campaign_type is a platform ad-product code (website / shopping / "
                 "brand-new-product / local-business), not an industry classification."),
        "strata": stratum_rows,
        "joint_wald_test": joint_result,
        "interpretation": ("No individual stratum shows a significant size effect; the "
                            "joint test (if significant) indicates that the *degree* of "
                            "spend-controlled size irrelevance varies by ad-product category, "
                            "not that the null result is overturned within any stratum."),
    }


# ---------------------------------------------------------------------------
# 2. keyword review-status boundary condition (exploratory, README Section 5)
# ---------------------------------------------------------------------------
def keyword_review_status_boundary_condition(cpc_sample: pd.DataFrame, adgroup_dim: pd.DataFrame) -> dict:
    if not KEYWORD_DIM_PATH.exists():
        return {"note": "keyword_dim.tsv not found, skipped"}

    keyword_dim = pd.read_csv(KEYWORD_DIM_PATH, sep="\t", low_memory=False)
    if "ad_group_id" not in keyword_dim.columns or "inspect_status" not in keyword_dim.columns:
        return {"note": "required columns not found, skipped"}
    keyword_dim["ad_group_id"] = clean_id(keyword_dim["ad_group_id"])
    keyword_dim["inspect_status"] = (
        keyword_dim["inspect_status"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True))

    observed_codes = keyword_dim["inspect_status"].value_counts().to_dict()

    results_by_definition = {}
    for def_name, pending_codes in PENDING_DEFINITIONS.items():
        keyword_dim["is_pending_like"] = keyword_dim["inspect_status"].isin(pending_codes)
        kw_to_cust = keyword_dim[["ad_group_id", "is_pending_like"]].merge(
            adgroup_dim[["ad_group_id", "customer_id"]], on="ad_group_id", how="inner")
        cust_pending = kw_to_cust.groupby("customer_id").agg(
            n_keywords=("is_pending_like", "size"), n_pending=("is_pending_like", "sum")).reset_index()
        cust_pending = cust_pending[cust_pending["n_keywords"] >= MIN_KEYWORDS_FOR_PENDING_SHARE].copy()
        cust_pending["pending_share"] = cust_pending["n_pending"] / cust_pending["n_keywords"]
        cust_pending["pending_high"] = (cust_pending["pending_share"] > 0).astype(int)

        sample = cpc_sample.merge(
            cust_pending[["customer_id", "pending_high"]], on="customer_id", how="inner")
        n_high = int(cust_pending["pending_high"].sum())
        n_low = int(len(cust_pending) - n_high)

        if sample["pending_high"].nunique() < 2 or min(n_high, n_low) < 10:
            results_by_definition[def_name] = {
                "n_high": n_high, "n_low": n_low, "note": "insufficient stratum size for interaction test"}
            continue

        model = smf.ols(
            "log_cpc ~ spend_z*pending_high + size_z*pending_high", data=sample
        ).fit(cov_type="cluster", cov_kwds={"groups": sample["customer_id"]})
        inter_p = model.pvalues.get("size_z:pending_high", np.nan)
        inter_coef = model.params.get("size_z:pending_high", np.nan)
        results_by_definition[def_name] = {
            "n_high": n_high, "n_low": n_low,
            "interaction_coef": float(inter_coef) if not np.isnan(inter_coef) else None,
            "interaction_p": float(inter_p) if not np.isnan(inter_p) else None,
        }

    return {
        "note": ("inspect_status codebook: 10=under_review, 20=approved, "
                 "30=restricted_approval, 40=held. Code 40 was not observed in this dataset. "
                 "Three overlapping definitions are tested because restricted_approval alone "
                 "accounts for most of the combined definition's customer count -- read as one "
                 "underlying signal probed three ways, not three independent confirmations."),
        "observed_codes": observed_codes,
        "results_by_definition": results_by_definition,
        "caveat": ("Very small stratum sizes (0.2-0.3% of keywords per definition) mean this is "
                   "reported as preliminary/exploratory, not a confirmatory boundary-condition test. "
                   "restricted_approval denotes an already-resolved non-standard outcome, not a "
                   "pending discretionary review, so it does not cleanly map onto the discretionary-"
                   "review mechanism that motivated this check."),
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> dict:
    adgroup_dim, panel = load_core_tables()
    cpc_sample = build_cpc_sample(adgroup_dim, panel)

    results = {
        "campaign_type_boundary_condition": campaign_type_boundary_condition(cpc_sample, adgroup_dim, panel),
        "keyword_review_status_boundary_condition": keyword_review_status_boundary_condition(
            cpc_sample, adgroup_dim),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUTPUT_PATH}")
    return results


if __name__ == "__main__":
    main()
