"""
Step E -- Before committing to a discrete latent-class growth model (GBTM),
check whether the achievable sample size can even recover the true number
of classes. Growth curves are summarized as quadratic-polynomial
coefficients and clustered with a Gaussian mixture as a lightweight proxy
for full GBTM/GMM fitting -- this is a *screening* simulation, not the
production trajectory model.

Historical finding: recovery probability was ~9% at k=2 true classes and
~0% at k=3/4, at the achievable sample size -- which is why this project
does not use a discrete latent-class model anywhere in the confirmatory
analysis (see docs/METHODOLOGY_NOTES.md).
"""
from __future__ import annotations

import numpy as np
from sklearn.mixture import GaussianMixture

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config


def simulate_recovery(n_obs: int, true_k: int, rng, sep: float = 1.5, n_days: int = 14, reps: int = 200) -> float:
    correct = 0
    for _ in range(reps):
        labels = rng.integers(0, true_k, size=n_obs)
        days = np.arange(n_days)
        feats = []
        for lab in labels:
            slope = sep * (lab - (true_k - 1) / 2) + rng.normal(0, 0.5)
            curve = slope * days + rng.normal(0, 1.0, size=n_days)
            feats.append(np.polyfit(days, curve, 2))
        X = np.array(feats)
        bics = [GaussianMixture(n_components=k, random_state=0, n_init=1).fit(X).bic(X)
                for k in range(1, min(true_k + 3, 6))]
        k_hat = int(np.argmin(bics)) + 1
        correct += int(k_hat == true_k)
    return correct / reps


def run(cfg: dict):
    ctx = step_a(cfg)
    n_true = len(ctx["usable"])
    reps = cfg["coldstart_diagnostics"]["n_sim_replications_class_count"]
    rng = np.random.default_rng(cfg["random_seed"])

    results = {}
    for k_test in (2, 3, 4):
        rate = simulate_recovery(n_true, k_test, rng, reps=reps)
        flag = "sufficient" if rate >= 0.7 else "insufficient"
        print(f"[step_e] true classes={k_test}, n={n_true}: BIC recovery rate (approx) = {rate:.0%} -> {flag}")
        results[k_test] = rate
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
