# Methodology Notes

This document is a narrative log of every point in this repository's analysis pipeline
where an initial modeling choice, framing choice, or diagnostic conclusion was found to be
unreliable, under-argued, or premature — and was subsequently corrected, retracted, or
reframed. It is treated as part of this repository's contribution, not as a section to be
edited out once the design was settled. The reasoning here is what makes both the
Level 1 confirmatory result and the Level 2 exploratory findings trustworthy rather than
merely reported.

Each entry follows the same shape: **what was assumed**, **how it was contradicted**, and
**what changed as a result**. Entries are grouped by which part of the repository they
affect. Nothing in this log alters an underlying computed statistic; every change here is a
change in framing, scope, labeling, or (where explicitly marked) a genuine retraction of an
invalid intermediate analysis.

---

## Part A — Pivots affecting Level 1 (confirmatory H1c)

### A1. An attempt to upgrade the identification tier (RDD/policy-change) was pursued, screened, and reframed — not silently dropped

**Assumed:** because the planned 2SLS strategy could not be completed (uncaught exception in
the first-stage F-statistic), a stronger causal design might be reachable via RDD or
policy-change event studies.

**Contradicted by:** a three-round screen (bandwidth filter → donut-hole robustness →
decisive customer-level re-analysis) found 0/5 RDD candidates and 0/5 policy-change dates
survive. Full detail in `supplementary_identification/SCREENING_SUMMARY.md`.

**Changed:** the repository's positioning was rewritten to describe itself as a **mediation
audit** (README §8) from the outset, under which these screenings are supplementary
robustness checks whose null result is consistent with, not required by, the H1c
conclusion — rather than "failed identification attempts."

`[affects: README §8, §11 Limitation 2]`

### A2. The Conversion/ROAS exclusion was generalized into the P4 boundary condition on SSI

**Assumed:** the exclusion was originally a data-quality note ("the conversion API backfills
inconsistently").

**Contradicted by:** re-examination showed the concern is not incompleteness per se but that
backfill completeness is plausibly *correlated with the independent variable under test*
(size) — which would manufacture a spurious H1c effect as a measurement artifact.

**Changed:** documented as a pre-specified construct-validity safeguard and generalized as
proposition P4 in the SSI boundary-condition framework (README §3.3).

`[affects: README §3.3, §4, §11 Limitation 4]`

### A3. The theoretical framework was extended to name the pattern itself as a construct (SSI)

**Assumed:** stating two competing predictions (statistical discrimination vs. behavioral
meritocracy) was a sufficient theoretical contribution.

**Contradicted by:** external review noted this reads as theory-application rather than
theory-contribution, since the pattern tested (a structural attribute's association
vanishing once a legitimate mediator is held constant) had no name as a standalone,
system-level property in either literature.

**Changed:** README §3.2 formally defines Structural Signal Irrelevance (SSI) and derives
boundary conditions P1–P4 (later P5, see B4 below).

`[affects: README §3.2–3.3]`

### A4. H1c's core model was subjected to an influence diagnostic for the first time, as a confirmatory (not exploratory) check

**Assumed:** influence diagnostics had, in earlier drafts, only been applied to Level 2's
exploratory sub-models (e.g., the local-business interaction term), leaving the primary H1c
model itself unaudited.

**Contradicted by:** a research-wide methodological self-audit flagged this as a procedural
gap — the paper's central claim had never been stress-tested against its own influential
observations.

**Changed:** a customer-level DFBETA diagnostic was run on the H1c core model
(spend_z + size_z, n=228), identifying 15 influential customers. Three **pre-specified**
exclusion rules (thin-observation, low performance-match-rate, both combined) — defined
before any coefficient was inspected — were applied. All four configurations (baseline + 3
rules) returned non-significant p-values (100% consistency). The confirmatory grade for H1c
was explicitly re-evaluated against this evidence and **maintained**.

**Important process note:** in the course of running this diagnostic, a related but
separate DFBETA calculation elsewhere in the pipeline (used on a Level 2 exploratory
sub-model) was found to contain a scale-mismatch bug — see B2 below. That bug did **not**
affect this entry's H1c core-model result, which was computed correctly from the start
using customer-level (not row-level-summed) DFBETA.

`[affects: README §5.2, §11 — new confirmatory-robustness content, not previously present]`

---

## Part B — Pivots affecting Level 2 (post-hoc exploratory analysis)

### B1. The original 2-level evidentiary structure (Level 1 vs. Level 2) was introduced to prevent HARKing after a sustained post-hoc investigation of a single subgroup

**Assumed (implicitly, across a long sequence of analyses):** a sequence of increasingly
elaborate analyses — campaign-type heterogeneity → serving-structure comparison → CPC/bid
relationship comparison → variance-structure comparison → structural-break testing →
leverage decomposition → counterfactual CPC comparison → subgroup-dependence testing
(H3) — could be added to the paper's evidence base incrementally, each new script justified
by the output of the one before it.

**Contradicted by:** external review identified this as the precise shape of an
outcome-driven exploratory spiral — not because any individual step was invalid, but
because the *cumulative rhetorical weight* of ~20 scripts investigating one subgroup
(local-business, originally the *least* significant of three tested interaction terms in
the pre-specified H2 battery, raw p=.099, non-significant under Bonferroni correction) is
disproportionate to what a single non-significant baseline result can support. The review
further noted that even fully disclosed post-hoc analysis, if allowed unlimited scope in
the main narrative, risks reading as a second confirmatory study by sheer volume.

**Changed:** the repository was restructured around an explicit **Level 1 / Level 2**
distinction (README §5–§6), with:
- every Level 2 claim tagged **[POST-HOC / EXPLORATORY]**,
- an explicit disclosure of *when* the guiding research question changed (README §2),
- a research-wide multiplicity audit (README §7) pooling all 25 officially-reported
  p-values across both levels, and
- a policy that Level 2 conclusions never upgrade Level 1's evidence grade, and vice versa.

This did not require discarding any analysis — every script's output is retained, either in
README §6 (summarized) or in `supplementary_localbiz_exploratory/` (full detail) — but it
changed how the cumulative weight of that output is presented and read.

`[affects: README §1, §2, §6, §7, §8, §9; this is the single largest reframing pass in this log]`

### B2. DFBETA threshold scale mismatch in the local-business influence diagnostic

**Assumed:** row-level DFBETA (computed per daily observation, then summed per customer
across ~190 days) could be compared directly against the standard 2/√n threshold, using
n = number of customers.

**Contradicted by:** this compares a customer-level *cumulative* quantity (summed over ~190
correlated daily rows) against a threshold derived for a *single-row-per-unit* regression.
The result — "0/228 customers exceed threshold" — was an artifact of an easy-to-pass
comparison, not evidence of low influence.

**Changed:** re-computed using a customer-level regression (1 customer = 1 row, values
averaged across days) so DFBETA and the 2/√n threshold share the same unit. Result: 6/228
customers exceed the corrected threshold. The leave-k-out re-fit results (which never had a
scale problem, since they simply re-estimate the full model after removing customers) were
unaffected and confirmed: no sign reversal across k=1,3,5,10,15.

`[affects: README §6.3, §6.5; corrects an earlier claim now explicitly retracted]`

### B3. `size_z` and `n_ad_groups_total` were discovered to be the same variable, invalidating an earlier "control" analysis

**Assumed:** an earlier analysis attempted to test whether the association between
advertiser size and performance-data missingness was a "mechanical artifact" of larger
accounts simply having more ad groups, by regressing missingness on both `size_z` and
`log(n_ad_groups_total)` "controlling for" one another.

**Contradicted by:** `size_z` is defined as the standardized log-transform of
`n_ad_groups_total` — i.e., the same variable under two names. The regression accordingly
produced VIF=∞ and a non-converging/uninterpretable logistic fit (coefficients present, but
p-values undefined). The "controlled" analysis was not merely underpowered; it was
structurally meaningless.

**Changed:** the entire "control for ad-group count" line of analysis is retracted. It was
replaced with a **combinatorial null model**: if missingness were purely a function of
"more ad groups → higher chance one is unmatched by chance," a simple independent-binomial
model should fit the observed missingness rate well. It does not (over-dispersion ratio
73×; goodness-of-fit χ²=16,583, df=6, p<.0001), indicating account-level clustering beyond
pure combinatorics — but the cause of that residual clustering remains unidentified.

`[affects: README §6.5, §11 Limitation 7; replaces an invalid analysis rather than merely
correcting one]`

### B4. Serving-structure heterogeneity was generalized into proposition P5 on the SSI boundary-condition framework

**Assumed:** the local-business/keyword-matching structural difference (§6.2) was, at first,
treated purely as a data-quality observation relevant only to the H2 robustness appendix.

**Contradicted by:** on reflection, this fact bears directly on the SSI construct's own
scope condition — the audit design presupposes an auction-based serving mechanism, which
this subgroup structurally lacks.

**Changed:** added as **P5 (mechanism applicability)** to the SSI boundary-condition
framework (README §3.3), explicitly marked as post-hoc — it did not exist prior to Level 2's
findings and is a candidate proposition, not an established one.

`[affects: README §3.3, §10]`

### B5. The local-business mechanism sub-chain was initially over-stated as a "confirmed causal chain" and was retracted

**Assumed (in an earlier internal draft):** because 2 of the 3 tested statistical signatures
(variance heterogeneity, relationship-slope heterogeneity, counterfactual CPC gap) plus the
underlying structural fact (0% keyword matching) were confirmed, and only leverage
heterogeneity was not, the overall verdict was framed as "the causal chain is supported."

**Contradicted by:** external review correctly identified "causal chain... supported" as
language claiming more than 3-of-4 statistically-detected, cross-sectional, non-identified
associations can support — particularly given that these tests were run on sub-clusters
with G≈13–72, below the conventional threshold for cluster-robust SE reliability.

**Changed:** reframed throughout as "3 of 4 tested links show a statistically detectable
pattern; this is reported as partial, mixed support for a mechanism-level explanation — not
as an established causal chain." All instances of "causal chain," "establishes," and
"confirms" in earlier internal drafts describing this analysis were replaced with
"consistent with," "detected pattern," or "does not establish."

`[affects: README §6.3, §6.6; language-only correction, no statistic changed]`

### B6. The leave-one-type-out (H3) ranking reversed after a correction, and both passes are disclosed

**Assumed:** an initial comparison of coefficient shifts across five campaign-type
exclusions could be ranked directly by raw magnitude of shift.

**Contradicted by:** this comparison is unfair across exclusions of very different sizes.
Excluding website customers (202/228, leaving only 26) produces an unstable estimate (95%
CI width 1.62) purely from sample depletion, inflating its apparent rank (1st) relative to
local-business exclusion (72/228 excluded, 156 remaining, CI width 0.71), which had
initially ranked 2nd on raw magnitude — a result that, taken at face value, undermined the
local-business-specific narrative being developed.

**Changed:** a corrected comparison re-ran the random-placebo test separately for each
campaign type's own exclusion size (rather than comparing raw shifts across unequal
exclusions), restricted to campaign types with stable remaining samples. Local-business
exclusion ranked 1st among these (empirical p=1.0% vs. 91.7% and 66.3% for the other two
stable types), reversing the initial ranking.

**Explicit disclosure policy adopted:** both the initial (unfavorable) and corrected
(favorable) results are reported together in README §6.4, with the reason for the
correction stated in the same breath as the result. This entry exists specifically because
reporting only the corrected pass — however statistically justified the correction — would
constitute selective disclosure of a result that initially cut against the paper's emerging
narrative.

`[affects: README §6.4, §11 Limitation 5, §12 transparency log entry 3]`

---

## Part C — Cross-cutting pivot: from single-narrative to explicitly-audited multiplicity

### C1. A research-wide multiplicity audit was added after individual-family corrections were found to be insufficient in aggregate

**Assumed:** each hypothesis family (H1c's 6-cell battery, H2's 3-interaction battery, the
RDD/policy-change 10-candidate screen, H3's subgroup-dependence tests) corrected for
multiple comparisons *within itself*, and this was treated as sufficient.

**Contradicted by:** pooling all 25 officially-reported p-values across the entire research
program into one test family and applying Bonferroni/BH-FDR correction shows that **0/25**
survive Bonferroni and only **3/25** (all from the Level 2 exploratory H3 analysis) survive
the more permissive FDR correction. No individual-family correction had previously surfaced
this aggregate picture.

**Changed:** README §7 was added as a standing, reproducible audit (re-run via
`research_wide_methodological_audit.py`), explicitly positioned as the single most important
evidence-calibration table in the repository — not as a result to be minimized, but as the
mechanism that prevents any Level 2 finding from being read at Level 1's confidence.

`[affects: README §7, §9, §11 Limitation 8]`

---

## Summary of what this log establishes

No underlying statistic reported anywhere in this repository was recomputed by a framing
pass; framing passes (A1, A2, A3, B1, B4, B5, C1) changed only how existing, unchanged
numbers are named, scoped, and weighted. Two entries (B2, B3) are genuine retractions of
invalid intermediate analyses, replaced with corrected or substitute analyses whose
different numbers are the ones now reported. One entry (A4) added a new confirmatory
robustness check that had not previously been run. One entry (B6) discloses a reversal
that occurred during exploratory analysis, reporting both the initial and corrected result
rather than only the latter.

The practice this log is meant to model: every point where a prior choice was found
wanting was logged, not quietly revised — including, and especially, the points where the
correction reversed a result in the direction the emerging narrative favored (B6) or where
an earlier framing had overclaimed (B5). A separate log of pivots specific to the descoped
longitudinal companion study is preserved in `../FUTURE_RESEARCH_STUDY2.md` rather than
here, since that study is not part of this repository's evidence base.
