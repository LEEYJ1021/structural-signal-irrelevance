"""
Step B -- Recompute the "true cold-start" sample from `regTm` under the
current extraction window, and report the registration -> first-active-day
gap. This step exists to catch drift between a hard-coded sample-size
assumption from an earlier extract and what the current data actually
supports.
"""
from __future__ import annotations

from src.coldstart_v5._sample_construction import build_coldstart_sample
from src.utils.io import load_config


def run(cfg: dict):
    adgroup_dim, panel, coldstart, usable, obs_start, obs_end = build_coldstart_sample(cfg)
    gap_days = (usable["perf_first_active"] - usable["regTm"]).dt.days
    print(f"[step_b] regTm -> first-active-day gap: median={gap_days.median():.1f}d, "
          f"IQR=[{gap_days.quantile(.25):.1f}, {gap_days.quantile(.75):.1f}]d")
    return usable, gap_days


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
