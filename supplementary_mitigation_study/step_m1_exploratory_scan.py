"""
step_m1_exploratory_scan.py -- M1: the exploratory strategy x model scan.

Runs a repeated 5-fold x 30-repetition customer-shuffle cross-validation across up
to 12 candidate strategies x 9 models x 4 local-business cutoffs, pools every
resulting test into one family, and applies Benjamini-Hochberg FDR correction
(root README §16.2; docs/RESULTS_SUMMARY.md §13).

This script is explicitly disclosed as HIGH SELECTION-BIAS RISK: because the search
space is wide, FDR-significant cells are EXPECTED even absent a real effect. No
individual FDR-flagged cell from this script is treated as a finding on its own --
see winner's_curse_check() below and step_m2_m3_model_class_bootstrap.py, which runs
an independent, pre-specified-model-class re-test rather than accepting this scan's
own top candidate at face value (docs/METHODOLOGY_NOTES.md, entry B9).

Usage:
    python supplementary_mitigation_study/step_m1_exploratory_scan.py \
        --input data/customer_panel.csv \
        --output-prefix supplementary_mitigation_study/mitigation_scan \
        --n-repeats 30 --n-folds 5
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mitigation_common import (  # noqa: E402
    RANDOM_SEED,
    STRATEGIES,
    evaluate_cell,
    fit_and_predict,
    localbiz_gap,
)

CUTOFFS = (0.00, 0.25, 0.50, 0.75)
MODELS = [
    "OLS", "Ridge", "Lasso", "ElasticNet", "BayesianRidge",
    "RandomForest", "HistGB_sq", "HistGB_MAE", "SVR_rbf",
]
WINNERS_CURSE_CHECK_MODELS = ["OLS", "HistGB_sq"]  # comparable earlier tooling exists for these two


def repeated_cv_scores(
    panel: pd.DataFrame, strategy_name: str, model_name: str,
    n_repeats: int, n_folds: int, seed: int,
) -> pd.DataFrame:
    """Repeated K-fold customer-shuffle CV. Returns one row of held-out metrics per
    (repeat, fold) so the caller can run a paired Wilcoxon test against Baseline.
    """
    from sklearn.model_selection import KFold

    strategy_fn = STRATEGIES[strategy_name]
    rows = []
    for r in range(n_repeats):
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=seed + r)
        for fold_id, (train_idx, test_idx) in enumerate(kf.split(panel)):
            train_panel = panel.iloc[train_idx].reset_index(drop=True)
            test_panel = panel.iloc[test_idx].reset_index(drop=True)

            X_train, y_train = strategy_fn(train_panel)
            X_test, y_test = strategy_fn(test_panel)
            # align columns between the (potentially different) train/test splits
            X_test = X_test.reindex(columns=X_train.columns, fill_value=0.0)

            weight_col = "__sample_weight__"
            sample_weight = None
            X_train_fit = X_train
            if weight_col in X_train.columns:
                sample_weight = X_train[weight_col].values
                X_train_fit = X_train.drop(columns=[weight_col])
                X_test = X_test.drop(columns=[weight_col])

            from mitigation_common import get_model
            model = get_model(model_name)
            try:
                if sample_weight is not None:
                    model.fit(X_train_fit, y_train, sample_weight=sample_weight)
                else:
                    model.fit(X_train_fit, y_train)
            except TypeError:
                model.fit(X_train_fit, y_train)
            y_pred = model.predict(X_test)

            cell = evaluate_cell(test_panel, y_pred, cutoffs=CUTOFFS)
            cell.update({"repeat": r, "fold": fold_id})
            rows.append(cell)
    return pd.DataFrame(rows)


def run_scan(panel: pd.DataFrame, strategies: list[str], models: list[str],
             n_repeats: int, n_folds: int, seed: int) -> pd.DataFrame:
    """Run repeated CV for every (strategy, model) cell and summarize to one row each."""
    summary_rows = []
    fold_level: dict[tuple[str, str], pd.DataFrame] = {}

    for strategy_name, model_name in product(strategies, models):
        scores = repeated_cv_scores(panel, strategy_name, model_name, n_repeats, n_folds, seed)
        fold_level[(strategy_name, model_name)] = scores
        row = {"strategy": strategy_name, "model": model_name}
        for col in scores.columns:
            if col in ("repeat", "fold"):
                continue
            row[col] = scores[col].mean()
        summary_rows.append(row)
        print(f"[M1 scan] {strategy_name:22s} x {model_name:12s} "
              f"RMSE={row['rmse']:.4f}  size_gap={row['size_gap']:.4f}  "
              f"localbiz_gap_cut0.00={row.get('localbiz_gap_cut0.00', float('nan')):.4f}")

    return pd.DataFrame(summary_rows), fold_level


def statistical_test_table(fold_level: dict, strategies: list[str], models: list[str]) -> pd.DataFrame:
    """Paired Wilcoxon signed-rank test of each (strategy, model) cell's per-fold
    localbiz_gap against Baseline's per-fold localbiz_gap on the SAME model, then
    Benjamini-Hochberg FDR correction across every test in this table.
    """
    metric_col = "localbiz_gap_cut0.00"
    tests = []
    for strategy_name, model_name in product(strategies, models):
        if strategy_name == "Baseline":
            continue
        strat_scores = fold_level[(strategy_name, model_name)][metric_col].values
        base_scores = fold_level[("Baseline", model_name)][metric_col].values
        n = min(len(strat_scores), len(base_scores))
        try:
            stat, p = stats.wilcoxon(strat_scores[:n], base_scores[:n])
        except ValueError:
            stat, p = np.nan, 1.0
        tests.append({
            "strategy": strategy_name, "model": model_name,
            "wilcoxon_stat": stat, "p_value": p,
        })
    test_df = pd.DataFrame(tests)

    # Benjamini-Hochberg FDR across every test in this scan
    m = len(test_df)
    order = test_df["p_value"].argsort()
    ranked = test_df.iloc[order].reset_index(drop=True)
    ranked["rank"] = np.arange(1, m + 1)
    ranked["bh_threshold"] = ranked["rank"] / m * 0.05
    ranked["fdr_significant"] = ranked["p_value"] <= ranked["bh_threshold"]
    # standard BH: once sorted, find largest k with p_(k) <= (k/m)*alpha; everything
    # up to that k is flagged significant
    sig_mask = ranked["fdr_significant"].values
    if sig_mask.any():
        last_true = np.where(sig_mask)[0].max()
        sig_mask[: last_true + 1] = True
    ranked["fdr_significant"] = sig_mask
    return ranked


def winners_curse_check(panel: pd.DataFrame, fdr_table: pd.DataFrame,
                         n_reps: int, seed: int) -> pd.DataFrame:
    """Independent customer-cluster bootstrap on the FDR-flagged candidates,
    restricted to the models with comparable earlier tooling (OLS, HistGB_sq).
    See docs/METHODOLOGY_NOTES.md entry B9.
    """
    from mitigation_common import customer_cluster_bootstrap, bootstrap_ci, make_fit_predict_fn

    candidates = fdr_table[
        (fdr_table["fdr_significant"]) & (fdr_table["model"].isin(WINNERS_CURSE_CHECK_MODELS))
    ]
    rows = []
    for _, r in candidates.iterrows():
        strategy_name, model_name = r["strategy"], r["model"]
        strat_fp = make_fit_predict_fn(strategy_name, model_name)
        base_fp = make_fit_predict_fn("Baseline", model_name)

        rng = np.random.default_rng(seed)
        n = len(panel)
        draws = np.empty(n_reps)
        for b in range(n_reps):
            idx = rng.integers(0, n, size=n)
            boot_panel = panel.iloc[idx].reset_index(drop=True)
            strat_gap = localbiz_gap(boot_panel, boot_panel["y"], strat_fp(boot_panel), cutoff=0.00)
            base_gap = localbiz_gap(boot_panel, boot_panel["y"], base_fp(boot_panel), cutoff=0.00)
            draws[b] = strat_gap - base_gap
        ci_lo, ci_hi = bootstrap_ci(draws)
        confirmed = ci_hi < 0  # negative gap_diff = improvement (smaller local-biz gap)
        reversed_ = ci_lo > 0
        rows.append({
            "strategy": strategy_name, "model": model_name,
            "gap_diff_ci_lo": ci_lo, "gap_diff_ci_hi": ci_hi,
            "confirmed_improvement": confirmed, "reversed_vs_scan": reversed_,
        })
        print(f"[M1 winner's-curse check] {strategy_name} x {model_name}: "
              f"95% CI=[{ci_lo:+.4f}, {ci_hi:+.4f}]  "
              f"confirmed={confirmed}  reversed={reversed_}")
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="M1 exploratory strategy x model scan.")
    parser.add_argument("--input", default="data/customer_panel.csv")
    parser.add_argument("--output-prefix", default="supplementary_mitigation_study/mitigation_scan")
    parser.add_argument("--n-repeats", type=int, default=30)
    parser.add_argument("--n-folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--n-boot-reps", type=int, default=200,
                         help="Bootstrap reps for the winner's-curse check.")
    args = parser.parse_args()

    from mitigation_common import load_panel
    panel = load_panel(args.input)

    strategies = list(STRATEGIES.keys())
    summary, fold_level = run_scan(panel, strategies, MODELS, args.n_repeats, args.n_folds, args.seed)
    fdr_table = statistical_test_table(fold_level, strategies, MODELS)
    curse_check = winners_curse_check(panel, fdr_table, n_reps=args.n_boot_reps, seed=args.seed)

    out_prefix = Path(args.output_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(f"{args.output_prefix}_strategy_summary.csv", index=False)
    fdr_table.to_csv(f"{args.output_prefix}_stattest_fdr.csv", index=False)
    curse_check.to_csv(f"{args.output_prefix}_winners_curse_check.csv", index=False)

    report = {
        "n_customers": len(panel),
        "n_strategies": len(strategies),
        "n_models": len(MODELS),
        "n_cutoffs": len(CUTOFFS),
        "total_tests": len(fdr_table),
        "fdr_significant_tests": int(fdr_table["fdr_significant"].sum()),
        "winners_curse_check_models": WINNERS_CURSE_CHECK_MODELS,
        "winners_curse_confirmed": int(curse_check["confirmed_improvement"].sum()) if len(curse_check) else 0,
        "winners_curse_reversed": int(curse_check["reversed_vs_scan"].sum()) if len(curse_check) else 0,
        "verdict": (
            "This scan is retained as a map of the strategy-model landscape (Figure 17) "
            "and a source of candidate hypotheses. No individual FDR-significant cell is "
            "cited as evidence on its own -- see the winner's-curse check above and "
            "step_m2_m3_model_class_bootstrap.py for the independently re-tested result "
            "(root README §16.2-§16.3)."
        ),
    }
    with open(f"{args.output_prefix}_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{report['fdr_significant_tests']}/{report['total_tests']} tests survive FDR correction.")
    print(f"Wrote {args.output_prefix}_strategy_summary.csv, _stattest_fdr.csv, "
          f"_winners_curse_check.csv, _report.json")


if __name__ == "__main__":
    main()
