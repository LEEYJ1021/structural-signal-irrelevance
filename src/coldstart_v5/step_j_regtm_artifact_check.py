"""
Step J -- Sanity-check `customer_first_regtm` (used by Step I as "account
age") against a common failure mode: a snapshot/migration date artifact
that would make many accounts look artificially old or artificially
"born on the same day." If a single date accounts for a large share of
`customer_first_regtm` values, the account-age numbers should be reported
as a lower bound only, not a real tenure estimate.
"""
from __future__ import annotations

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.utils.io import load_config


def run(cfg: dict):
    ctx = step_a(cfg)
    adgroup_dim, usable = ctx["adgroup_dim"], ctx["usable"]

    all_customer_first = adgroup_dim.groupby("customer_id")["regTm"].min()
    print(f"[step_j] first-registration month distribution (all {all_customer_first.shape[0]} customers):\n"
          f"{all_customer_first.dt.to_period('M').value_counts().sort_index().head(20)}")

    top_dates = all_customer_first.dt.date.value_counts().head(5)
    top1_share = top_dates.iloc[0] / all_customer_first.shape[0]
    print(f"[step_j] most-frequent single first-registration date: {top_dates.index[0]} "
          f"({top1_share:.1%} of customers)")
    verdict = "snapshot/migration artifact suspected -- treat account age as a lower bound only" \
        if top1_share > 0.05 else "no unusual clustering -- account age estimate appears reliable"
    print(f"[step_j] verdict: {verdict}")
    return top1_share


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
