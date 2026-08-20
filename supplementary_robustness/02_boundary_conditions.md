# Supplementary Robustness 02 — Boundary Conditions

Feeds root [`README.md`](../README.md) §5.5 (H2) and §9a (RQ2). Script:
[`02_boundary_conditions.py`](02_boundary_conditions.py).

---

## 1. `campaign_type` heterogeneity (H2, Figure 8)

`campaign_type` is a platform-defined ad-product code (website / shopping /
brand-new-product / local-business) — not an industry classification (see
[`appendix/exploratory_industry_classification.md`](../appendix/exploratory_industry_classification.md)
for why an industry field was piloted separately and not used here).

Stratifying the spend-controlled CPC model by `campaign_type` and running a
joint Wald test on the size × product-type interaction:

| Product type | n (rows) | n (customers) | c′ (size, net of spend) | 95% CI (approx.) | p |
|---|---|---|---|---|---|
| Website (1) | 11,894 | 184 | −0.279 | [−0.559, 0.001] | .052 |
| Local business (6) | 1,306 | 27 | +0.312 | [0.132, 0.492] | .211* |
| Shopping (2) | 2,161 | 17 | +0.245 | [0.098, 0.392] | .151* |
| **Joint Wald test (size × product-type)** | | | | | **.023** |

*Stratum-level p-values above .05 despite visually tight CIs reflect the
small-sample cluster-robust variance correction at n=27/n=17; the CI column
is an illustrative normal-approximation band for the figure, not the
stratum's own robust SE, which is wider once clustering is accounted for.

**Reading the result.** No individual stratum's coefficient is significant
on its own, but the *joint* interaction test is (p = .023): the degree to
which size shows no residual association varies by ad-product category,
plausibly because different product types route through different
approval pipelines (e.g., shopping campaigns undergo product-feed
validation that standard search campaigns do not). This is H2 rejected —
not H1c overturned.

**Sample-size caveat.** Local-business (n=27) and shopping (n=17) strata
are small; the joint test's significance should be interpreted with this
imbalance in mind (README §11, limitation 8).

## 2. Keyword review-status interaction (RQ2, exploratory)

Only 0.5% of keywords in this dataset carry a non-standard `inspect_status`
code, so this check is under-powered by construction.

| Definition | n (pending-share > 0) | n (all zero) | size × pending interaction p |
|---|---|---|---|
| Under-review only | 22 | 230 | .638 |
| Restricted-approval only | 106 | 146 | .016 |
| Combined | 111 | 141 | .016 |

The combined definition's significance is driven almost entirely by the
restricted-approval component (106 of 111 customers), not by an
independent contribution from the under-review component — one underlying
signal probed three ways, not three independent confirmations.

**A mechanism caveat.** Restricted-approval denotes an *already-resolved*
outcome, not a pending discretionary review — so this result does not
cleanly map onto the "discretionary review as a leakage channel" mechanism
that motivated the check. It is reported here as directionally interesting
and preliminary, not confirmatory (README §9a).

## 3. Cross-platform generalizability statement (README §9b, reproduced for completeness)

The pattern documented in the main report is associated with a property of
the serving architecture — real-time, unit-level auctions with continuous
re-ranking and no persistent account-level scoring layer — not with this
platform's brand specifically. It is expected to plausibly weaken:

- under **mandatory human review** in the approval pipeline;
- in **new categories without established auction liquidity**;
- on platforms whose ranking algorithm **explicitly incorporates account
  tenure or verification status** as a feature.

No claim is made that magnitudes, only direction, generalize.
