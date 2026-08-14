"""
Step A -- Dynamically re-confirm the observation window and the date of the
mass spike-account deletion event (never hard-code these; derive them from
the data every run so a re-extract can't silently invalidate downstream
thresholds).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.utils.identifiers import clean_id
from src.coldstart_v5._sample_construction import build_coldstart_sample
from src.utils.io import load_config


def run(cfg: dict) -> dict:
    adgroup_dim, panel, coldstart, usable, obs_start, obs_end = build_coldstart_sample(cfg)

    spike_json = Path(cfg["paths"]["intermediate_dir"]) / "spike_account_ids.json"
    spike_ids = set(clean_id(pd.Series(json.loads(spike_json.read_text())["spike_account_ids"]))) \
        if spike_json.exists() else set()
    print(f"[step_a] spike accounts loaded: {len(spike_ids)}")

    spike_last_active = panel[panel["customer_id"].isin(spike_ids)].groupby("ad_group_id")["date"].max()
    spike_date_detected = spike_last_active.mode().iloc[0] if len(spike_last_active) else None
    print(f"[step_a] spike-account modal last-active date (dynamically detected): {spike_date_detected}")

    return {
        "obs_start": obs_start, "obs_end": obs_end,
        "spike_ids": spike_ids, "spike_date_detected": spike_date_detected,
        "adgroup_dim": adgroup_dim, "panel": panel, "coldstart": coldstart, "usable": usable,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
