"""
Pipeline v4, Step 4 -- synthesis.

Runs Steps 0-3 (if their outputs aren't already on disk) and collapses
them into a single outputs/_v4_synthesis/summary.json, so that
figures/ scripts and the RESULTS_SUMMARY.md table have one canonical
place to read v4-generation findings from.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.pipeline_v4.step0_data_prep_v4 import run as step0
from src.pipeline_v4.step1_variance_decomposition_v4 import run as step1
from src.pipeline_v4.step2_advertiser_size_fairness_v4 import run as step2
from src.pipeline_v4.step3_churn_appendix_v4 import run as step3
from src.utils.io import load_config


def run(cfg: dict):
    print("[step4_v4] running/re-reading Steps 0-3 for synthesis...")
    ctx0 = step0(cfg)
    variance_result = step1(cfg)
    fairness_result = step2(cfg)
    churn_result = step3(cfg)

    summary = {
        "n_customers": int(ctx0["panel"]["customer_id"].nunique()),
        "n_ad_groups": int(ctx0["panel"]["ad_group_id"].nunique()),
        "n_spike_accounts": len(ctx0["spike_ids"]),
        "variance_decomposition": variance_result.to_dict(orient="records") if variance_result is not None else None,
        "fairness": {
            "observed_beta_cost_per_active_day": float(fairness_result["observed_beta"]),
            "n_specs": int(len(fairness_result["specification_curve"])),
        } if fairness_result is not None else None,
        "churn_benchmark": churn_result,
    }

    out_dir = Path(cfg["paths"]["v4_intermediate_dir"]).parent / "_v4_synthesis"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "summary.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"[step4_v4] wrote {out_path}")
    print(json.dumps(summary, indent=2, default=str))
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
