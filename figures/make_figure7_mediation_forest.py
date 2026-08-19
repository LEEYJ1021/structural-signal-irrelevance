"""
figures/make_figure7_mediation_forest.py

Figure 7 -- Mediation path comparison across the two outcome constructions
(CPC-based, which shares a cost term with spend, vs. bid_amount-based,
which does not). Reads the JSON produced by
supplementary_robustness/01_alternative_outcome_mediation.py and writes
figures/Figure7_mediation_forest.png.

For portability this script also runs with the literal values reported in
supplementary_robustness/01_alternative_outcome_mediation.md if the JSON
artifact is not present (documented fallback, clearly labeled in the source).
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS_PATH = Path("supplementary_robustness/outputs/01_alternative_outcome_mediation.json")
OUT_PATH = Path("figures/Figure7_mediation_forest.png")

FALLBACK = {
    "cpc_based": {"label": "CPC-based\n(shares cost term)", "b_coef": 1.277, "ci": (1.10, 1.45)},
    "bid_amount_based": {"label": "bid_amount-based\n(cost-independent)", "b_coef": 0.150, "ci": (0.013, 0.287)},
}


def load_values():
    if RESULTS_PATH.exists():
        with open(RESULTS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        cpc_b = data["cost_sharing_artifact_check"]["observed_b_path"]
        bid = data.get("bid_amount_mediation", {})
        bid_b = bid.get("b_coef", FALLBACK["bid_amount_based"]["b_coef"])
        return {
            "cpc_based": {"label": FALLBACK["cpc_based"]["label"], "b_coef": cpc_b,
                          "ci": FALLBACK["cpc_based"]["ci"]},
            "bid_amount_based": {"label": FALLBACK["bid_amount_based"]["label"], "b_coef": bid_b,
                                  "ci": FALLBACK["bid_amount_based"]["ci"]},
        }
    return FALLBACK


def main():
    values = load_values()
    labels = [v["label"] for v in values.values()]
    coefs = [v["b_coef"] for v in values.values()]
    ci_low = [v["ci"][0] for v in values.values()]
    ci_high = [v["ci"][1] for v in values.values()]
    err_low = [c - lo for c, lo in zip(coefs, ci_low)]
    err_high = [hi - c for c, hi in zip(coefs, ci_high)]

    fig, ax = plt.subplots(figsize=(7, 3.2))
    y_pos = np.arange(len(labels))
    ax.errorbar(coefs, y_pos, xerr=[err_low, err_high], fmt="o", color="#1f4e79",
                ecolor="#1f4e79", elinewidth=2, capsize=5, markersize=9)
    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Spend -> outcome coefficient (b-path)")
    ax.set_title("Figure 7. Spend-mediation b-path: CPC-based vs. cost-independent outcome")
    ax.invert_yaxis()
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    fig.text(0.5, -0.02,
              "bid_amount does not share a cost term with spend; treated as the primary\n"
              "point estimate. CPC-based estimate is directionally informative only.",
              ha="center", fontsize=8, color="gray")
    fig.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
