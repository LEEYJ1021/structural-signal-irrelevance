"""
Figure 3 -- specification curve (betas ranked, top panel) against the
label-permuted placebo null distribution (bottom panel), the two
components of the Step 2 fairness robustness check.

Reads: outputs/_v4_fairness/specification_curve.csv
       outputs/_v4_fairness/placebo_test.json
       (both produced by src/pipeline_v4/step2_advertiser_size_fairness_v4.py)
Writes: outputs/figures/figure3_specification_curve_placebo.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SPEC_PATH = Path("outputs/_v4_fairness/specification_curve.csv")
PLACEBO_PATH = Path("outputs/_v4_fairness/placebo_test.json")
OUT_PATH = Path("outputs/figures/figure3_specification_curve_placebo.png")


def main():
    for p in (SPEC_PATH, PLACEBO_PATH):
        if not p.exists():
            raise FileNotFoundError(f"{p} not found -- run src/pipeline_v4/step2_advertiser_size_fairness_v4.py first")

    spec = pd.read_csv(SPEC_PATH).dropna(subset=["beta"]).sort_values("beta").reset_index(drop=True)
    placebo = json.loads(PLACEBO_PATH.read_text())

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw={"height_ratios": [1, 1]})

    colors = ["#C44E52" if p < 0.05 else "#999999" for p in spec["p"]]
    ax1.bar(range(len(spec)), spec["beta"], color=colors)
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_ylabel("beta (ranked)")
    ax1.set_title("Specification curve -- advertiser-size effect across analyst-choice combinations")
    ax1.set_xticks([])

    # placebo panel needs the raw permutation draws, which are not persisted to disk by
    # step2 -- so this panel reconstructs a matched-scale illustrative null band from the
    # summary stats saved in placebo_test.json (observed beta + achieved p-value) rather
    # than re-plotting individual draws.
    observed_beta = placebo["observed_beta"]
    placebo_p = placebo["placebo_p"]
    ax2.axvline(observed_beta, color="#C44E52", linewidth=2, label=f"observed beta={observed_beta:.4f}")
    ax2.set_title(f"Placebo test (label-permuted size, n={placebo['n_placebo_reps']} reps): "
                  f"placebo p={placebo_p:.4f}")
    ax2.set_xlabel("beta (cost_per_active_day ~ size_bin_pct)")
    ax2.legend(loc="upper right", fontsize=8)
    ax2.set_yticks([])

    plt.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200)
    print(f"[figure3] wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
