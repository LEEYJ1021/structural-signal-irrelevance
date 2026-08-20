# Data — Expected Schema & Access

No data files are committed to this repository. The underlying panel data
are proprietary, provided by a Korean ad-tech data and analytics provider
under a research data-sharing agreement. See root [`README.md`](../README.md)
§14 for the current access statement. Everything below documents the
schema every script in `src/` and `figures/` expects, so a compatible
extract can be substituted directly.

## Tables

### `ad_performance_log` (19,373,916 rows · 321 advertisers)

Daily/hourly performance at the ad-group level.

| Column | Type | Notes |
|---|---|---|
| `customer_id` | string | Advertiser identifier |
| `campaign_id` | string | |
| `ad_group_id` | string | |
| `date` / `hour` | date / int | Granularity varies by source table version |
| `impressions`, `clicks`, `cost` | int / int / float | Cost in platform currency units |
| `ad_rank` | float | Lower = better in this platform's convention |
| `conversions` | — | **Excluded from all analyses** — the platform's conversion API backfills retroactively per account on a delayed, inconsistent schedule, breaking construct validity (root README §4) |

### `campaign_dimension` (1,504 rows · 263/321 advertisers)

| Column | Type | Notes |
|---|---|---|
| `campaign_id` | string | |
| `customer_id` | string | |
| `campaign_type` | categorical code | Platform-defined **ad-product** code (website / shopping / brand-new-product / local-business) — **not** an industry field (see `appendix/exploratory_industry_classification.md`) |

### `ad_group_dimension` (9,823 rows · 263/321 advertisers, snapshot)

| Column | Type | Notes |
|---|---|---|
| `ad_group_id` | string | |
| `bid_amount` | float | Advertiser's set bid price — the cost-independent outcome used in README §5.4 method 8 |
| `registration_ts`, `deletion_ts` | timestamp | **Snapshot table** — `account_age_days` derived from this is a lower bound, not exact tenure (root README §11, limitation 4) |
| `on_off_status` | bool | |

### `keyword_dimension` (1,503,289 rows · 256/321 advertisers)

| Column | Type | Notes |
|---|---|---|
| `keyword_id` | string | |
| `brand_type` | categorical | |
| `inspect_status` | categorical code | Review/approval code; only 0.5% carry a non-standard value (used in the RQ2 boundary check, README §9a) |
| `bid_price` | float | |

## Fields intentionally absent

| Field | Why absent |
|---|---|
| `category_name` (industry, top-level) | Not a platform API field. No native industry taxonomy exists; a proxy pipeline was piloted (`appendix/exploratory_industry_classification.md`) but not adopted, due to a moderate-at-best label-reliability ceiling. |
| `conversion_*`, `roas_*` | Retroactive backfill breaks construct validity (see `ad_performance_log` above). |

## Requesting an extract

Researchers interested in replication should contact the data provider
directly for a schema-compatible extract. All code in this repository is
runnable end-to-end against any dataset matching the schema documented
above; nothing is hard-coded to this specific provider's internal IDs
beyond the pre-specified test-account exclusion list in
`config/config.yaml` (`sample_definition.known_test_account_ids`), which
is meaningless outside this specific extract and can be safely cleared.
