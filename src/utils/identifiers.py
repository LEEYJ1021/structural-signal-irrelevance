"""
Shared identifier-cleaning and timestamp-normalization helpers, used by
every step in coldstart_v5, pipeline_v4, and src/analysis so that ID
joins and date comparisons behave identically everywhere in the
pipeline.
"""
from __future__ import annotations

import pandas as pd


def clean_id(series: pd.Series) -> pd.Series:
    """Normalize an identifier column across sources that may encode it
    as int, float (NaN-promoted, e.g. '123.0'), or string.

    Steps: string-cast -> strip whitespace -> drop a trailing '.0'
    artifact left behind when pandas upcasts an int column containing
    nulls to float before CSV export.
    """
    s = series.astype(str).str.strip()
    return s.str.replace(r"\.0$", "", regex=True)


def to_naive(series: pd.Series) -> pd.Series:
    """Strip timezone information if present, leaving the clock time
    itself unchanged, so that all downstream date arithmetic is
    tz-naive regardless of how the source extract encoded timestamps.
    """
    if isinstance(series.dtype, pd.DatetimeTZDtype):
        return series.dt.tz_localize(None)
    return series
