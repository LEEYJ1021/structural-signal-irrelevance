"""
Figure 13 — Serving-structure heterogeneity across campaign types
[POST-HOC / EXPLORATORY]

Reads:
  supplementary_localbiz_exploratory/detail/localbiz_structural_heterogeneity_causal_chain_report.json
Writes:
  figures/Figure13_serving_structure.png

Used in root README §6.2, §6.3.
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font", family="NanumGothic")
matplotlib.rcParams["axes.unicode_minus"] = False

DETAIL = Path(__file__).resolve().parent.parent / "supplementary_localbiz_exploratory" / "detail"
report = json.load(
    open(DETAIL / "localbiz_structural_heterogeneity_causal_chain_report.json", encoding="utf-8")
)
rows = report["sections"]["part1_master_table"]

labels = [r["label"] for r in rows]
kw_match = [r["pct_keyword_matched"] for r in rows]
ratio = [r["median_ratio_actual_to_bid"] if r["median_ratio_actual_to_bid"] is not None else np.nan for r in rows]
auction_like = [r["auction_like"] for r in rows]
colors = ["#34495e" if a else "#c0392b" for a in auction_like]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

bars0 = axes[0].bar(labels, kw_match, color=colors)
axes[0].set_ylabel("% ad groups matched in keyword_dim")
axes[0].set_title("A. Keyword-auction matching rate\n(red = classified non-auction-like, threshold 5%)")
axes[0].axhline(5, color="gray", ls="--", lw=0.8)
axes[0].tick_params(axis="x", rotation=20)
for b, v in zip(bars0, kw_match):
    axes[0].text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}%", ha="center", fontsize=8)

bars1 = axes[1].bar(labels, ratio, color=colors)
axes[1].axhline(1.0, color="gray", ls="--", lw=0.8, label="ratio = 1 (bid ≈ actual CPC)")
axes[1].set_ylabel("Median (actual CPC / bid amount)")
axes[1].set_title("B. Bid–CPC decoupling\n(red = structurally decoupled from bid price)")
axes[1].tick_params(axis="x", rotation=20)
axes[1].legend(fontsize=8)
for b, v in zip(bars1, ratio):
    if not np.isnan(v):
        axes[1].text(b.get_x() + b.get_width() / 2, v + 0.05, f"{v:.2f}", ha="center", fontsize=8)

fig.suptitle(
    "Serving-structure heterogeneity by campaign type [POST-HOC / EXPLORATORY]",
    fontsize=11, y=1.02,
)
plt.tight_layout()
out_path = Path(__file__).resolve().parent / "Figure13_serving_structure.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"saved: {out_path}")
