from pathlib import Path
import pandas as pd


def load_table(path_or_buffer) -> pd.DataFrame:
    """Load a tabular file without assuming particular health columns."""
    name = getattr(path_or_buffer, "name", str(path_or_buffer))
    suffix = Path(name).suffix.lower()
    if suffix == ".tsv":
        df = pd.read_csv(path_or_buffer, sep="\t")
    elif suffix == ".txt":
        df = pd.read_csv(path_or_buffer, sep=None, engine="python")
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path_or_buffer)
    else:
        df = pd.read_csv(path_or_buffer)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def numeric_columns(df: pd.DataFrame) -> list[str]:
    """Return numeric columns, including mostly-numeric text columns."""
    cols = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            cols.append(col)
            continue
        converted = pd.to_numeric(df[col], errors="coerce")
        nonempty = int(df[col].notna().sum())
        if nonempty >= 5 and converted.notna().sum() / max(nonempty, 1) >= 0.8:
            cols.append(col)
    return cols


def summarize(df: pd.DataFrame) -> dict:
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_columns": numeric_columns(df),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }
