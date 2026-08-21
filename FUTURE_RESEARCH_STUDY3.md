# Future Research — Study 3: A Preregistered Confirmatory Test of P5 and the Level 2 Findings

**Status: [FUTURE WORK — not yet run].** This document proposes, but does not execute, a
confirmatory follow-up study. It exists to give Level 2's exploratory findings (root
README §6) a clear path toward confirmatory status, and to preregister the design *before*
new data is collected, so that a future replication is not subject to the same post-hoc
concerns that apply to the current Level 2 analysis.

---

## 1. Why this study is needed

Level 2 of the main study (root README §6) surfaced a plausible but unconfirmed pattern:
local-business advertising appears to run through a structurally different, non-auction
serving pathway, and this structural difference is associated with instability in the H1c
estimate. Every part of that finding was discovered *after* Level 1 was run, using the
same sample. No amount of additional diagnostics on that same sample — split-sample
replication, influence diagnostics, sensitivity checks — can fully substitute for an
independent test, because all of it is still drawn from the 228–321 advertisers already
examined.

Study 3 is designed to test the single most load-bearing claim to emerge from Level 2: the
candidate boundary condition **P5 (mechanism applicability)**, stated in root README §3.3.

## 2. Primary hypothesis (to be preregistered)

> **H-P5.** The Structural Signal Irrelevance (SSI) null found for H1c in Level 1 holds
> specifically within auction/bidding-mediated serving mechanisms, and does not
> generalize, without qualification, to non-auction serving mechanisms (e.g.,
> location/business-channel-based serving, as used for local-business campaigns on this
> platform).

**Directional prediction:** in a new, independent sample of advertisers stratified by
serving mechanism, the direct-path coefficient for size (H1c) will be closer to zero and
more stable across specifications within the auction-mechanism stratum than within the
non-auction-mechanism stratum.

## 3. Design

- **Sampling frame.** A new cross-sectional pull of advertiser-level data from the same
  platform, covering a period that does not overlap with the current sample's observation
  window (2025-08-23 to 2026-07-21), to avoid re-analyzing the same underlying
  transactions.
- **Stratification (fixed in advance, not discovered from data).** Advertisers are
  stratified into "auction-like" and "non-auction-like" serving mechanisms using the same
  operational rule already used in the current study (keyword-dimension match rate ≥ 5%
  → auction-like), applied *before* any outcome variable is examined.
- **Target sample size.** A minimum of 42 clusters (customers) per stratum, informed by
  the G≥42 rule-of-thumb for cluster-robust SE validity flagged as a limitation in the
  current study (root README §11, item 3). This directly addresses the small-cluster
  problem that limited Level 2's own internal precision.
- **Primary model.** The same H1c specification used in Level 1 (`log_cpc ~ spend_z +
  size_z`, cluster-robust SEs), estimated separately within each stratum and compared via
  a preregistered joint interaction test (size_z × stratum).
- **Preregistered robustness plan.** A subset of the Level 1 robustness battery — cluster
  wild-bootstrap, temporal split, and TOST equivalence testing against the same
  pre-specified SESOI used in the current study — applied identically to both strata.

## 4. What would confirm, and what would disconfirm, P5

| Outcome | Interpretation |
|---|---|
| Auction stratum: null holds (TOST equivalence confirmed); non-auction stratum: null does not hold or equivalence is not confirmed | **P5 supported** — SSI's applicability is bounded by serving mechanism, as suggested by Level 2 |
| Both strata show a stable null | **P5 not supported** — SSI appears mechanism-general; Level 2's pattern was likely sample-specific noise |
| Non-auction stratum shows a stable null and auction stratum does not | **P5 contradicted** — would require revisiting the theoretical account entirely |

## 5. Secondary, exploratory tracks (not confirmatory even after this study runs)

- **Track 1 — mechanism identification.** If P5 is supported, a natural follow-up is
  identifying *what* about non-auction serving produces the instability (e.g.,
  discretionary review, location-based ranking rules). This remains exploratory even after
  Study 3, since it was not part of the preregistered test.
- **Track 2 — the indirect proxy candidates surfaced during Level 2's post-hoc mechanism
  scan** (registration/deletion cycles, activity-gap irregularity, channel-registration
  lag, and the unexplored-moderator scan) are not part of the confirmatory design above.
  They remain candidate leads for future exploratory work and should not be cited as
  supporting or refuting P5 on their own.

## 6. Relationship to the current repository

This document does not change any statistic reported in the root README. It exists solely
to specify, in advance, what a confirmatory test of P5 would look like, so that if this
study is run in the future, its design cannot be accused of having been adapted to fit
whatever result comes out of it.
