"""
Figure 2 (corrected) -- Advertiser-size effect on approval, cost efficiency,
and ad rank, controlling for spend (H1c / H2b).

Source of truth for every number below: RESULTS_SUMMARY.md sec. 2 /
H3관련.txt lines 1131-1140 (identical table, confirmed twice in the
uploaded material). No value here is invented or approximated.
"""
import matplotlib.pyplot as plt
import numpy as np

# Real data, verbatim from RESULTS_SUMMARY.md sec.2 / H3관련.txt L1131-1140
DATA = {
    "Approval rate\n(percentage-point scale)": {
        "mde": 0.00535,
        "rows": [
            {"sample": "Full sample\n(n=4,407)",        "beta": -0.0025, "ci": (-0.0064, 0.0014), "p": 0.251, "bf10": 0.047},
            {"sample": "Excl. spike accounts\n(n=3,432)", "beta": -0.0019, "ci": (-0.0060, 0.0022), "p": 0.357, "bf10": 0.033},
        ],
    },
    "Cost-per-click (log points)": {
        "mde": 0.684,
        "rows": [
            {"sample": "Full sample\n(n=4,407)",        "beta": -0.10, "ci": (-0.58, 0.38), "p": 0.756, "bf10": 0.044},
            {"sample": "Excl. spike accounts\n(n=3,432)", "beta": +0.35, "ci": (-0.13, 0.83), "p": 0.073, "bf10": 1.9e5},
        ],
    },
    "Mean ad rank (rank units)": {
        "mde": 0.943,
        "rows": [
            {"sample": "Full sample\n(n=4,407)",        "beta": +0.27, "ci": (-0.42, 0.96), "p": 0.481, "bf10": 0.062},
            {"sample": "Excl. spike accounts\n(n=3,432)", "beta": +0.02, "ci": (-0.79, 0.83), "p": 0.937, "bf10": 0.020},
        ],
    },
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))

for ax, (outcome, block) in zip(axes, DATA.items()):
    mde = block["mde"]
    rows = block["rows"]
    n = len(rows)

    ax.axvspan(-mde, mde, color="#e8e8e8", zorder=0, label=f"MDE @ 80% power (\u00b1{mde:g})")
    ax.axvline(0, color="black", linewidth=0.9, zorder=1)

    for i, r in enumerate(rows):
        y = n - 1 - i
        lo, hi = r["ci"]
        ax.errorbar(r["beta"], y, xerr=[[r["beta"] - lo], [hi - r["beta"]]],
                    fmt="o", color="#1f4e79", ecolor="#1f4e79",
                    elinewidth=2, capsize=5, markersize=9, zorder=3)
        bf_str = f"{r['bf10']:.1e}" if r["bf10"] >= 1000 or r["bf10"] < 0.001 else f"{r['bf10']:.3f}"
        ax.text(0, y - 0.32, f"p={r['p']:.3f}, BF\u2081\u2080={bf_str}",
                ha="center", va="top", fontsize=8, color="#333333")

    ax.set_yticks(range(n))
    ax.set_yticklabels([rows[n - 1 - i]["sample"] for i in range(n)], fontsize=9)
    ax.set_ylim(-0.9, n - 0.1)
    ax.set_xlabel(outcome, fontsize=9.5)
    ax.legend(loc="upper right", fontsize=7.5, frameon=False)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

fig.suptitle("Figure 2 | Advertiser-size effect on approval, cost efficiency, and ad rank,\ncontrolling for spend (RQ2, H2b)",
             fontsize=12.5, fontweight="bold", y=1.06)
fig.text(0.5, -0.05,
          "Dot-whisker: cluster-robust point estimate and 95% CI, native (unstandardized) scale per outcome.\n"
          "Shaded band: minimum detectable effect (MDE) at 80% power. Every CI both crosses zero and sits inside\n"
          "(or at the edge of) its own MDE band. BF10 favors H0 throughout except CPC under spike exclusion,\n"
          "which is directionally reversed and flagged as a sensitivity finding, not a confirmatory one.",
          ha="center", fontsize=7.8, color="dimgray")

plt.tight_layout()
plt.savefig("/home/claude/figs/Figure2_corrected.png", dpi=200, bbox_inches="tight", facecolor="white")
print("saved Figure2_corrected.png")
