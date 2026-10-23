"""Starter exploration script for a downloaded NASA OSD-575 table."""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
files = [p for p in DATA_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".csv", ".tsv", ".txt", ".xlsx", ".xls"}]
if not files:
    print("No table found. Run scripts/download_osdr_inspiration4.py or download from:")
    print("https://osdr.nasa.gov/bio/repo/data/studies/OSD-575")
for path in files:
    print("\nFILE:", path.name)
    if path.suffix.lower() == ".tsv":
        df = pd.read_csv(path, sep="\t")
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, sep=None, engine="python")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head())
    print("\nMissing values:\n", df.isna().sum().sort_values(ascending=False).head(20))
