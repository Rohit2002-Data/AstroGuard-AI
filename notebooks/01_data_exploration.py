"""AstroGuard AI — Phase 1 public dataset exploration.

Run from the project root:
    python notebooks/01_data_exploration.py

Or copy cells into Jupyter/Colab. MMASH is public but is human ground-based
wearable/sleep research, NOT astronaut data. Review the dataset documentation.
"""
from pathlib import Path
import pandas as pd
from src.mmash_loader import download_mmash, inventory_csvs

data_root = download_mmash()
inventory = inventory_csvs(data_root)

print("Number of CSV files:", len(inventory))
display(inventory.head(30)) if "display" in globals() else print(inventory.head(30).to_string(index=False))

# Pick a file only after reviewing its path and column definitions.
# Example:
# selected = data_root / "path" / "to" / "a" / "documented_file.csv"
# df = pd.read_csv(selected)
# print(df.shape)
# print(df.columns.tolist())
# display(df.head()) if "display" in globals() else print(df.head())
