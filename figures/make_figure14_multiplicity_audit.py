"""
Figure 14 — Research-wide multiplicity audit across all 25 reported p-values
[CROSS-CUTTING — applies to both Level 1 and Level 2]

Reads:
  research_wide_audit/detail/research_wide_audit_detail/part1_all_reported_tests.csv
Writes:
  figures/Figure14_multiplicity_audit.png

Used in root README §7.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font", family="NanumGothic")
matplotlib.rcParams["axes.unicode_minus"] = False

DETAIL = Path(__file__).resolve().parent.parent / "research_wide_audit" / "detail" / "research_wide_audit_detail"
df = pd.read_csv(DETAIL / "part1_all_reported_tests.csv")
df = df.sort_values("p").reset_index(drop=True)
df["neglog10p"] = -np.log10(df["p"])

m = len(df)
families = sorted(df["family"].unique())
palette = plt.cm.tab10(np.linspace(0, 1, len(families)))
color_map = dict(zip(families, palette))
point_colors = df["family"].map(color_map)

bonf_alpha = 0.05 / m
bonf_line = -np.log10(bonf_alpha)
bh_thresh = (np.arange(1, m + 1) / m) * 0.05
bh_line = -np.log10(bh_thresh)

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.scatter(range(m), df["neglog10p"], c=list(point_colors), s=70, zorder=3, edgecolor="white", linewidth=0.5)
ax.axhline(bonf_line, color="black", ls="--", lw=1.2, label=f"Bonferroni threshold (p<{bonf_alpha:.4f}) — 0/{m} survive")
ax.plot(range(m), bh_line, color="gray", ls=":", lw=1.2, label=f"BH-FDR threshold (rank-dependent) — 3/{m} survive")

for fam, c in color_map.items():
    ax.scatter([], [], color=c, label=fam, s=50)

ax.set_xticks([])
ax.set_ylabel("-log10(p)")
ax.set_xlabel("All 25 officially-reported p-values, sorted by significance")
ax.set_title(
    "Research-wide multiplicity audit: 0/25 survive Bonferroni, 3/25 survive BH-FDR\n"
    "(the 3 survivors are all Level 2 exploratory results — see root README §7)",
    fontsize=10,
)
ax.legend(fontsize=7.5, ncol=2, loc="upper left", framealpha=0.9)
plt.tight_layout()
out_path = Path(__file__).resolve().parent / "Figure14_multiplicity_audit.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"saved: {out_path}")
