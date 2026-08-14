"""
Pipeline v4, Step 0 -- data preparation and dynamic spike-account
detection.

This is the earlier-generation pipeline's entry point and the sole
producer of `spike_account_ids.json`, an intermediate artifact re-used
throughout coldstart_v5 (see data/README.md, section 3). A "spike
account" is a customer whose ad-group footprint drops sharply within a
short window -- consistent with a mass account-deletion or migration
event on the platform side, rather than organic churn -- detected
dynamically from the panel so that a re-extract cannot silently
invalidate the detection logic.

Also produces the customer-day aggregate panel used by
step1_variance_decomposition_v4.py and step3_churn_appendix_v4.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.utils.io import find_column, load_config, peek_header, read_perf_panel_columns_only, smart_read_table
from src.utils.identifiers import clean_id, to_naive


def detect_spike_accounts(panel: pd.DataFrame, cfg: dict) -> set[str]:
    """A customer is flagged as a spike account if its count of
    distinct active ad groups drops by more than
    `drop_fraction_threshold` within any `burst_window_days`-day
    window over the observation period -- i.e. a large fraction of its
    ad groups all stop appearing in the panel within a few days of
    each other, which is the signature of a bulk deletion/migration
    event rather than independent, organically-timed churn."""
    scfg = cfg["pipeline_v4"]["spike_detection"]
    drop_th, window_days = scfg["drop_fraction_threshold"], scfg["burst_window_days"]

    daily_active = (
        panel.groupby(["customer_id", "date"])["ad_group_id"].nunique().rename("n_active").reset_index()
    )
    spike_ids = set()
    for cust_id, g in daily_active.groupby("customer_id"):
        g = g.sort_values("date").set_index("date")["n_active"]
        full_idx = pd.date_range(g.index.min(), g.index.max())
        g = g.reindex(full_idx, fill_value=0)
        peak = g.rolling(f"{window_days}D").max()
        trough_after = g[::-1].rolling(f"{window_days}D").min()[::-1]
        drop_frac = (peak - trough_after) / peak.replace(0, np.nan)
        if (drop_frac >= drop_th).any():
            spike_ids.add(cust_id)
    return spike_ids


def run(cfg: dict) -> dict:
    paths = cfg["paths"]
    adgroup_dim = smart_read_table(paths["adgroup_dim"])
    reg_col = find_column(adgroup_dim, ["regtm", "reg_dt", "reg_date", "created", "reg"])
    cust_col_a = find_column(adgroup_dim, ["customer_id", "cust_id", "customer"])
    adg_col_a = find_column(adgroup_dim, ["ad_group_id", "adgroup_id", "ad_group"])
    assert reg_col and cust_col_a and adg_col_a, "required columns not found in adgroup_dim -- see data/README.md"

    adgroup_dim = adgroup_dim.rename(columns={reg_col: "regTm", cust_col_a: "customer_id", adg_col_a: "ad_group_id"})
    adgroup_dim["regTm"] = to_naive(pd.to_datetime(adgroup_dim["regTm"], errors="coerce"))
    adgroup_dim["customer_id"] = clean_id(adgroup_dim["customer_id"])
    adgroup_dim["ad_group_id"] = clean_id(adgroup_dim["ad_group_id"])

    perf_path = Path(paths["perf_panel"])
    header = peek_header(perf_path)
    date_col = find_column(header, ["date", "dt", "day"])
    cust_col_p = find_column(header, ["customer_id", "cust_id", "customer"])
    adg_col_p = find_column(header, ["ad_group_id", "adgroup_id", "ad_group"])
    cost_col_p = find_column(header, ["cost"])
    assert date_col and cust_col_p and adg_col_p and cost_col_p

    panel = read_perf_panel_columns_only(
        perf_path, usecols=[date_col, cust_col_p, adg_col_p, cost_col_p],
        dtype={cust_col_p: str, adg_col_p: str},
    )
    panel = panel.rename(columns={date_col: "date", cust_col_p: "customer_id", adg_col_p: "ad_group_id", cost_col_p: "cost"})
    panel["date"] = to_naive(pd.to_datetime(panel["date"], errors="coerce")).dt.normalize()
    panel["customer_id"] = clean_id(panel["customer_id"])
    panel["ad_group_id"] = clean_id(panel["ad_group_id"])
    panel["cost"] = pd.to_numeric(panel["cost"], errors="coerce").fillna(0)
    panel = panel.dropna(subset=["date"])
    panel = panel.groupby(["ad_group_id", "customer_id", "date"], as_index=False)["cost"].sum()

    print(f"[step0_v4] panel loaded: {len(panel):,} ad-group x day rows, "
          f"{panel['customer_id'].nunique()} customers, {panel['ad_group_id'].nunique()} ad groups")

    spike_ids = detect_spike_accounts(panel, cfg)
    print(f"[step0_v4] spike accounts detected: {len(spike_ids)}")

    intermediate_dir = Path(paths["v4_intermediate_dir"])
    intermediate_dir.mkdir(parents=True, exist_ok=True)
    spike_json_path = intermediate_dir / "spike_account_ids.json"
    spike_json_path.write_text(json.dumps({"spike_account_ids": sorted(spike_ids)}, ensure_ascii=False, indent=2))
    print(f"[step0_v4] wrote {spike_json_path}")

    customer_daily = panel.groupby(["customer_id", "date"], as_index=False)["cost"].sum()
    customer_daily_path = intermediate_dir / "customer_daily_panel.csv"
    customer_daily.to_csv(customer_daily_path, index=False)
    print(f"[step0_v4] wrote {customer_daily_path} ({len(customer_daily):,} rows)")

    return {"adgroup_dim": adgroup_dim, "panel": panel, "spike_ids": spike_ids, "customer_daily": customer_daily}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
