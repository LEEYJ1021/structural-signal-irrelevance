# Supplementary Robustness Analyses

This folder contains additional analyses that support specific claims made in the root [`README.md`](../README.md) but are detailed here rather than in the main narrative, to keep the primary results focused. Each file is self-contained and states which section of the root README it supports.

| File | Supports | One-line summary |
|---|---|---|
| [`01_alternative_outcome_mediation.md`](01_alternative_outcome_mediation.md) | §2.4 | Isolates the mechanical spend–CPC artifact and replicates Study 1's spend-mediation result on `bid_amount`, an outcome that does not share a cost term with spend |
| [`02_boundary_conditions.md`](02_boundary_conditions.md) | §2.5, §5 | Tests whether the spend-controlled size effect is homogeneous across campaign product types and across keyword review-status strata |
| [`03_equivalence_and_sensitivity_notes.md`](03_equivalence_and_sensitivity_notes.md) | §3.2, §6 | TOST equivalence tests for the two central null results, plus Oster's delta omitted-variable-bias sensitivity for the bid-based mediation estimate |
| [`04_design_artifact_future_work.md`](04_design_artifact_future_work.md) | §3.4 | Formalizes the early-flagging decision rule implied by §3.3 as a design artifact, and reports why its empirical backtest is treated as future work rather than a confirmed result |

## How to read these files

Each file distinguishes explicitly between:
- results that are **load-bearing** for a claim in the root README (reported with full statistics and treated as confirmatory), and
- results that are **exploratory or preliminary** (reported transparently, with the specific reason — usually sample size — that keeps them out of the confirmatory set).

This separation is intentional: a robustness check that fails to confirm a hypothesis is still reported, but it is never presented with the same evidentiary weight as a pre-registered confirmatory test.
