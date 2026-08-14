"""
Pipeline v4, Step 1 -- variance decomposition of daily ad-group cost
across nested levels (customer -> campaign -> ad group) plus a
cross-cutting placebo level (device_type, which should carry little
independent variance if the decomposition is behaving sensibly, since
device mix is largely a within-ad-group allocation choice rather than
a source of genuine performance heterogeneity).

Produces the variance-share table consumed by
figures/make_figure1_variance_decomposition.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.pipeline_v4.step0_data_prep_v4 import run as step0
from src.utils.io import find_column, load_config, peek_header, read_perf_panel_columns_only
from src.utils.identifiers import clean_id, to_naive


def variance_components(df: pd.DataFrame, metric: str, levels: list[str]) -> pd.DataFrame:
    """Sequential (nested) variance-share decomposition: at each level
    in `levels`, compute the share of total variance in `metric`
    explained by between-group means at that level, after removing the
    variance already attributed to coarser levels above it in the
    list. This is a lightweight ANOVA-style decomposition, not a full
    mixed-effects variance-components model -- adequate for the
    descriptive purpose here (see figures/make_figure1)."""
    total_var = df[metric].var()
    rows = []
    residual = df[metric].copy()
    explained_so_far = 0.0
    for level in levels:
        if level not in df.columns:
            rows.append({"level": level, "variance_share": np.nan, "note": "column not present"})
            continue
        group_means = df.groupby(level)[metric].transform("mean")
        between_var = np.var(group_means)
        share = between_var / total_var if total_var else np.nan
        rows.append({"level": level, "variance_share": share})
        residual = residual - group_means + residual.mean()
        explained_so_far += share if not np.isnan(share) else 0.0
    rows.append({"level": "residual", "variance_share": max(0.0, 1.0 - explained_so_far)})
    return pd.DataFrame(rows)


def run(cfg: dict):
    ctx = step0(cfg)
    panel, adgroup_dim = ctx["panel"], ctx["adgroup_dim"]
    vcfg = cfg["pipeline_v4"]["variance_decomposition"]
    metric, levels = vcfg["metric"], vcfg["levels"]

    # attach campaign_id and device_type where available (device_type only
    # exists at panel granularity, so it is re-pulled with the metric column)
    paths = cfg["paths"]
    header = peek_header(Path(paths["perf_panel"]))
    date_col = find_column(header, ["date"])
    adg_col = find_column(header, ["ad_group_id"])
    device_col = find_column(header, ["device_type"])
    cost_col = find_column(header, ["cost"])
    if device_col:
        extra = read_perf_panel_columns_only(
            Path(paths["perf_panel"]), usecols=[date_col, adg_col, device_col, cost_col],
            dtype={adg_col: str},
        )
        extra = extra.rename(columns={date_col: "date", adg_col: "ad_group_id", device_col: "device_type", cost_col: "cost"})
        extra["date"] = to_naive(pd.to_datetime(extra["date"], errors="coerce")).dt.normalize()
        extra["ad_group_id"] = clean_id(extra["ad_group_id"])
        extra["cost"] = pd.to_numeric(extra["cost"], errors="coerce").fillna(0)
        df = extra.groupby(["ad_group_id", "date", "device_type"], as_index=False)["cost"].sum()
    else:
        df = panel.copy()
        df["device_type"] = "unknown"

    df = df.merge(adgroup_dim[["ad_group_id", "customer_id"]].drop_duplicates(), on="ad_group_id", how="left")
    if "campaign_id" in adgroup_dim.columns:
        df = df.merge(adgroup_dim[["ad_group_id", "campaign_id"]].drop_duplicates(), on="ad_group_id", how="left")

    result = variance_components(df, metric, levels)
    print(f"[step1_v4] variance decomposition of '{metric}' across {levels}:\n{result.to_string(index=False)}")
    print("[step1_v4] note: device_type is included as a placebo level -- a large variance share "
          "attributed to it would suggest the decomposition is picking up allocation noise rather "
          "than genuine performance heterogeneity; see figures/make_figure1_variance_decomposition.py.")

    out_dir = Path(cfg["paths"]["v4_intermediate_dir"]).parent / "_v4_variance_decomposition"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "variance_decomposition.json"
    out_path.write_text(json.dumps(result.to_dict(orient="records"), indent=2))
    print(f"[step1_v4] wrote {out_path}")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
