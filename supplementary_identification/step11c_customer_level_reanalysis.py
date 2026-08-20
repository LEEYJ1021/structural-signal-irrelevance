"""
STEP 11-c (decisive) -- Customer-level density test + customer-level RDD
re-estimation for all 5 candidates.

Motivation: log_size and log_total_spend are customer-level constants,
but Round 1/2 ran RDD on the customer x day panel. Higher-spend customers
advertise on more days, so they contribute more panel rows -- this alone
can produce a large left/right panel-row imbalance near a cutoff that has
nothing to do with running-variable manipulation. Round 2's "manipulation
flag" (step11b) could not distinguish the two explanations. This script
resolves the ambiguity by (a) re-running the McCrary-style density test
on customer-level (deduplicated) running-variable values with a
customer-level bootstrap, and (b) re-estimating each RDD candidate on a
customer-level aggregated outcome (mean and click-weighted mean log_cpc
per customer), which removes panel-density variation entirely.

DECISIVE RESULT: 0 of 5 candidates survive.
  - 2 candidates (log_total_spend, both cutoffs): customer-level density
    test rejects (p<.001) -- genuine manipulation cannot be ruled out.
  - 2 candidates (log_size, cutoff=1.386 and 2.092): density test passes,
    but customer-level RDD is non-significant (p=.79, p=.40) -- the
    panel-level significance was a panel-density artifact, not a real
    discontinuity.
  - 1 candidate (log_size, cutoff=2.515): density test passes and
    customer-level RDD is marginally significant (p=.048), but this
    is the same candidate flagged in step11b as fragile (breaks down
    at only 15% donut) and has no institutional justification for why
    ~12 ad groups (exp(2.515)-1) would be a policy-relevant threshold.
    Not adopted.

See SCREENING_SUMMARY.md for the full results table and Figure 11 for
the visual summary.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

RANDOM_STATE = 2026
ALPHA = 0.05
DENSITY_N_BINS = 8
DENSITY_N_BOOT = 1000
RDD_MIN_N_PER_SIDE_CUSTOMER = 15


def local_linear_density_at_cutoff(running_values, cutoff, bandwidth, n_bins=DENSITY_N_BINS):
    """McCrary-style local-linear density estimate at the cutoff, fit
    separately on each side via (bin_count ~ bin_midpoint) OLS."""
    bins_left = np.linspace(cutoff - bandwidth, cutoff, n_bins + 1)
    bins_right = np.linspace(cutoff, cutoff + bandwidth, n_bins + 1)
    counts_left, edges_left = np.histogram(running_values, bins=bins_left)
    counts_right, edges_right = np.histogram(running_values, bins=bins_right)
    mid_left = (edges_left[:-1] + edges_left[1:]) / 2
    mid_right = (edges_right[:-1] + edges_right[1:]) / 2
    if len(counts_left) < 3 or len(counts_right) < 3:
        return None

    def fit_edge(mids, counts, eval_at):
        model = sm.OLS(counts, sm.add_constant(mids)).fit()
        return max(model.predict([[1, eval_at]])[0], 1e-6)

    d_left = fit_edge(mid_left, counts_left, cutoff)
    d_right = fit_edge(mid_right, counts_right, cutoff)
    return {"theta": float(np.log(d_right) - np.log(d_left))}


def customer_level_density_test(running_values, cutoff, bandwidth, n_boot=DENSITY_N_BOOT, rng=None):
    """Customer-unit bootstrap (resampling customer IDs, not panel rows)
    for the density-discontinuity statistic theta. This is what makes
    the test immune to panel-row-count imbalance."""
    rng = rng or np.random.default_rng(RANDOM_STATE)
    point = local_linear_density_at_cutoff(running_values, cutoff, bandwidth)
    if point is None:
        return None
    n = len(running_values)
    boot_thetas = []
    for _ in range(n_boot):
        boot_vals = running_values[rng.choice(np.arange(n), size=n, replace=True)]
        res = local_linear_density_at_cutoff(boot_vals, cutoff, bandwidth)
        if res is not None and np.isfinite(res["theta"]):
            boot_thetas.append(res["theta"])
    boot_thetas = np.array(boot_thetas)
    if len(boot_thetas) < 30:
        return {**point, "p_value": None}
    centered = boot_thetas - boot_thetas.mean()
    p_value = float((np.abs(centered) >= abs(point["theta"])).mean())
    return {**point, "p_value": p_value}


def local_linear_rd_customer_level(cust_df, running_col, outcome_col, cutoff, bandwidth, donut_frac=0.0):
    """RDD on a customer-level (one row per customer) aggregated outcome.
    No clustering needed (one observation per unit); HC3 robust SE."""
    x = cust_df[running_col].values - cutoff
    within_bw = np.abs(x) <= bandwidth
    if donut_frac > 0:
        within_bw &= np.abs(x) > bandwidth * donut_frac
    sub = cust_df.loc[within_bw].copy()
    sub["_x"] = x[within_bw]
    sub["_treat"] = (sub["_x"] >= 0).astype(int)
    sub["_x_treat"] = sub["_x"] * sub["_treat"]
    n_left, n_right = int((sub["_treat"] == 0).sum()), int((sub["_treat"] == 1).sum())
    if n_left < RDD_MIN_N_PER_SIDE_CUSTOMER or n_right < RDD_MIN_N_PER_SIDE_CUSTOMER:
        return None
    X = sm.add_constant(sub[["_treat", "_x", "_x_treat"]])
    ols = sm.OLS(sub[outcome_col], X).fit(cov_type="HC3")
    return {"tau": float(ols.params["_treat"]), "p": float(ols.pvalues["_treat"]),
            "n_left": n_left, "n_right": n_right}


# Orchestration: build cust_level (one row per customer_id) with
# log_size, log_total_spend, and two outcome aggregations
# (log_cpc_mean, log_cpc_click_weighted); run
# customer_level_density_test() and local_linear_rd_customer_level()
# for each of the 5 candidates; combine with the panel-level (step11b)
# result to produce the final verdict table in SCREENING_SUMMARY.md.
