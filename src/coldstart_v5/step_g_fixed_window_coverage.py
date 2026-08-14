"""
Step G -- Directly test the Step F re-interpretation: instead of measuring
the date *span* between first and last active day (which passes even if
activity is sparse in between), measure what fraction of days inside a
fixed post-registration window actually have recorded activity.

A low coverage ratio here reflects genuine data gaps (on/off cycling,
budget exhaustion, approval delay), not censoring.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config


def run(cfg: dict):
    ctx = step_a(cfg)
    coldstart, panel, obs_end = ctx["coldstart"], ctx["panel"], ctx["obs_end"]
    windows = cfg["coldstart_diagnostics"]["window_lengths_days"]
    threshold = cfg["coldstart_diagnostics"]["window_coverage_threshold"]

    panel_dates_by_adg = panel.groupby("ad_group_id")["date"].apply(set)

    rows = []
    for window in windows:
        n_elapsed, n_covered, ratios = 0, 0, []
        for _, row in coldstart.iterrows():
            start = row["perf_first_active"]
            end = start + pd.Timedelta(days=window - 1)
            if end > obs_end:
                continue  # window not yet fully elapsed -- exclude, don't penalize
            n_elapsed += 1
            dates = panel_dates_by_adg.get(row["ad_group_id"], set())
            obs_days = sum(1 for d in pd.date_range(start, end) if d in dates)
            ratio = obs_days / window
            ratios.append(ratio)
            if ratio >= threshold:
                n_covered += 1
        rows.append((window, n_elapsed, n_covered, n_covered / n_elapsed if n_elapsed else np.nan,
                     float(np.mean(ratios)) if ratios else np.nan))

    summary = pd.DataFrame(rows, columns=["window_days", "n_elapsed", f"n_coverage_ge_{threshold:.0%}",
                                           "usable_share", "mean_coverage"])
    print(f"[step_g] fixed-window coverage (threshold={threshold:.0%}):\n{summary.to_string(index=False)}")
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
