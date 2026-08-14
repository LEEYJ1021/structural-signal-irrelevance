"""
Figure 6 -- two-panel figure: (left) RQ2 within-customer LOCO predictive
rho as a function of prediction horizon (early/later window pair), and
(right) RQ3 flagging lift over random by decision cutoff, restricted to
the reliable threshold bands (Step M6-1).

Reads: outputs/analysis/rq2_results.csv
       (produced by src/analysis/rq2_prediction_validation.py)
       outputs/coldstart_v5/step_m_precision_recall_lift.csv
       (produced by src/coldstart_v5/step_m_intervention_timing_simulation.py)
Writes: outputs/figures/figure6_rq2_horizon_rq3_lift.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RQ2_PATH = Path("outputs/analysis/rq2_results.csv")
M_PATH = Path("outputs/coldstart_v5/step_m_precision_recall_lift.csv")
OUT_PATH = Path("outputs/figures/figure6_rq2_horizon_rq3_lift.png")


def main():
    if not RQ2_PATH.exists():
        raise FileNotFoundError(f"{RQ2_PATH} not found -- run src/analysis/rq2_prediction_validation.py first")
    if not M_PATH.exists():
        raise FileNotFoundError(f"{M_PATH} not found -- run src/coldstart_v5/step_m_intervention_timing_simulation.py first")

    rq2 = pd.read_csv(RQ2_PATH)
    rq2["horizon_label"] = rq2["early_window"].astype(str) + "/" + rq2["later_window"].astype(str)

    m = pd.read_csv(M_PATH)
    m_reliable = m[m["reliable"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    ax1.plot(rq2["horizon_label"], rq2["within_base"], "o-", label="H2a (base features)", color="#4C72B0")
    ax1.plot(rq2["horizon_label"], rq2["within_plus"], "o-", label="H2b (+maturity)", color="#DD8452")
    ax1.axhline(0, color="gray", linewidth=0.8)
    ax1.set_xlabel("early/later window (days)")
    ax1.set_ylabel("within-customer LOCO rho")
    ax1.set_title("RQ2: predictive signal decays with horizon")
    ax1.legend(fontsize=8)

    for cutoff, g in m_reliable.groupby("cutoff"):
        ax2.plot(g["threshold"], g["lift"], "o-", label=f"cutoff={cutoff}d")
    ax2.axhline(1.0, color="black", linestyle="--", linewidth=0.8, label="random (lift=1.0)")
    ax2.set_xlabel("flagging threshold (bottom quantile)")
    ax2.set_ylabel("lift over random")
    ax2.set_title("RQ3: flagging lift by decision cutoff\n(reliable thresholds only)")
    ax2.legend(fontsize=8)

    plt.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200)
    print(f"[figure6] wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
