"""
Figure 4 -- churn-prediction benchmark appendix: group-CV AUC per model.

Reads: outputs/_v4_churn_appendix/churn_benchmark.json
       (produced by src/pipeline_v4/step3_churn_appendix_v4.py)
Writes: outputs/figures/figure4_churn_benchmark.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

IN_PATH = Path("outputs/_v4_churn_appendix/churn_benchmark.json")
OUT_PATH = Path("outputs/figures/figure4_churn_benchmark.png")


def main():
    if not IN_PATH.exists():
        raise FileNotFoundError(f"{IN_PATH} not found -- run src/pipeline_v4/step3_churn_appendix_v4.py first")
    results = json.loads(IN_PATH.read_text())

    models = list(results.keys())
    aucs = [results[m]["mean_auc"] for m in models]
    n_folds = [results[m]["n_folds_valid"] for m in models]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(models, aucs, color=["#4C72B0", "#55A868"][: len(models)])
    ax.axhline(0.5, color="black", linestyle="--", linewidth=0.8, label="chance (AUC=0.5)")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Group-CV AUC (customer-grouped folds)")
    ax.set_title("Churn-prediction benchmark (appendix)")
    for bar, n in zip(bars, n_folds):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f"{n} folds",
                ha="center", fontsize=8)
    ax.legend()
    plt.tight_layout()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200)
    print(f"[figure4] wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
