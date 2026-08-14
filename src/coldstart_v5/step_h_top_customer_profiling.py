"""
Step H -- Profile the top-N customers driving the clustering density found
in Step D. The goal is to distinguish "genuinely large advertiser" from
"template/bulk-generated test accounts," using four independent signals:

  H1  all-time scale       -- is this customer large outside the cold-start window too?
  H2  registration burst   -- were ad groups created in a tight burst (bulk setup) or spread out?
  H3  template signal      -- repeated business_channel_id / bid_amount / naming patterns
  H4  real spend            -- non-trivial spend, or near-zero (test/template setup)

Feeds directly into `sample_definition.test_account_exclusion` in config.yaml.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import find_column, read_perf_panel_columns_only
from src.utils.identifiers import clean_id
from src.utils.io import load_config


def _name_prefix(name):
    if pd.isna(name):
        return "N/A"
    core = re.sub(r"[\d_\-#]+", "", str(name)).strip()
    return core[:8] if core else "N/A"


def run(cfg: dict):
    ctx = step_a(cfg)
    adgroup_dim, usable = ctx["adgroup_dim"], ctx["usable"]
    top_n = cfg["coldstart_diagnostics"]["top_n_customers_profile"]
    burst_hours = cfg["coldstart_diagnostics"]["burst_window_hours"]

    per_customer = usable.groupby("customer_id").size().sort_values(ascending=False)
    top_customers = per_customer.head(top_n)
    alltime_count = adgroup_dim.groupby("customer_id").size()

    # H1: all-time scale
    h1 = pd.DataFrame({
        "customer_id": top_customers.index,
        "coldstart_n": top_customers.values,
        "all_time_n": [int(alltime_count.get(c, 0)) for c in top_customers.index],
    })
    print(f"[step_h] H1 all-time scale:\n{h1.to_string(index=False)}")

    # H2: registration burst
    h2_rows = []
    for cust_id in top_customers.index:
        reg_times = usable.loc[usable["customer_id"] == cust_id, "regTm"].sort_values()
        if len(reg_times) < 2:
            h2_rows.append({"customer_id": cust_id, "n": len(reg_times), "burst_ratio": np.nan, "span_days": 0})
            continue
        gaps_hours = reg_times.diff().dropna().dt.total_seconds() / 3600
        h2_rows.append({
            "customer_id": cust_id, "n": len(reg_times),
            "burst_ratio": (gaps_hours <= burst_hours).mean(),
            "span_days": (reg_times.max() - reg_times.min()).days,
        })
    h2 = pd.DataFrame(h2_rows)
    print(f"[step_h] H2 registration burst pattern:\n{h2.to_string(index=False)}")

    # H3: template signal
    h3_rows = []
    for cust_id in top_customers.index:
        sub = usable[usable["customer_id"] == cust_id]
        row = {"customer_id": cust_id, "n": len(sub)}
        for col in ["business_channel_id_mobile", "business_channel_id_pc", "campaign_id"]:
            if col in sub.columns:
                row[f"unique_{col}"] = sub[col].nunique(dropna=True)
        if "bid_amount" in sub.columns:
            bid = pd.to_numeric(sub["bid_amount"], errors="coerce")
            row["bid_cv"] = bid.std() / bid.mean() if bid.mean() else np.nan
        if "ad_group_name" in sub.columns:
            prefixes = sub["ad_group_name"].apply(_name_prefix)
            row["name_prefix_top_share"] = prefixes.value_counts(normalize=True).max()
        h3_rows.append(row)
    h3 = pd.DataFrame(h3_rows)
    print(f"[step_h] H3 template signal:\n{h3.to_string(index=False)}")

    # H4: real spend (chunked re-scan of raw panel)
    path = Path(cfg["paths"]["perf_panel"])
    header = pd.read_csv(path, sep="\t" if path.suffix == ".tsv" else ",", nrows=5)
    adg_c, cost_c = find_column(header, ["ad_group_id"]), find_column(header, ["cost"])
    target_ids = set(usable.loc[usable["customer_id"].isin(top_customers.index), "ad_group_id"])
    accum = []
    for chunk in read_perf_panel_columns_only(path, usecols=[adg_c, cost_c], dtype={adg_c: str}, chunksize=2_000_000):
        chunk = chunk.rename(columns={adg_c: "ad_group_id", cost_c: "cost"})
        chunk["ad_group_id"] = clean_id(chunk["ad_group_id"])
        chunk = chunk[chunk["ad_group_id"].isin(target_ids)]
        if len(chunk):
            accum.append(chunk)
    cost_by_adg = pd.concat(accum, ignore_index=True).groupby("ad_group_id")["cost"].sum() if accum else pd.Series(dtype=float)

    h4_rows = []
    for cust_id in top_customers.index:
        adg_ids = usable.loc[usable["customer_id"] == cust_id, "ad_group_id"]
        costs = cost_by_adg.reindex(adg_ids).fillna(0)
        h4_rows.append({
            "customer_id": cust_id, "n": len(adg_ids), "mean_cost": costs.mean(),
            "median_cost": costs.median(), "zero_spend_share": (costs == 0).mean(), "total_cost": costs.sum(),
        })
    h4 = pd.DataFrame(h4_rows)
    print(f"[step_h] H4 real spend:\n{h4.to_string(index=False)}")

    print("\n[step_h] Classify each top customer as (a) genuine large advertiser, "
          "(b) template/bulk-generated, or (c) ambiguous, using H1-H4 jointly. "
          "Customers meeting the config.sample_definition.test_account_exclusion "
          "thresholds (near-zero total spend / high zero-spend share) should be "
          "excluded from the confirmatory sample.")
    return {"h1": h1, "h2": h2, "h3": h3, "h4": h4}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
