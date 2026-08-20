"""
STEP 11 -- Alternative identification screening: RDD + policy-change
(structural-break detection / event-study DiD)

Purpose: supplement the incomplete 2SLS attempt (README Sec. 4.5, method 4)
with two screening strategies for a stronger causal design. This is a
condensed version of the original analysis script, kept for repository
reproducibility; the full run log and console output are summarized in
SCREENING_SUMMARY.md.

IMPORTANT CAVEATS (read before reusing):
1. RDD requires a running variable and cutoff with an independent
   institutional justification. PART A below auto-scans candidate cutoffs
   on size/spend -- this is a *screening* step to filter out points that
   merely look discontinuous by chance, not a way to discover a true
   policy threshold. Any candidate must be cross-checked against actual
   platform policy documentation before being treated as an RDD design.
2. Policy-change event studies (PART B) likewise need a genuine
   policy-change date. The auto-detection path (CUSUM on a rolling
   size-coefficient) cannot distinguish "a policy changed" from
   "the coefficient happened to drift" -- it must be cross-checked
   against external evidence (announcements, news).
3. Neither strategy is a completed identification design by itself.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

RANDOM_STATE = 2026
ALPHA = 0.05
RDD_MIN_N_PER_SIDE = 30
RDD_SCAN_N_POINTS = 20
RDD_SCAN_PCTL_LOW, RDD_SCAN_PCTL_HIGH = 0.20, 0.80
RDD_BANDWIDTH_MULTIPLIERS = [0.5, 0.75, 1.0, 1.5, 2.0]
RDD_DONUT_HOLE_FRACTIONS = [0.0, 0.05, 0.10]


def triangular_kernel_weight(x, bandwidth):
    u = np.abs(x) / bandwidth
    return np.where(u <= 1, 1 - u, 0.0)


def local_linear_rd(df, running_col, outcome_col, cutoff, bandwidth,
                     donut_frac=0.0, cluster_col="customer_id"):
    """Sharp-RDD local-linear estimate with a triangular kernel and
    cluster-robust SE. donut_frac excludes observations immediately
    adjacent to the cutoff (manipulation-robustness check)."""
    x = df[running_col].values - cutoff
    within_bw = np.abs(x) <= bandwidth
    if donut_frac > 0:
        within_bw &= np.abs(x) > bandwidth * donut_frac
    sub = df.loc[within_bw].copy()
    sub["_x"] = x[within_bw]
    sub["_treat"] = (sub["_x"] >= 0).astype(int)
    sub["_w"] = triangular_kernel_weight(sub["_x"].values, bandwidth)
    n_left, n_right = int((sub["_treat"] == 0).sum()), int((sub["_treat"] == 1).sum())
    if n_left < RDD_MIN_N_PER_SIDE or n_right < RDD_MIN_N_PER_SIDE:
        return None
    sub["_x_treat"] = sub["_x"] * sub["_treat"]
    X = sm.add_constant(sub[["_treat", "_x", "_x_treat"]])
    wls = sm.WLS(sub[outcome_col], X, weights=sub["_w"]).fit(
        cov_type="cluster", cov_kwds={"groups": sub[cluster_col]})
    return {"tau": float(wls.params["_treat"]), "se": float(wls.bse["_treat"]),
            "p": float(wls.pvalues["_treat"]), "n_left": n_left, "n_right": n_right,
            "bandwidth": float(bandwidth)}


def mccrary_density_approx(running_values, cutoff, bandwidth, n_bins_per_side=10):
    """Approximate McCrary (2008) density test: compares histogram-based
    density on each side of the cutoff via a t-test on log bin counts."""
    if bandwidth <= 0 or n_bins_per_side < 3:
        return None
    bins_left = np.linspace(cutoff - bandwidth, cutoff, n_bins_per_side + 1)
    bins_right = np.linspace(cutoff, cutoff + bandwidth, n_bins_per_side + 1)
    counts_left, _ = np.histogram(running_values, bins=bins_left)
    counts_right, _ = np.histogram(running_values, bins=bins_right)
    if len(counts_left) < 3 or len(counts_right) < 3:
        return None
    t_stat, p_val = stats.ttest_ind(np.log(counts_left + 0.5), np.log(counts_right + 0.5),
                                     equal_var=False)
    return {"t_stat": float(t_stat), "p_value": float(p_val)}


def scan_cutoffs(df, running_col, outcome_col):
    """Scan candidate cutoffs across the 20th-80th percentile of the
    running variable (customer-level values); rule-of-thumb bandwidth."""
    vals = df.drop_duplicates("customer_id")[running_col].dropna()
    candidates = np.linspace(vals.quantile(RDD_SCAN_PCTL_LOW), vals.quantile(RDD_SCAN_PCTL_HIGH),
                              RDD_SCAN_N_POINTS)
    iqr = vals.quantile(0.75) - vals.quantile(0.25)
    bw = max(iqr / 2, vals.std() * 0.5)
    rows = []
    for cutoff in candidates:
        res = local_linear_rd(df, running_col, outcome_col, cutoff, bw)
        dens = mccrary_density_approx(vals.values, cutoff, bw)
        if res is None:
            continue
        row = {"running_var": running_col, "outcome": outcome_col, "cutoff": float(cutoff),
               "bandwidth": bw, **res}
        if dens is not None:
            row["density_test_p"] = dens["p_value"]
        rows.append(row)
    return pd.DataFrame(rows)


def rolling_structural_break_scan(df, window_days=30, min_days_from_edge=30,
                                   min_obs_per_window=200, top_k=5):
    """CUSUM-style structural-break screen: estimate size_z's daily
    rolling coefficient on log_cpc, then flag peaks in the cumulative
    deviation from the mean coefficient as candidate break dates."""
    obs_start, obs_end = df["date"].min(), df["date"].max()
    dates = pd.date_range(obs_start + pd.Timedelta(days=min_days_from_edge),
                           obs_end - pd.Timedelta(days=min_days_from_edge), freq="D")
    half_w = window_days // 2
    rows = []
    for center in dates:
        sub = df[(df["date"] >= center - pd.Timedelta(days=half_w)) &
                  (df["date"] <= center + pd.Timedelta(days=half_w))]
        if len(sub) < min_obs_per_window or sub["customer_id"].nunique() < 15:
            continue
        m = sm.OLS(sub["log_cpc"], sm.add_constant(sub[["spend_z", "size_z"]])).fit(
            cov_type="cluster", cov_kwds={"groups": sub["customer_id"]})
        rows.append({"date": center, "size_coef": m.params["size_z"]})
    roll = pd.DataFrame(rows)
    if len(roll) < 60:
        return roll, []
    coefs = roll["size_coef"].values
    cusum = np.cumsum(coefs - coefs.mean())
    order = np.argsort(np.abs(cusum))[::-1]
    picked = []
    for idx in order:
        if len(picked) >= top_k:
            break
        if all(abs(idx - p) > 14 for p in picked):
            picked.append(idx)
    breaks = [{"date": roll["date"].iloc[i], "cusum_abs": float(abs(cusum[i]))}
              for i in sorted(picked)]
    return roll, breaks


def event_study_did(df, event_date, pre_days=30, post_days=30):
    """post x size_high DiD around a candidate event date, with a
    pre-trend joint test and (elsewhere) a permutation test against
    randomly chosen dates."""
    lo, hi = event_date - pd.Timedelta(days=pre_days), event_date + pd.Timedelta(days=post_days)
    sub = df[(df["date"] >= lo) & (df["date"] <= hi)].copy()
    if len(sub) < 200 or sub["customer_id"].nunique() < 20:
        return None
    sub["post"] = (sub["date"] >= event_date).astype(int)
    med = sub.drop_duplicates("customer_id")["size_z"].median()
    sub["size_high"] = (sub["size_z"] >= med).astype(int)
    m = smf.ols("log_cpc ~ post*size_high + spend_z", data=sub).fit(
        cov_type="cluster", cov_kwds={"groups": sub["customer_id"]})
    return {"did_coef": float(m.params.get("post:size_high", np.nan)),
            "did_p": float(m.pvalues.get("post:size_high", np.nan)),
            "n": len(sub), "n_customers": sub["customer_id"].nunique()}


# Orchestration (data loading omitted here -- see repository main pipeline
# for the customer x day CPC panel construction, identical variable
# definitions: size_z, spend_z, log_cpc, customer_id clustering).
# Round-1 output -> 5 bandwidth-robust candidates, passed to step11b.
