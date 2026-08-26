# ============================================================
# Figure 19: Campaign-stratified (S9) bootstrap results by model class
#            (companion to Figure 16 / M2-M3)
#
#   See root README.md §16.3.1 and docs/METHODOLOGY_NOTES.md entries
#   B10, B11.
#
#   Difference from Figure 16 (disclosed):
#   - The OLS row remains numerically unstable in its right tail even
#     after near-constant-column removal (tail_ratio > 3). For that row
#     only, this figure plots median + IQR instead of mean + 95% CI.
#     Which cells get this treatment is decided upstream, by the
#     `*_right_tail_unstable` flag computed in
#     rq3_confirm_v2_robust_summary_postprocess.py — this script does
#     not choose the display style after the fact to make results look
#     better.
#   - The other three model classes (HistGB, RandomForest, SVR-RBF) are
#     plotted exactly as in Figure 16: mean + 95% percentile CI.
#
#   Inputs (produced upstream, this script does not refit any model):
#     - rq3_confirm_v2_bootstrap_raw_patched.csv
#     - rq3_confirm_v2_robust_summary.csv
#
#   DEMO_MODE: if those two files are not found (e.g. running this
#   outside the researcher's environment, where the underlying ad-
#   platform data is not available), the script falls back to a small
#   synthetic bootstrap sample built to reproduce the *qualitative*
#   pattern already reported in root README §16.3.1 / RESULTS_SUMMARY.md
#   §15-16 (NO_EFFECT on RMSE/size_gap for all four model classes; OLS
#   uniquely shows a median-confirmed worsening of localbiz_gap with an
#   unstable right tail). DEMO_MODE output is for illustrating what the
#   figure looks like only — it is not a re-analysis of real data and
#   must not be cited as a result.
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# CONFIG — adjust these two paths to match your repository layout
# ---------------------------------------------------------------
AD_DATA_DIR = Path("/home/yjlee/Research/Ad_Advance/AD_Data")
OUT_DIR = AD_DATA_DIR.parent
FIGURES_DIR = OUT_DIR.parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

RAW_PATH = OUT_DIR / "rq3_confirm_v2_bootstrap_raw_patched.csv"
ROBUST_SUMMARY_PATH = OUT_DIR / "rq3_confirm_v2_robust_summary.csv"
FIG_PATH = FIGURES_DIR / "Figure19_campaign_stratified_model_class_bootstrap.png"

TARGET_STRATEGY = "S9_Campaign_stratified"
MODEL_ORDER = ["OLS", "HistGB", "RandomForest", "SVR_rbf"]
MODEL_LABELS = {
    "OLS": "OLS\n(linear)",
    "HistGB": "HistGB\n(boosting)",
    "RandomForest": "RandomForest\n(bagging)",
    "SVR_rbf": "SVR-RBF\n(kernel)",
}
METRICS = [
    ("rmse_overall_diff", "ΔRMSE"),
    ("size_gap_diff", "Δsize_gap"),
    ("localbiz_gap_diff", "Δlocalbiz_gap"),
]
TAIL_RATIO_THRESHOLD = 3.0
N_BOOT_DEMO = 200
DEMO_SEED = 42


def build_demo_dataframe():
    """Synthetic stand-in for rq3_confirm_v2_bootstrap_raw_patched.csv,
    calibrated to reproduce the qualitative pattern already reported for
    S9_Campaign_stratified: NO_EFFECT on RMSE/size_gap for all four model
    classes, and a median-confirmed, right-tail-unstable worsening of
    localbiz_gap for OLS only. Values are illustrative, not real data."""
    rng = np.random.RandomState(DEMO_SEED)
    records = []

    # (model, metric_col) -> (center, spread, right_tail_outliers)
    # right_tail_outliers=True adds a handful of extreme draws to mimic
    # the near-constant-column instability disclosed for OLS (entry B11).
    specs = {
        ("OLS", "rmse_overall_diff"):     dict(center=0.02, spread=0.10, unstable=True),
        ("OLS", "size_gap_diff"):         dict(center=0.00, spread=0.15, unstable=True),
        ("OLS", "localbiz_gap_diff"):     dict(center=0.08, spread=0.08, unstable=True, shift_positive=True),
        ("HistGB", "rmse_overall_diff"):  dict(center=0.02, spread=0.10, unstable=False),
        ("HistGB", "size_gap_diff"):      dict(center=-0.05, spread=0.18, unstable=False),
        ("HistGB", "localbiz_gap_diff"):  dict(center=0.05, spread=0.18, unstable=False),
        ("RandomForest", "rmse_overall_diff"): dict(center=0.00, spread=0.12, unstable=False),
        ("RandomForest", "size_gap_diff"):     dict(center=-0.10, spread=0.25, unstable=False),
        ("RandomForest", "localbiz_gap_diff"): dict(center=0.05, spread=0.18, unstable=False),
        ("SVR_rbf", "rmse_overall_diff"): dict(center=0.05, spread=0.15, unstable=False),
        ("SVR_rbf", "size_gap_diff"):     dict(center=-0.05, spread=0.30, unstable=False),
        ("SVR_rbf", "localbiz_gap_diff"): dict(center=0.05, spread=0.20, unstable=False),
    }

    for (model, col), spec in specs.items():
        core = rng.normal(loc=spec["center"], scale=spec["spread"], size=N_BOOT_DEMO)
        if spec.get("shift_positive"):
            core = np.abs(core) + 0.01  # keep the IQR entirely positive (median-confirmed worsening)
        if spec["unstable"]:
            n_outliers = 10
            outlier_idx = rng.choice(N_BOOT_DEMO, size=n_outliers, replace=False)
            core[outlier_idx] = rng.uniform(1.0, 3.8, size=n_outliers)
        for b, v in enumerate(core):
            records.append({"boot": b, "model": model, "strategy": TARGET_STRATEGY, col: v})

    # Pivot the long records (one metric per row) into one row per
    # (boot, model) with all three metric columns, matching the real
    # CSV's wide layout.
    wide = {}
    for r in records:
        key = (r["boot"], r["model"])
        wide.setdefault(key, {"boot": r["boot"], "model": r["model"], "strategy": TARGET_STRATEGY})
        for col, _ in METRICS:
            if col in r:
                wide[key][col] = r[col]
    return pd.DataFrame(list(wide.values()))


def compute_robust_summary(raw_df):
    """Recreates the relevant columns of rq3_confirm_v2_robust_summary.csv
    on the fly, so DEMO_MODE does not depend on a second file."""
    rows = []
    for (strategy, model), g in raw_df.groupby(["strategy", "model"]):
        row = {"strategy": strategy, "model": model}
        for col, prefix in [(c, c.replace("_diff", "")) for c, _ in METRICS]:
            vals = g[col].dropna().values
            if len(vals) == 0:
                continue
            median_val = np.median(vals)
            ci_lo, ci_hi = np.percentile(vals, [2.5, 97.5])
            right_tail = ci_hi - median_val
            left_tail = median_val - ci_lo
            tail_ratio = right_tail / max(left_tail, 1e-9)
            row[f"{prefix}_right_tail_unstable"] = bool(tail_ratio > TAIL_RATIO_THRESHOLD)
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------
# Load real data if available, otherwise fall back to the labeled demo
# ---------------------------------------------------------------
if RAW_PATH.exists() and ROBUST_SUMMARY_PATH.exists():
    raw = pd.read_csv(RAW_PATH)
    robust = pd.read_csv(ROBUST_SUMMARY_PATH)
    demo_mode = False
else:
    print("[DEMO_MODE] Real CSV inputs not found at the configured paths.")
    print("[DEMO_MODE] Rendering an illustrative figure from synthetic data that")
    print("[DEMO_MODE] reproduces the reported pattern only. Do not cite this PNG")
    print("[DEMO_MODE] as a result — rerun with the real CSVs to get the real figure.")
    raw = build_demo_dataframe()
    robust = compute_robust_summary(raw)
    demo_mode = True

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)

for ax, (metric_col, metric_label) in zip(axes, METRICS):
    ys = np.arange(len(MODEL_ORDER))
    for i, model in enumerate(MODEL_ORDER):
        g = raw[(raw.strategy == TARGET_STRATEGY) & (raw.model == model)][metric_col].dropna().values
        r = robust[(robust.strategy == TARGET_STRATEGY) & (robust.model == model)]
        prefix = metric_col.replace("_diff", "")
        is_unstable = bool(r[f"{prefix}_right_tail_unstable"].values[0]) if len(r) else False

        if is_unstable:
            # Right tail remains unstable even after near-constant-column
            # removal — report median/IQR instead of mean/95% CI.
            center = np.median(g)
            lo, hi = np.percentile(g, [25, 75])
            marker, color, label_suffix = "D", "#d95f02", "median [IQR]"
        else:
            center = np.mean(g)
            lo, hi = np.percentile(g, [2.5, 97.5])
            marker, color, label_suffix = "o", "#1b9e77", "mean [95% CI]"

        ax.plot([lo, hi], [ys[i], ys[i]], color=color, lw=2, zorder=1)
        ax.scatter([center], [ys[i]], color=color, marker=marker, s=70, zorder=2)
        ax.text(hi, ys[i] + 0.15, label_suffix, fontsize=7, color=color, ha="left")

    ax.axvline(0, color="gray", lw=1, linestyle="--")
    ax.set_title(metric_label, fontsize=11)
    ax.set_yticks(ys)
    ax.set_yticklabels([MODEL_LABELS[m] for m in MODEL_ORDER], fontsize=9)
    ax.invert_yaxis()  # OLS on top, SVR-RBF on bottom, same flexibility order as Figure 16

title_suffix = "  [DEMO_MODE — illustrative, synthetic data]" if demo_mode else ""
fig.suptitle(
    "Figure 19 — Campaign-stratified (S9) vs Baseline, by model flexibility\n"
    "(OLS shown as median/IQR due to residual numerical instability — see entry B11)"
    + title_suffix,
    fontsize=10,
)
fig.text(
    0.5, 0.01,
    "Orange (◆) = median/IQR (flagged-unstable cells only)  ·  Green (●) = mean/95% CI  ·  "
    "dashed line = 0 (same as Baseline)",
    ha="center", fontsize=8,
)
plt.tight_layout(rect=[0, 0.04, 1, 0.93])
plt.savefig(FIG_PATH, dpi=200)
print(f"Saved: {FIG_PATH}")
