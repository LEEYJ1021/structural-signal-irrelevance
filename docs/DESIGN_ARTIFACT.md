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

This repository's current scope is organized around two evidentiary tiers documented in the
root [`README.md`](../README.md):

- **Level 1** — the pre-specified confirmatory test of whether advertiser size confers a
  direct algorithmic advantage (H1a/H1b/H1c).
- **Level 2** — a post-hoc exploratory investigation of local-business campaign
  serving-structure heterogeneity, motivated by patterns observed after Level 1 was run.

Neither level makes use of, or depends on, the ad-group early-warning flagging rule
described in this stub. If a citation or old link led here expecting flagging-rule content,
it does not exist in this repository's current scope — see the link above for the original
specification, retained for reference in the descoped-study document.

## Where to find the full artifact

See [`FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md), section "Design Artifact:
Ad-Group Early Warning Flagging Rule," for:

- the full input/output specification and design principles (DP1–DP3),
- the empirical backtest (own-signal precision vs. a random-flagging baseline, 9
  specifications),
- the note on why a naive size/tenure-based comparison is structurally ill-posed, and
- the version history documenting the within-customer-demeaning bug that produced an early,
  incorrect "naive-rule victory" result — logged there in the same disclosure style used for
  the reversal documented in this repository's `docs/METHODOLOGY_NOTES.md` (entry B6).
