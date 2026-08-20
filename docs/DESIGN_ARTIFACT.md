# Design Artifact: Ad-Group Early Warning Flagging Rule

**This file is a redirect stub.** The full specification, backtest grid, and version history for
this artifact are preserved in
[`../FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md#design-artifact-ad-group-early-warning-flagging-rule).

## Why this moved

The Ad-Group Early Warning Flagging Rule was grounded entirely in the descoped longitudinal
study's confirmed within-customer result — an ad group's own early operating signal predicts its
near-term growth, and adding account maturity produces no within-customer improvement at any
tested horizon (formerly root README §5.4). Because that longitudinal study (account maturity vs.
a new ad group's growth trajectory, n = 29 customers) has been removed from this paper's evidence
base and reported separately as future work, the design artifact built on top of it has no
remaining basis in this repository's current scope (advertiser-size fairness, cross-sectional).

Root `README.md` (current version) makes no reference to this artifact. It is retained here only
as a pointer so that old links and citations into `docs/DESIGN_ARTIFACT.md` resolve to where the
content now lives, rather than to a broken or silently emptied file.

## Where to find it

See [`FUTURE_RESEARCH_STUDY2.md`](../FUTURE_RESEARCH_STUDY2.md), section "Design Artifact:
Ad-Group Early Warning Flagging Rule," for:
- the full input/output specification and design principles (DP1–DP3),
- the empirical backtest (own-signal precision vs. a random-flagging baseline, 9
  specifications),
- the note on why a naive size/tenure-based comparison is structurally ill-posed, and
- the version history documenting the within-customer-demeaning bug that produced an early,
  incorrect "naive-rule victory" result.
