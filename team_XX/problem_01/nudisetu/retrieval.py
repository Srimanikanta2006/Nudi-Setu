"""Retrieve safe Kannada examples for optional model refinement."""
from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path

from .normalize import normalize_text

ROOT = Path(__file__).resolve().parent.parent


def _ngrams(text: str) -> Counter[str]:
    value = normalize_text(text).replace(" ", "")
    return Counter(value[index:index + width] for width in (2, 3, 4) for index in range(max(0, len(value) - width + 1)))


def _similarity(left: str, right: str) -> float:
    a, b = _ngrams(left), _ngrams(right)
    dot = sum(count * b.get(gram, 0) for gram, count in a.items())
    norm_a = math.sqrt(sum(count * count for count in a.values()))
    norm_b = math.sqrt(sum(count * count for count in b.values()))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def _read(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except (OSError, csv.Error, UnicodeError):
        return []


def get_similar_examples(
    text: str,
    dialect: str,
    *,
    root: str | Path = ROOT,
    limit: int = 5,
) -> list[dict[str, str]]:
    """Return same-dialect pairs from training data, never from test or synthetic rows.

    If the collected training split is empty, only the three official challenge
    examples are used as prompt context. Synthetic examples and unreviewed public
    source candidates are deliberately excluded.
    """
    project = Path(root)
    train_rows = _read(project / "data" / "splits" / "train.csv")
    rows = [
        row for row in train_rows
        if row.get("dialect") == dialect
        and row.get("source") == "collected"
        and row.get("synthetic", "false").strip().lower() == "false"
        and row.get("dialect_text", "").strip()
        and row.get("standard_text", "").strip()
    ]
    if not rows:
        rows = [
            row for row in _read(project / "data" / "dataset.csv")
            if row.get("dialect") == dialect
            and row.get("source") == "official_example"
            and row.get("dialect_text", "").strip()
            and row.get("standard_text", "").strip()
        ]
    unique: dict[str, dict[str, str]] = {}
    for row in rows:
        unique.setdefault(normalize_text(row["dialect_text"]), row)
    ranked = sorted(
        unique.values(),
        key=lambda row: _similarity(text, row["dialect_text"]),
        reverse=True,
    )
    return [
        {"dialect_text": row["dialect_text"], "standard_text": row["standard_text"]}
        for row in ranked[:max(0, limit)]
    ]


def find_exact_public_pair(text: str, dialect: str, *, root: str | Path = ROOT) -> dict[str, str] | None:
    """Find an exact, same-dialect public-source pair without fuzzy guessing."""
    normalized = normalize_text(text)
    folder = Path(root) / "data" / "public_source_pairs"
    for path in sorted(folder.glob("*.csv")):
        for row in _read(path):
            if (
                row.get("dialect") == dialect
                and normalize_text(row.get("dialect_text", "")) == normalized
                and row.get("standard_text", "").strip()
            ):
                return row
    return None
