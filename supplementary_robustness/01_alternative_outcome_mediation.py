"""
supplementary_robustness/01_alternative_outcome_mediation.py

Isolates the mechanical spend-CPC cost-sharing artifact and replicates
Study 1's spend-mediation result on `bid_amount`, an outcome that does not
share a cost term with spend.

Supports: root README.md Section 2.4 ("Stress-testing the result across
independent methods and outcome constructions").

Three analyses, run in order:
  1. Customer-level permutation check that isolates the purely mechanical
     component of the spend -> CPC relationship (click reshuffled within
     customer, cost held fixed).
  2. Lagged mediation (spend at t -> CPC at t+1 / t+7) as a same-day-
     cost-sharing-immune replication.
  3. Formal mediation analysis (size -> spend -> bid_amount | size),
     customer-level, HC3 SE, bootstrap + permutation inference on the
     indirect effect.

Expected inputs (see data/README.md for schema):
  - adgroup_dim.tsv   (customer_id, ad_group_id, bid_amount, ...)
  - ad_performance.tsv (date, customer_id, click, cost, ...)

Output: supplementary_robustness/outputs/01_alternative_outcome_mediation.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

# ---------------------------------------------------------------------------
# CONFIG -- point these at your local extract; see data/README.md for schema
# ---------------------------------------------------------------------------
DATA_DIR = Path("data")
ADGROUP_DIM_PATH = DATA_DIR / "adgroup_dim.tsv"
PERF_PANEL_PATH = DATA_DIR / "ad_performance.tsv"
OUTPUT_PATH = Path("supplementary_robustness/outputs/01_alternative_outcome_mediation.json")

RANDOM_STATE = 2026
ALPHA = 0.05
MIN_CLICKS_FOR_CPC = 1
N_PERMUTATIONS_ARTIFACT = 2000
N_BOOTSTRAP_MEDIATION = 5000
N_PERMUTATIONS_MEDIATION = 5000
LAG_DAYS = [1, 7]


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def clean_id(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.replace(r"\.0$", "", regex=True)


def cluster_robust_ols(df: pd.DataFrame, y_col: str, x_cols: list[str]) -> sm.regression.linear_model.RegressionResultsWrapper:
    """Repeated-measures (customer x day) panel -- customer-clustered SE."""
    X = sm.add_constant(df[x_cols])
    return sm.OLS(df[y_col], X).fit(cov_type="cluster", cov_kwds={"groups": df["customer_id"]})


def ols_hc3(df: pd.DataFrame, y_col: str, x_cols: list[str]) -> sm.regression.linear_model.RegressionResultsWrapper:
    """One row per customer -- HC3 heteroskedasticity-robust SE."""
    X = sm.add_constant(df[x_cols])
    return sm.OLS(df[y_col], X).fit(cov_type="HC3")


def load_panel() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and lightly clean the ad-group dimension table and the daily
    performance panel. Adjust column names to match your extract's schema."""
    adgroup_dim = pd.read_csv(ADGROUP_DIM_PATH, sep="\t", low_memory=False)
    adgroup_dim["customer_id"] = clean_id(adgroup_dim["customer_id"])

    panel = pd.read_csv(PERF_PANEL_PATH, sep="\t", low_memory=False,
                         dtype={"customer_id": str})
    panel["customer_id"] = clean_id(panel["customer_id"])
    panel["date"] = pd.to_datetime(panel["date"], errors="coerce").dt.normalize()
    panel["click"] = pd.to_numeric(panel["click"], errors="coerce").fillna(0)
    panel["cost"] = pd.to_numeric(panel["cost"], errors="coerce").fillna(0)
    panel = panel.dropna(subset=["date"])
    return adgroup_dim, panel


def build_customer_day_panel(adgroup_dim: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    """Customer x day aggregation with standardized size (log all-time
    ad-group count) and standardized spend (log cost)."""
    cust_day = panel.groupby(["customer_id", "date"], as_index=False).agg(
        click=("click", "sum"), cost=("cost", "sum"))

    size_df = adgroup_dim.groupby("customer_id").size().rename("all_time_ad_group_count").reset_index()
    size_df["log_size"] = np.log1p(size_df["all_time_ad_group_count"])
    size_df["size_z"] = (size_df["log_size"] - size_df["log_size"].mean()) / size_df["log_size"].std()

    cust_day = cust_day.merge(size_df[["customer_id", "size_z"]], on="customer_id", how="inner")
    cust_day["log_spend"] = np.log1p(cust_day["cost"])
    cust_day["spend_z"] = (cust_day["log_spend"] - cust_day["log_spend"].mean()) / cust_day["log_spend"].std()
    return cust_day


def build_cpc_sample(cust_day: pd.DataFrame) -> pd.DataFrame:
    cpc = cust_day[cust_day["click"] >= MIN_CLICKS_FOR_CPC].copy()
    cpc["cpc"] = cpc["cost"] / cpc["click"]
    cpc = cpc[cpc["cpc"] > 0].copy()
    cpc["log_cpc"] = np.log(cpc["cpc"])
    return cpc


# ---------------------------------------------------------------------------
# 1. Mechanical-artifact isolation (spend and CPC share a cost term)
# ---------------------------------------------------------------------------
def cost_sharing_artifact_check(cpc_sample: pd.DataFrame, n_perm: int = N_PERMUTATIONS_ARTIFACT) -> dict:
    """Reshuffle click within customer (cost held fixed) to build the null
    distribution of the spend -> CPC coefficient under pure mechanical
    cost-sharing, with no genuine behavioral relationship present."""
    observed = cluster_robust_ols(cpc_sample, "log_cpc", ["spend_z", "size_z"])
    observed_b = observed.params["spend_z"]
    observed_p = observed.pvalues["spend_z"]

    rng = np.random.default_rng(RANDOM_STATE)
    customer_ids = cpc_sample["customer_id"].values
    click = cpc_sample["click"].values
    cost = cpc_sample["cost"].values
    spend_z = cpc_sample["spend_z"].values
    size_z = cpc_sample["size_z"].values
    idx_by_customer = cpc_sample.groupby("customer_id").indices

    null_b = []
    for _ in range(n_perm):
        click_perm = click.copy()
        for _, idx in idx_by_customer.items():
            idx = np.asarray(idx)
            if len(idx) > 1:
                click_perm[idx] = rng.permutation(click[idx])
        valid = click_perm > 0
        if valid.sum() < 30:
            continue
        perm_df = pd.DataFrame({
            "customer_id": customer_ids[valid],
            "log_cpc_perm": np.log(cost[valid] / click_perm[valid]),
            "spend_z": spend_z[valid], "size_z": size_z[valid],
        })
        try:
            m = cluster_robust_ols(perm_df, "log_cpc_perm", ["spend_z", "size_z"])
            null_b.append(m.params["spend_z"])
        except Exception:
            continue

    null_b = np.array(null_b)
    ci_low, ci_high = np.percentile(null_b, [2.5, 97.5])
    return {
        "observed_b_path": float(observed_b),
        "observed_b_path_p": float(observed_p),
        "n_valid_permutations": int(len(null_b)),
        "null_mean": float(null_b.mean()),
        "null_ci_low": float(ci_low),
        "null_ci_high": float(ci_high),
        "observed_below_null_ci": bool(observed_b < ci_low),
        "observed_inside_null_ci": bool(ci_low <= observed_b <= ci_high),
        "note": ("If observed falls at/below the mechanical null CI, the raw CPC "
                 "coefficient should not be reported as a stand-alone behavioral "
                 "estimate -- use the bid_amount-based mediation result instead."),
    }


def lagged_mediation_check(cust_day: pd.DataFrame, cpc_sample: pd.DataFrame,
                            lags: list[int] = LAG_DAYS) -> list[dict]:
    """spend(t) -> CPC(t+lag): immune to same-day cost-sharing."""
    predictor = cust_day[["customer_id", "date", "spend_z", "size_z"]].copy()
    outcome = cpc_sample[["customer_id", "date", "log_cpc"]].copy()

    results = []
    for lag in lags:
        shifted = outcome.copy()
        shifted["date_t0"] = shifted["date"] - pd.Timedelta(days=lag)
        merged = predictor.merge(
            shifted[["customer_id", "date_t0", "log_cpc"]],
            left_on=["customer_id", "date"], right_on=["customer_id", "date_t0"], how="inner")
        if len(merged) < 100 or merged["customer_id"].nunique() < 15:
            results.append({"lag_days": lag, "note": "insufficient sample"})
            continue
        m = cluster_robust_ols(merged, "log_cpc", ["spend_z", "size_z"])
        results.append({
            "lag_days": lag, "n": int(len(merged)),
            "n_customers": int(merged["customer_id"].nunique()),
            "b_coef": float(m.params["spend_z"]), "b_p": float(m.pvalues["spend_z"]),
        })
    return results


# ---------------------------------------------------------------------------
# 2. bid_amount-based mediation (primary, cost-independent outcome)
# ---------------------------------------------------------------------------
def build_bid_amount_sample(adgroup_dim: pd.DataFrame, cust_day: pd.DataFrame) -> pd.DataFrame:
    bid_valid = adgroup_dim.dropna(subset=["bid_amount"])
    bid_valid = bid_valid[bid_valid["bid_amount"] > 0]
    cust_bid = bid_valid.groupby("customer_id")["bid_amount"].mean().rename("mean_bid_amount").reset_index()
    cust_bid["log_bid_amount"] = np.log1p(cust_bid["mean_bid_amount"])

    total_spend = cust_day.groupby("customer_id")["cost"].sum().rename("total_cost").reset_index()
    total_spend["log_total_spend"] = np.log1p(total_spend["total_cost"])
    total_spend["total_spend_z"] = (
        (total_spend["log_total_spend"] - total_spend["log_total_spend"].mean())
        / total_spend["log_total_spend"].std())

    size_df = cust_day.drop_duplicates("customer_id")[["customer_id", "size_z"]]
    df = cust_bid.merge(total_spend[["customer_id", "total_spend_z"]], on="customer_id", how="inner")
    df = df.merge(size_df, on="customer_id", how="inner")
    return df.dropna(subset=["log_bid_amount", "total_spend_z", "size_z"])


def bid_amount_mediation(df: pd.DataFrame, n_boot: int = N_BOOTSTRAP_MEDIATION,
                          n_perm: int = N_PERMUTATIONS_MEDIATION) -> dict:
    """size -> total_spend -> bid_amount | size, with bootstrap + permutation
    inference on the indirect (a * b) effect."""
    m_a = ols_hc3(df, "total_spend_z", ["size_z"])
    m_b = ols_hc3(df, "log_bid_amount", ["total_spend_z", "size_z"])
    m_c = ols_hc3(df, "log_bid_amount", ["size_z"])

    a_coef, a_p = m_a.params["size_z"], m_a.pvalues["size_z"]
    b_coef, b_p = m_b.params["total_spend_z"], m_b.pvalues["total_spend_z"]
    c_prime_coef, c_prime_p = m_b.params["size_z"], m_b.pvalues["size_z"]
    c_coef, c_p = m_c.params["size_z"], m_c.pvalues["size_z"]
    indirect = a_coef * b_coef

    rng = np.random.default_rng(RANDOM_STATE)
    n = len(df)
    boot_indirects = []
    for _ in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        sub = df.iloc[idx]
        if sub["size_z"].std() == 0 or sub["total_spend_z"].std() == 0:
            continue
        try:
            ma = ols_hc3(sub, "total_spend_z", ["size_z"])
            mb = ols_hc3(sub, "log_bid_amount", ["total_spend_z", "size_z"])
            boot_indirects.append(ma.params["size_z"] * mb.params["total_spend_z"])
        except Exception:
            continue
    boot_indirects = np.array(boot_indirects)
    boot_ci_low, boot_ci_high = np.percentile(boot_indirects, [2.5, 97.5])

    rng2 = np.random.default_rng(RANDOM_STATE + 1)
    size_vals = df["size_z"].values.copy()
    null_indirects = []
    for _ in range(n_perm):
        shuffled = rng2.permutation(size_vals)
        perm_df = df.copy()
        perm_df["size_z"] = shuffled
        try:
            ma = ols_hc3(perm_df, "total_spend_z", ["size_z"])
            mb = ols_hc3(perm_df, "log_bid_amount", ["total_spend_z", "size_z"])
            null_indirects.append(ma.params["size_z"] * mb.params["total_spend_z"])
        except Exception:
            continue
    null_indirects = np.array(null_indirects)
    perm_p = float((np.abs(null_indirects) >= np.abs(indirect)).mean())

    return {
        "n_customers": int(n),
        "a_coef": float(a_coef), "a_p": float(a_p),
        "b_coef": float(b_coef), "b_p": float(b_p),
        "c_prime_coef": float(c_prime_coef), "c_prime_p": float(c_prime_p),
        "c_coef": float(c_coef), "c_p": float(c_p),
        "indirect_effect": float(indirect),
        "indirect_bootstrap_ci": [float(boot_ci_low), float(boot_ci_high)],
        "indirect_bootstrap_excludes_zero": bool(not (boot_ci_low <= 0 <= boot_ci_high)),
        "indirect_permutation_p": perm_p,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> dict:
    adgroup_dim, panel = load_panel()
    cust_day = build_customer_day_panel(adgroup_dim, panel)
    cpc_sample = build_cpc_sample(cust_day)

    results = {
        "cost_sharing_artifact_check": cost_sharing_artifact_check(cpc_sample),
        "lagged_mediation_check": lagged_mediation_check(cust_day, cpc_sample),
    }

    bid_df = build_bid_amount_sample(adgroup_dim, cust_day)
    if len(bid_df) >= 30:
        results["bid_amount_mediation"] = bid_amount_mediation(bid_df)
    else:
        results["bid_amount_mediation"] = {"note": f"insufficient sample (n={len(bid_df)})"}

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUTPUT_PATH}")
    return results


if __name__ == "__main__":
    main()
