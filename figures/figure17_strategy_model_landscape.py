"""
Figure 17 — Exploratory strategy x model landscape (M1 scan).
RMSE (x) vs size_gap (y), bubble size = localbiz_gap (cut0.00), color = strategy.

Source data: supplementary_mitigation_study/rq3_v4_strategy_summary.csv
             (internal pipeline filename retained per docs/METHODOLOGY_NOTES.md
             entry B8 — see appendix/hypothesis_id_legacy_mapping.md; this figure
             itself is labeled M1 throughout the README and this repository)
Supports: root README.md §16.2 (M1); docs/RESULTS_SUMMARY.md §13
Output: figures/Figure17_strategy_model_landscape.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

# real values transcribed from the M1 multi-model / multi-cutoff scan
data17 = {
    "Baseline": {
        "color": OKABE_ITO["gray"],
        "points": [
            ("OLS", 1.1691, 0.2363, 0.0404), ("Ridge", 1.1691, 0.2363, 0.0404),
            ("Lasso", 1.1691, 0.2341, 0.0420), ("ElasticNet", 1.1688, 0.2354, 0.0408),
            ("BayesianRidge", 1.1691, 0.2363, 0.0404), ("RandomForest", 1.2485, 0.2963, 0.0628),
            ("HistGB_sq", 1.2194, 0.3914, 0.0727), ("HistGB_MAE", 1.1593, 0.3286, 0.0554),
            ("SVR_rbf", 1.3668, 0.2984, 0.1180),
        ],
    },
    "A_Size_blind": {
        "color": OKABE_ITO["blue"],
        "points": [
            ("OLS", 1.1786, 0.2179, 0.1282), ("Ridge", 1.1786, 0.2179, 0.1282),
            ("Lasso", 1.1775, 0.2165, 0.1244), ("ElasticNet", 1.1778, 0.2174, 0.1249),
            ("BayesianRidge", 1.1786, 0.2179, 0.1280), ("RandomForest", 1.1745, 0.1295, 0.0903),
            ("HistGB_sq", 1.1842, 0.1931, 0.0626), ("HistGB_MAE", 1.1624, 0.1118, 0.0767),
            ("SVR_rbf", 1.2382, 0.0989, 0.0412),
        ],
    },
    "B_Spend_normalized": {
        "color": OKABE_ITO["orange"],
        "points": [
            ("OLS", 1.3048, 0.1613, 0.1259), ("Ridge", 1.3048, 0.1613, 0.1258),
            ("Lasso", 1.3016, 0.1594, 0.1205), ("ElasticNet", 1.3028, 0.1607, 0.1226),
            ("BayesianRidge", 1.3047, 0.1614, 0.1257), ("RandomForest", 1.4674, 0.1133, 0.1423),
            ("HistGB_sq", 1.5267, 0.1802, 0.1359), ("HistGB_MAE", 1.5055, 0.2509, 0.1486),
            ("SVR_rbf", 1.5153, 0.4352, 0.2815),
        ],
    },
    "C_Campaign_adaptive": {
        "color": OKABE_ITO["purple"],
        "points": [
            ("OLS", 1.2008, 0.1808, 0.0503), ("Ridge", 1.2008, 0.1808, 0.0503),
            ("Lasso", 1.1973, 0.1907, 0.0458), ("ElasticNet", 1.1971, 0.1899, 0.0479),
            ("BayesianRidge", 1.2006, 0.1812, 0.0503), ("RandomForest", 1.2517, 0.3253, 0.0695),
            ("HistGB_sq", 1.2300, 0.3955, 0.0743), ("HistGB_MAE", 1.1812, 0.3334, 0.0735),
            ("SVR_rbf", 1.4100, 0.2092, 0.0719),
        ],
    },
}

fig, ax = plt.subplots(figsize=(8.6, 6.6))

for strategy, d in data17.items():
    xs = [p[1] for p in d["points"]]
    ys = [p[2] for p in d["points"]]
    sizes = [max(p[3], 0.001) * 2600 for p in d["points"]]
    ax.scatter(xs, ys, s=sizes, color=d["color"], alpha=0.55, edgecolor="white",
               linewidth=0.9, label=strategy, zorder=3)

# annotate the candidates independently re-tested in Figure 16 / M2-M3
highlight = [
    ("A_Size_blind", "SVR_rbf", 1.2382, 0.0989, "Size-blind × SVR-RBF\n(confirmed at M2/M3: all 3 metrics improve)"),
    ("A_Size_blind", "RandomForest", 1.1745, 0.1295, "Size-blind × RandomForest\n(confirmed: RMSE, size_gap improve)"),
    ("Baseline", "SVR_rbf", 1.3668, 0.2984, "Baseline × SVR-RBF"),
]
for strat, model, x, y, label in highlight:
    ax.annotate(label, xy=(x, y), xytext=(x + 0.045, y + 0.045),
                fontsize=8.3, color="#222222",
                arrowprops=dict(arrowstyle="-", color="#666666", lw=0.8),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#999999", lw=0.6, alpha=0.92))

ax.set_xlabel("RMSE (overall, lower = more accurate)")
ax.set_ylabel("size_gap (large − small advertiser error gap, lower = fairer)")
ax.set_title(
    "Figure 17 — Exploratory strategy × model landscape (M1)\n"
    "(bubble size = local-business gap, cut0.00; larger = worse local-business disparity)",
    fontsize=11.5
)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(True, which="major", linestyle=":", linewidth=0.5, color="#cccccc", zorder=0)

leg1 = ax.legend(loc="upper left", frameon=False, fontsize=9, title="Strategy", title_fontsize=9.5)
ax.add_artist(leg1)

size_handles = [
    plt.scatter([], [], s=0.05 * 2600, color="#888888", alpha=0.4, label="localbiz_gap = 0.05"),
    plt.scatter([], [], s=0.15 * 2600, color="#888888", alpha=0.4, label="localbiz_gap = 0.15"),
    plt.scatter([], [], s=0.28 * 2600, color="#888888", alpha=0.4, label="localbiz_gap = 0.28"),
]
ax.legend(handles=size_handles, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False,
          fontsize=8.3, title="Bubble size", title_fontsize=8.8, labelspacing=1.8, borderpad=1.0)

# Repo-relative output path (run from repository root)
OUT_PATH = "figures/Figure17_strategy_model_landscape.png"
fig.savefig(OUT_PATH, bbox_inches="tight", pad_inches=0.3)
plt.close(fig)
print(f"Figure 17 written to {OUT_PATH}")
