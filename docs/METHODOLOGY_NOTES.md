# Methodology Notes

This document is a narrative log of every point in the advertiser-size mediation-audit pipeline
(`src/pipeline_v4/`, plus the alternative-identification screening in
`supplementary_identification/`) where an initial modeling choice — or an initial framing
choice — was found to be structurally unreliable or under-argued, and replaced with a more
defensible alternative, and why. It is treated as part of the project's contribution, not as a
section to be edited out once the final design was settled — the reasoning here is what makes
the confirmatory H1c result (and the honest null result in `supplementary_identification/`)
trustworthy rather than merely reported.

Each entry follows the same shape: **what we assumed**, **how the diagnostic (or external
review) contradicted it**, and **what changed as a result**.

Cross-references: the root [`README.md`](../README.md) links directly into specific entries
below wherever it leans on one (mainly §2, §2.5, §3.1, §4.5.9, and §5); the exact statistics
each pivot produced live in [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md).

> **Scope note.** An earlier version of this log also documented a longitudinal cold-start
> analysis (account maturity vs. a new ad group's growth trajectory) and its own methodological
> pivots. That study has been descoped from this paper; its pivot log has moved in full to
> [`../FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md). The entries below are
> renumbered to cover only the pivots that bear on the advertiser-size analysis reported in this
> repository's `README.md`.

---

## 1. An attempt to upgrade the identification tier (RDD / policy-change) was pursued, screened, and abandoned — honestly, not silently

**Assumed:** because the planned 2SLS identification strategy (method 4 in root README §4.5)
could not be completed due to a code-level exception (Transparency Log #2), a stronger causal
design might be reachable by screening two alternative strategies: (a) regression discontinuity
(RDD) on `size` and `total spend`, scanning for an institutionally meaningful cutoff, and (b)
policy-change event-study DiD around a genuine platform policy change, located either from
external knowledge or an automated structural-break scan of the size-CPC relationship. The
initial motivating hypothesis was that a successful alternative identification strategy could
raise the confidence tier of the H1c null result from associational to quasi-causal.

**Contradicted by, in three rounds:**
- **Round 1** (`supplementary_identification/step11_alt_identification_RDD_policy.py`) scanned
  40 candidate RDD cutoffs and found 5 that survived an initial bandwidth-sensitivity filter; a
  parallel CUSUM scan flagged 5 candidate structural-break dates.
- **Round 2** (`step11b_donut_hole_full_scan.py`) ran a fine-grained donut-hole sensitivity scan
  on the 5 RDD candidates: 2 of 5 broke down (lost significance) at a donut fraction as small as
  2%, meaning the estimate depended almost entirely on the handful of observations immediately
  adjacent to the cutoff -- the classic symptom of running-variable manipulation. A naive
  left/right sample-count-ratio flag was also raised for several candidates, but this flag could
  not, by itself, distinguish genuine manipulation from an artifact of the underlying customer x
  day panel: higher-spend customers are active on more days and so contribute more panel rows
  near any spend-based cutoff, independent of any manipulation.
- **Round 3, decisive** (`step11c_customer_level_reanalysis.py`) resolved the Round-2 ambiguity
  by re-running both the density test and the RDD estimate **at the customer level** (one row
  per customer, aggregating the outcome to a per-customer mean), which removes panel-density
  variation entirely. Result: 2 of 5 candidates fail a genuine customer-level density test
  (p<.001, manipulation cannot be ruled out); 2 more lose significance entirely once
  re-estimated at the customer level (the panel-level result was a density artifact, not a real
  discontinuity); the remaining candidate survives density testing but is only marginally
  significant (p=.048), broke down at just 15% donut in Round 2, and has no independent
  institutional justification. On the policy-change side, all 5 event-study DiD coefficients
  were non-significant (p=.16-.58) and indistinguishable from 500 randomly chosen placebo dates
  (permutation p=.23-.76).

**Changed:** the original motivating hypothesis -- that a stronger causal design was reachable --
was rejected by the data. Rather than omit this work or selectively report only the more
favorable-looking Round-1/Round-2 numbers, the full three-round screening process is archived in
`supplementary_identification/` and summarized transparently in root README §4.5.9 and Figure
11. As entry 3 below documents, this entry's *framing* was itself revised in a later pass: the
work is now described as a supplementary robustness screening under the mediation-audit
positioning of README §5, not as a "failed identification strategy" — the underlying statistics
in this entry are unchanged.

`[affects: README §4.5.9, §5, §6, §8 (Limitation 2, 6), Figure 11]`

## 2. The Conversion/ROAS exclusion was documented as a limitation before its construct-validity rationale was made explicit

**Assumed:** early data-preparation notes recorded the decision to exclude conversion and ROAS
variables as an operational fact ("Naver's conversion API backfills inconsistently") without
connecting that fact to the specific identification threat it poses to H1c specifically.

**Contradicted by:** re-examining the decision against the same mechanical-artifact logic already
applied elsewhere in the pipeline (comparable to the CPC-vs-`bid_amount` substitution in root
README §4.5, method 7): the concern is not simply that conversion data is incomplete, but that
**backfill completeness is plausibly correlated with the independent variable under test**
(`size`) -- larger or more established advertisers are plausibly more likely to have a fully
integrated, low-latency conversion pipeline. If true, this would mean any conversion- or
ROAS-based outcome could manufacture a spurious H1c effect as a measurement artifact of
differential data completeness, rather than reflecting a genuine algorithmic effect. This is a
stronger and more specific claim than "the data is incomplete," and it was not stated this
precisely in the original limitation note.

**Changed:** the exclusion is now documented in root README §3.1 as a pre-specified
construct-validity safeguard, explicitly parallel to the CPC/`bid_amount` logic in §4.5 method
7, rather than solely as a data-quality limitation. As entry 3 below documents, this reasoning
was later generalized: §3.1's exclusion is now cited as the concrete empirical instance of a
named, general boundary condition on the SSI construct (root README §2.5.3, proposition P4:
measurability), rather than standing as a platform-specific caveat alone. The original
limitation-table entry is retained (root README §8, item 5) but now points back to §3.1 and
§2.5.3 for the full argument.

`[affects: README §3.1, §2.5.3 (P4), §4.5 (cross-reference), §8 (Limitation 5); RESULTS_SUMMARY.md data-exclusion audit]`

## 3. The theoretical framework named two competing accounts but never named the pattern itself as a construct

**Assumed:** the original theoretical framework (root README §2, prior version) was judged
sufficient by stating two competing, falsifiable predictions (statistical discrimination vs.
behavioral meritocracy) and testing which one the data supported. This was treated as a complete
theoretical contribution.

**Contradicted by:** external review of a draft summary of this repository noted that framing
the contribution as "we tested two existing theories against each other" reads, to a reviewer,
as an *application* of prior theory rather than a *contribution to* theory — even though the null
pattern tested here (a structural attribute's association with an algorithmic outcome vanishing
once a legitimate behavioral mediator is held constant) does not yet have a name in either the
statistical-discrimination or the algorithmic-fairness literature as a standalone,
system-level property. Re-reading Dwork et al. (2012) and the broader algorithmic-fairness
literature confirmed that "individual fairness" is a *normative benchmark*, not a *descriptive
construct restricted to the structural-vs-behavioral attribute axis* — meaning the pattern this
repository tests is adjacent to, but not identical with, any single named construct already in
use.

**Changed:** root README §2.5 was added, formally defining **structural signal irrelevance
(SSI)** as Y ⊥ S | (B, X), explicitly distinguishing it from statistical discrimination
(decision-maker-side account), individual fairness (normative benchmark), and generic mediation
analysis (single-coefficient result vs. a claim requiring convergence across many independent
robustness methods, and ideally across independent samples/time axes). Four falsifiable
boundary-condition propositions (P1–P4, §2.5.3) were derived from the platform-governance
literature already cited in §2.3, and a four-item research agenda (§2.5.4) was added so the
construct generates testable follow-up work rather than standing as a label alone — including an
explicit pointer to the planned longitudinal replication now described in
[`../FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md). Existing empirical results were
**not re-analyzed**; §2.5 only reframes how the existing H1c null result (unchanged) is named
and situated in the literature. Every downstream reference to "the pattern" in §4.4, §4.8, §6,
and §7 was updated to cite §2.5 where appropriate, and the H2 exception (§4.6) and the
Conversion/ROAS exclusion (§3.1) were each explicitly mapped onto one of the P1–P4 propositions
as concrete empirical instances, which they had not previously been connected to.

`[affects: README §2.5 (new), §4.4, §4.8, §6, §7, §3.1 (cross-ref to P4); RESULTS_SUMMARY.md §0, evidence-summary table]`

## 4. The repository's identification attempts were framed as failures of a causal-inference goal, rather than as a bounded feature of an audit design

**Assumed:** root README §5 (prior version, "Associational-Language Statement") described the
2SLS, RDD, and policy-change screenings as identification *attempts* that did not reach a usable
design, and used hedging language ("did not reach a usable causal design," reported "openly
rather than folded into the confirmatory evidence") to manage the resulting gap between what was
attempted and what was achieved.

**Contradicted by:** external review observed that this framing implicitly concedes the
repository's goal *was* causal identification and that the goal was not met — which invites the
natural follow-up question "why should a reader trust a study whose primary identification
strategy failed twice?" This is an accurate description of the attempts but an inaccurate
description of the study's actual design goal: at no point was platform access available to run
a sock-puppet or field-experimental audit (the design that *would* support causal claims), so
2SLS/RDD/policy-change were never load-bearing for the core H1c conclusion — they were always
supplementary probes of whether a stronger tier was reachable, run and reported honestly
regardless of outcome (as entry 1 above already documents at the statistical level).

**Changed:** root README §5 was rewritten as "Methodological Positioning — This Study as a
Mediation Audit," explicitly situating the repository's design within the algorithm-audit
literature (Sandvig et al., 2014; Metaxa et al., 2021; Raji et al., 2020) as a **mediation
audit** — a third audit type, alongside correlation audits and sock-puppet audits, appropriate
when platform access for controlled intervention is unavailable. Under this framing, the
2SLS/RDD/policy-change screenings (§4.5 method 4, §4.5.9) are now explicitly labeled
"supplementary robustness only," and every "failed" / "did not succeed" phrasing describing them
elsewhere in the repository (§4.5.9's heading, §6's Figure 11 caption, §8 Limitation 2, the
transparency log) was revised to "supplementary robustness screening whose null result is
consistent with, but not required by, the mediation-audit conclusion." No statistical result
changed; entry 1 above remains the authoritative record of what was run and what it found. This
revision also gave §2.5.4's research agenda item 4 (a portable SSI audit protocol) a clear
methodological home to be proposed from.

`[affects: README §5 (rewritten), §4.5.9 (heading + framing), §6 (Figure 11 caption), §8 (Limitation 2), §9 (log entry 7); supplementary_identification/SCREENING_SUMMARY.md (framing pass)]`

---

## Summary of what changed in this revision pass (entries 1–4)

No underlying statistic reported anywhere in this repository (H1a/b/c, H2, or the RDD/
policy-change screening numbers) was recomputed or altered by this revision pass. What changed
is: (1) the pattern these statistics jointly demonstrate now has a name and a formal definition
(SSI, §2.5); and (2) the repository's relationship to causal identification is now stated as a
design choice from the outset (mediation audit, §5) rather than as a series of attempts that
fell short of an implied goal. These are documentation and framing changes made in response to
external review, consistent with this repository's stated practice (README preamble) of logging
every point where a prior choice was found wanting and revised, honestly, rather than quietly.

A further round of pivots — specific to the descoped longitudinal study (account maturity, cold-
start reframing, small-sample power/Bayes-factor treatment, and the design-artifact backtest) —
is preserved in full in [`../FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md) rather
than in this file, since that study is no longer part of this manuscript's evidence base.
