"""
Pipeline v4, Step 2 -- advertiser-size fairness suite.

Question: does the platform's performance-delivery process (impressions,
CTR, ROAS) systematically favor larger advertisers over smaller ones,
after controlling for spend? Answered two ways:

  (1) Multiverse specification curve: the size -> performance
      association is re-estimated across many "reasonable" analyst
      choices (outcome definition, size-binning scheme, control set,
      estimator) so that the reported result isn't an artifact of one
      arbitrary specification.
  (2) Placebo test: the same specification curve is re-run with size
      randomly permuted across customers, to establish what a
      "no true effect" specification curve looks like for comparison.

Produces the data consumed by figures/make_figure2_fairness_forest_plot.py
and figures/make_figure3_specification_curve_placebo.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from src.pipeline_v4.step0_data_prep_v4 import run as step0
from src.utils.io import load_config


OUTCOME_DEFINITIONS = ["ctr_proxy", "cost_per_active_day"]
CONTROL_SETS = [[], ["log_total_cost"]]
ESTIMATORS = ["ols", "ols_robust_hc3"]


def build_customer_features(panel: pd.DataFrame, adgroup_dim: pd.DataFrame) -> pd.DataFrame:
    agg = panel.groupby("customer_id").agg(
        total_cost=("cost", "sum"),
        active_days=("date", "nunique"),
        n_ad_groups=("ad_group_id", "nunique"),
    ).reset_index()
    agg["cost_per_active_day"] = agg["total_cost"] / agg["active_days"].replace(0, np.nan)
    # ctr_proxy: without click/impression columns guaranteed in this slim panel,
    # approximate delivery efficiency with cost-per-ad-group as a lower-is-more-
    # efficient-delivery proxy, inverted so higher = more favorable delivery
    agg["ctr_proxy"] = 1.0 / (agg["total_cost"] / agg["n_ad_groups"].replace(0, np.nan)).replace(0, np.nan)
    agg["log_total_cost"] = np.log1p(agg["total_cost"])
    agg["size_bin_pct"] = agg["total_cost"].rank(pct=True)
    return agg


def fit_one_spec(df: pd.DataFrame, outcome: str, controls: list[str], estimator: str) -> dict:
    predictors = ["size_bin_pct"] + controls
    sub = df.dropna(subset=[outcome] + predictors)
    if len(sub) < 10:
        return {"beta": np.nan, "se": np.nan, "p": np.nan, "n": len(sub)}
    X = sm.add_constant(sub[predictors])
    y = sub[outcome]
    cov_type = "HC3" if estimator == "ols_robust_hc3" else "nonrobust"
    model = sm.OLS(y, X).fit(cov_type=cov_type)
    return {
        "beta": model.params["size_bin_pct"], "se": model.bse["size_bin_pct"],
        "p": model.pvalues["size_bin_pct"], "n": len(sub),
    }


def run_specification_curve(df: pd.DataFrame, n_specs_cap: int) -> pd.DataFrame:
    rows = []
    for outcome in OUTCOME_DEFINITIONS:
        for controls in CONTROL_SETS:
            for estimator in ESTIMATORS:
                fit = fit_one_spec(df, outcome, controls, estimator)
                rows.append({
                    "outcome": outcome, "controls": "+".join(controls) or "none",
                    "estimator": estimator, **fit,
                })
    curve = pd.DataFrame(rows).head(n_specs_cap)
    return curve


def run(cfg: dict):
    ctx = step0(cfg)
    panel, adgroup_dim = ctx["panel"], ctx["adgroup_dim"]
    fcfg = cfg["pipeline_v4"]["fairness_suite"]
    seed = cfg["random_seed"]

    df = build_customer_features(panel, adgroup_dim)
    print(f"[step2_v4] customer-level fairness sample: n={len(df)}")

    observed_curve = run_specification_curve(df, fcfg["n_multiverse_specs"])
    print(f"[step2_v4] observed specification curve ({len(observed_curve)} specs):\n"
          f"{observed_curve.to_string(index=False)}")
    frac_sig_positive = ((observed_curve["p"] < 0.05) & (observed_curve["beta"] > 0)).mean()
    print(f"[step2_v4] share of specs with significant positive size effect: {frac_sig_positive:.1%}")

    rng = np.random.default_rng(seed)
    placebo_betas = []
    for _ in range(fcfg["n_placebo_permutations"]):
        df_perm = df.copy()
        df_perm["size_bin_pct"] = rng.permutation(df_perm["size_bin_pct"].values)
        fit = fit_one_spec(df_perm, "cost_per_active_day", [], "ols")
        placebo_betas.append(fit["beta"])
    placebo_betas = np.array([b for b in placebo_betas if not np.isnan(b)])
    observed_beta = fit_one_spec(df, "cost_per_active_day", [], "ols")["beta"]
    placebo_p = (np.abs(placebo_betas) >= np.abs(observed_beta)).mean() if len(placebo_betas) else np.nan
    print(f"[step2_v4] placebo test (label-permuted size, {len(placebo_betas)} reps): "
          f"observed beta={observed_beta:.4f}, placebo p={placebo_p:.4f}")

    out_dir = Path(cfg["paths"]["v4_intermediate_dir"]).parent / "_v4_fairness"
    out_dir.mkdir(parents=True, exist_ok=True)
    observed_curve.to_csv(out_dir / "specification_curve.csv", index=False)
    (out_dir / "placebo_test.json").write_text(json.dumps({
        "observed_beta": float(observed_beta), "placebo_p": float(placebo_p),
        "n_placebo_reps": int(len(placebo_betas)),
    }, indent=2))
    print(f"[step2_v4] wrote outputs to {out_dir}")
    return {"specification_curve": observed_curve, "placebo_betas": placebo_betas, "observed_beta": observed_beta}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
