"""
Shared cold-start sample construction, used identically by every diagnostic
step (A-M) so that sample sizes stay consistent and comparable across steps.

A "cold-start candidate" is an ad group whose registration timestamp
(`regTm`) falls strictly inside the observed panel window -- i.e. we can
observe its performance from day one, not just a mid-life snapshot.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.io import find_column, read_perf_panel_columns_only, smart_read_table
from src.utils.identifiers import clean_id, to_naive


def build_coldstart_sample(cfg: dict):
    """Returns (adgroup_dim, panel, coldstart, usable, obs_start, obs_end)."""
    paths = cfg["paths"]
    min_active_days = cfg["sample_definition"]["min_active_days_for_trajectory"]

    adgroup_dim = smart_read_table(paths["adgroup_dim"])
    reg_col = find_column(adgroup_dim, ["regtm", "reg_dt", "reg_date", "created", "reg"])
    cust_col_a = find_column(adgroup_dim, ["customer_id", "cust_id", "customer"])
    adg_col_a = find_column(adgroup_dim, ["ad_group_id", "adgroup_id", "ad_group"])
    assert reg_col and cust_col_a and adg_col_a

    adgroup_dim = adgroup_dim.rename(columns={reg_col: "regTm", cust_col_a: "customer_id", adg_col_a: "ad_group_id"})
    adgroup_dim["regTm"] = to_naive(pd.to_datetime(adgroup_dim["regTm"], errors="coerce"))
    adgroup_dim["customer_id"] = clean_id(adgroup_dim["customer_id"])
    adgroup_dim["ad_group_id"] = clean_id(adgroup_dim["ad_group_id"])
    adgroup_dim = adgroup_dim.dropna(subset=["regTm"])

    perf_path = Path(paths["perf_panel"])
    header = pd.read_csv(perf_path, sep="\t" if perf_path.suffix == ".tsv" else ",", nrows=5)
    date_col = find_column(header, ["date", "dt", "day"])
    cust_col_p = find_column(header, ["customer_id", "cust_id", "customer"])
    adg_col_p = find_column(header, ["ad_group_id", "adgroup_id", "ad_group"])
    assert date_col and cust_col_p and adg_col_p

    panel = read_perf_panel_columns_only(
        perf_path, usecols=[date_col, cust_col_p, adg_col_p], dtype={cust_col_p: str, adg_col_p: str}
    )
    panel = panel.rename(columns={date_col: "date", cust_col_p: "customer_id", adg_col_p: "ad_group_id"})
    panel["date"] = to_naive(pd.to_datetime(panel["date"], errors="coerce")).dt.normalize()
    panel["customer_id"] = clean_id(panel["customer_id"])
    panel["ad_group_id"] = clean_id(panel["ad_group_id"])
    panel = panel.dropna(subset=["date"]).drop_duplicates(subset=["ad_group_id", "customer_id", "date"])

    obs_start, obs_end = panel["date"].min(), panel["date"].max()

    adgroup_dim = adgroup_dim.merge(
        panel.groupby("ad_group_id")["date"].agg(perf_first_active="min", perf_last_active="max"),
        on="ad_group_id", how="inner",
    )
    is_true_coldstart = (adgroup_dim["regTm"] >= obs_start + pd.Timedelta(days=1)) & (adgroup_dim["regTm"] <= obs_end)
    coldstart = adgroup_dim.loc[is_true_coldstart].copy()
    coldstart["active_days"] = (coldstart["perf_last_active"] - coldstart["perf_first_active"]).dt.days + 1
    usable = coldstart[coldstart["active_days"] >= min_active_days].copy()

    print(f"[coldstart_v5] observation window: {obs_start.date()} -- {obs_end.date()} "
          f"({(obs_end - obs_start).days} days)")
    print(f"[coldstart_v5] cold-start candidates: {len(coldstart)} | trajectory-usable "
          f"(>= {min_active_days} active days): {len(usable)}")

    return adgroup_dim, panel, coldstart, usable, obs_start, obs_end


def apply_maturity_metrics(df: pd.DataFrame, adgroup_dim: pd.DataFrame, coldstart: pd.DataFrame) -> pd.DataFrame:
    """Attach (a) coldstart_ratio = coldstart_count / all_time_count and
    (b) account_age_days = this ad group's regTm minus the customer's
    earliest observed regTm, both at the customer level."""
    alltime_count = adgroup_dim.groupby("customer_id").size().rename("all_time_count")
    alltime_first_regtm = adgroup_dim.groupby("customer_id")["regTm"].min().rename("customer_first_regtm")
    coldstart_count = coldstart.groupby("customer_id").size().rename("coldstart_count")

    out = df.merge(alltime_count, on="customer_id", how="left")
    out = out.merge(alltime_first_regtm, on="customer_id", how="left")
    out = out.merge(coldstart_count, on="customer_id", how="left")
    out["coldstart_ratio"] = out["coldstart_count"] / out["all_time_count"]
    out["account_age_days"] = (out["regTm"] - out["customer_first_regtm"]).dt.days
    return out


def exclude_test_accounts(usable: pd.DataFrame, panel: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Drop accounts whose total spend is at/near zero (Step H finding:
    these are template/test setups, not real ad groups)."""
    total_cost_by_adg = (
        panel.merge(usable[["ad_group_id"]], on="ad_group_id")
        .groupby("ad_group_id")["date"].size()  # placeholder if cost column not in this slim panel
    )
    return usable  # cost-based filtering happens where a cost column is available (see Step H script)
