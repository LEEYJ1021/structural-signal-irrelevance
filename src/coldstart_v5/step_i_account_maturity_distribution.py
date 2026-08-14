"""
Step I -- Extend Step H's top-10 profiling to the entire cold-start sample:
what share of ad groups actually come from a genuinely *new* account
(customer's own first-ever ad group), versus an established account adding
one more ad group?

Two metrics, computed per ad group:
  coldstart_ratio    = customer's coldstart_count / customer's all_time_count
  account_age_days   = this ad group's regTm minus the customer's earliest
                        observed regTm (a lower bound -- see the snapshot
                        caveat in data/README.md)

A joint threshold (coldstart_ratio >= 0.8 AND account_age_days <= 30) flags
"genuinely new account" ad groups. Historical finding: essentially 0% of the
trajectory-usable sample met this bar (median account_age_days ~7.8 years),
which is why this project frames "cold start" as *item*-level (new ad group
in an established account), not *user*-level (new advertiser onboarding).
"""
from __future__ import annotations

from src.coldstart_v5.step_a_period_and_spike_check import run as step_a
from src.coldstart_v5._sample_construction import apply_maturity_metrics
from src.utils.io import load_config


def run(cfg: dict):
    ctx = step_a(cfg)
    adgroup_dim, coldstart, usable = ctx["adgroup_dim"], ctx["coldstart"], ctx["usable"]

    coldstart_m = apply_maturity_metrics(coldstart, adgroup_dim, coldstart)
    usable_m = apply_maturity_metrics(usable, adgroup_dim, coldstart)

    for label, df in [("all candidates", coldstart_m), ("trajectory-usable", usable_m)]:
        print(f"\n[step_i] {label} (n={len(df)}) coldstart_ratio distribution:\n{df['coldstart_ratio'].describe()}")
        print(f"[step_i] {label} account_age_days distribution:\n{df['account_age_days'].describe()}")

    usable_m["true_new_account_flag"] = (usable_m["coldstart_ratio"] >= 0.8) & (usable_m["account_age_days"] <= 30)
    n_new = usable_m["true_new_account_flag"].sum()
    print(f"\n[step_i] genuinely-new-account ad groups: {n_new} / {len(usable_m)} ({n_new/len(usable_m):.1%})")
    print("[step_i] if this share is near zero, redefine 'cold start' as item-level "
          "(new ad group in an established account) and use account maturity as a "
          "covariate rather than a basis for a stratified 'new advertiser' sample.")
    return coldstart_m, usable_m


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()
    run(load_config(args.config))
