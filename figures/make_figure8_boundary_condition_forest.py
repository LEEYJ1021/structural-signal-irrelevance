"""
Figure 8 (corrected) -- Campaign product-type heterogeneity (H2).

The original script used an ARBITRARY illustrative half-width
(`max(0.15, abs(c) * 0.6)`) that was never disclosed as an approximation.
This version backs out SE from the reported two-sided p-value under a
normal approximation (SE = |beta| / z, z = Phi^-1(1 - p/2)), which is the
standard way to reconstruct a CI when only beta and p are on record.
This is disclosed explicitly in the figure footnote -- it is still an
approximation (not the original cluster-robust SE), but it is a
principled, reproducible one instead of an invented constant.

Data source: RESULTS_SUMMARY.md sec.4 / H3관련.txt L1149 (verbatim).
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

STRATA = [
    {"label": "Website (1)\n(n=184)",        "beta": -0.279, "p": 0.052},
    {"label": "Local business (6)\n(n=27)",  "beta": +0.312, "p": 0.211},
    {"label": "Shopping (2)\n(n=17)",        "beta": +0.245, "p": 0.151},
]
JOINT_P = 0.023

for s in STRATA:
    z = norm.ppf(1 - s["p"] / 2)
    s["se_approx"] = abs(s["beta"]) / z
    s["ci"] = (s["beta"] - 1.96 * s["se_approx"], s["beta"] + 1.96 * s["se_approx"])

fig, ax = plt.subplots(figsize=(8, 4.4))
y = np.arange(len(STRATA))[::-1]

for yi, s in zip(y, STRATA):
    lo, hi = s["ci"]
    color = "#c0392b" if s["p"] < 0.05 else "#1f4e79"
    ax.errorbar(s["beta"], yi, xerr=[[s["beta"] - lo], [hi - s["beta"]]],
                fmt="o", color=color, ecolor="gray", elinewidth=1.5,
                capsize=5, markersize=9, zorder=3)
    ax.text(s["beta"], yi + 0.32, f"p={s['p']:.3f}", ha="center", fontsize=8, color="#333333")

ax.axvline(0, color="gray", linestyle="--", linewidth=1)
ax.set_yticks(y)
ax.set_yticklabels([s["label"] for s in STRATA])
ax.set_ylim(-0.8, len(STRATA) - 0.2)
ax.set_xlabel("c' (size, net of spend) -- CPC-based model")
ax.set_title(f"Figure 8. Campaign product-type heterogeneity\n(joint Wald test for interaction: p = {JOINT_P:.3f})",
             fontsize=11.5, pad=14)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.text(0.5, -0.06,
          "No individual stratum reaches p<.05; the joint test indicates the degree of size irrelevance\n"
          "varies by ad-product category, not that the null is overturned. CI here is reconstructed from the\n"
          "reported (beta, p) via normal approximation (SE = |beta|/z) -- an approximation of the original\n"
          "cluster-robust SE, disclosed here because the source SE was not separately persisted.",
          ha="center", fontsize=7.8, color="dimgray")

plt.tight_layout()
plt.savefig("/home/claude/figs/Figure8_corrected.png", dpi=200, bbox_inches="tight", facecolor="white")
print("saved Figure8_corrected.png")
for s in STRATA:
    print(s["label"].replace(chr(10), " "), "SE~", round(s["se_approx"], 4), "CI~", tuple(round(x, 3) for x in s["ci"]))
