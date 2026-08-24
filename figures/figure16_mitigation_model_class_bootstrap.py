"""
Figure 16 — Mitigation effect of the Size-blind strategy across four
pre-specified model classes (customer-cluster bootstrap, 200 reps).

Source data: supplementary_mitigation_study/model_class_bootstrap_size_blind.csv
Supports: root README.md §16.3 (M2/M3); docs/RESULTS_SUMMARY.md §14
Output: figures/Figure16_mitigation_model_class_bootstrap.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10.5,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.color": "#333333",
    "ytick.color": "#333333",
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
    "yellow": "#F0E442",
    "skyblue": "#56B4E9",
}

models = ["OLS\n(linear)", "HistGB\n(boosting)", "RandomForest\n(tree ensemble)", "SVR-RBF\n(kernel)"]

# (delta, ci_lo, ci_hi) for each metric, ordered OLS, HistGB, RF, SVR-RBF
# — matches supplementary_mitigation_study/model_class_bootstrap_size_blind.csv
rmse = [(0.010, -0.006, 0.027), (0.006, -0.012, 0.024), (-0.074, -0.096, -0.052), (-0.129, -0.151, -0.107)]
size_gap = [(-0.018, -0.043, 0.009), (0.004, -0.021, 0.030), (-0.167, -0.201, -0.134), (-0.200, -0.231, -0.168)]
localbiz_gap = [(0.082, 0.051, 0.114), (0.031, 0.008, 0.055), (0.028, 0.006, 0.051), (-0.077, -0.094, -0.059)]

panels = [
    ("Δ RMSE\n(Size-blind − Baseline)", rmse),
    ("Δ size_gap\n(Size-blind − Baseline)", size_gap),
    ("Δ localbiz_gap\n(Size-blind − Baseline)", localbiz_gap),
]

fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.4), sharey=False)
y_pos = np.arange(len(models))[::-1]

for ax, (title, data) in zip(axes, panels):
    for i, (d, lo, hi) in enumerate(data):
        sig_improve = hi < 0
        sig_harm = lo > 0
        if sig_improve:
            color = OKABE_ITO["blue"]
        elif sig_harm:
            color = OKABE_ITO["red"]
        else:
            color = OKABE_ITO["gray"]
        y = y_pos[i]
        ax.plot([lo, hi], [y, y], color=color, lw=2.2, solid_capstyle="round", zorder=2)
        ax.plot(d, y, marker="o", markersize=7, color=color, markeredgecolor="white",
                markeredgewidth=0.8, zorder=3)
    ax.axvline(0, color="#444444", lw=1.0, linestyle="--", zorder=1)
    ax.set_title(title, fontsize=10.5, pad=8)
    ax.set_ylim(-0.7, len(models) - 0.3)
    ax.set_yticks(y_pos)
    if ax is axes[0]:
        ax.set_yticklabels(models, fontsize=10)
    else:
        ax.set_yticklabels([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Δ (95% customer-cluster bootstrap CI)", fontsize=9)

legend_handles = [
    mpatches.Patch(color=OKABE_ITO["blue"], label="CI excludes 0 — significant improvement"),
    mpatches.Patch(color=OKABE_ITO["red"], label="CI excludes 0 — significant harm"),
    mpatches.Patch(color=OKABE_ITO["gray"], label="CI includes 0 — no effect"),
]
fig.legend(handles=legend_handles, loc="lower center", ncol=3, frameon=False,
           bbox_to_anchor=(0.5, -0.06), fontsize=9.5)

fig.suptitle(
    "Figure 16 — Mitigation effect of the Size-blind strategy is contingent on model flexibility\n"
    "(customer-cluster bootstrap, 200 reps; four model classes pre-specified before testing)",
    fontsize=11.5, y=1.04
)
fig.tight_layout()

# Repo-relative output path (run from repository root)
OUT_PATH = "figures/Figure16_mitigation_model_class_bootstrap.png"
fig.savefig(OUT_PATH, bbox_inches="tight", pad_inches=0.35)
plt.close(fig)
print(f"Figure 16 written to {OUT_PATH}")
