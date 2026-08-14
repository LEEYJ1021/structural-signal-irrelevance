"""
RQ2 confirmatory test -- can early operating signals (first 14-30 days)
predict later performance (H2a), and does account maturity add
predictive value on top of them (H2b)?

Re-uses the exact feature engineering, leakage-safe evaluation designs,
and within/between-customer decomposition established and validated in
src/coldstart_v5/step_l_rq2_feature_engineering.py, run here across
every (early, later) window pair in config.rq2_prediction.window_pairs
(the full confirmatory grid, vs. the narrower diagnostic subset used
during design).

Interpretation rule (fixed by the coldstart_v5 diagnostic pipeline):
trust the within-customer LOCO improvement and the repeated-split
Wilcoxon result over the pooled LOCO number. A pooled LOCO improvement
concentrated in the between-customer component reflects RQ1-level
signal leaking into a pooled metric, not genuine ad-group-level
predictive improvement -- this is checked explicitly for every window
pair below, not assumed.
"""
from __future__ import annotations

import pandas as pd

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.coldstart_v5._sample_construction import apply_maturity_metrics
from src.coldstart_v5.step_l_rq2_feature_engineering import (
    FEATURE_COLS_BASE, FEATURE_COLS_PLUS, build_window_features, load_perf_detail,
    loco_within_between_eval, repeated_group_split_eval,
)
from src.utils.io import load_config
from pathlib import Path


def run(cfg: dict):
    ctx = step_a(cfg)
    adgroup_dim, coldstart, usable, obs_end = ctx["adgroup_dim"], ctx["coldstart"], ctx["usable"], ctx["obs_end"]
    rcfg = cfg["rq2_prediction"]
    seed = cfg["random_seed"]

    excl = set(cfg["sample_definition"].get("known_test_account_ids", []))
    usable_m = apply_maturity_metrics(usable, adgroup_dim, coldstart)
    sample = usable_m[~usable_m["customer_id"].isin(excl)].copy()
    print(f"[rq2] sample after test-account exclusion: {len(sample)} ad groups, "
          f"{sample['customer_id'].nunique()} customers")

    perf = load_perf_detail(cfg, set(sample["ad_group_id"]))

    all_results = []
    for early_d, later_d in rcfg["window_pairs"]:
        feat_df = build_window_features(sample, perf, obs_end, early_d, later_d)
        n_cust = feat_df["customer_id"].nunique() if len(feat_df) else 0
        print(f"\n[rq2] early={early_d}d/later={later_d}d -> n={len(feat_df)}, customers={n_cust}")
        if len(feat_df) < 20 or n_cust < 5:
            print(f"[rq2]   insufficient sample -- skipped")
            continue

        split_result = repeated_group_split_eval(feat_df, rcfg["n_repeated_splits"], rcfg["test_size"], seed)
        loco_result = loco_within_between_eval(feat_df, seed)
        print(f"[rq2]   H2a base rho={split_result['rho_base_mean']:.3f}, "
              f"H2b +maturity rho={split_result['rho_plus_mean']:.3f}, "
              f"Wilcoxon p={split_result['wilcoxon_p']:.4f}")
        print(f"[rq2]   LOCO within-customer improvement (RQ2-relevant): "
              f"{loco_result['within_improvement']:+.3f} "
              f"(base={loco_result['within_base']:.3f}, plus={loco_result['within_plus']:.3f})")
        print(f"[rq2]   LOCO between-customer improvement (RQ1-signal proxy): "
              f"{loco_result['between_improvement']:+.3f} "
              f"(base={loco_result['between_base']:.3f}, plus={loco_result['between_plus']:.3f})")

        h2a_supported = split_result["rho_base_mean"] > 0.2  # descriptive threshold, not a formal test
        h2b_supported = (
            split_result["wilcoxon_p"] < 0.05
            and split_result["improvement_mean"] > 0
            and loco_result["within_improvement"] > 0.02  # improvement must show up within-customer, not just pooled
        )
        print(f"[rq2]   H2a descriptive support: {h2a_supported} | "
              f"H2b supported (within-customer confirmed): {h2b_supported}")

        all_results.append({
            "early_window": early_d, "later_window": later_d, "n": len(feat_df), "n_customers": n_cust,
            **split_result, **loco_result, "h2a_supported": h2a_supported, "h2b_supported": h2b_supported,
        })

    results_df = pd.DataFrame(all_results)
    print("\n[rq2] === confirmatory summary across all window pairs ===")
    print(results_df.to_string(index=False))
    print("\n[rq2] Interpretation rule: H2b is only credited where the within-customer LOCO "
          "improvement is also positive -- a positive pooled/between-customer improvement alone "
          "is treated as RQ1 signal leaking through a pooled metric, not as RQ2 support.")

    out_dir = Path("outputs/analysis")
    out_dir.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(out_dir / "rq2_results.csv", index=False)
    print(f"[rq2] wrote {out_dir / 'rq2_results.csv'}")

    return results_df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
