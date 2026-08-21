"""
Figure 12 (corrected) -- RQ2c leave-one-campaign-type-out: uncorrected vs.
corrected ranking. Renamed from legacy "H3" label per METHODOLOGY_NOTES.md
entry B7. Data verbatim from RESULTS_SUMMARY.md sec.8c/8d.
"""
import matplotlib.pyplot as plt
import numpy as np

# Panel A: initial (uncorrected) ranking by |beta shift|
RAW = [
    {"label": "Website",        "n_excl": 202, "n_remain": 26,  "abs_shift": 0.313, "unstable": True},
    {"label": "Local business", "n_excl": 72,  "n_remain": 156, "abs_shift": 0.247, "unstable": False},
    {"label": "Power content",  "n_excl": 13,  "n_remain": 215, "abs_shift": 0.014, "unstable": False},
    {"label": "Shopping",       "n_excl": 24,  "n_remain": 204, "abs_shift": 0.061, "unstable": False},
]

# Panel B: corrected, exclusion-size-matched empirical p, stable types only
CORR = [
    {"label": "Local business", "emp_p": 1.0},
    {"label": "Power content",  "emp_p": 66.3},
    {"label": "Shopping",       "emp_p": 91.7},
]

raw_sorted = sorted(RAW, key=lambda r: -r["abs_shift"])
corr_sorted = sorted(CORR, key=lambda r: r["emp_p"])

fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))

labels_a = [r["label"] for r in raw_sorted]
shifts_a = [r["abs_shift"] for r in raw_sorted]
colors_a = ["#c0392b" if r["unstable"] else "#34495e" for r in raw_sorted]
y_a = np.arange(len(raw_sorted))[::-1]
axes[0].barh(y_a, shifts_a, color=colors_a)
axes[0].set_yticks(y_a)
axes[0].set_yticklabels(labels_a)
axes[0].set_xlabel("|\u03b2 shift| vs. full-sample H1c estimate")
axes[0].set_title("A. Raw ranking (uncorrected)\nby |\u03b2 shift| \u2014 unstable remaining sample in red", fontsize=10)
axes[0].axvline(0, color="gray", lw=0.8)
for yi, v in zip(y_a, shifts_a):
    axes[0].text(v + 0.006, yi, f"{v:+.3f}", va="center", fontsize=8)

labels_b = [r["label"] for r in corr_sorted]
emp_p = [r["emp_p"] for r in corr_sorted]
colors_b = ["#1e8449" if r["label"] == "Local business" else "#34495e" for r in corr_sorted]
y_b = np.arange(len(corr_sorted))[::-1]
axes[1].barh(y_b, emp_p, color=colors_b)
axes[1].set_yticks(y_b)
axes[1].set_yticklabels(labels_b)
axes[1].set_xlabel("Empirical p (%) \u2014 lower = more anomalous vs. random exclusion")
axes[1].set_title("B. Corrected empirical p (%)\nsame-size random placebo \u2014 local business in green", fontsize=10)
axes[1].axvline(20, color="gray", ls="--", lw=0.8, label="20% reference line")
for yi, v in zip(y_b, emp_p):
    axes[1].text(v + 1.5, yi, f"{v:.1f}%", va="center", fontsize=8)
axes[1].legend(fontsize=8, loc="lower right")

fig.suptitle("RQ2c: Does H1c's null depend on local-business inclusion? [POST-HOC / EXPLORATORY]\n"
             "(formerly labeled \u201cH3\u201d in earlier drafts \u2014 renamed per METHODOLOGY_NOTES.md entry B7)",
             fontsize=10.5, y=1.06)
plt.tight_layout()
plt.savefig("/home/claude/figs/Figure12_corrected.png", dpi=200, bbox_inches="tight", facecolor="white")
print("saved Figure12_corrected.png")
