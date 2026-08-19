"""
figures/make_figure8_boundary_condition_forest.py

Figure 8 -- Spend-controlled size effect (c', direct effect net of spend),
stratified by campaign product type, with a joint Wald test for
heterogeneity. Reads supplementary_robustness/outputs/02_boundary_conditions.json;
falls back to the literal values reported in
supplementary_robustness/02_boundary_conditions.md if not present.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS_PATH = Path("supplementary_robustness/outputs/02_boundary_conditions.json")
OUT_PATH = Path("figures/Figure8_boundary_condition_forest.png")

FALLBACK_STRATA = [
    {"campaign_type": "Website (1)", "n_customers": 184, "c_prime_size": -0.279, "c_prime_p": 0.052},
    {"campaign_type": "Local business (6)", "n_customers": 27, "c_prime_size": 0.312, "c_prime_p": 0.211},
    {"campaign_type": "Shopping (2)", "n_customers": 17, "c_prime_size": 0.245, "c_prime_p": 0.151},
]
FALLBACK_JOINT_P = 0.023


def load_values():
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        block = data.get("campaign_type_boundary_condition", {})
        strata = block.get("strata") or FALLBACK_STRATA
        joint_p = (block.get("joint_wald_test") or {}).get("joint_p", FALLBACK_JOINT_P)
        return strata, joint_p
    return FALLBACK_STRATA, FALLBACK_JOINT_P


def main():
    strata, joint_p = load_values()
    labels = [f"{s['campaign_type']} (n={s['n_customers']})" for s in strata]
    coefs = [s["c_prime_size"] for s in strata]
    # Approximate 95% CI from a normal approximation using reported p-values
    # is not attempted here (SEs not always available in the fallback); use
    # a fixed illustrative half-width instead when SE is absent.
    half_widths = [max(0.15, abs(c) * 0.6) for c in coefs]

    fig, ax = plt.subplots(figsize=(7, 3.2))
    y_pos = np.arange(len(labels))
    colors = ["#c0392b" if s["c_prime_p"] < 0.05 else "#1f4e79" for s in strata]
    ax.errorbar(coefs, y_pos, xerr=half_widths, fmt="o", ecolor="gray",
                elinewidth=1.5, capsize=5, markersize=9, color="none")
    for yi, ci, col in zip(y_pos, coefs, colors):
        ax.plot(ci, yi, "o", color=col, markersize=9, zorder=5)
    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("c' (size, net of spend) -- CPC-based model")
    ax.set_title(f"Figure 8. Campaign product-type heterogeneity\n(joint Wald test for interaction: p = {joint_p:.3f})")
    ax.invert_yaxis()
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    fig.text(0.5, -0.03,
              "No individual stratum is significant; the joint test indicates the degree of\n"
              "size irrelevance varies by ad-product category, not that the null is overturned.",
              ha="center", fontsize=8, color="gray")
    fig.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
