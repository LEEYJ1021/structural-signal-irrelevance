"""
Figure 1 (corrected, REAL DATA) -- Multilevel variance decomposition.

Every number below is transcribed verbatim from the pipeline log
(step1_variance_decomposition_v4.log, provided by the user), specifically:
  - 30 cluster-bootstrap iterations per outcome (log_cost, ctr_logit),
    each reporting ICC at 4 levels (ad_group, campaign, customer, residual)
  - unconditional ICC (STEP 3) and month-FE-conditional ICC (STEP 3c)
This is the exact data-generating process the original Figure 1 claimed to
visualize -- no values are invented or approximated here.
"""
import matplotlib.pyplot as plt
import numpy as np

LEVELS = ["Ad group", "Campaign", "Customer", "Residual"]
LEVEL_KEYS = ["ad_group_id", "campaign_id", "customer_id", "residual"]

# ---- log_cost: 30 bootstrap iterations (verbatim from log) ----
LOG_COST_BOOT = [
    (0.070, 0.060, 0.039, 0.830), (0.077, 0.060, 0.055, 0.808),
    (0.085, 0.074, 0.059, 0.782), (0.070, 0.076, 0.048, 0.806),
    (0.053, 0.047, 0.035, 0.865), (0.073, 0.058, 0.053, 0.816),
    (0.073, 0.036, 0.063, 0.828), (0.065, 0.052, 0.050, 0.834),
    (0.088, 0.086, 0.048, 0.778), (0.056, 0.068, 0.040, 0.835),
    (0.085, 0.094, 0.069, 0.752), (0.066, 0.039, 0.040, 0.855),
    (0.074, 0.075, 0.053, 0.798), (0.062, 0.049, 0.047, 0.842),
    (0.054, 0.043, 0.052, 0.851), (0.050, 0.067, 0.057, 0.826),
    (0.089, 0.065, 0.063, 0.783), (0.060, 0.071, 0.064, 0.805),
    (0.068, 0.042, 0.047, 0.843), (0.062, 0.059, 0.034, 0.845),
    (0.073, 0.050, 0.037, 0.840), (0.056, 0.055, 0.053, 0.836),
    (0.095, 0.073, 0.066, 0.765), (0.064, 0.055, 0.034, 0.848),
    (0.081, 0.054, 0.050, 0.814), (0.072, 0.064, 0.054, 0.810),
    (0.075, 0.058, 0.047, 0.820), (0.062, 0.057, 0.040, 0.841),
    (0.064, 0.050, 0.042, 0.844), (0.085, 0.062, 0.051, 0.803),
]
LOG_COST_UNCOND = {"ad_group_id": 0.068, "campaign_id": 0.057, "customer_id": 0.050, "residual": 0.825}
LOG_COST_COND   = {"ad_group_id": 0.068, "campaign_id": 0.057, "customer_id": 0.049, "residual": 0.826}
LOG_COST_N = 663044

# ---- ctr_logit: 30 bootstrap iterations (verbatim from log) ----
CTR_BOOT = [
    (0.317, 0.215, 0.233, 0.235), (0.320, 0.239, 0.238, 0.203),
    (0.298, 0.230, 0.238, 0.234), (0.284, 0.202, 0.243, 0.271),
    (0.334, 0.221, 0.157, 0.288), (0.323, 0.174, 0.231, 0.272),
    (0.290, 0.191, 0.236, 0.283), (0.341, 0.191, 0.229, 0.239),
    (0.305, 0.183, 0.231, 0.281), (0.273, 0.192, 0.255, 0.280),
    (0.269, 0.224, 0.185, 0.322), (0.310, 0.236, 0.103, 0.351),
    (0.337, 0.217, 0.159, 0.287), (0.280, 0.195, 0.170, 0.355),
    (0.305, 0.193, 0.234, 0.268), (0.330, 0.232, 0.157, 0.280),
    (0.341, 0.179, 0.225, 0.255), (0.345, 0.218, 0.177, 0.260),
    (0.346, 0.213, 0.223, 0.218), (0.321, 0.306, 0.135, 0.238),
    (0.234, 0.230, 0.256, 0.280), (0.313, 0.212, 0.180, 0.295),
    (0.375, 0.217, 0.153, 0.255), (0.300, 0.188, 0.242, 0.271),
    (0.274, 0.218, 0.250, 0.257), (0.339, 0.224, 0.219, 0.218),
    (0.236, 0.268, 0.157, 0.339), (0.355, 0.168, 0.226, 0.251),
    (0.269, 0.198, 0.211, 0.322), (0.286, 0.192, 0.249, 0.273),
]
CTR_UNCOND = {"ad_group_id": 0.301, "campaign_id": 0.218, "customer_id": 0.200, "residual": 0.281}
CTR_COND   = {"ad_group_id": 0.302, "campaign_id": 0.220, "customer_id": 0.194, "residual": 0.283}
CTR_N = 663021

def plot_panel(ax, boot_rows, uncond, cond, title, n_obs):
    boot_rows = np.array(boot_rows)  # shape (30, 4)
    parts = ax.violinplot([boot_rows[:, i] for i in range(4)],
                           positions=range(1, 5), showmeans=False, showextrema=True, widths=0.7)
    for pc in parts['bodies']:
        pc.set_facecolor("#8fb4d9")
        pc.set_edgecolor("#4c72b0")
        pc.set_alpha(0.7)

    for i, key in enumerate(LEVEL_KEYS):
        ax.scatter(i + 1, uncond[key], marker="D", color="black", s=55, zorder=5,
                   label="Unconditional ICC (point est.)" if i == 0 else None)
        ax.scatter(i + 1, cond[key], marker="s", facecolors="white", edgecolors="black",
                   s=55, zorder=5, label="Month-FE-conditional ICC" if i == 0 else None)

    ax.set_xticks(range(1, 5))
    ax.set_xticklabels(LEVELS, rotation=15, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Intraclass correlation (ICC)")
    ax.set_title(f"{title}\n(n = {n_obs:,} obs.; 30-iteration cluster bootstrap)", fontsize=10.5)
    ax.legend(fontsize=7.5, loc="upper right")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
plot_panel(axes[0], LOG_COST_BOOT, LOG_COST_UNCOND, LOG_COST_COND, "Ad spend (log cost)", LOG_COST_N)
plot_panel(axes[1], CTR_BOOT, CTR_UNCOND, CTR_COND, "Click-through rate (logit)", CTR_N)

fig.suptitle("Figure 1 | Multilevel variance decomposition of advertising performance",
             fontsize=13.5, fontweight="bold", y=1.03)
fig.text(0.5, -0.05,
          "Violin plots show the full 30-iteration cluster-bootstrap sampling distribution at each nested level.\n"
          "Diamonds/squares mark unconditional and month-fixed-effects-conditional point estimates; close agreement\n"
          "between the two indicates the variance structure is not driven by seasonality. All values transcribed\n"
          "verbatim from step1_variance_decomposition_v4.log (no simulated or approximated data).",
          ha="center", fontsize=8, color="dimgray")

plt.tight_layout()
plt.savefig("/home/claude/figs/Figure1_corrected.png", dpi=200, bbox_inches="tight", facecolor="white")
print("saved Figure1_corrected.png")
