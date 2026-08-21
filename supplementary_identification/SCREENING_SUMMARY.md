# Alternative-Identification Screening — Summary (RDD & Policy-Change Event Studies)

**Status: both strategies screened and not adopted.** This document is supplementary
robustness material for **Level 1** (the confirmatory H1c test in the root
[`README.md`](../README.md) §5). It has no relationship to **Level 2**'s post-hoc
local-business exploration (root README §6); nothing in this document should be read as
bearing on that separate, exploratory line of analysis.

This folder documents a post-hoc attempt to strengthen H1c's causal-identification tier
beyond the incomplete 2SLS attempt. Two strategies were screened — regression discontinuity
(RDD) and policy-change event studies — using the same variable definitions and cluster
structure as the main pipeline (`size_z`, `spend_z`, `log_cpc`, `bid_amount`, `customer_id`
clustering). **Neither produced a causally interpretable result.** Both are reported here in
full for transparency; only a short summary and the corresponding figure are referenced from
the root README.

Scripts (in this folder): `step11_alt_identification_RDD_policy.py` (initial scan),
`step11b_donut_hole_full_scan.py` (bandwidth/donut-hole robustness across all 5 candidates),
`step11c_customer_level_reanalysis.py` (customer-level density test + customer-level RDD
re-estimation — the decisive check).

---

## 1. Why this was attempted

H1c's central result is associational, not causally identified — the one identification
attempt in the main pipeline (2SLS) could not be completed due to a code-level exception in
the first-stage F-statistic. Two supplementary strategies were screened to see whether a
defensible causal design could raise the confidence tier of the H1c null result: (1) RDD on
`size`/`spend`, screening for institutionally-meaningful discontinuities, and (2)
event-study DiD around auto-detected or known policy-change dates.

Both are exploratory **screening tools**, not completed identification strategies — a cutoff
or date found this way still needs independent institutional confirmation before it could be
used as an identification design.

## 2. RDD — three rounds of screening, 0/5 candidates survive

| Round | What was done | Result |
|---|---|---|
| Round 1 | Scanned 40 candidate cutoffs (20 each on `log_size`, `log_total_spend`, 20th–80th percentile) with local-linear RDD + McCrary-style density approximation, then bandwidth-sensitivity filtering | 5 candidates survived bandwidth sensitivity |
| Round 2 | Fine-grained donut-hole scan (0/2/5/8/10/15/20%) on all 5 candidates, on the panel (customer × day) | 2/5 broke down by 2% donut; 2/5 by 15%; 1/5 held to 20% but flagged a suspicious left/right sample-count ratio |
| Round 3 (decisive) | Re-ran the density test and RDD estimate **at the customer level** (one row per customer), because the panel-level left/right imbalance in Round 2 could be a panel-density artifact (customers with more spend are active on more days, independent of any manipulation) rather than genuine running-variable manipulation | **0/5 candidates survive.** 2 fail a genuine customer-level density test (p<.001); 2 lose significance entirely once re-estimated at the customer level; the remaining candidate survives density testing but is only marginally significant (p=.048), broke down at 15% donut, and has no independent institutional justification |

**Independent reasons this rules out an RDD design here, beyond the numeric results:**
- `log_size` and `log_total_spend` are the X and M variables of H1c's own mediation model —
  scanning cutoffs along the same axis being tested for mediation is not equivalent to
  finding an institutionally meaningful policy threshold.
- Both running variables are plausibly self-manipulable by an advertiser.
- No independent institutional documentation ties any candidate cutoff to an actual
  SearchM/Naver policy rule.

| Running var. | Cutoff | Round-1 p | Donut breakdown | Customer-level density p | Customer-level RDD p | Verdict |
|---|---|---|---|---|---|---|
| log_size | 1.386 | .017 | 2% | .90 (pass) | .79 | Panel-level significance is a density artifact — reject |
| log_size | 2.092 | .039 | 2% | .17 (pass) | .40 | Panel-level significance is a density artifact — reject |
| log_size | 2.515 | .0001 | 15% | .15 (pass) | .048 | Marginal, fragile, no institutional cutoff — not adopted |
| log_total_spend | 11.515 | .0485 | 15% | .001 (fail) | .86 | Manipulation suspected — reject |
| log_total_spend | 11.912 | .0003 | 20% (held) | <.0001 (fail) | .21 | Manipulation suspected — reject |

## 3. Policy-change event studies — no discontinuity detected at any candidate date

No independently known policy-change date was available for this platform/agency
relationship, so candidate dates were auto-detected via a CUSUM scan of a 30-day rolling
estimate of `size_z`'s instantaneous effect on `log_cpc`. Five candidate dates emerged,
spaced roughly 15 days apart across a 2-month window — a pattern more consistent with a
single gradual coefficient drift than 5 discrete breaks (logged as a limitation of the
auto-detection approach, not resolved).

| Candidate date | DiD coefficient (post × size-high) | DiD p | Pre-trend test | Permutation p (vs. 500 random dates) |
|---|---|---|---|---|
| 2026-02-03 | +0.021 | .58 | passes (uninformative given null DiD) | .58 |
| 2026-02-18 | −0.014 | .41 | passes | .41 |
| 2026-03-05 | +0.033 | .23 | passes | .23 |
| 2026-03-20 | −0.008 | .58 | passes | .76 |
| 2026-04-04 | +0.019 | .34 | passes | .34 |

All 5 dates non-significant and statistically indistinguishable from a randomly chosen date.

## 4. How this is used in the main paper

Neither strategy is presented as an adopted identification design. Root README §5.3
(supplementary methodological positioning) reports only the summary verdict and links here
for full detail. Under the mediation-audit framing (root README §8), this null result is not
"a causal identification attempt that failed" — it is a supplementary robustness angle whose
null outcome is directionally consistent with, not required by, the Level 1 H1c mediation-
audit result: no detectable discontinuity in the size–CPC relationship at any scanned
threshold or auto-detected date.

`docs/METHODOLOGY_NOTES.md` entry A1 documents the framing pivot from "failed causal
identification attempt" to "supplementary robustness screening" in the same disclosure
format used for every other reframing and correction in this repository — including the
reversals and retractions specific to Level 2's exploratory analysis (entries B2, B3, B5,
B6), which this document is unrelated to but shares a documentation standard with.
