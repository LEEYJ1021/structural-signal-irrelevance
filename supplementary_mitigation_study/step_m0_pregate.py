"""
step_m0_pregate.py — M0: the pre-registered gate for the mitigation study.

Tests whether two candidate mitigation strategies (Size-blind, Campaign-adaptive)
produce a customer-cluster-bootstrap-detectable change in the local-business gap
(gap_diff = localbiz_gap[strategy] - localbiz_gap[Baseline]) on two models fixed in
advance (OLS, HistGB-MAE) -- BEFORE any wider exploratory scan is run.

Per docs/METHODOLOGY_NOTES.md entry B9 and root README §16.1: only because this gate
did not trigger did the analysis proceed to step_m1_exploratory_scan.py (an explicitly
labeled exploratory scan) followed by step_m2_m3_model_class_bootstrap.py (an
independent, pre-specified re-test), rather than a single undifferentiated pass.

Usage:
    python supplementary_mitigation_study/step_m0_pregate.py \
        --input data/customer_panel.csv \
        --output supplementary_mitigation_study/mitigation_gate_table.csv \
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
    GATE_STRATEGIES,
    GATE_MODELS,
    RANDOM_SEED,
    bootstrap_ci,
    customer_cluster_bootstrap,
    load_panel,
    localbiz_gap,
    make_fit_predict_fn,
)


def gap_diff_metric_factory(baseline_pred_lookup):
    """Return a metric_fn(panel, y_pred) -> gap_diff, comparing this replicate's
    localbiz_gap against the ALREADY-COMPUTED baseline localbiz_gap for the same
    bootstrap replicate (matched by row order, since both are drawn from the same
    resampled panel within one bootstrap iteration -- see run_gate() below).
    """

    def _metric(panel: pd.DataFrame, y_pred: np.ndarray) -> float:
        strat_gap = localbiz_gap(panel, panel["y"], y_pred, cutoff=0.00)
        base_gap = baseline_pred_lookup(panel)
        return strat_gap - base_gap

    return _metric


def run_gate(panel: pd.DataFrame, n_reps: int, seed: int) -> pd.DataFrame:
    """Run the M0 gate: for each (strategy, model) in GATE_STRATEGIES x GATE_MODELS,
    bootstrap gap_diff = localbiz_gap(strategy) - localbiz_gap(Baseline), using the
    SAME resampled customers for both the strategy fit and the Baseline fit within
    each replicate (paired bootstrap, reduces variance vs. two independent bootstraps).
    """
    rng = np.random.default_rng(seed)
    n = len(panel)
    rows = []

    for model_name in GATE_MODELS:
        baseline_fit_predict = make_fit_predict_fn("Baseline", model_name)

        for strategy_name in GATE_STRATEGIES:
            strat_fit_predict = make_fit_predict_fn(strategy_name, model_name)

            # Point estimate on the full panel
            base_pred_full = baseline_fit_predict(panel)
            strat_pred_full = strat_fit_predict(panel)
            point_gap_diff = (
                localbiz_gap(panel, panel["y"], strat_pred_full, cutoff=0.00)
                - localbiz_gap(panel, panel["y"], base_pred_full, cutoff=0.00)
            )

            # Paired customer-cluster bootstrap
            draws = np.empty(n_reps)
            for b in range(n_reps):
                idx = rng.integers(0, n, size=n)
                boot_panel = panel.iloc[idx].reset_index(drop=True)
                base_pred = baseline_fit_predict(boot_panel)
                strat_pred = strat_fit_predict(boot_panel)
                base_gap = localbiz_gap(boot_panel, boot_panel["y"], base_pred, cutoff=0.00)
                strat_gap = localbiz_gap(boot_panel, boot_panel["y"], strat_pred, cutoff=0.00)
                draws[b] = strat_gap - base_gap

            ci_lo, ci_hi = bootstrap_ci(draws)
            triggered = ci_lo > 0 or ci_hi < 0

            rows.append({
                "strategy": strategy_name,
                "model": model_name,
                "gap_diff_point": point_gap_diff,
                "gap_diff_ci_lo": ci_lo,
                "gap_diff_ci_hi": ci_hi,
                "n_reps": n_reps,
                "gate_triggered": triggered,
            })
            print(
                f"[M0 gate] {strategy_name:22s} x {model_name:12s} "
                f"gap_diff={point_gap_diff:+.4f}  95% CI=[{ci_lo:+.4f}, {ci_hi:+.4f}]  "
                f"triggered={triggered}"
            )

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="M0 pre-registered mitigation gate.")
    parser.add_argument("--input", default="data/customer_panel.csv",
                         help="Path to the schema-compatible customer-level extract.")
    parser.add_argument("--output", default="supplementary_mitigation_study/mitigation_gate_table.csv")
    parser.add_argument("--report", default="supplementary_mitigation_study/mitigation_gate_report.json")
    parser.add_argument("--n-reps", type=int, default=200)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args()

    panel = load_panel(args.input)
    result = run_gate(panel, n_reps=args.n_reps, seed=args.seed)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)

    gate_triggered_overall = bool(result["gate_triggered"].any())
    report = {
        "n_customers": len(panel),
        "n_reps": args.n_reps,
        "seed": args.seed,
        "gate_strategies": GATE_STRATEGIES,
        "gate_models": GATE_MODELS,
        "cells_tested": len(result),
        "cells_triggered": int(result["gate_triggered"].sum()),
        "gate_triggered_overall": gate_triggered_overall,
        "verdict": (
            "Gate TRIGGERED: at least one cell's 95% CI excludes 0 -- a pre-specified "
            "mitigation effect is directly supported at this tier. See root README §16.1."
            if gate_triggered_overall else
            "Gate NOT triggered: all cells' 95% CIs include 0. Per the rule fixed before "
            "this diagnostic ran, proceed to step_m1_exploratory_scan.py, whose findings "
            "are disclosed as post-hoc exploration rather than a continuation of this "
            "pre-registered plan. See root README §16.1 and Figure 18."
        ),
    }
    with open(args.report, "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + report["verdict"])
    print(f"\nWrote {args.output} and {args.report}")


if __name__ == "__main__":
    main()
