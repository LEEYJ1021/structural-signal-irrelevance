"""
Figure 15 — Observed vs. combinatorially-predicted data-missingness rate
[POST-HOC / EXPLORATORY]

Reads:
  supplementary_localbiz_exploratory/detail/combinatoric_null_model_detail/part1_bin_summary.csv
Writes:
  figures/Figure15_combinatoric_null_model.png

Used in root README §6.5.
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font", family="NanumGothic")
matplotlib.rcParams["axes.unicode_minus"] = False

DETAIL = (
    Path(__file__).resolve().parent.parent
    / "supplementary_localbiz_exploratory" / "detail" / "combinatoric_null_model_detail"
)
bins = pd.read_csv(DETAIL / "part1_bin_summary.csv")

fig, ax = plt.subplots(figsize=(8.5, 5.2))
x = range(len(bins))
ax.plot(x, bins["observed_rate"], marker="o", color="#c0392b", lw=2, label="Observed")
ax.plot(x, bins["predicted_rate"], marker="s", color="#34495e", lw=2, ls="--",
        label="Predicted (independent-binomial null model)")
ax.fill_between(x, bins["observed_rate"], bins["predicted_rate"], alpha=0.15, color="#c0392b")

xtick_labels = [f"{int(round(r.mean_n_adgroups))}" for _, r in bins.iterrows()]
ax.set_xticks(list(x))
ax.set_xticklabels(xtick_labels, rotation=0)
ax.set_xlabel("Mean ad groups per customer, by bin")
ax.set_ylabel("P(customer has ≥1 ad group unmatched to performance data)")
ax.set_title(
    "Observed vs. combinatorially-expected missingness rate\n"
    "Gap = residual account-level clustering (over-dispersion 73×, χ²=16,583, df=6, p<.0001)",
    fontsize=10,
)
ax.set_ylim(0, 1.05)
ax.legend(loc="lower right")
plt.tight_layout()
out_path = Path(__file__).resolve().parent / "Figure15_combinatoric_null_model.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"saved: {out_path}")
