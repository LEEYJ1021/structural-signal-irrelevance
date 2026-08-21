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

This repository's current scope is organized around a confirmatory / post-hoc exploratory
split documented in the root [`README.md`](../README.md):

- **H1 and H2 (confirmatory)** — pre-specified tests of whether advertiser size confers a
  direct algorithmic advantage, net of spend (H1a/H1b/H1c), and whether that relationship
  is uniform across campaign types (H2).
- **RQ2a, RQ2b, RQ2c (post-hoc exploratory)** — three research questions, formulated after
  H2's result was observed, asking respectively where the heterogeneity concentrates
  (RQ2a), why it might arise from local-business campaign serving-structure differences
  (RQ2b), and whether H1's headline conclusion depends on local-business inclusion beyond
  sample-size effects (RQ2c — this question was numbered "H3" in earlier drafts of this
  repository; see `docs/METHODOLOGY_NOTES.md`, entry B7, for why that name was retracted).

None of H1, H2, or RQ2a–RQ2c makes use of, or depends on, the ad-group early-warning
flagging rule described in this stub. If a citation or old link led here expecting
flagging-rule content, it does not exist in this repository's current scope — see the link
above for the original specification, retained for reference in the descoped-study
document.

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
  RQ2c) and for the naming correction in entry B7.
