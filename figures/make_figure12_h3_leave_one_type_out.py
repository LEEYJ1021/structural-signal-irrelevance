"""
Figure 12 — H3 leave-one-type-out: uncorrected vs. corrected ranking
[POST-HOC / EXPLORATORY]

Reads:
  supplementary_localbiz_exploratory/detail/h3_subgroup_dependence_report.json
  supplementary_localbiz_exploratory/detail/h3_type_matched_fairness_correction_report.json
Writes:
  figures/Figure12_h3_leave_one_type_out.png

Used in root README §6.4 and §12 (transparency log entry 3).
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font", family="NanumGothic")
matplotlib.rcParams["axes.unicode_minus"] = False

DETAIL = Path(__file__).resolve().parent.parent / "supplementary_localbiz_exploratory" / "detail"

raw = json.load(open(DETAIL / "h3_subgroup_dependence_report.json", encoding="utf-8"))
corr = json.load(open(DETAIL / "h3_type_matched_fairness_correction_report.json", encoding="utf-8"))

raw_rows = raw["sections"]["part4_leave_one_type_out"]
corr_rows = corr["sections"]["part1_type_observed"]
matched_p = corr["sections"]["part2_type_matched_placebo"]

# Panel A: raw ranking by |beta shift| (uncorrected) — unstable (website) flagged
raw_sorted = sorted(raw_rows, key=lambda r: -r["abs_beta_shift"])
labels_a = [r["label"] for r in raw_sorted]
shifts_a = [r["abs_beta_shift"] for r in raw_sorted]
colors_a = ["#c0392b" if l == "웹사이트" else "#34495e" for l in labels_a]

# Panel B: corrected empirical-p ranking, stable types only
stable_keys = [k for k, v in corr_rows.items() if not v["unstable_flag"]]
stable_sorted = sorted(stable_keys, key=lambda k: matched_p[k]["empirical_p_shift_ge_observed"])
labels_b = [corr_rows[k]["label"] for k in stable_sorted]
emp_p = [matched_p[k]["empirical_p_shift_ge_observed"] * 100 for k in stable_sorted]
colors_b = ["#1e8449" if l == "지역소상공인" else "#34495e" for l in labels_b]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))

axes[0].barh(labels_a, shifts_a, color=colors_a)
axes[0].invert_yaxis()
axes[0].set_title("A. Raw ranking (uncorrected)\nby |β shift| — unstable remaining sample in red")
axes[0].set_xlabel("|β shift| vs. full-sample H1c estimate")
axes[0].axvline(0, color="gray", lw=0.8)
for i, v in enumerate(shifts_a):
    axes[0].text(v + 0.005, i, f"{v:+.3f}", va="center", fontsize=8)

axes[1].barh(labels_b, emp_p, color=colors_b)
axes[1].invert_yaxis()
axes[1].set_title("B. Corrected empirical p (%)\nsame-size random placebo — local business in green")
axes[1].set_xlabel("Empirical p (%) — lower = more anomalous vs. random exclusion")
axes[1].axvline(20, color="gray", ls="--", lw=0.8, label="20% reference line")
for i, v in enumerate(emp_p):
    axes[1].text(v + 1, i, f"{v:.1f}%", va="center", fontsize=8)
axes[1].legend(fontsize=8, loc="lower right")

fig.suptitle(
    "H3: Does H1c's null depend on local-business inclusion? [POST-HOC / EXPLORATORY]",
    fontsize=11, y=1.02,
)
plt.tight_layout()
out_path = Path(__file__).resolve().parent / "Figure12_h3_leave_one_type_out.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"saved: {out_path}")
