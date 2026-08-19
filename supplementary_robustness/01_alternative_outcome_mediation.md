# Alternative-Outcome Mediation: Isolating and Replicating the Spend Effect Independently of Cost-Sharing

**Supports:** root README §2.4 (Study 1 stress-testing)

## Why this analysis exists

Study 1's primary outcome family includes cost-per-click (CPC = cost / click). Because spend (the mediating variable of interest) and CPC both contain a cost term, any observed spend → CPC association carries a mechanical component by construction — clicks fixed, more cost necessarily raises CPC. Reporting the raw spend → CPC coefficient as if it were a purely behavioral (bidding-efficiency) relationship would overstate the evidence. This file isolates the mechanical component, then replicates the mediation result on an outcome (`bid_amount`) that does not share a cost term with spend.

## Step 1 — Isolating the mechanical component

A customer-level permutation procedure holds `cost` fixed and reshuffles `click` within each customer (2,000 iterations), reconstructing the CPC outcome from the shuffled click counts under a spend–size regression each time. This produces the distribution of spend → CPC coefficients that would be observed from cost-sharing alone, with no genuine behavioral relationship present.

- **Observed spend → log(CPC) coefficient:** +1.277 (cluster-robust p < .001)
- **Purely mechanical (permuted) null distribution:** mean +1.552, 95% range [+1.544, +1.556]; 100% of permuted draws are themselves "significant" at p<.05

The observed coefficient falls *below* the lower bound of the mechanical null distribution rather than inside or above it. This rules out the concern that the CPC result is entirely an artifact inflated beyond the mechanical baseline; if anything, the true CPC relationship offsets some of the mechanical inflation (consistent with larger advertisers achieving somewhat better bidding efficiency at a given spend level). But because the mechanical component is large and the observed value sits close to the edge of that mechanical distribution, the CPC-based point estimate is not used as a stand-alone quantitative claim anywhere in the main text — it is treated as directionally informative only, and the `bid_amount`-based analysis below is the load-bearing result.

**Lagged replication.** As an additional, structurally distinct check, spend on day *t* is regressed against CPC on day *t*+1 and *t*+7 (customer-grouped, cluster-robust). Same-day cost-sharing cannot explain a lagged relationship. Both lags return significant, same-signed coefficients (t+1: β=+0.538, p<.001; t+7: β=+0.544, p<.001), consistent with a genuine behavioral spend–efficiency relationship coexisting with the mechanical artifact identified above.

## Step 2 — Replication on a cost-independent outcome

`bid_amount` (the advertiser's set bid price at the ad-group level) does not contain a cost or click term, so it carries none of the mechanical relationship isolated in Step 1. The same mediation structure as Study 1's main analysis (size → spend → outcome, controlling for size in the outcome equation) is estimated on customer-level aggregates (n=263).

| Path | Coefficient | p-value |
|---|---|---|
| a-path: size → total spend | +0.537 | < .001 |
| b-path: total spend → bid_amount \| size | +0.150 | .032 |
| c'-path: size → bid_amount \| spend (direct effect) | +0.037 | .634 |
| c-path: size → bid_amount, unconditional (total effect) | +0.117 | .072 |
| Indirect effect (a × b) | +0.081 | — |

- **Bootstrap 95% CI on indirect effect (5,000 customer-level resamples):** [0.008, 0.159] — excludes zero
- **Cluster permutation test on indirect effect (5,000 iterations):** p < .001
- **Direction agreement:** the sign of the spend → efficiency-outcome relationship matches between the CPC-based and bid_amount-based models

**Interpretation.** The direct effect of size on bid_amount, net of spend, is non-significant (p=.634) — the same qualitative conclusion as Study 1's primary result, now replicated on an outcome immune to the cost-sharing artifact identified in Step 1. The indirect (spend-mediated) effect is significant and bootstrap-confirmed. This is the analysis referenced in root README §2.4 as the eighth independent verification method and is the primary evidentiary basis for Study 1's efficiency-outcome conclusion; the CPC-based coefficients reported elsewhere in the pipeline are retained for transparency but are secondary to this result.

A formal omitted-variable-bias sensitivity check (Oster's delta) for the bid_amount b-path is reported in [`03_equivalence_and_sensitivity_notes.md`](03_equivalence_and_sensitivity_notes.md), including an important caveat about when that statistic is and is not interpretable.
