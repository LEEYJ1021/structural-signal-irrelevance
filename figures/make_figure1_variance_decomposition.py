"""
Figure 1 -- variance decomposition of daily ad-group cost across
nested levels (customer -> campaign -> ad group -> device_type
placebo -> residual).

Reads: outputs/_v4_variance_decomposition/variance_decomposition.json
       (produced by src/pipeline_v4/step1_variance_decomposition_v4.py)
Writes: outputs/figures/figure1_variance_decomposition.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

IN_PATH = Path("outputs/_v4_variance_decomposition/variance_decomposition.json")
OUT_PATH = Path("outputs/figures/figure1_variance_decomposition.png")


def main():
    if not IN_PATH.exists():
        raise FileNotFoundError(f"{IN_PATH} not found -- run src/pipeline_v4/step1_variance_decomposition_v4.py first")
    records = json.loads(IN_PATH.read_text())
    levels = [r["level"] for r in records]
    shares = [r.get("variance_share") or 0 for r in records]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = ["#4C72B0"] * (len(levels) - 2) + ["#DD8452", "#999999"]  # highlight device_type placebo + residual
    ax.bar(levels, shares, color=colors[: len(levels)])
    ax.set_ylabel("Share of total variance in daily cost")
    ax.set_title("Variance decomposition of ad-group daily cost")
    ax.set_ylim(0, 1)
    for i, s in enumerate(shares):
        ax.text(i, s + 0.01, f"{s:.1%}", ha="center", fontsize=9)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200)
    print(f"[figure1] wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
