from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_oews_table(xlsx_path: str | Path) -> pd.DataFrame:
    return pd.read_excel(xlsx_path)
