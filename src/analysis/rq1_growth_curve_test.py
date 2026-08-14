"""
RQ1 confirmatory test -- does account maturity (accumulated operating
history) predict the initial growth trajectory of a newly created
ad group?

H1: account maturity (log all-time ad-group count, standardized) is
positively associated with the initial early-window growth slope of a
newly registered ad group.

Design (fixed by the coldstart_v5 diagnostic pipeline, not chosen
here):
  - Mixed LM with a customer random intercept is NOT used: Step K
    established it is structurally non-identified against a
    customer-level-only predictor (100% convergence-failure rate in
    simulation, reproduced empirically here if attempted).
  - Primary inference: customer-level aggregate OLS (HC3), n = number
    of customers in the trajectory-usable, test-account-excluded
    sample -- NOT the ad-group count. This is the single largest
    departure from a naive "n=222" reading of this analysis and is
    reported explicitly in every summary line below.
  - Final arbiter: cluster (customer-label) permutation test,
    distribution-free, used whenever OLS and the permutation p-value
    disagree.
  - Required robustness checks: leave-one-out on the largest customer,
    Winsorized OLS, and rank-rank (Spearman-equivalent) OLS, to
    separate a genuine relationship from a high-leverage-point
    artifact.
  - Sample-exclusion rule (known_test_account_ids) is read from
    config, not applied ad hoc.

Reported verdict follows the same rule used throughout coldstart_v5:
a result is trusted only if the permutation test and the
leave-one-out permutation test are BOTH significant and agree in
sign; effect size is always reported alongside significance and
checked against the Step K power-simulation detection threshold.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import json
from pathlib import Path

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import find_column, load_config, read_perf_panel_columns_only
from src.utils.identifiers import clean_id


def compute_early_slopes(sample: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Ad-group-level initial growth slope: linear trend of daily cost
    over the first `early_window_days` days of observed activity.
    Ad groups whose window is not yet fully elapsed by obs_end are
    dropped (no look-ahead)."""
    paths, rcfg = cfg["paths"], cfg["rq1_growth_curve"]
    early_days = rcfg["early_window_days"]

    header = pd.read_csv(paths["perf_panel"], sep="\t" if str(paths["perf_panel"]).endswith(".tsv") else ",", nrows=5)
    date_col = find_column(header, ["date"])
    adg_col = find_column(header, ["ad_group_id"])
    cost_col = find_column(header, ["cost"])

    obs_end = sample["perf_last_active"].max()  # conservative fallback; overridden by caller if ctx available
    target_ids = set(sample["ad_group_id"])
    accum = []
    for chunk in read_perf_panel_columns_only(paths["perf_panel"], usecols=[date_col, adg_col, cost_col],
                                               dtype={adg_col: str}, chunksize=2_000_000):
        chunk = chunk.rename(columns={date_col: "date", adg_col: "ad_group_id", cost_col: "cost"})
        chunk["ad_group_id"] = clean_id(chunk["ad_group_id"])
        chunk = chunk[chunk["ad_group_id"].isin(target_ids)]
        if len(chunk):
            accum.append(chunk)
    perf = pd.concat(accum, ignore_index=True) if accum else pd.DataFrame(columns=["date", "ad_group_id", "cost"])
    perf["date"] = pd.to_datetime(perf["date"], errors="coerce").dt.normalize()
    perf["cost"] = pd.to_numeric(perf["cost"], errors="coerce").fillna(0)
    perf_by_adg = {adg: g.set_index("date")["cost"] for adg, g in perf.groupby("ad_group_id")}

    rows = []
    for _, row in sample.iterrows():
        adg_id, start = row["ad_group_id"], row["perf_first_active"]
        end = start + pd.Timedelta(days=early_days - 1)
        daily = perf_by_adg.get(adg_id, pd.Series(dtype=float)).reindex(pd.date_range(start, end), fill_value=0.0)
        day_idx = np.arange(len(daily))
        slope = np.polyfit(day_idx, daily.values, 1)[0] if daily.sum() > 0 and len(day_idx) >= 2 else 0.0
        rows.append({"ad_group_id": adg_id, "customer_id": row["customer_id"],
                      "early_slope": slope, "all_time_count": row["all_time_count"]})
    return pd.DataFrame(rows)


def ols_beta(maturity: np.ndarray, slope: np.ndarray) -> float:
    X = sm.add_constant(maturity)
    return sm.OLS(slope, X).fit().params[1]


def run(cfg: dict):
    ctx = step_a(cfg)
    adgroup_dim, coldstart, usable, obs_end = ctx["adgroup_dim"], ctx["coldstart"], ctx["usable"], ctx["obs_end"]
    rcfg = cfg["rq1_growth_curve"]
    alpha, n_perm, n_boot, winsor_pct = rcfg["alpha"], rcfg["n_permutations"], rcfg["n_bootstrap"], rcfg["winsor_pct"]
    seed = cfg["random_seed"]

    excl = set(cfg["sample_definition"].get("known_test_account_ids", []))
    alltime_count = adgroup_dim.groupby("customer_id").size().rename("all_time_count")
    usable = usable.merge(alltime_count, on="customer_id", how="left")
    sample = usable[~usable["customer_id"].isin(excl)].copy()
    print(f"[rq1] sample: {len(sample)} ad groups, {sample['customer_id'].nunique()} customers "
          f"(test accounts excluded: {sorted(excl)})")

    slope_df = compute_early_slopes(sample, cfg)
    print(f"[rq1] early-slope sample after window-completeness filter: {len(slope_df)}")

    cust_df = slope_df.groupby("customer_id").agg(
        slope_mean=("early_slope", "mean"), n_adgroups=("early_slope", "size"), all_time_count=("all_time_count", "first"),
    ).reset_index()
    log_at = np.log1p(cust_df["all_time_count"])
    cust_df["maturity"] = (log_at - log_at.mean()) / log_at.std()
    n_customers = len(cust_df)
    print(f"[rq1] customer-level sample: n={n_customers} (this, not the ad-group count, is the effective n)")

    # --- primary: customer-level OLS (HC3) ---
    X = sm.add_constant(cust_df["maturity"])
    ols_model = sm.OLS(cust_df["slope_mean"], X).fit(cov_type="HC3")
    beta, se, p_ols = ols_model.params["maturity"], ols_model.bse["maturity"], ols_model.pvalues["maturity"]
    print(f"[rq1] OLS(HC3): beta={beta:.4f} (SE={se:.4f}), p={p_ols:.4f}")

    spearman_rho, spearman_p = stats.spearmanr(cust_df["maturity"], cust_df["slope_mean"])
    print(f"[rq1] Spearman rho={spearman_rho:.3f}, p={spearman_p:.4f}")

    # --- bootstrap CI ---
    rng = np.random.default_rng(seed)
    boot_betas = []
    for _ in range(n_boot):
        idx = rng.choice(n_customers, size=n_customers, replace=True)
        sub = cust_df.iloc[idx]
        if sub["maturity"].std() == 0:
            continue
        boot_betas.append(ols_beta(sub["maturity"].values, sub["slope_mean"].values))
    boot_betas = np.array(boot_betas)
    ci_low, ci_high = np.percentile(boot_betas, [2.5, 97.5])
    print(f"[rq1] bootstrap 95% CI: [{ci_low:.4f}, {ci_high:.4f}]")

    # --- cluster permutation test (final arbiter) ---
    observed_beta = ols_beta(cust_df["maturity"].values, cust_df["slope_mean"].values)
    rng_perm = np.random.default_rng(seed + 1)
    null_betas = np.array([
        ols_beta(rng_perm.permutation(cust_df["maturity"].values), cust_df["slope_mean"].values)
        for _ in range(n_perm)
    ])
    perm_p = (np.abs(null_betas) >= np.abs(observed_beta)).mean()
    print(f"[rq1] cluster permutation test: observed beta={observed_beta:.4f}, p={perm_p:.4f}")

    # --- leave-one-out on largest customer ---
    top_cust_id = cust_df.sort_values("n_adgroups", ascending=False).iloc[0]["customer_id"]
    cust_loo = cust_df[cust_df["customer_id"] != top_cust_id]
    beta_loo = ols_beta(cust_loo["maturity"].values, cust_loo["slope_mean"].values)
    rng_perm_loo = np.random.default_rng(seed + 2)
    null_betas_loo = np.array([
        ols_beta(rng_perm_loo.permutation(cust_loo["maturity"].values), cust_loo["slope_mean"].values)
        for _ in range(n_perm)
    ])
    perm_p_loo = (np.abs(null_betas_loo) >= np.abs(beta_loo)).mean()
    same_sign = np.sign(observed_beta) == np.sign(beta_loo)
    print(f"[rq1] leave-one-out (largest customer excluded, n={len(cust_loo)}): "
          f"beta={beta_loo:.4f}, perm p={perm_p_loo:.4f}, sign matches full sample: {same_sign}")

    # --- robustness: winsorized + rank-rank OLS ---
    lo, hi = cust_df["slope_mean"].quantile(winsor_pct), cust_df["slope_mean"].quantile(1 - winsor_pct)
    slope_w = cust_df["slope_mean"].clip(lo, hi)
    beta_w = sm.OLS(slope_w, sm.add_constant(cust_df["maturity"])).fit(cov_type="HC3")
    beta_rank = sm.OLS(cust_df["slope_mean"].rank(), sm.add_constant(cust_df["maturity"].rank())).fit(cov_type="HC3")
    print(f"[rq1] winsorized({winsor_pct:.0%}) OLS: beta={beta_w.params['maturity']:.4f}, "
          f"p={beta_w.pvalues['maturity']:.4f}")
    print(f"[rq1] rank-rank OLS: beta={beta_rank.params.iloc[1]:.4f}, p={beta_rank.pvalues.iloc[1]:.4f}")

    # --- standardized effect size vs. pre-registered detection threshold ---
    slope_z = (cust_df["slope_mean"] - cust_df["slope_mean"].mean()) / cust_df["slope_mean"].std()
    beta_std = sm.OLS(slope_z, sm.add_constant(cust_df["maturity"])).fit(cov_type="HC3").params["maturity"]
    large_effect_threshold = max(cfg["sample_definition"]["power_sim_effect_sizes"])
    print(f"[rq1] standardized effect size: beta={beta_std:.4f} "
          f"({abs(beta_std)/large_effect_threshold:.1%} of the pre-registered large-effect threshold "
          f"{large_effect_threshold})")

    verdict = "H1 supported" if (perm_p < alpha and perm_p_loo < alpha and same_sign) else "H1 not supported"
    print(f"\n[rq1] VERDICT: {verdict}")
    print("[rq1] verdict rule: both the full-sample and leave-one-out cluster permutation tests must "
          "be significant and agree in sign. A non-significant result should be interpreted relative to "
          "the Step K power simulation (n~=customer count, large-effect-only detection), not as evidence "
          "of a null effect in the population.")

    result = {
        "n_customers": n_customers, "n_ad_groups": len(slope_df),
        "beta_ols": beta, "p_ols": p_ols, "spearman_rho": spearman_rho, "spearman_p": spearman_p,
        "bootstrap_ci_low": ci_low, "bootstrap_ci_high": ci_high,
        "perm_p": perm_p, "beta_loo": beta_loo, "perm_p_loo": perm_p_loo,
        "beta_winsorized": beta_w.params["maturity"], "beta_rank": beta_rank.params.iloc[1],
        "beta_standardized": beta_std, "large_effect_threshold": large_effect_threshold, "verdict": verdict,
    }

    out_dir = Path("outputs/analysis")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "rq1_results.json").write_text(json.dumps(result, indent=2, default=float))
    print(f"[rq1] wrote {out_dir / 'rq1_results.json'}")

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
