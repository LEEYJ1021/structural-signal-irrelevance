"""
Figure 5 -- two-panel figure: (left) the cold-start sample-construction
funnel (candidates -> trajectory-usable -> test-account-excluded), and
(right) the RQ1 null result, shown as the observed customer-level
effect against its bootstrap CI and the pre-registered large-effect
detection threshold from the Step K power simulation.

Reads: outputs/coldstart_v5/ (Steps A-D artifacts, regenerated live
       via the pipeline rather than a cached file, since the funnel
       counts are cheap to recompute and this keeps the figure
       synchronized with the current sample-definition config)
       outputs/analysis/rq1_results.json
       (produced by src/analysis/rq1_growth_curve_test.py)
Writes: outputs/figures/figure5_coldstart_funnel_and_rq1_null.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config

RQ1_PATH = Path("outputs/analysis/rq1_results.json")
OUT_PATH = Path("outputs/figures/figure5_coldstart_funnel_and_rq1_null.png")


def main():
    cfg = load_config("config/config.yaml")
    ctx = step_a(cfg)
    coldstart, usable = ctx["coldstart"], ctx["usable"]
    excl = set(cfg["sample_definition"].get("known_test_account_ids", []))
    final = usable[~usable["customer_id"].isin(excl)]

    funnel_labels = ["Cold-start\ncandidates", "Trajectory-\nusable", "Test-accounts\nexcluded"]
    funnel_counts = [len(coldstart), len(usable), len(final)]

    if not RQ1_PATH.exists():
        raise FileNotFoundError(f"{RQ1_PATH} not found -- run src/analysis/rq1_growth_curve_test.py first")
    rq1 = json.loads(RQ1_PATH.read_text())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    ax1.bar(funnel_labels, funnel_counts, color="#4C72B0")
    for i, c in enumerate(funnel_counts):
        ax1.text(i, c + max(funnel_counts) * 0.02, str(c), ha="center", fontsize=10)
    ax1.set_title("Cold-start sample-construction funnel")
    ax1.set_ylabel("n ad groups")

    beta = rq1["beta_standardized"]
    ci_low, ci_high = 0, 0  # standardized CI not separately bootstrapped; show raw-scale CI instead
    threshold = rq1["large_effect_threshold"]
    ax2.errorbar([0], [beta], yerr=[[beta - rq1["bootstrap_ci_low"] / max(abs(rq1["beta_ols"]), 1e-9) * abs(beta)],
                                     [rq1["bootstrap_ci_high"] / max(abs(rq1["beta_ols"]), 1e-9) * abs(beta) - beta]],
                 fmt="o", color="#C44E52", capsize=5, markersize=10, label="observed (standardized beta)")
    ax2.axhline(threshold, color="black", linestyle="--", label=f"pre-registered large-effect threshold ({threshold})")
    ax2.axhline(-threshold, color="black", linestyle="--")
    ax2.axhline(0, color="gray", linewidth=0.8)
    ax2.set_xlim(-1, 1)
    ax2.set_xticks([])
    ax2.set_ylabel("Standardized effect (account maturity -> initial growth slope)")
    ax2.set_title(f"RQ1: {rq1['verdict']}\n(n_customers={rq1['n_customers']}, perm p={rq1['perm_p']:.3f})")
    ax2.legend(fontsize=8, loc="upper right")

    plt.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200)
    print(f"[figure5] wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
