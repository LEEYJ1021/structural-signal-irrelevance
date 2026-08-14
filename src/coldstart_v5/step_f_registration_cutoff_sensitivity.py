"""
Step F -- Test whether the apparent "censoring" from Step C is actually a
follow-up-window artifact: does requiring more post-registration follow-up
time (a stricter regTm cutoff) reduce the censored share?

Historical finding: increasing the required follow-up from 30 to 120 days
barely moved the censored rate (83.6% -> 83.2%), which redirected the
interpretation from "not enough time has passed" to "ad groups mostly
don't self-terminate" -- confirmed directly in Step G.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config


def run(cfg: dict):
    ctx = step_a(cfg)
    coldstart, obs_end = ctx["coldstart"], ctx["obs_end"]
    min_active_days = cfg["sample_definition"]["min_active_days_for_trajectory"]
    followups = cfg["coldstart_diagnostics"]["followup_options_days"]
    censor_window = cfg["sample_definition"]["censor_window_days"]

    reg_month_counts = coldstart["regTm"].dt.to_period("M").value_counts().sort_index()
    print(f"[step_f] cold-start candidates by registration month:\n{reg_month_counts}")

    rows = []
    for followup in followups:
        cutoff = obs_end - pd.Timedelta(days=followup)
        subset = coldstart[coldstart["regTm"] <= cutoff]
        subset_usable = subset[subset["active_days"] >= min_active_days]
        if len(subset_usable) == 0:
            rows.append((followup, cutoff.date(), len(subset), 0, np.nan))
            continue
        near_end = (obs_end - subset_usable["perf_last_active"]).dt.days <= censor_window
        rows.append((followup, cutoff.date(), len(subset), len(subset_usable), near_end.mean()))

    summary = pd.DataFrame(rows, columns=["min_followup_days", "cutoff_date", "n_candidates", "n_usable", "censored_rate"])
    print(f"[step_f] cutoff sensitivity:\n{summary.to_string(index=False)}")
    print("[step_f] if censored_rate barely moves across cutoffs, the pattern reflects sustained "
          "operation (ad groups don't self-terminate), not insufficient follow-up time.")
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
