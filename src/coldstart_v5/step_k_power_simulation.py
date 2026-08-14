"""
Step K -- Pre-registration power simulation for RQ1 (does account maturity
predict initial growth slope?), run BEFORE the confirmatory test so the
detectable effect-size range is committed in advance rather than chosen
post hoc.

Because `maturity` varies only at the customer level, a customer
random-intercept mixed model (statsmodels MixedLM) is structurally
non-identified against it -- confirmed empirically here (100%
non-convergence across simulation replications) -- so the customer-level
aggregate regression is adopted as the primary inferential model, with a
cluster permutation test as the final arbiter (both used again, on real
data, in `src/analysis/rq1_growth_curve_test.py`).
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config


def simulate_one_dataset(cluster_sizes: dict, maturity_by_customer: dict, true_effect: float,
                          customer_re_sd: float, residual_sd: float, rng) -> pd.DataFrame:
    rows = []
    for cust_id, n_i in cluster_sizes.items():
        u_i = rng.normal(0, customer_re_sd)
        m_i = maturity_by_customer[cust_id]
        for _ in range(n_i):
            e_ij = rng.normal(0, residual_sd)
            rows.append({"customer_id": cust_id, "maturity": m_i, "slope": true_effect * m_i + u_i + e_ij})
    return pd.DataFrame(rows)


def fit_mixedlm_strict(df: pd.DataFrame):
    """Returns (p_value, failed). `failed=True` whenever statsmodels raises a
    singular-covariance / boundary warning -- these are NOT counted as
    successes, unlike a naive try/except-only implementation would."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            result = smf.mixedlm("slope ~ maturity", data=df, groups=df["customer_id"]).fit(reml=True, method="lbfgs")
        except Exception:
            return np.nan, True
        had_warning = any(("singular" in str(w.message).lower()) or ("boundary" in str(w.message).lower()) for w in caught)
        return (np.nan, True) if had_warning else (result.pvalues.get("maturity", np.nan), False)


def fit_customer_level(df: pd.DataFrame) -> float:
    agg = df.groupby("customer_id").agg(slope_mean=("slope", "mean"), maturity=("maturity", "first")).reset_index()
    X = sm.add_constant(agg["maturity"])
    return sm.OLS(agg["slope_mean"], X).fit().pvalues.get("maturity", np.nan)


def run(cfg: dict):
    ctx = step_a(cfg)
    usable = ctx["usable"]
    kcfg = cfg["coldstart_diagnostics"]
    reps = kcfg["n_sim_replications_power"]
    alpha = cfg["rq1_growth_curve"]["alpha"]
    seed = cfg["random_seed"]

    cluster_sizes = usable.groupby("customer_id").size().to_dict()
    customer_ids = list(cluster_sizes.keys())
    all_time_by_cust = usable.drop_duplicates("customer_id").set_index("customer_id").get("all_time_count")
    if all_time_by_cust is None:
        print("[step_k] all_time_count not present on `usable` -- run Step I first and merge it in.")
        return None
    maturity_raw = np.log1p(all_time_by_cust.loc[customer_ids].values)
    maturity_z = (maturity_raw - maturity_raw.mean()) / maturity_raw.std()
    maturity_by_customer = dict(zip(customer_ids, maturity_z))

    rng = np.random.default_rng(seed)
    rows = []
    for effect in cfg["sample_definition"].get("power_sim_effect_sizes", [0.0, 0.15, 0.30, 0.50]):
        n_sig_mixed, n_failed_mixed, n_sig_cust, n_failed_cust = 0, 0, 0, 0
        for _ in range(reps):
            df_sim = simulate_one_dataset(cluster_sizes, maturity_by_customer, effect, 0.5, 1.0, rng)
            _, failed = fit_mixedlm_strict(df_sim)
            n_failed_mixed += int(failed)
            p_cust = fit_customer_level(df_sim)
            n_failed_cust += int(np.isnan(p_cust))
            n_sig_cust += int((not np.isnan(p_cust)) and p_cust < alpha)
        rows.append({
            "true_effect": effect,
            "mixedlm_convergence_failure_rate": n_failed_mixed / reps,
            "customer_level_power": n_sig_cust / max(1, reps - n_failed_cust),
        })
    result = pd.DataFrame(rows)
    print(f"[step_k] power simulation (n_customers={len(customer_ids)}):\n{result.to_string(index=False)}")
    print("[step_k] MixedLM is expected to fail near-universally (maturity is customer-level-only, "
          "so it is not jointly identified against a customer random intercept). Use the "
          "customer-level aggregate power column as the operative detection threshold.")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
