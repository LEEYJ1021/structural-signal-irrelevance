# Methodology Notes

This document is a narrative log of every point in this repository's analysis pipeline
where an initial modeling choice, framing choice, or naming choice was found to be
unreliable, under-argued, or premature — and was subsequently corrected, retracted, or
reframed. It is treated as part of this repository's contribution, not as a section to be
edited out once the design was settled. The reasoning here is what makes the confirmatory
(H1, H2) results, the post-hoc exploratory (RQ2a–RQ2c) findings, and the further post-hoc
mitigation extension (M1–M3, root README §16) trustworthy rather than merely reported.

Each entry follows the same shape: **what was assumed**, **how it was contradicted**, and
**what changed as a result**. Entries are grouped by which part of the repository they
affect. Nothing in this log alters an underlying computed statistic; every change here is a
change in framing, scope, labeling, or (where explicitly marked) a genuine retraction of an
invalid intermediate analysis.

---

## Part A — Pivots affecting the confirmatory hypotheses (H1, H2)

### A1. An attempt to upgrade the identification tier (RDD/policy-change) was pursued, screened, and reframed — not silently dropped

**Assumed:** because the planned 2SLS strategy could not be completed (uncaught exception
in the first-stage F-statistic), a stronger causal design might be reachable via RDD or
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

**Assumed:** influence diagnostics had, in earlier drafts, only been applied to the
post-hoc exploratory sub-models (e.g., the local-business interaction term), leaving the
primary H1c model itself unaudited.

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
separate DFBETA calculation elsewhere in the pipeline (used on a post-hoc exploratory
sub-model, RQ2b) was found to contain a scale-mismatch bug — see B2 below. That bug did
**not** affect this entry's H1c core-model result, which was computed correctly from the
start using customer-level (not row-level-summed) DFBETA.

`[affects: README §5.3, §11 — new confirmatory-robustness content, not previously present]`

---

## Part B — Pivots affecting the post-hoc exploratory research questions (RQ2a–RQ2c) and the mitigation extension (M1–M3)

### B1. An explicit confirmatory/post-hoc split was introduced to prevent HARKing after a sustained post-hoc investigation of a single subgroup

**Assumed (implicitly, across a long sequence of analyses):** a sequence of increasingly
elaborate analyses — campaign-type heterogeneity → serving-structure comparison → CPC/bid
relationship comparison → variance-structure comparison → structural-break testing →
leverage decomposition → counterfactual CPC comparison → subgroup-dependence testing —
could be added to the paper's evidence base incrementally, each new script justified by
the output of the one before it.

**Contradicted by:** external review identified this as the precise shape of an
outcome-driven exploratory spiral — not because any individual step was invalid, but
because the *cumulative rhetorical weight* of ~20 scripts investigating one subgroup
(local-business, originally the *least* significant of three tested interaction terms in
the pre-specified H2 battery, raw p=.099, non-significant under Bonferroni correction) is
disproportionate to what a single non-significant baseline result can support. The review
further noted that even fully disclosed post-hoc analysis, if allowed unlimited scope in
the main narrative, risks reading as a second confirmatory study by sheer volume.

**Changed:** the repository was restructured around an explicit **confirmatory
(H1, H2) / post-hoc exploratory** distinction (README §5–§6), with:
- every post-hoc claim tagged **[POST-HOC / EXPLORATORY]**,
- an explicit disclosure of *when* the guiding research question changed (README §2),
- a research-wide multiplicity audit (README §7) pooling all 25 officially-reported
  p-values across both tiers, and
- a policy that post-hoc findings never upgrade the confirmatory evidence grade, and vice
  versa.

This did not require discarding any analysis — every script's output is retained, either in
README §6 (summarized) or in `supplementary_localbiz_exploratory/` (full detail) — but it
changed how the cumulative weight of that output is presented and read. (This split was
originally implemented as a two-level "Level 1 / Level 2" structure; see entry B7 below for
a further naming refinement that does not alter this entry's substance. The same discipline
was later extended one tier further for the mitigation study — see B8/B9 below.)

`[affects: README §1, §2, §6, §7, §8, §9; this was the largest reframing pass in this log
until B7]`

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

`[affects: README §6.2.2, §6.2.3 (RQ2b); corrects an earlier claim now explicitly retracted]`

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
replaced with a **combinatorial null model** (RQ2b): if missingness were purely a function
of "more ad groups → higher chance one is unmatched by chance," a simple
independent-binomial model should fit the observed missingness rate well. It does not
(over-dispersion ratio 73×; goodness-of-fit χ²=16,583, df=6, p<.0001), indicating
account-level clustering beyond pure combinatorics — but the cause of that residual
clustering remains unidentified.

`[affects: README §6.2.3, §11 Limitation 7; replaces an invalid analysis rather than merely
correcting one]`

### B4. Serving-structure heterogeneity was generalized into proposition P5 on the SSI boundary-condition framework

**Assumed:** the local-business/keyword-matching structural difference (§6.2.1) was, at
first, treated purely as a data-quality observation relevant only to the H2 robustness
appendix.

**Contradicted by:** on reflection, this fact bears directly on the SSI construct's own
scope condition — the audit design presupposes an auction-based serving mechanism, which
this subgroup structurally lacks.

**Changed:** added as **P5 (mechanism applicability)** to the SSI boundary-condition
framework (README §3.3), explicitly marked as post-hoc — it did not exist prior to RQ2b's
findings and is a candidate proposition, not an established one. (README §16.5 later
proposes a still more tentative extension of P5, connecting it to predictive-model
flexibility, without elevating it to a numbered boundary condition.)

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

`[affects: README §6.2.2, §6.4 (RQ2b); language-only correction, no statistic changed]`

### B6. The leave-one-type-out sensitivity ranking reversed after a correction, and both passes are disclosed

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
(favorable) results are reported together in README §6.3 (RQ2c), with the reason for the
correction stated in the same breath as the result. This entry exists specifically because
reporting only the corrected pass — however statistically justified the correction — would
constitute selective disclosure of a result that initially cut against the paper's emerging
narrative.

`[affects: README §6.3, §11 Limitation 5, §12 transparency log entry 3]`

### B7. "H3" was retracted as a name; the post-hoc investigation is now three named research questions (RQ2a, RQ2b, RQ2c)

**Assumed:** once the confirmatory/post-hoc split was in place (B1) and every post-hoc
claim carried a **[POST-HOC / EXPLORATORY]** tag, it was defensible to keep numbering the
post-hoc investigation into H2's heterogeneity as a single "H3" — reasoning that the
evidence-tag, not the name, was doing the work of preventing HARKing, and that "H3" simply
preserved narrative continuity with H1 and H2.

**Contradicted by:** external review noted that the word "hypothesis" carries a
pre-registration connotation independent of whatever tag is attached to it. Numbering a
post-hoc question "H3" alongside pre-specified "H1" and "H2" — even fully disclosed as
post-hoc in prose — risks giving a skimming reader the impression that all three were set
out in advance, which is precisely the appearance the confirmatory/post-hoc split (B1) was
built to prevent. The review also noted that "H3" had been asked to do three different
jobs at once — locate the heterogeneity, explain it, and test whether it mattered for
H1's conclusion — which are three different kinds of claims with three different
evidentiary bars, collapsed into one label.

**Changed:** the post-hoc investigation is now three explicitly-named **research
questions**, each doing one job:
- **RQ2a** (where): does the heterogeneity found in H2 concentrate in a particular
  campaign type? (continuous-share re-specification)
- **RQ2b** (why): what platform-mechanism pattern is consistent with that concentration?
  (serving-structure comparison, mechanism-signature tests, alternative-explanation audits)
- **RQ2c** (does it matter for H1): does H1's headline null depend on local-business
  inclusion, beyond sample-size effects alone? (leave-one-type-out sensitivity analysis,
  formerly labeled "H3")

No underlying statistic changed. Every number previously reported under "H3" is reported
identically under RQ2c; every number previously reported under the continuous-share
re-specification or the serving-structure/mechanism analyses is reported identically under
RQ2a/RQ2b respectively. Only the name, and the section boundaries separating "where" from
"why" from "does it matter," changed. Some underlying script variable names and one
figure's legend (Figure 12, Figure 14) still read "H3" internally; `README §13` and
`appendix/hypothesis_id_legacy_mapping.md` document the mapping so no reader is misled by
the older label surviving in generated artifacts.

`[affects: README title banner, §1, §2, §6 (renamed and re-split from a single subsection
into 6.1/6.2/6.3), §7, §9, §11 Limitation 11 (new), §12, §13, §14; this was the second
largest reframing pass in this log, after B1, until B8/B9 below]`

### B8. The mitigation-study extension's internal legacy pipeline label was retracted before it ever reached this README, in favor of M1–M3

**Assumed:** the underlying `Ad_Advance` pipeline scripts that produced the algorithmic
mitigation analysis (README §16) internally label this line of work with a legacy
pipeline-stage identifier throughout their filenames and logs. Reusing that identifier
directly in this README would have preserved continuity with the underlying scripts' own
naming.

**Contradicted by:** this repository's own README already uses that same identifier as an
*internal pipeline-stage number* for something entirely unrelated — Figure 4, the
churn-prediction appendix (see the naming note at the top of README, and README §13's
Figure Gallery). Reusing it a second time, for the mitigation study, would recreate exactly
the ambiguity that entry B7 was written to eliminate: a reader encountering that label in
this repository would not be able to tell, from the label alone, whether it referred to the
churn-prediction appendix or the mitigation study, without cross-referencing this log.

**Changed:** the mitigation extension is named **M1 (exploratory scan), M2 (independent
robustness re-test design), M3 (headline model-class pattern)** in this README (§16), never
the legacy pipeline label. No underlying statistic is affected — every number reported
under the underlying pipeline's internal filenames is reported identically under M1/M2/M3
in README §16 and in `supplementary_mitigation_study/` (renamed to the `mitigation_*`
prefix). `appendix/hypothesis_id_legacy_mapping.md` is extended to include this mapping
alongside the existing legacy-label mappings.

`[affects: README title banner, §1, §2, §7, §9, §10, §11 Limitation 14, §12, §13, §14, §16
in full, and the supplementary_mitigation_study/ filenames; this is the third-largest
reframing pass in this log, and the first to be applied before, rather than after, a
section was drafted and circulated]`

### B9. An FDR-flagged candidate from the mitigation exploratory scan was not accepted at face value, given its selection process

**Assumed:** the 108-combination exploratory scan (README §16.2) identifies the
best-performing (strategy, model) combination via Benjamini–Hochberg FDR correction across
728 tests; because FDR correction already guards against false positives from multiple
testing, a combination surviving FDR correction could be reported as the study's headline
mitigation result.

**Contradicted by:** FDR correction controls the *expected proportion* of false discoveries
among all tests that clear the threshold; it does not correct for the fact that the
specific combination being reported was *chosen* because it was the best-looking cell in
that same 108-combination search — a classic winner's-curse / regression-to-the-mean
setup. A direct check confirmed the concern: an independent customer-cluster bootstrap on
two of the FDR-flagged candidates from this scan (OLS and HistGB-squared, the two models
for which comparable earlier tooling existed) found the OLS combination showed **no
effect** (CI included 0) and the HistGB-squared combination was **reversed** (CI entirely
positive, i.e., the gap widened rather than narrowed) — directly contradicting what the FDR
scan's own significance flag implied for these two cells.

**Changed:** rather than reporting the scan's own top FDR-flagged candidate
(Size-blind × SVR-RBF) directly, an independent re-test was designed with model classes
**pre-specified for theoretical representativeness, before re-inspecting which cell had
scored best** (README §16.3): OLS (linear), HistGB (boosting), RandomForest (bagged trees),
SVR-RBF (kernel), each crossed only with Size-blind. This re-test happened to confirm a
positive result for SVR-RBF (and a partial one for RandomForest) — but the point of this
entry is procedural, not that the result validated: the re-test's model-class list was
fixed by theoretical criteria first, and only then were the four bootstraps run, rather
than bootstrapping whichever single cell the 108-combination scan had already flagged as
best. README §16.6 additionally logs, as still-outstanding validation debt, that the full
108-combination distribution has not yet been reported alongside this re-test, and that the
other three candidate strategies from the scan have not received the same treatment.

`[affects: README §16.2, §16.3, §16.6, §11 Limitations 12–15, §12 transparency log entry 9;
this is a process discipline entry — analogous to B1 for RQ2a–RQ2c but applied within a
single, narrower exploratory scan rather than across a whole research-question family]`

### B10. Campaign-stratified (S9) was independently re-tested with the same rigor as M2/M3 — filling an outstanding item from §16.6

**Assumed:** The M2/M3 four-model-class re-test had only been applied to Size-blind,
leaving this as outstanding debt in §16.6.

**Contradicted by:** The comparison requested in advisory feedback was "pooled model vs. a
model that distinguishes campaign type" — this actually corresponds to Campaign-stratified,
not Size-blind. The question M2/M3 had answered and the comparison now being requested
turned out to test two different interventions.

**Changed:** Campaign-stratified was independently re-tested using the same four model
classes and 200-rep bootstrap (§16.3.1). Result: 0/4 combinations showed simultaneous
improvement across all three metrics. For OLS, the local-business gap worsened
significantly on a median basis — suggesting that the same-direction pattern seen for
Size-blind × OLS/HistGB (§16.3) recurs regardless of intervention approach.

`[affects: README §16.3.1 (new), §16.4, §16.5, §16.6, §12, §13, §14]`

### B11. An in-sample prediction bug and OLS numerical instability were discovered and fixed sequentially during the Campaign-stratified re-test

**Assumed:** The initial version of the re-test script used in-sample prediction within
each bootstrap sample (predicting directly on the training data).

**Contradicted by:** This approach differs from M2/M3's OOF methodology, and, particularly
for Campaign-stratified — which splits the sample by group — the overfitting caused by the
resulting sample shrinkage produced an artifact that looked like a "performance
improvement." This showed up in the initial run as an unnatural pattern in which every
model class improved uniformly. After correcting to OOF, a separate problem was found in
which only the two OLS × stratified combinations had CI upper bounds 10–40× wider than
the other combinations — presumed to be caused by the other campaign-share columns within
the local-business subgroup becoming nearly constant, making the OLS design matrix
near-singular.

**Changed:** (1) Fully corrected to OOF cross-validation. (2) Added a safeguard that
removes near-constant columns (based on each fold's training data) from both train and
test sets (removal log: `rq3_confirm_v2_dropped_columns_log_patch.csv`) — this shrank the
CI upper bound from 25 to 3.9. (3) Even so, residual right-tail instability (tail_ratio
7–12×) remained in the two OLS × stratified combinations, so median/IQR is reported
alongside the mean-based 95% CI for these two cells only — explicitly disclosed as a
departure from M2/M3's original reporting convention.

`[affects: README §16.3.1, §16.6, §12, §13, §14 — a methodological incident record; a
procedural-safeguard entry of the same kind as B2 and B9]`

---

## Part C — Cross-cutting pivot: from single-narrative to explicitly-audited multiplicity

### C1. A research-wide multiplicity audit was added after individual-family corrections were found to be insufficient in aggregate

**Assumed:** each hypothesis or research-question family (H1c's 6-cell battery, H2's
3-interaction battery, the RDD/policy-change 10-candidate screen, RQ2c's
subgroup-dependence tests) corrected for multiple comparisons *within itself*, and this was
treated as sufficient.

**Contradicted by:** pooling all 25 officially-reported p-values across the entire research
program into one test family and applying Bonferroni/BH-FDR correction shows that **0/25**
survive Bonferroni and only **3/25** (all from the RQ2c exploratory subgroup-dependence
analysis) survive the more permissive FDR correction. No individual-family correction had
previously surfaced this aggregate picture.

**Changed:** README §7 was added as a standing, reproducible audit (re-run via
`research_wide_methodological_audit.py`), explicitly positioned as the single most important
evidence-calibration table in the repository — not as a result to be minimized, but as the
mechanism that prevents any post-hoc finding from being read at the confirmatory tier's
confidence. **This audit was not extended to pool in the M-series' 728 tests (§16.2)** —
see the note at the top of README §7 explaining why the M-series maintains its own,
separate multiplicity accounting rather than being folded into this table, at least in this
revision.

`[affects: README §7, §9, §11 Limitation 8]`

---

## Summary of what this log establishes

No underlying statistic reported anywhere in this repository was recomputed by a framing
pass; framing passes (A1, A2, A3, B1, B4, B5, B7, B8, C1) changed only how existing,
unchanged numbers are named, scoped, and weighted. Two entries (B2, B3) are genuine
retractions of invalid intermediate analyses, replaced with corrected or substitute
analyses whose different numbers are the ones now reported. One entry (A4) added a new
confirmatory robustness check that had not previously been run. One entry (B6) discloses a
reversal that occurred during exploratory analysis, reporting both the initial and
corrected result rather than only the latter. One entry (B7) retracts the repository's own
earlier naming choice ("H3"), on the grounds that numbering a post-hoc question alongside
pre-specified hypotheses undercuts the very transparency mechanism (B1) the naming was meant
to serve. One entry (B8) applies that same naming discipline pre-emptively to a newly-added
section, before circulation, rather than as a later correction. One entry (B9) documents a
procedural safeguard — an independent, pre-specified re-test — adopted specifically because
an FDR-based selection from a wide exploratory scan was not trusted at face value, and
because that distrust was directly validated by a bootstrap check that reversed two of the
scan's own flagged candidates. Two further entries (B10, B11) extend the same re-test
protocol to a second candidate strategy (Campaign-stratified) and disclose a numerical-
stability issue discovered while doing so, following the same "log it, don't quietly fix
it" discipline established by B2 and B9.

The practice this log is meant to model: every point where a prior choice was found
wanting was logged, not quietly revised — including, and especially, the points where the
correction reversed a result in the direction the emerging narrative favored (B6, B9),
where an earlier framing had overclaimed (B5), or where the repository's own disclosure
apparatus was itself found to be imperfectly built (B7) or was applied proactively to head
off a foreseeable repeat of the same problem in a new section (B8). A separate log of
pivots specific to the descoped longitudinal companion study is preserved in
`../FUTURE_RESEARCH_STUDY2.md` rather than here, since that study is not part of this
repository's evidence base.
