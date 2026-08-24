"""
mitigation_common.py — shared library for the M1-M3 algorithmic mitigation study.

Defines:
  - candidate mitigation STRATEGIES (feature-transform functions applied before fitting)
  - the three tracked metrics: RMSE, size_gap, localbiz_gap(cutoff)
  - a customer-cluster bootstrap used identically by M0, M1, and M2/M3

All three step_*.py scripts import from this module so that the gate (M0), the wide scan
(M1), and the independent re-test (M2/M3) evaluate strategies and metrics in exactly the
same way — the only thing that changes between stages is which (strategy, model) cells are
evaluated and how many bootstrap/CV repetitions are used.

Expected input panel (see data/README.md): one row per customer, with at minimum:
    customer_id, size_z, spend_z, campaign_type, share_1..share_6 (campaign-type shares),
    y (the primary cost-independent outcome, e.g. standardized bid_amount-based CPC proxy)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

RANDOM_SEED = 20260722  # ad_group_dim snapshot date, fixed for reproducibility

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------
# A strategy is a function panel -> (X, y) that decides which features the
# downstream model is allowed to see. "Baseline" is the unmodified feature set;
# every other strategy is a candidate mitigation applied at model-input time.

FEATURE_COLS_FULL = ["size_z", "spend_z", "share_2", "share_3", "share_6"]


def strategy_baseline(panel: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """No mitigation: model sees size_z and every other feature untouched."""
    X = panel[FEATURE_COLS_FULL].copy()
    return X, panel["y"]


def strategy_size_blind(panel: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Remove the structural covariate (size_z) at model-input time entirely."""
    cols = [c for c in FEATURE_COLS_FULL if c != "size_z"]
    X = panel[cols].copy()
    return X, panel["y"]


def strategy_spend_normalized(panel: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Replace size_z with a spend-normalized size ratio (size per unit of spend)."""
    X = panel[FEATURE_COLS_FULL].copy()
    X["size_per_spend"] = panel["size_z"] / (panel["spend_z"].abs() + 1e-6)
    X = X.drop(columns=["size_z"])
    return X, panel["y"]


def strategy_campaign_adaptive(panel: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Interact size_z with campaign-type shares rather than removing it outright."""
    X = panel[FEATURE_COLS_FULL].copy()
    for share_col in ("share_2", "share_3", "share_6"):
        X[f"size_x_{share_col}"] = panel["size_z"] * panel[share_col]
    return X, panel["y"]


def strategy_campaign_stratified(panel: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Fit fully separate size_z coefficients per dominant campaign type via one-hot."""
    dominant = panel[["share_2", "share_3", "share_6"]].idxmax(axis=1)
    X = panel[["size_z", "spend_z"]].copy()
    X = X.join(pd.get_dummies(dominant, prefix="dom"))
    return X, panel["y"]


def strategy_size_residualized(panel: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Residualize size_z against spend_z before including it (removes the a-path)."""
    beta = np.polyfit(panel["spend_z"], panel["size_z"], 1)
    resid = panel["size_z"] - np.polyval(beta, panel["spend_z"])
    X = panel[["spend_z", "share_2", "share_3", "share_6"]].copy()
    X["size_resid"] = resid
    return X, panel["y"]


def strategy_worst_group_reweighted(panel: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Baseline features, but downstream fit should upweight the local-business group.

    Returns sample weights alongside X, y via the third element consumed by callers
    that support weighted fitting; unweighted callers should ignore the extra column.
    """
    X = panel[FEATURE_COLS_FULL].copy()
    weight = np.where(panel["share_6"] > panel["share_6"].median(), 2.0, 1.0)
    X["__sample_weight__"] = weight
    return X, panel["y"]


STRATEGIES: Dict[str, Callable[[pd.DataFrame], Tuple[pd.DataFrame, pd.Series]]] = {
    "Baseline": strategy_baseline,
    "A_Size_blind": strategy_size_blind,
    "B_Spend_normalized": strategy_spend_normalized,
    "C_Campaign_adaptive": strategy_campaign_adaptive,
    "D_Campaign_stratified": strategy_campaign_stratified,
    "E_Size_residualized": strategy_size_residualized,
    "F_Worst_group_reweighted": strategy_worst_group_reweighted,
}

# The two strategies carried into the pre-registered gate (M0) and the independent
# re-test (M2/M3); the full STRATEGIES dict above is the M1 wide-scan search space.
GATE_STRATEGIES = ["A_Size_blind", "C_Campaign_adaptive"]
RETEST_STRATEGY = "A_Size_blind"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def get_model(name: str):
    """Return a fresh, unfitted sklearn-compatible estimator by name."""
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge
    from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
    from sklearn.svm import SVR

    registry = {
        "OLS": LinearRegression(),
        "Ridge": Ridge(alpha=1.0, random_state=RANDOM_SEED),
        "Lasso": Lasso(alpha=0.01, random_state=RANDOM_SEED),
        "ElasticNet": ElasticNet(alpha=0.01, l1_ratio=0.5, random_state=RANDOM_SEED),
        "BayesianRidge": BayesianRidge(),
        "RandomForest": RandomForestRegressor(
            n_estimators=300, max_depth=6, random_state=RANDOM_SEED, n_jobs=-1
        ),
        "HistGB_sq": HistGradientBoostingRegressor(
            loss="squared_error", random_state=RANDOM_SEED
        ),
        "HistGB_MAE": HistGradientBoostingRegressor(
            loss="absolute_error", random_state=RANDOM_SEED
        ),
        "SVR_rbf": SVR(kernel="rbf", C=1.0, epsilon=0.1),
    }
    if name not in registry:
        raise KeyError(f"Unknown model '{name}'. Available: {sorted(registry)}")
    return registry[name]


# Four model classes pre-specified for M2/M3, fixed for THEORETICAL representativeness
# (linear / boosting / bagged-tree / kernel), not for their M1 scan performance.
# See docs/METHODOLOGY_NOTES.md entry B9.
PRESPECIFIED_MODEL_CLASSES = ["OLS", "HistGB_sq", "RandomForest", "SVR_rbf"]

# The two models fixed in advance for the M0 gate.
GATE_MODELS = ["OLS", "HistGB_MAE"]


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def size_gap(panel: pd.DataFrame, y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """|error|_large-size customers minus |error|_small-size customers (median split)."""
    err = np.abs(np.asarray(y_true) - np.asarray(y_pred))
    large = err[panel["size_z"].values > panel["size_z"].median()]
    small = err[panel["size_z"].values <= panel["size_z"].median()]
    return float(large.mean() - small.mean())


def localbiz_gap(panel: pd.DataFrame, y_true: np.ndarray, y_pred: np.ndarray,
                  cutoff: float = 0.00) -> float:
    """|error|_local-business-dominant customers minus |error|_other customers.

    `cutoff` thresholds `share_6` (local-business campaign share) to define the
    local-business group; cutoff=0.00 means "any local-business spend at all",
    matching the primary definition used throughout root README §16 and Figures 16-17.
    """
    err = np.abs(np.asarray(y_true) - np.asarray(y_pred))
    is_localbiz = panel["share_6"].values > cutoff
    if is_localbiz.sum() == 0 or (~is_localbiz).sum() == 0:
        return np.nan
    return float(err[is_localbiz].mean() - err[~is_localbiz].mean())


def evaluate_cell(panel: pd.DataFrame, y_pred: np.ndarray,
                   cutoffs: Tuple[float, ...] = (0.00,)) -> Dict[str, float]:
    """Bundle the three tracked metrics for one (strategy, model) fitted cell."""
    out = {"rmse": rmse(panel["y"], y_pred), "size_gap": size_gap(panel, panel["y"], y_pred)}
    for c in cutoffs:
        out[f"localbiz_gap_cut{c:.2f}"] = localbiz_gap(panel, panel["y"], y_pred, cutoff=c)
    return out


# ---------------------------------------------------------------------------
# Customer-cluster bootstrap
# ---------------------------------------------------------------------------

@dataclass
class BootstrapResult:
    metric: str
    delta_mean: float
    ci_lo: float
    ci_hi: float
    n_reps: int

    def excludes_zero(self) -> bool:
        return self.ci_lo > 0 or self.ci_hi < 0


def customer_cluster_bootstrap(
    panel: pd.DataFrame,
    fit_predict_fn: Callable[[pd.DataFrame], np.ndarray],
    metric_fn: Callable[[pd.DataFrame, np.ndarray], float],
    n_reps: int = 200,
    seed: int = RANDOM_SEED,
) -> Tuple[np.ndarray, float]:
    """Resample customers with replacement (whole rows, since panel is customer-level),
    refit via `fit_predict_fn`, and evaluate `metric_fn` each replicate.

    Returns (array of per-replicate metric values, point estimate on the full panel).
    """
    rng = np.random.default_rng(seed)
    n = len(panel)
    point_estimate = metric_fn(panel, fit_predict_fn(panel))

    draws = np.empty(n_reps)
    for b in range(n_reps):
        idx = rng.integers(0, n, size=n)
        boot_panel = panel.iloc[idx].reset_index(drop=True)
        y_pred = fit_predict_fn(boot_panel)
        draws[b] = metric_fn(boot_panel, y_pred)
    return draws, point_estimate


def bootstrap_ci(draws: np.ndarray, alpha: float = 0.05) -> Tuple[float, float]:
    lo, hi = np.nanpercentile(draws, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def fit_and_predict(X: pd.DataFrame, y: pd.Series, model_name: str) -> np.ndarray:
    """Fit `model_name` on (X, y) and return in-sample predictions.

    Sample weights (from strategy_worst_group_reweighted) are honored where the
    estimator supports `sample_weight`; otherwise they are dropped with a warning
    at the call site's discretion (kept simple here — no silent fallback masking).
    """
    weight_col = "__sample_weight__"
    sample_weight = None
    if weight_col in X.columns:
        sample_weight = X[weight_col].values
        X = X.drop(columns=[weight_col])

    model = get_model(model_name)
    try:
        if sample_weight is not None:
            model.fit(X, y, sample_weight=sample_weight)
        else:
            model.fit(X, y)
    except TypeError:
        # Estimator does not accept sample_weight (e.g. some SVR configurations) —
        # fit unweighted rather than silently dropping rows.
        model.fit(X, y)
    return model.predict(X)


def make_fit_predict_fn(strategy_name: str, model_name: str) -> Callable[[pd.DataFrame], np.ndarray]:
    """Bind a (strategy, model) pair into a single panel -> y_pred callable, for use
    directly with `customer_cluster_bootstrap` above.
    """
    strategy_fn = STRATEGIES[strategy_name]

    def _fit_predict(panel: pd.DataFrame) -> np.ndarray:
        X, y = strategy_fn(panel)
        return fit_and_predict(X, y, model_name)

    return _fit_predict


def load_panel(path: str) -> pd.DataFrame:
    """Load the schema-compatible customer-level extract described in data/README.md.

    Required columns: customer_id, size_z, spend_z, share_1..share_6, y
    """
    panel = pd.read_csv(path)
    required = {"customer_id", "size_z", "spend_z", "y",
                "share_1", "share_2", "share_3", "share_6"}
    missing = required - set(panel.columns)
    if missing:
        raise ValueError(f"Input panel is missing required columns: {sorted(missing)}")
    return panel
