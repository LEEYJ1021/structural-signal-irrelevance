"""
Figure 2 -- forest plot of the advertiser-size effect (beta +/- 95% CI)
across every specification in the fairness multiverse.

Reads: outputs/_v4_fairness/specification_curve.csv
       (produced by src/pipeline_v4/step2_advertiser_size_fairness_v4.py)
Writes: outputs/figures/figure2_fairness_forest_plot.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

IN_PATH = Path("outputs/_v4_fairness/specification_curve.csv")
OUT_PATH = Path("outputs/figures/figure2_fairness_forest_plot.png")


def main():
    if not IN_PATH.exists():
        raise FileNotFoundError(f"{IN_PATH} not found -- run src/pipeline_v4/step2_advertiser_size_fairness_v4.py first")
    df = pd.read_csv(IN_PATH).dropna(subset=["beta", "se"]).reset_index(drop=True)
    df["label"] = df["outcome"] + " | " + df["controls"] + " | " + df["estimator"]
    df["ci_low"] = df["beta"] - 1.96 * df["se"]
    df["ci_high"] = df["beta"] + 1.96 * df["se"]
    df = df.sort_values("beta").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(8, max(3, 0.4 * len(df))))
    y = range(len(df))
    colors = ["#C44E52" if p < 0.05 else "#4C72B0" for p in df["p"]]
    ax.errorbar(df["beta"], y, xerr=[df["beta"] - df["ci_low"], df["ci_high"] - df["beta"]],
                fmt="o", ecolor="gray", capsize=3, color="black", zorder=3)
    for i, c in zip(y, colors):
        ax.scatter(df.loc[i, "beta"], i, color=c, zorder=4)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_yticks(list(y))
    ax.set_yticklabels(df["label"], fontsize=8)
    ax.set_xlabel("Advertiser-size effect (beta, 95% CI)")
    ax.set_title("Fairness specification curve -- advertiser size vs. performance")
    plt.tight_layout()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200)
    print(f"[figure2] wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
