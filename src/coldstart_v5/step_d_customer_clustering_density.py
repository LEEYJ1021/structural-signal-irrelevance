"""
Step D -- Quantify how concentrated the cold-start sample is across
customers. High concentration (a small number of customers contributing a
large share of ad groups) is the trigger for mandatory cluster-robust /
permutation inference throughout every downstream test, and for the
leave-one-out sensitivity check in the RQ1 confirmatory analysis
(src/analysis/rq1_growth_curve_test.py).
"""
from __future__ import annotations

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config


def run(cfg: dict):
    ctx = step_a(cfg)
    usable = ctx["usable"]

    per_customer = usable.groupby("customer_id").size().sort_values(ascending=False)
    n_customers = per_customer.shape[0]
    top_n = max(1, int(0.1 * n_customers))
    top_share = per_customer.head(top_n).sum() / len(usable)

    print(f"[step_d] customers in sample: {n_customers} | ad groups: {len(usable)} "
          f"| mean per customer: {len(usable)/n_customers:.2f}")
    print(f"[step_d] distribution:\n{per_customer.describe()}")
    print(f"[step_d] top-10%-of-customers share of sample: {top_share:.1%} -> "
          f"{'clustering material; permutation/cluster-robust inference required' if top_share > 0.3 else 'clustering impact appears limited'}")
    return per_customer, top_share


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
