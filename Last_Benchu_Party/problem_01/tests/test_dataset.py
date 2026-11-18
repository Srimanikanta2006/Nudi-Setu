import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_dataset_required_columns():
    with (ROOT/'data'/'dataset.csv').open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f); assert {'dialect','town','dialect_text','standard_text','age_band'}.issubset(reader.fieldnames)
