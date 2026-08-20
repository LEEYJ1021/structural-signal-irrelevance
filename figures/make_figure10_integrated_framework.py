"""
Figure 10 | Integrated framework — structural signal irrelevance across two
independent tests (cross-sectional Study 1 + longitudinal Study 2).

Reads no external data (this is a conceptual/synthesis diagram, not a
statistical plot) — all numbers embedded are pulled directly from
RESULTS_SUMMARY.md / DESIGN_ARTIFACT.md and are static labels, not computed.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.lines as mlines

fig, ax = plt.subplots(figsize=(15, 9))
ax.set_xlim(0, 15)
ax.set_ylim(0, 9)
ax.axis("off")

# ---------- palette ----------
c_structural = "#B0B7C6"   # grey-blue: structural attribute boxes
c_mediator   = "#2E86AB"   # blue: legitimate mediator / own-signal boxes
c_outcome    = "#1B4965"   # dark navy: outcome boxes
c_null       = "#C1121F"   # red: null / severed direct path
c_synth      = "#EAF4F4"   # light background for synthesis box
c_text_dark  = "#1B1B1B"

def box(x, y, w, h, text, facecolor, textcolor="white", fontsize=10.5, weight="bold"):
    b = FancyBboxPatch((x, y), w, h,
                        boxstyle="round,pad=0.02,rounding_size=0.08",
                        linewidth=1.4, edgecolor="#333333",
                        facecolor=facecolor, zorder=3)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, color=textcolor, weight=weight, zorder=4,
             linespacing=1.35)
    return b

def solid_arrow(x1, y1, x2, y2, color="#333333", lw=2.2, connectionstyle="arc3,rad=0.0"):
    arr = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=18,
                           linewidth=lw, color=color, connectionstyle=connectionstyle, zorder=2)
    ax.add_patch(arr)

def dashed_null_arrow(x1, y1, x2, y2, connectionstyle="arc3,rad=-0.35"):
    arr = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
                           linewidth=1.8, color=c_null, linestyle=(0, (5, 3)),
                           connectionstyle=connectionstyle, zorder=2, alpha=0.9)
    ax.add_patch(arr)

# ================= Title =================
ax.text(7.5, 8.65, "Figure 10 | Integrated Framework", ha="center", fontsize=17, weight="bold")
ax.text(7.5, 8.25,
        "Two independent samples, two independent time axes, one converging pattern:\n"
        "structural attributes show no residual direct association with algorithmic outcomes",
        ha="center", fontsize=10.5, color="#444444", linespacing=1.4)

# ================= Panel A: Study 1 (cross-sectional) =================
ax.text(3.4, 7.55, "Study 1 — Cross-sectional", ha="center", fontsize=13, weight="bold", color=c_text_dark)
ax.text(3.4, 7.22, "n = 321 advertisers · 19.3M rows", ha="center", fontsize=9, color="#555555")

box(0.6, 5.7, 3.0, 0.95, "Advertiser Size\n(structural attribute)", c_structural, textcolor="#222222")
box(0.6, 3.9, 3.0, 0.95, "Total Spend\n(legitimate mediator)", c_mediator)
box(0.6, 2.1, 3.0, 0.95, "Algorithmic Outcome\n(approval · CPC · ad rank)", c_outcome)

solid_arrow(2.1, 5.7, 2.1, 4.85, color="#1B4965")
ax.text(2.55, 5.28, "H1a: +\n(p<.001)", fontsize=8.3, color="#1B4965", ha="left")
solid_arrow(2.1, 3.9, 2.1, 3.05, color="#1B4965")
ax.text(2.55, 3.48, "H1b: +\n(p=.032, bid_amount)", fontsize=8.3, color="#1B4965", ha="left")

dashed_null_arrow(0.55, 6.1, 0.55, 2.5, connectionstyle="arc3,rad=0.55")
ax.text(-0.15, 4.3, "H1c — no direct path\n(cluster-robust p>.07,\n8/8 robustness methods null)",
        fontsize=8.0, color=c_null, ha="center", rotation=90, va="center", weight="bold")

# ================= Panel B: Study 2 (longitudinal) =================
ax.text(11.6, 7.55, "Study 2 — Longitudinal", ha="center", fontsize=13, weight="bold", color=c_text_dark)
ax.text(11.6, 7.22, "n = 29 customers · 204 ad groups (independent sample)", ha="center", fontsize=9, color="#555555")

box(10.0, 5.7, 3.2, 0.95, "Account Maturity\n(structural / tenure attribute)", c_structural, textcolor="#222222")
box(10.0, 3.9, 3.2, 0.95, "Ad Group's Own\nEarly Signal (mediator)", c_mediator)
box(10.0, 2.1, 3.2, 0.95, "Near-term Growth\n(14-day-ahead rank)", c_outcome)

solid_arrow(11.6, 3.9, 11.6, 3.05, color="#1B4965")
ax.text(12.1, 3.48, "predictive:\nρ ≈ 0.39–0.47", fontsize=8.3, color="#1B4965", ha="left")

dashed_null_arrow(14.15, 6.1, 14.15, 2.5, connectionstyle="arc3,rad=-0.55")
ax.text(14.85, 4.3, "RQ1 — no direct path\n(β=8.34, p=.576;\nTOST inconclusive, p=.197)",
        fontsize=8.0, color=c_null, ha="center", rotation=90, va="center", weight="bold")

dashed_null_arrow(10.05, 5.9, 10.05, 4.35, connectionstyle="arc3,rad=0.4")
ax.text(9.15, 5.1, "maturity adds\nno within-customer\nimprovement\n(Δρ ≈ 0, RQ2/H2b)",
        fontsize=7.6, color=c_null, ha="center", va="center")

# ================= divider =================
ax.plot([7.5, 7.5], [1.85, 7.85], color="#CCCCCC", linewidth=1.2, linestyle=":", zorder=1)

# ================= Synthesis box =================
synth = FancyBboxPatch((1.0, 0.25), 13.0, 1.35,
                        boxstyle="round,pad=0.03,rounding_size=0.1",
                        linewidth=1.6, edgecolor="#1B4965", facecolor=c_synth, zorder=3)
ax.add_patch(synth)
ax.text(7.5, 1.28,
        "The direct effect of structural attributes (size, tenure) is absent in BOTH independent samples,\nacross BOTH independent time axes",
        ha="center", fontsize=11.2, weight="bold", color="#1B4965", linespacing=1.4)
ax.text(7.5, 0.62,
        "Real-time behavioral signals (spend / the unit's own early operating signal) consistently do the explanatory work instead\n"
        "(both are associational patterns, not causal claims — 2SLS incomplete in Study 1; TOST inconclusive in Study 2)",
        ha="center", fontsize=8.6, color="#333333", linespacing=1.5)

solid_arrow(3.4, 2.05, 6.6, 0.95, color="#1B4965", lw=1.6, connectionstyle="arc3,rad=-0.15")
solid_arrow(11.6, 2.05, 8.4, 0.95, color="#1B4965", lw=1.6, connectionstyle="arc3,rad=0.15")

# ================= Legend =================
legend_items = [
    mpatches.Patch(color=c_structural, label="Structural attribute (tested)"),
    mpatches.Patch(color=c_mediator, label="Legitimate mediator / unit signal"),
    mpatches.Patch(color=c_outcome, label="Algorithmic outcome"),
    mlines.Line2D([], [], color=c_null, linestyle=(0, (5, 3)), linewidth=1.8, label="Direct path — null (rejected / not established)"),
]
ax.legend(handles=legend_items, loc="lower center", bbox_to_anchor=(0.5, -0.06),
          ncol=4, frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig("/home/claude/repo/figures/Figure10_integrated_framework.png", dpi=220, bbox_inches="tight",
            facecolor="white")
print("saved")
