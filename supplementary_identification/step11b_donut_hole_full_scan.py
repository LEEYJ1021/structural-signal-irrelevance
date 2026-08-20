"""
STEP 11-b -- Fine-grained donut-hole robustness scan of the 5 RDD
candidates that survived Round 1's bandwidth-sensitivity filter.

Reuses local_linear_rd() from step11_alt_identification_RDD_policy.py.
Tests donut fractions [0, 2, 5, 8, 10, 15, 20]% and records the fraction
at which significance first breaks down ("breakdown point") -- a smaller
breakdown point means the original estimate depended heavily on the
handful of observations immediately adjacent to the cutoff, which is the
classic symptom of running-variable manipulation.

Result summary (see SCREENING_SUMMARY.md for full detail):
  log_size,        cutoff=1.386  -> breaks down at donut=2%  (reject)
  log_size,        cutoff=2.092  -> breaks down at donut=2%  (reject)
  log_size,        cutoff=2.515  -> breaks down at donut=15% (weak)
  log_total_spend, cutoff=11.515 -> breaks down at donut=15% (weak/reject,
                                     see step11c manipulation flag)
  log_total_spend, cutoff=11.912 -> holds to donut=20% ("robust" at the
                                     panel level -- but see step11c, which
                                     shows this is a panel-density artifact)
"""

import numpy as np
import pandas as pd
from step11_alt_identification_RDD_policy import local_linear_rd

DONUT_FRACTIONS_FINE = [0.00, 0.02, 0.05, 0.08, 0.10, 0.15, 0.20]
ALPHA = 0.05

ROUND1_CANDIDATES = [
    {"running_var": "log_size", "cutoff": 1.386, "bandwidth": 1.128},
    {"running_var": "log_size", "cutoff": 2.092, "bandwidth": 1.128},
    {"running_var": "log_size", "cutoff": 2.515, "bandwidth": 1.128},
    {"running_var": "log_total_spend", "cutoff": 11.515, "bandwidth": 3.349},
    {"running_var": "log_total_spend", "cutoff": 11.912, "bandwidth": 3.349},
]


def donut_hole_breakdown(cpc_panel_df, candidate, outcome="log_cpc"):
    """Return the first donut fraction at which p >= ALPHA, or None if
    significance holds through the full DONUT_FRACTIONS_FINE grid."""
    rows = []
    for donut in DONUT_FRACTIONS_FINE:
        r = local_linear_rd(cpc_panel_df, candidate["running_var"], outcome,
                             candidate["cutoff"], candidate["bandwidth"], donut_frac=donut)
        if r is None:
            continue
        rows.append({"donut_fraction": donut, **r})
    df = pd.DataFrame(rows)
    if len(df) == 0:
        return None, df
    breakdown = next((row["donut_fraction"] for _, row in df.sort_values("donut_fraction").iterrows()
                       if row["p"] >= ALPHA), None)
    return breakdown, df


def flag_sample_imbalance(row, threshold=2.0):
    """Panel-level left/right sample-count ratio flag. NOTE (see
    step11c): this flag conflates two distinct phenomena on a
    customer x day panel -- genuine running-variable manipulation vs.
    higher-spend customers simply having more active days (more panel
    rows) than lower-spend customers. It is retained here as an initial
    screen only; step11c resolves the ambiguity at the customer level."""
    ratio = row["n_right"] / max(row["n_left"], 1)
    return ratio > threshold or ratio < 1 / threshold, ratio


# Orchestration: for each of the 5 Round-1 candidates, run
# donut_hole_breakdown() and flag_sample_imbalance(), then pass the
# panel-level "surviving" subset to step11c for the decisive
# customer-level re-analysis.
