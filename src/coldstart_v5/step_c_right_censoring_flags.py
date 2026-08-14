"""
Step C -- Flag ad groups whose trajectory is right-censored: either because
their last active day sits near the extraction end date, or because it sits
near the spike-account deletion event.

Historical finding (kept here as a comment, not a hard-coded assumption):
in the original run 83.8% of the trajectory-usable sample was flagged
"observation-end censored," and increasing the required follow-up window
(see Step F) did not reduce that rate -- which redirected the investigation
away from "censoring" and toward Step G (fixed-window coverage) instead.
"""
from __future__ import annotations

import pandas as pd

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config


def run(cfg: dict):
    ctx = step_a(cfg)
    usable, obs_end = ctx["usable"], ctx["obs_end"]
    spike_ids, spike_date = ctx["spike_ids"], ctx["spike_date_detected"]
    window = cfg["sample_definition"]["censor_window_days"]

    is_spike_account = usable["customer_id"].isin(spike_ids)
    near_obs_end = (obs_end - usable["perf_last_active"]).dt.days <= window
    near_spike = (spike_date is not None) & (
        (usable["perf_last_active"] - spike_date).dt.days.abs() <= window
    )

    usable = usable.copy()
    usable["censor_flag"] = "natural_end"
    usable.loc[near_obs_end, "censor_flag"] = "observation_end_censored"
    usable.loc[is_spike_account & near_spike, "censor_flag"] = "spike_account_censored"

    summary = usable["censor_flag"].value_counts()
    censor_rate = 1 - summary.get("natural_end", 0) / len(usable)
    print(f"[step_c] censoring flag distribution:\n{summary}")
    print(f"[step_c] suspected-censored share: {censor_rate:.1%} "
          f"({'include an explicit censoring indicator in any survival/trajectory model' if censor_rate > 0.05 else 'censoring impact appears limited'})")
    return usable


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
