# Data Access

No data files are committed to this repository. All source data are
proprietary and were provided under a research data-sharing agreement by
**SearchM**, a Korean ad-tech data and analytics provider that processes
performance data for a major Korean paid-search advertising platform.

## Requesting access

Researchers wishing to replicate or extend this analysis should contact
SearchM directly to request an equivalent data extract. Access is granted at
SearchM's discretion under their standard research-data terms. This
repository does not act as a data broker and cannot itself grant access.

When requesting data, reference the schema below so that the extract you
receive is compatible with the pipeline in this repository without
modification.

## Expected schema

The pipeline expects two source tables, whose paths are set in
`config/config.yaml` under `paths.adgroup_dim` and `paths.perf_panel`.

### 1. Ad-group dimension table (`adgroup_dim`, `.tsv`)

One row per ad group (a stable snapshot; deleted ad groups are not
retained -- see the account-age lower-bound caveat in
`docs/METHODOLOGY_NOTES.md`).

| column | type | notes |
|---|---|---|
| `customer_id` | string/int | advertiser account identifier |
| `ad_group_id` | string/int | unique ad group identifier |
| `campaign_id` | string/int | parent campaign identifier |
| `ad_group_name` | string | free text |
| `bid_amount` | numeric | |
| `regTm` | datetime | ad group registration timestamp |
| `delTm` | datetime, nullable | deletion timestamp, if applicable |
| `business_channel_id_mobile` / `business_channel_id_pc` | string | landing-page / channel identifiers |
| `shared_budget_id` | string, nullable | |
| `content_type`, `ad_group_type` | categorical | |

Column names are matched case-insensitively by keyword (see
`src/utils/io.py:find_column`), so minor naming variants (e.g.
`reg_dt` instead of `regTm`) are tolerated automatically.

### 2. Daily/hourly performance panel (`perf_panel`, `.tsv`)

Large file (tens of millions of rows); the pipeline reads it in
column-filtered chunks rather than loading it in full wherever possible
(see `src/utils/io.py:read_perf_panel_columns_only`).

| column | type | notes |
|---|---|---|
| `Date` | date | |
| `Hours` | int, optional | hourly granularity if present; collapsed to daily by all pipeline steps |
| `customer_id` | string/int | |
| `campaign_id` | string/int | |
| `ad_group_id` | string/int | |
| `ad_id` | string/int | |
| `impression`, `click`, `cost` | numeric | |
| `sum_of_ad_rank` | numeric | |
| `conversion_count`, `sales_by_conversion` | numeric | |
| `CTR`, `CVR`, `ROAS` | numeric | precomputed rates, recomputed independently by the pipeline where needed |
| `Depth` | numeric | |
| `device_type` | categorical | used only as a placebo outcome/level in the v4 fairness suite and variance decomposition |

### 3. Intermediate artifacts (generated, not sourced)

`spike_account_ids.json` -- a list of `customer_id`s affected by a
mass account-deletion event detected dynamically from the panel (see
`src/pipeline_v4/step0_data_prep_v4.py` / `src/coldstart_v5/step_a_period_and_spike_check.py`).
This file is produced by the pipeline itself and does not need to be
requested from SearchM.

`customer_daily_panel.csv` -- customer-day aggregate of `cost`,
produced alongside `spike_account_ids.json` by
`src/pipeline_v4/step0_data_prep_v4.py`, and consumed by the v4
variance-decomposition and churn-appendix steps.

## Privacy and identifiers

All identifiers (`customer_id`, `ad_group_id`, `campaign_id`) in the source
extract are already pseudonymized by SearchM prior to release; no
personally identifying information (advertiser names, contact details,
landing-page URLs) is included in the schema used by this pipeline. This
repository additionally never logs or prints identifier values alongside
free-text fields (e.g. ad group names) except in aggregate diagnostic
summaries (`src/coldstart_v5/step_h_top_customer_profiling.py`), which was
necessary to distinguish genuine large advertisers from templated/test
accounts during sample-construction diagnostics.

## Known limitations of the extract

- `adgroup_dim` is a **current-state snapshot** (dated in its filename),
  not a change-log: ad groups deleted before the extract date are not
  present at all. This means `all_time_count` and `customer_first_regtm`
  (used throughout `src/coldstart_v5/_sample_construction.py` and
  `src/analysis/rq1_growth_curve_test.py`) are **lower bounds**, not exact
  counts/dates -- a customer who created and later deleted earlier ad
  groups will appear more "new" than they actually are. Step J
  (`src/coldstart_v5/step_j_regtm_artifact_check.py`) checks for -- and did
  not find -- a migration/snapshot date artifact large enough to
  invalidate this further; the lower-bound caveat itself remains and
  should be stated wherever account-age or all-time-count figures are
  reported.
