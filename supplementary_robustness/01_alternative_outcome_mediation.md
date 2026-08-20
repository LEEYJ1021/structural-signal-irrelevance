# Supplementary Robustness 01 — Alternative-Outcome Mediation

Feeds root [`README.md`](../README.md) §5.4 (methods 7–8) and Figure 7.
Script: [`01_alternative_outcome_mediation.py`](01_alternative_outcome_mediation.py).

---

## 1. Why an alternative outcome is needed

CPC = cost / click, and spend is built from cost, so any spend–CPC
association carries a mechanical component by construction — independent
of any real bidding-efficiency behavior. Any mediation claim resting only
on CPC would be partly an artifact of how the outcome is defined, not
purely a behavioral finding.

## 2. Method 7 — isolating the mechanical component

A customer-level permutation procedure reshuffles `click` within customer
while holding `cost` fixed (2,000 iterations), producing a null
distribution for the spend–log(CPC) coefficient that reflects *only* the
mechanical cost-sharing relationship, with no real click-level signal.

| Statistic | Value |
|---|---|
| Observed spend → log(CPC) coefficient | +1.277 |
| Purely-mechanical null distribution, mean | +1.552 |
| Purely-mechanical null distribution, 95% range | [1.544, 1.556] |
| Observed coefficient vs. null range | below the lower bound |

The observed coefficient falling *below* the mechanical null's lower bound
means the CPC-based estimate is not simply inflated by the artifact — but
it sits close enough to the mechanical distribution that it is treated as
directionally informative rather than a stand-alone quantitative claim.

**Lagged replication** (spend at day *t* → CPC at *t*+1 and *t*+7, immune
to same-day cost-sharing):

| Lag | β | p |
|---|---|---|
| t+1 | +0.538 | < .001 |
| t+7 | +0.544 | < .001 |

Same-signed, significant at both lags — consistent with, though not proof
of, a genuine behavioral relationship coexisting with the mechanical
artifact.

## 3. Method 8 — replication on `bid_amount` (cost-independent)

`bid_amount` (the advertiser's set bid price) shares no cost or click term
with spend, so it carries none of the artifact isolated in method 7.
Re-estimating the full decomposition at the customer level (n = 263):

| Path | Estimate | 95% CI / p |
|---|---|---|
| Indirect (spend-linked) association | +0.081 | bootstrap 95% CI [0.008, 0.159], excludes zero; permutation p < .001 |
| Direct association of size, net of spend | +0.037 | p = .634 |

Same qualitative pattern as the CPC-based model — indirect present, direct
absent — now on an outcome immune to the mechanical artifact. This is the
load-bearing result for H1a/H1b (README §5.4).

## 4. Full path table (also in `docs/RESULTS_SUMMARY.md`)

| Path | CPC-based (secondary) | bid_amount-based (primary) |
|---|---|---|
| H1a (a-path) | +0.537 (p < .001) | +0.537 (p < .001) |
| H1b (b-path) | +1.277 (p < .001) | +0.150 (p = .032) |
| H1c (c′-path) | −0.253 (p = .062) | +0.037 (p = .634) |
| Indirect (a × b) | +0.253 | +0.081 |

## 5. Why this, not the CPC-based estimate, is primary

Wherever the two diverge, the bid_amount-based estimate is treated as the
primary quantitative claim (README §5.4, §11 limitation 2), precisely
because it cannot inherit the mechanical component quantified in §2 above.
