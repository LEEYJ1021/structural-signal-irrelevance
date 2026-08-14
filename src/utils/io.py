"""
Shared I/O utilities: config loading, case-insensitive/keyword column
matching (so minor schema variants like `reg_dt` vs `regTm` are
tolerated automatically, per data/README.md), and chunked readers for
the large performance panel so no step needs to load the full file
into memory unless it explicitly wants to.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Iterator, Optional

import pandas as pd
import yaml


def load_config(path: str | Path) -> dict:
    """Load config.yaml into a plain dict. No defaults are silently
    injected here -- every step is expected to read the keys it needs
    directly from the returned dict, so a missing key fails loudly
    (KeyError) at the point of use rather than being masked."""
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def find_column(df: pd.DataFrame, keywords: Iterable[str]) -> Optional[str]:
    """Return the first column whose lower-cased name contains any of
    `keywords` (checked in keyword order, then column order). Returns
    None if nothing matches -- callers should assert on this rather
    than silently proceeding with the wrong column."""
    lower_map = {c.lower(): c for c in df.columns}
    for kw in keywords:
        for lower_name, orig_name in lower_map.items():
            if kw in lower_name:
                return orig_name
    return None


def smart_read_table(path: str | Path) -> pd.DataFrame:
    """Read a full table, inferring the separator from the extension
    (.tsv -> tab, everything else -> comma). Intended for the smaller
    dimension tables (adgroup_dim, campaign_dim), not the multi-GB
    performance panel -- use read_perf_panel_columns_only for that."""
    path = Path(path)
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    return pd.read_csv(path, sep=sep, low_memory=False)


def peek_header(path: str | Path, nrows: int = 5) -> pd.DataFrame:
    """Read just the first few rows of a (possibly huge) panel file,
    to detect column names/dtypes before committing to a full or
    chunked read."""
    path = Path(path)
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    return pd.read_csv(path, sep=sep, nrows=nrows, low_memory=False)


def read_perf_panel_columns_only(
    path: str | Path,
    usecols: list[str],
    dtype: Optional[dict] = None,
    chunksize: Optional[int] = None,
) -> pd.DataFrame | Iterator[pd.DataFrame]:
    """Read only the requested columns from the (large, tens-of-millions-
    of-rows) performance panel. If `chunksize` is given, returns an
    iterator of DataFrame chunks (for steps that need to filter down to
    a target ad_group_id set before concatenating, e.g. Step H/L cost
    re-scans); otherwise reads the filtered columns in one pass, which
    is still far cheaper than loading every column.
    """
    path = Path(path)
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    reader = pd.read_csv(
        path, sep=sep, low_memory=False, usecols=usecols, dtype=dtype, chunksize=chunksize
    )
    return reader
