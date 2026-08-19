"""
figures/make_figure9_tost_equivalence.py

Figure 9 -- TOST equivalence plot for the two central null results (RQ1:
account maturity -> initial growth slope; RQ2/H2b: does maturity improve
growth prediction). Shows the observed effect against its pre-specified
equivalence margin (SESOI); reads
supplementary_robustness/outputs/03_equivalence_and_sensitivity_notes.json,
falling back to the literal values reported in
supplementary_robustness/03_equivalence_and_sensitivity_notes.md.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS_PATH = Path("supplementary_robustness/outputs/03_equivalence_and_sensitivity_notes.json")
OUT_PATH = Path("figures/Figure9_tost_equivalence.png")

FALLBACK = {
    "RQ1\n(maturity -> growth slope)": {"observed": 0.085, "margin": 0.20, "tost_p": 0.197},
    "RQ2 / H2b\n(maturity -> prediction improvement)": {"observed": 0.023, "margin": 0.05, "tost_p": 0.290},
}


def load_values():
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        rq1 = data.get("rq1_tost", {})
        rq2 = data.get("rq2_h2b_tost", {})
        out = dict(FALLBACK)
        if "observed_beta" in rq1:
            out["RQ1\n(maturity -> growth slope)"] = {
                "observed": rq1["observed_beta"], "margin": rq1["margin"], "tost_p": rq1["tost_p"]}
        if "mean_improvement" in rq2:
            out["RQ2 / H2b\n(maturity -> prediction improvement)"] = {
                "observed": rq2["mean_improvement"], "margin": rq2["margin"], "tost_p": rq2["tost_p"]}
        return out
    return FALLBACK


def main():
    values = load_values()
    fig, axes = plt.subplots(1, len(values), figsize=(9, 3.4), sharey=False)
    if len(values) == 1:
        axes = [axes]

    for ax, (label, v) in zip(axes, values.items()):
        margin, observed = v["margin"], v["observed"]
        ax.axvspan(-margin, margin, color="#d9ead3", alpha=0.7, label="Equivalence region (SESOI)")
        ax.axvline(0, color="gray", linestyle="--", linewidth=1)
        ax.plot(observed, 0, "o", color="#c0392b", markersize=12, zorder=5)
        span = max(margin, abs(observed)) * 1.8
        ax.set_xlim(-span, span)
        ax.set_yticks([])
        ax.set_xlabel("Effect size")
        equivalence = "established" if v["tost_p"] < 0.05 else "NOT established"
        ax.set_title(f"{label}\nTOST p = {v['tost_p']:.3f} ({equivalence})", fontsize=9)
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)

    fig.suptitle("Figure 9. TOST equivalence tests for the two central null results", y=1.05)
    handles, labels_ = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels_, loc="lower center", ncol=1, bbox_to_anchor=(0.5, -0.12), fontsize=8, frameon=False)
    fig.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
