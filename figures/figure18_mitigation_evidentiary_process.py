"""
Figure 18 — Two-stage evidentiary process diagram for the M-series
mitigation study (schematic; no invented statistics — see docs/RESULTS_SUMMARY.md
§§12-14 for the actual gate, scan, and re-test results this diagram summarizes).

Supports: root README.md §16.1 (M0 gate); docs/RESULTS_SUMMARY.md §12
Output: figures/Figure18_mitigation_evidentiary_process.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10.5,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 300,
})

OKABE_ITO = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "red": "#D55E00",
    "purple": "#CC79A7",
    "gray": "#999999",
}

fig, ax = plt.subplots(figsize=(10.5, 4.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis("off")

boxes = [
    (0.3, 1.3, 2.5, 1.6, "Pre-registered gate\n(M0)\nBootstrap gap_diff:\nSize-blind / Campaign-adaptive\nvs Baseline (OLS, HistGB_MAE)", OKABE_ITO["gray"]),
    (3.3, 1.3, 2.5, 1.6, "Gate outcome:\nall 4 cells' 95% CI\ninclude 0\n→ gate NOT triggered", OKABE_ITO["red"]),
    (6.3, 1.9, 2.5, 1.0, "Exploratory scan (M1)\n(12 strategies × 9 models)\nFDR-flagged candidates\n[winner's-curse risk]", OKABE_ITO["orange"]),
    (6.3, 0.3, 2.5, 1.0, "Independent re-test (M2/M3)\n(OLS/HistGB/RF/SVR-RBF)\npre-specified, independent\nbootstrap, 200 reps", OKABE_ITO["blue"]),
]
for x, y, w, h, text, color in boxes:
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.08",
                                    linewidth=1.4, edgecolor=color, facecolor=color + "22")
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.6, color="#222222")

# arrows
ax.annotate("", xy=(3.3, 2.1), xytext=(2.8, 2.1), arrowprops=dict(arrowstyle="->", lw=1.4, color="#333333"))
ax.annotate("", xy=(6.3, 2.4), xytext=(5.8, 2.05), arrowprops=dict(arrowstyle="->", lw=1.4, color="#333333"))
ax.annotate("", xy=(6.3, 0.8), xytext=(5.8, 1.65), arrowprops=dict(arrowstyle="->", lw=1.4, color="#333333"))
ax.text(6.1, 3.15, "gate skip →\nmarked exploratory throughout", fontsize=7.6, color="#555555", ha="center")

ax.set_title("Figure 18 — Evidentiary process for the mitigation (M-series) study",
             fontsize=11.5, pad=10)

fig.tight_layout()

# Repo-relative output path (run from repository root)
OUT_PATH = "figures/Figure18_mitigation_evidentiary_process.png"
fig.savefig(OUT_PATH, bbox_inches="tight", pad_inches=0.3)
plt.close(fig)
print(f"Figure 18 written to {OUT_PATH}")
