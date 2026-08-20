# Alternative-Identification Screening — Summary (RDD & Policy-Change Event Studies)

**Status: both strategies screened and not adopted.** This folder documents a post-hoc attempt to
strengthen the study's causal identification beyond the incomplete 2SLS attempt (root
`README.md` §4.5, method 4). Two strategies were screened — regression discontinuity (RDD) and
policy-change event studies — using the same variable definitions and cluster structure as the
main pipeline (`size_z`, `spend_z`, `log_cpc`, `bid_amount`, `customer_id` clustering).
**Neither produced a causally interpretable result.** Both are reported here in full for
transparency; only a short summary and
[Figure 11](../figures/Figure11_identification_screening.png) are referenced from the main
README.

Scripts (in this folder): `step11_alt_identification_RDD_policy.py` (initial scan),
`step11b_donut_hole_full_scan.py` (bandwidth/donut-hole robustness across all 5 candidates),
`step11c_customer_level_reanalysis.py` (customer-level density test + customer-level RDD
re-estimation — the decisive check).

---

## 1. Why this was attempted

The core mediation result (H1a/H1b/H1c) is associational, not causally identified — the one
identification attempt in the main pipeline (2SLS) could not be completed due to a code-level
exception in the first-stage F-statistic (Transparency Log #2). Two supplementary strategies were
screened to see whether a defensible causal design could raise the confidence tier of the H1c null
result: (1) RDD on `size`/`spend`, screening for institutionally-meaningful discontinuities, and
(2) event-study DiD around auto-detected or known policy-change dates.

Both are exploratory **screening tools**, not completed identification strategies — a cutoff or
date found this way still needs independent institutional confirmation (an actual platform policy
document, a dated announcement) before it could be used as an identification design. See the
caveats embedded in each script's docstring.

## 2. RDD — three rounds of screening, 0/5 candidates survive

| Round | What was done | Result |
|---|---|---|
| Round 1 (`step11`) | Scanned 40 candidate cutoffs (20 each on `log_size`, `log_total_spend`, 20th–80th percentile) with local-linear RDD + McCrary-style density approximation, then bandwidth-sensitivity filtering | 5 candidates survived bandwidth sensitivity |
| Round 2 (`step11b`) | Fine-grained donut-hole scan (0/2/5/8/10/15/20%) on all 5 candidates, on the panel (customer × day) | 2/5 broke down by 2% donut; 2/5 by 15%; 1/5 ("robust") held to 20% but flagged a suspicious left/right sample-count ratio |
| Round 3 (`step11c`, decisive) | Re-ran the density test and RDD **at the customer level** (one row per customer), because the running variables (`log_size`, `log_total_spend`) are customer-level constants and the panel-level left/right imbalance in Round 2 could be a panel-density artifact (customers with more spend simply have more active days, not necessarily more customers) rather than genuine running-variable manipulation | **0/5 candidates survive.** 2 candidates show a genuine customer-level density discontinuity (p<.001 — manipulation cannot be ruled out); 2 candidates' panel-level significance evaporates entirely once aggregated to the customer level (customer-level RDD p=.79, .40); the remaining candidate (`log_size`, cutoff=2.515) survives density testing but only 1 of 5 donut fractions was significant, sits at p=.048, and has no institutional justification for why that particular ad-group count should be a policy threshold |

**Independent reasons this rules out an RDD design here, beyond the numeric results:**
- `log_size` and `log_total_spend` are the X and M variables of the study's own mediation model — scanning cutoffs along the same axis being tested for mediation is not equivalent to finding an institutionally meaningful policy threshold (e.g., a VIP-tier spend cutoff).
- Both running variables are plausibly self-manipulable by an advertiser (creating ad groups, adjusting spend), which is the core assumption sharp RDD requires to rule out.
- No independent institutional documentation (platform tier definitions, published thresholds) was located tying any candidate cutoff to an actual SearchM/Naver policy rule.

**See [Figure 11](../figures/Figure11_identification_screening.png), panel A**, and
`step11c_customer_level_reanalysis.py` output for the full breakdown.

## 3. Policy-change event studies — no discontinuity detected at any candidate date

Two sources of candidate "policy change" dates were used: (a) user-specified known dates (none were
available for this platform/agency relationship) and (b) dates auto-detected via a CUSUM scan of a
30-day rolling estimate of `size_z`'s instantaneous effect on `log_cpc`. The CUSUM scan surfaced 5
candidate dates, spaced roughly 15 days apart across a 2-month window — a pattern more consistent
with a single gradual drift in the coefficient than with 5 discrete breaks.

For each candidate date, an event-study DiD (`log_cpc ~ post * size_high + spend_z`, ±30-day window,
cluster-robust SE) tested whether the size-high/size-low CPC gap shifted at that date:

| Check | Result |
|---|---|
| DiD coefficient significance (5 dates) | All non-significant, p = .16–.58 |
| Pre-trend joint test (parallel-trends check) | Passed for all 5 (uninformative given the DiD itself is null) |
| Permutation test vs. 500 random dates | All 5 dates indistinguishable from a randomly chosen date (permutation p = .23–.76) |

**See [Figure 11](../figures/Figure11_identification_screening.png), panels B–C.**

## 4. How this is used in the main paper

Neither strategy is presented as an adopted identification design. The root `README.md` reports
only the summary verdict (§4.5.9) and links here and to Figure 11 for full detail. Framed correctly,
the **null result itself is informative**: it means the size–CPC relationship does not show a
detectable discontinuity at any auto-scanned threshold or auto-detected policy-change date, which is
directionally consistent with — not contradictory to — the main H1c finding that size has no direct
association with outcomes once spend is controlled for. This is reported as a second, independent
angle of robustness evidence (a time-axis/threshold-axis check) rather than as a causal claim.

`docs/METHODOLOGY_NOTES.md` entry #1 documents the pivot from "attempt a stronger causal design" to
"report the screening honestly as a null robustness check" in the same narrative-log format as the
other methodology pivots in this repository.
