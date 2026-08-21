"""
Figure 3 (corrected) -- Multiverse specification curve and placebo test.

Panel B: EXACT match, transcribed verbatim from step2_advertiser_size_fairness_v4.log:
  - H2a real, distributional (pct_approved KW):      p = 5.598944e-04  (matches image's 0.00056)
  - H2d placebo, distributional (device_type_share):  p = 1.394e-08     (matches image's 1.4e-08)
  - H2b real, spend-controlled (pct_approved):         p = 2.512943e-01 (matches image's 0.25)
  - H2d placebo, spend-controlled:                     p = 0.5521       (matches image's 0.55)
This confirms Panel B is fully reproducible from real pipeline output.

Panel A: the log confirms "48 specifications executed" (16 per outcome x 3
outcomes) with 0/48 reaching significance, and reports per-outcome
aggregate stats (pct_positive_coef, median_coef, median_p_value) -- but
NOT the 48 individual beta values. Rather than fabricate 48 points to
mimic the original scatter, this version plots what the log actually
supports: a per-outcome summary of the same 48-specification run,
explicitly labeled as aggregate (not individual-point) data.
"""
import matplotlib.pyplot as plt
import numpy as np

# ---- Panel A: REAL aggregate stats from H2e log (verbatim) ----
SPEC_SUMMARY = [
    {"outcome": "pct_approved",  "n": 16, "pct_pos": 0.000, "pct_sig": 0.0, "median_coef": -0.001039, "median_p": 0.511955},
    {"outcome": "cpc",           "n": 16, "pct_pos": 0.500, "pct_sig": 0.0, "median_coef":  0.005815, "median_p": 0.678047},
    {"outcome": "mean_ad_rank",  "n": 16, "pct_pos": 0.625, "pct_sig": 0.0, "median_coef":  0.146970, "median_p": 0.574956},
]

# ---- Panel B: REAL, exact p-values from H2a/H2b/H2d log output ----
PANEL_B = [
    {"label": "Real outcome\n(H2a, distributional)",    "p": 5.598944e-04, "hatch": None},
    {"label": "Placebo outcome\n(H2d, distributional)",  "p": 1.394e-08,    "hatch": "//"},
    {"label": "Real outcome\n(H2b, size | spend)",       "p": 2.512943e-01, "hatch": None},
    {"label": "Placebo outcome\n(H2d, size | spend)",    "p": 0.5521,       "hatch": "//"},
]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7.5), gridspec_kw={"height_ratios": [1, 1]})

# --- Panel A ---
x = np.arange(len(SPEC_SUMMARY))
width = 0.35
bars_pos = ax1.bar(x - width/2, [s["pct_pos"] * 100 for s in SPEC_SUMMARY], width,
                    label="% specs with positive coef.", color="#4c72b0")
bars_med = ax1.bar(x + width/2, [abs(s["median_coef"]) * 100 for s in SPEC_SUMMARY], width,
                    label="|median standardized coef.| x100 (scaled for display)", color="#dd8452")
ax1.set_xticks(x)
ax1.set_xticklabels([s["outcome"] for s in SPEC_SUMMARY])
ax1.set_ylabel("value (see legend, two different scales)")
ax1.set_title("A. Specification curve summary: 48 analytic choices (16/outcome x 3 outcomes),\n"
              "0/48 reach significance for any outcome", fontsize=10.5)
ax1.legend(fontsize=7.5, loc="upper left")
for i, s in enumerate(SPEC_SUMMARY):
    ax1.text(i, max(s["pct_pos"]*100, abs(s["median_coef"])*100) + 3,
              f"median p={s['median_p']:.2f}", ha="center", fontsize=7.5, color="#333333")
ax1.text(0.5, 1.14, "NOTE: log reports per-outcome aggregates (16 specs each), not the 48 individual\n"
                     "beta values -- this panel shows the real aggregate stats rather than a fabricated scatter.",
          transform=ax1.transAxes, ha="center", fontsize=7.3, color="#a33", style="italic")

# --- Panel B ---
labels = [r["label"] for r in PANEL_B]
neglogp = [-np.log10(r["p"]) for r in PANEL_B]
colors = ["#4c72b0", "#dd8452", "#4c72b0", "#dd8452"]
bars = ax2.bar(range(len(PANEL_B)), neglogp, color=colors)
for bar, r in zip(bars, PANEL_B):
    if r["hatch"]:
        bar.set_hatch(r["hatch"])
ax2.axhline(-np.log10(0.05), color="black", linestyle="--", linewidth=1, label="alpha = .05 threshold")
ax2.axvspan(1.5, 3.5, color="lightgray", alpha=0.3, zorder=0)
ax2.set_xticks(range(len(PANEL_B)))
ax2.set_xticklabels(labels, fontsize=8.5)
ax2.set_ylabel("-log10(p)")
p_strs = [f"p={r['p']:.2e}" if r["p"] < 0.001 else f"p={r['p']:.2f}" for r in PANEL_B]
for i, (bar, ps) in enumerate(zip(bars, p_strs)):
    ax2.text(i, bar.get_height() + 0.15, ps, ha="center", fontsize=8)
ax2.set_title("B. Distributional (KW) tests are significant for both real and placebo outcomes --\n"
              "the informative comparison is the spend-controlled regression (shaded), where both are null",
              fontsize=10)
ax2.legend(fontsize=8, loc="upper right")
for spine in ("top", "right"):
    ax2.spines[spine].set_visible(False)

fig.suptitle("Figure 3 | Multiverse specification curve and placebo test (RQ2 robustness suite)",
             fontsize=13, fontweight="bold", y=1.02)
fig.text(0.5, -0.02,
          "Panel B values transcribed verbatim from step2_advertiser_size_fairness_v4.log (H2a/H2b/H2d), "
          "confirmed to exact match. Panel A uses real per-outcome aggregate statistics from the same log; "
          "individual 48-point beta values were not separately persisted by the pipeline.",
          ha="center", fontsize=7.8, color="dimgray")

plt.tight_layout()
plt.savefig("/home/claude/figs/Figure3_corrected.png", dpi=200, bbox_inches="tight", facecolor="white")
print("saved Figure3_corrected.png")
