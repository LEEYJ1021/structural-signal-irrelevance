"""
step_m2_m3_model_class_bootstrap.py -- M2 (design) -> M3 (headline result).

Runs an independent customer-cluster bootstrap (200 reps) for the Size-blind
strategy crossed with four model classes pre-specified for THEORETICAL
representativeness -- linear (OLS), gradient-boosted trees (HistGB, squared
loss), bagged tree ensemble (RandomForest), and a kernel machine (SVR-RBF) --
fixed BEFORE re-inspecting which cell scored best in step_m1_exploratory_scan.py.

This is the one M-series finding reported at higher confidence than M1's raw scan
results (docs/METHODOLOGY_NOTES.md entry B9; root README §16.3). Its output is the
direct source of Figure 16 (figures/scripts/figure16_mitigation_model_class_bootstrap.py).

Usage:
    python supplementary_mitigation_study/step_m2_m3_model_class_bootstrap.py \
        --input data/customer_panel.csv \
        --output supplementary_mitigation_study/model_class_bootstrap_size_blind.csv \
        --n-reps 200
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mitigation_common import (  # noqa: E402
    PRESPECIFIED_MODEL_CLASSES,
    RANDOM_SEED,
    RETEST_STRATEGY,
    bootstrap_ci,
    load_panel,
    localbiz_gap,
    make_fit_predict_fn,
    rmse,
    size_gap,
)


def run_model_class_retest(panel: pd.DataFrame, n_reps: int, seed: int) -> pd.DataFrame:
    """For each pre-specified model class, bootstrap Delta(metric) = metric[Size-blind]
    - metric[Baseline] across RMSE, size_gap, and localbiz_gap(cut0.00), using a paired
    bootstrap (same resampled customers feed both the Size-blind and Baseline fits
    within each replicate, matching step_m0_pregate.py's design).
    """
    rng = np.random.default_rng(seed)
    n = len(panel)
    rows = []

    for model_name in PRESPECIFIED_MODEL_CLASSES:
        strat_fp = make_fit_predict_fn(RETEST_STRATEGY, model_name)
        base_fp = make_fit_predict_fn("Baseline", model_name)

        # Point estimates on the full panel
        strat_pred_full = strat_fp(panel)
        base_pred_full = base_fp(panel)
        point = {
            "rmse": rmse(panel["y"], strat_pred_full) - rmse(panel["y"], base_pred_full),
            "size_gap": (
                size_gap(panel, panel["y"], strat_pred_full)
                - size_gap(panel, panel["y"], base_pred_full)
            ),
            "localbiz_gap": (
                localbiz_gap(panel, panel["y"], strat_pred_full, cutoff=0.00)
                - localbiz_gap(panel, panel["y"], base_pred_full, cutoff=0.00)
            ),
        }

        draws = {"rmse": np.empty(n_reps), "size_gap": np.empty(n_reps), "localbiz_gap": np.empty(n_reps)}
        for b in range(n_reps):
            idx = rng.integers(0, n, size=n)
            boot_panel = panel.iloc[idx].reset_index(drop=True)
            strat_pred = strat_fp(boot_panel)
            base_pred = base_fp(boot_panel)
            draws["rmse"][b] = rmse(boot_panel["y"], strat_pred) - rmse(boot_panel["y"], base_pred)
            draws["size_gap"][b] = (
                size_gap(boot_panel, boot_panel["y"], strat_pred)
                - size_gap(boot_panel, boot_panel["y"], base_pred)
            )
            draws["localbiz_gap"][b] = (
                localbiz_gap(boot_panel, boot_panel["y"], strat_pred, cutoff=0.00)
                - localbiz_gap(boot_panel, boot_panel["y"], base_pred, cutoff=0.00)
            )

        row = {"model": model_name, "model_class": _model_class_label(model_name)}
        for metric_name in ("rmse", "size_gap", "localbiz_gap"):
            ci_lo, ci_hi = bootstrap_ci(draws[metric_name])
            row[f"delta_{metric_name}"] = point[metric_name]
            row[f"delta_{metric_name}_ci_lo"] = ci_lo
            row[f"delta_{metric_name}_ci_hi"] = ci_hi
            row[f"delta_{metric_name}_verdict"] = _verdict(metric_name, ci_lo, ci_hi)
        rows.append(row)
        print(f"[M2/M3] {model_name:12s} "
              f"dRMSE={row['delta_rmse']:+.3f} [{row['delta_rmse_ci_lo']:+.3f},{row['delta_rmse_ci_hi']:+.3f}]  "
              f"dsize_gap={row['delta_size_gap']:+.3f} "
              f"dlocalbiz_gap={row['delta_localbiz_gap']:+.3f}")

    return pd.DataFrame(rows)


def _model_class_label(model_name: str) -> str:
    return {
        "OLS": "Linear / unregularized",
        "HistGB_sq": "Gradient-boosted trees",
        "RandomForest": "Bagged tree ensemble",
        "SVR_rbf": "Kernel machine",
    }[model_name]


def _verdict(metric_name: str, ci_lo: float, ci_hi: float) -> str:
    """For RMSE and size_gap, negative = improvement. For localbiz_gap, negative is
    also improvement (smaller local-business error gap). All three metrics share the
    "negative delta = better" convention here, so a single rule applies."""
    if ci_hi < 0:
        return "significant_improvement"
    if ci_lo > 0:
        return "significant_harm"
    return "no_effect"


def summarize_headline_pattern(result: pd.DataFrame) -> str:
    """M3: state whether mitigation effectiveness is monotonic in model flexibility."""
    flexibility_order = ["OLS", "HistGB_sq", "RandomForest", "SVR_rbf"]
    ordered = result.set_index("model").loc[flexibility_order]
    all_three_improve = (
        (ordered["delta_rmse_verdict"] == "significant_improvement")
        & (ordered["delta_size_gap_verdict"] == "significant_improvement")
        & (ordered["delta_localbiz_gap_verdict"] == "significant_improvement")
    )
    if all_three_improve.iloc[-1] and not all_three_improve.iloc[:-1].any():
        return (
            "M3 headline pattern: only the most flexible pre-specified model class "
            f"({flexibility_order[-1]}) achieves a simultaneous, statistically detectable "
            "improvement across RMSE, size_gap, and localbiz_gap. Less flexible classes "
            "show no accuracy/size benefit and, for the two least flexible, a statistically "
            "detectable INCREASE in the local-business gap. See root README §16.3-§16.4."
        )
    return (
        "M3 pattern differs from the pre-registered README narrative for this run's data "
        "-- re-verify against root README §16.3 before citing a monotonic-flexibility claim."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="M2/M3 independent model-class bootstrap re-test.")
    parser.add_argument("--input", default="data/customer_panel.csv")
    parser.add_argument("--output", default="supplementary_mitigation_study/model_class_bootstrap_size_blind.csv")
    parser.add_argument("--report", default="supplementary_mitigation_study/model_class_bootstrap_report.json")
    parser.add_argument("--n-reps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args()

    panel = load_panel(args.input)
    result = run_model_class_retest(panel, n_reps=args.n_reps, seed=args.seed)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)

    headline = summarize_headline_pattern(result)
    report = {
        "n_customers": len(panel),
        "n_reps": args.n_reps,
        "seed": args.seed,
        "strategy": RETEST_STRATEGY,
        "model_classes": PRESPECIFIED_MODEL_CLASSES,
        "headline_pattern": headline,
        "outstanding_validation_debt": [
            "Only Size-blind has received this four-model-class bootstrap; "
            "Spend-normalized and Campaign-adaptive have not (root README §16.6, item 1).",
            "The full M1 108-combination bootstrap distribution has not been computed "
            "alongside this re-test (item 2).",
            "No SHAP/partial-dependence mechanism test has been run on Size-blind x "
            "SVR-RBF specifically (item 3).",
            "Only the cut0.00 local-business definition is used here; cutoff sensitivity "
            "(0.25/0.50/0.75) has not yet been checked for the M-series (item 4).",
            "No independent sample has been used to check replication (item 5).",
        ],
    }
    with open(args.report, "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + headline)
    print(f"\nWrote {args.output} and {args.report}")


if __name__ == "__main__":
    main()
