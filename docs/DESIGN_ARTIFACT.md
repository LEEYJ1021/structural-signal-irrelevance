# Design Artifact: Ad-Group Early Warning Flagging Rule

**This file is a redirect stub.** The full specification, backtest grid, and version
history for this artifact are preserved in
[`../FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md#design-artifact-ad-group-early-warning-flagging-rule).

## Why this moved

The Ad-Group Early Warning Flagging Rule was grounded entirely in a descoped longitudinal
companion study's confirmed within-customer result — an ad group's own early operating
signal predicts its near-term growth, and adding account maturity produces no
within-customer improvement at any tested horizon. That longitudinal study (account
maturity vs. a new ad group's growth trajectory, n=29 customers) was removed from this
repository's evidence base and is reported separately as future work. The design artifact
built on top of it accordingly has no remaining basis in this repository's current scope.

## Not to be confused with

This repository's current scope is organized around a three-tier evidentiary structure
documented in the root [`README.md`](../README.md):

- **H1 and H2 (confirmatory)** — pre-specified tests of whether advertiser size confers a
  direct algorithmic advantage, net of spend (H1a/H1b/H1c), and whether that relationship
  is uniform across campaign types (H2).
- **RQ2a, RQ2b, RQ2c (post-hoc exploratory)** — three research questions, formulated after
  H2's result was observed, asking respectively where the heterogeneity concentrates
  (RQ2a), why it might arise from local-business campaign serving-structure differences
  (RQ2b), and whether H1's headline conclusion depends on local-business inclusion beyond
  sample-size effects (RQ2c — this question was numbered "H3" in earlier drafts of this
  repository; see `docs/METHODOLOGY_NOTES.md`, entry B7, for why that name was retracted).
- **M1, M2, M3 (post-hoc, further exploratory extension)** — a later-added extension
  (root README §16) asking whether the disparity documented by RQ2a–RQ2c can be *reduced*
  by an algorithmic design choice at model-input time, disciplined by a pre-registered gate
  (M0), a disclosed exploratory scan (M1), and an independent, pre-specified-model-class
  re-test (M2/M3). See `docs/METHODOLOGY_NOTES.md`, entries B8 and B9, for why this
  extension's own internal naming was fixed before drafting, rather than corrected
  afterward as RQ2a–RQ2c's naming was. The M-series was later extended to include the
  Campaign-stratified strategy under the same protocol (entries B10/B11) — this extension
  is likewise unrelated to the flagging rule.

None of H1, H2, RQ2a–RQ2c, or M1–M3 makes use of, or depends on, the ad-group
early-warning flagging rule described in this stub. The flagging rule is scoped entirely to
the descoped longitudinal companion study and shares no sample, model, or outcome variable
with any of this repository's current confirmatory or post-hoc claims. If a citation or old
link led here expecting flagging-rule content, it does not exist in this repository's
current scope — see the link above for the original specification, retained for reference
in the descoped-study document.

## Where to find the full artifact

See [`FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md), section "Design Artifact:
Ad-Group Early Warning Flagging Rule," for:

- the full input/output specification and design principles (DP1–DP3),
- the empirical backtest (own-signal precision vs. a random-flagging baseline, 9
  specifications),
- the note on why a naive size/tenure-based comparison is structurally ill-posed, and
- the version history documenting the within-customer-demeaning bug that produced an early,
  incorrect "naive-rule victory" result — logged there in the same disclosure style used
  for the reversal documented in this repository's `docs/METHODOLOGY_NOTES.md` (entry B6,
  RQ2c), the naming correction in entry B7, and the pre-emptive naming discipline applied
  to the M-series in entry B8.
