"""
supplementary_robustness/03_equivalence_and_sensitivity_notes.py

Two complementary checks on the repository's central null results:

  1. TOST (two one-sided tests) equivalence testing -- assesses whether an
     effect can be formally bounded within a pre-specified equivalence
     margin (SESOI), rather than merely failing to reject a point-null.
     Applied to RQ1 (account maturity -> initial growth slope) and
     RQ2/H2b (does adding account maturity improve growth prediction?).

  2. Oster's delta (Oster, 2019) -- an omitted-variable-bias sensitivity
     statistic for the bid_amount b-path reported in
     01_alternative_outcome_mediation.py, including the numerical-
     stability guard described in 03_equivalence_and_sensitivity_notes.md:
     delta* is only interpreted as evidence of robustness when the R^2
     increment from the additional control clears a minimum threshold.

Supports: root README.md Sections 3.2 and 6.

Expected inputs:
  - RQ1: a customer-level dataframe with columns [customer_id, maturity_z,
    slope_z] (one row per customer; maturity_z = standardized log all-time
    ad-group count, slope_z = standardized mean early-window growth slope).
    Produced by the cold-start trajectory pipeline (coldstart_v5/step_k).
  - RQ2/H2b: an array of per-split Spearman-rho improvements (own-signal +
    maturity vs. own-signal alone) from repeated group-shuffled splits.
    Produced by src/analysis/rq2_prediction_validation.py.
  - bid_amount mediation: reuses build_bid_amount_sample() from
    01_alternative_outcome_mediation.py.

This script is written so each function accepts already-prepared arrays /
dataframes with a documented schema, since the upstream feature-engineering
pipelines (cold-start sample construction, RQ2 window features) live in
src/coldstart_v5/ and src/analysis/ rather than being duplicated here.

Output: supplementary_robustness/outputs/03_equivalence_and_sensitivity_notes.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

RANDOM_STATE = 2026
ALPHA = 0.05

RQ1_CUSTOMER_LEVEL_PATH = Path("outputs/coldstart_v5/rq1_customer_level.csv")
RQ2_SPLIT_IMPROVEMENTS_PATH = Path("outputs/coldstart_v5/rq2_splithalf_improvements.csv")
ADGROUP_DIM_PATH = Path("data/adgroup_dim.tsv")
PERF_PANEL_PATH = Path("data/ad_performance.tsv")

OUTPUT_PATH = Path("supplementary_robustness/outputs/03_equivalence_and_sensitivity_notes.json")

# TOST margins (pre-specified SESOI, see docs/METHODOLOGY_NOTES.md)
RQ1_TOST_MARGIN_STD = 0.20      # standardized-effect-size units
RQ2_H2B_TOST_MARGIN_RHO = 0.05  # Spearman-rho units
N_BOOTSTRAP_TOST = 5000

# Oster's delta config
OSTER_RMAX_MULTIPLIER = 1.3
OSTER_ROBUST_THRESHOLD = 1.0
OSTER_MIN_R2_INCREMENT = 0.01   # below this, delta* is reported but not used as evidence


# ---------------------------------------------------------------------------
# 1. TOST equivalence testing (generic, bootstrap-based two one-sided test)
# ---------------------------------------------------------------------------
def ols_beta_1d(x: np.ndarray, y: np.ndarray) -> float:
    X = sm.add_constant(x)
    return float(sm.OLS(y, X).fit().params[1])


def tost_bivariate(customer_df: pd.DataFrame, x_col: str, y_col: str, margin: float,
                    n_boot: int = N_BOOTSTRAP_TOST, seed: int = RANDOM_STATE) -> dict:
    """TOST for a bivariate customer-level regression coefficient (e.g. RQ1:
    maturity_z -> slope_z). Uses a customer-level bootstrap to build the
    sampling distribution of the standardized coefficient, then evaluates
    the probability mass beyond +/- margin as the two one-sided p-values."""
    n = len(customer_df)
    observed_beta = ols_beta_1d(customer_df[x_col].values, customer_df[y_col].values)

    rng = np.random.default_rng(seed)
    boot_betas = []
    idx_arr = np.arange(n)
    for _ in range(n_boot):
        idx = rng.choice(idx_arr, size=n, replace=True)
        sub = customer_df.iloc[idx]
        if sub[x_col].std() == 0:
            continue
        boot_betas.append(ols_beta_1d(sub[x_col].values, sub[y_col].values))
    boot_betas = np.array(boot_betas)

    p_upper = float((boot_betas >= margin).mean())
    p_lower = float((boot_betas <= -margin).mean())
    tost_p = max(p_upper, p_lower)

    return {
        "n": int(n), "observed_beta": observed_beta, "margin": margin,
        "n_valid_bootstrap": int(len(boot_betas)),
        "p_upper": p_upper, "p_lower": p_lower, "tost_p": tost_p,
        "equivalence_established": bool(tost_p < ALPHA),
        "verdict": ("equivalence established -- can be upgraded to a genuine confirmed null"
                    if tost_p < ALPHA else
                    "equivalence not established -- report as non-significant, "
                    "formal equivalence inconclusive, not as a confirmed null"),
    }


def tost_univariate_improvement(improvements: np.ndarray, margin: float) -> dict:
    """TOST for a one-sample quantity (e.g. RQ2/H2b: per-split Spearman-rho
    improvement from adding account maturity as a feature). Uses the
    empirical distribution of `improvements` directly (already produced by
    repeated group-shuffled splits upstream), so no further resampling of
    customers is needed here."""
    improvements = np.asarray(improvements)
    p_upper = float((improvements >= margin).mean())
    p_lower = float((improvements <= -margin).mean())
    tost_p = max(p_upper, p_lower)

    return {
        "n_splits": int(len(improvements)), "mean_improvement": float(improvements.mean()),
        "margin": margin, "p_upper": p_upper, "p_lower": p_lower, "tost_p": tost_p,
        "equivalence_established": bool(tost_p < ALPHA),
        "verdict": ("equivalence established" if tost_p < ALPHA else
                    "equivalence not established -- report as non-significant, "
                    "formal equivalence inconclusive"),
    }


# ---------------------------------------------------------------------------
# 2. Oster's delta -- omitted-variable-bias sensitivity, with a stability guard
# ---------------------------------------------------------------------------
def oster_delta(beta_restricted: float, beta_full: float, r2_restricted: float, r2_full: float,
                 rmax_multiplier: float = OSTER_RMAX_MULTIPLIER,
                 min_r2_increment: float = OSTER_MIN_R2_INCREMENT,
                 robust_threshold: float = OSTER_ROBUST_THRESHOLD) -> dict:
    """Oster (2019) delta*: how much stronger an unobserved confounder would
    need to be, relative to the observed controls, to explain away the
    coefficient of interest.

    delta* = (beta_full / (beta_restricted - beta_full)) * (Rmax - R2_full) / (R2_full - R2_restricted)

    IMPORTANT: the R^2 increment (R2_full - R2_restricted) sits in the
    denominator. When it is close to zero, delta* diverges regardless of
    the underlying relationship's true robustness -- a large |delta*| in
    that regime is a numerical artifact, not evidence of robustness. This
    function therefore reports a `stability_flag` and refuses to certify
    "robust" when the R^2 increment falls below `min_r2_increment`, even if
    |delta*| clears `robust_threshold`.
    """
    r_max = min(1.0, rmax_multiplier * r2_full)
    denom_beta = beta_restricted - beta_full
    denom_r2 = r2_full - r2_restricted

    result = {
        "beta_restricted": float(beta_restricted), "r2_restricted": float(r2_restricted),
        "beta_full": float(beta_full), "r2_full": float(r2_full),
        "r2_increment": float(denom_r2), "r2_increment_min_threshold": min_r2_increment,
        "r_max": float(r_max), "robust_threshold": robust_threshold,
    }

    if denom_beta == 0 or denom_r2 <= 0 or r_max <= r2_full:
        result.update({"delta_star": None, "stability_flag": "degenerate",
                        "verdict": ("delta* not computable -- R^2 decreased or the coefficient "
                                    "did not move when the additional control was added; Oster's "
                                    "premise (controls move R^2 and the coefficient together) does "
                                    "not hold here.")})
        return result

    delta_star = (beta_full / denom_beta) * (r_max - r2_full) / denom_r2
    result["delta_star"] = float(delta_star)

    if denom_r2 < min_r2_increment:
        result.update({
            "stability_flag": "unstable_small_r2_increment",
            "verdict": (f"delta*={delta_star:+.3f} is computed but the R^2 increment "
                        f"({denom_r2:.4f}) is below the stability threshold ({min_r2_increment}); "
                        "the additional control adds essentially no explanatory power, so delta* "
                        "is near the formula's singularity and is NOT reported as evidence of "
                        "robustness. The R^2 increment itself is the more interpretable statistic "
                        "here."),
        })
        return result

    coef_sign_stable = np.sign(beta_restricted) == np.sign(beta_full)
    if not coef_sign_stable:
        result.update({"stability_flag": "stable_but_sign_flip",
                        "verdict": "R^2 increment is adequate, but the coefficient sign flipped "
                                   "between the restricted and full model, so delta*'s magnitude "
                                   "is not a meaningful robustness statistic here."})
    elif abs(delta_star) >= robust_threshold:
        result.update({"stability_flag": "stable_robust",
                        "verdict": f"|delta*|={abs(delta_star):.3f} >= {robust_threshold} in a "
                                   "numerically stable region -- conventional robustness criterion met."})
    else:
        result.update({"stability_flag": "stable_not_robust",
                        "verdict": f"|delta*|={abs(delta_star):.3f} < {robust_threshold} in a "
                                   "numerically stable region -- an omitted confounder weaker than "
                                   "the observed controls could account for this effect."})
    return result


def ols_hc3(df: pd.DataFrame, y_col: str, x_cols: list[str]):
    X = sm.add_constant(df[x_cols])
    return sm.OLS(df[y_col], X).fit(cov_type="HC3")


def bid_amount_oster_delta() -> dict:
    """Refits the restricted (spend-only) and full (spend + size) bid_amount
    models to compute Oster's delta for the b-path (total_spend_z ->
    log_bid_amount). Reuses the sample-construction logic from
    01_alternative_outcome_mediation.py; see that file for
    build_bid_amount_sample()."""
    try:
        from importlib import import_module
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        mod01 = import_module("01_alternative_outcome_mediation")
    except Exception as e:
        return {"note": f"could not import 01_alternative_outcome_mediation.py ({e}), skipped"}

    adgroup_dim, panel = mod01.load_panel()
    cust_day = mod01.build_customer_day_panel(adgroup_dim, panel)
    bid_df = mod01.build_bid_amount_sample(adgroup_dim, cust_day)
    if len(bid_df) < 30:
        return {"note": f"insufficient sample (n={len(bid_df)}), skipped"}

    m_restricted = ols_hc3(bid_df, "log_bid_amount", ["total_spend_z"])
    m_full = ols_hc3(bid_df, "log_bid_amount", ["total_spend_z", "size_z"])

    return oster_delta(
        beta_restricted=m_restricted.params["total_spend_z"], r2_restricted=m_restricted.rsquared,
        beta_full=m_full.params["total_spend_z"], r2_full=m_full.rsquared,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> dict:
    results = {}

    if RQ1_CUSTOMER_LEVEL_PATH.exists():
        rq1_df = pd.read_csv(RQ1_CUSTOMER_LEVEL_PATH)
        results["rq1_tost"] = tost_bivariate(rq1_df, "maturity_z", "slope_z", RQ1_TOST_MARGIN_STD)
    else:
        results["rq1_tost"] = {"note": f"{RQ1_CUSTOMER_LEVEL_PATH} not found, skipped"}

    if RQ2_SPLIT_IMPROVEMENTS_PATH.exists():
        improvements = pd.read_csv(RQ2_SPLIT_IMPROVEMENTS_PATH)["improvement"].values
        results["rq2_h2b_tost"] = tost_univariate_improvement(improvements, RQ2_H2B_TOST_MARGIN_RHO)
    else:
        results["rq2_h2b_tost"] = {"note": f"{RQ2_SPLIT_IMPROVEMENTS_PATH} not found, skipped"}

    results["bid_amount_bpath_oster_delta"] = bid_amount_oster_delta()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUTPUT_PATH}")
    return results


if __name__ == "__main__":
    main()
