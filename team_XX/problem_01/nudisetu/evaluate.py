"""Metrics and human-review error analysis for held-out collected pairs."""
from __future__ import annotations

import csv
from pathlib import Path

from sacrebleu.metrics import CHRF

from .normalize import tokenize
from .pipeline import convert

CHRF_METRIC = CHRF(char_order=6, word_order=0, beta=2)
ERROR_FIELDS = [
    "sentence_id", "dialect", "town", "topic", "dialect_text", "reference",
    "rule_output", "llm_output", "applied_rules", "glossary_entries", "meaning_ok", "reviewer_notes",
]


def edit_distance(left: list[str], right: list[str]) -> int:
    """Levenshtein distance with O(len(right)) memory."""
    previous = list(range(len(right) + 1))
    for i, token in enumerate(left, start=1):
        current = [i]
        for j, other in enumerate(right, start=1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (token != other)))
        previous = current
    return previous[-1]


def _prediction(row: dict[str, str], mode: str, api_key: str | None = None) -> str:
    if mode == "copy":
        return row["dialect_text"]
    result = convert(row["dialect_text"], row["dialect"], use_llm=(mode == "rules+llm"), api_key=api_key)
    if mode == "rules+llm" and result["llm_note"] not in {"LLM refined", "LLM cached result"}:
        raise RuntimeError(f"LLM ablation did not complete: {result['llm_note']}")
    return str(result["output"])


def metrics(rows: list[dict[str, str]], dialect: str | None = None, mode: str = "rules") -> dict[str, float | int]:
    """Compute exact match, 1-WER, CER, and sentence-averaged sacreBLEU chrF."""
    chosen = [row for row in rows if dialect is None or row.get("dialect") == dialect]
    if not chosen:
        return {"count": 0, "exact_match": 0.0, "word_accuracy": 0.0, "cer": 0.0, "chrf": 0.0}

    exact = word_errors = word_count = char_errors = char_count = 0
    chrf_scores: list[float] = []
    for row in chosen:
        prediction = _prediction(row, mode)
        reference = row["standard_text"]
        exact += prediction == reference
        predicted_words, reference_words = tokenize(prediction), tokenize(reference)
        word_errors += edit_distance(predicted_words, reference_words)
        word_count += max(1, len(reference_words))
        char_errors += edit_distance(list(prediction), list(reference))
        char_count += max(1, len(reference))
        chrf_scores.append(CHRF_METRIC.sentence_score(prediction, [reference]).score / 100)
    return {
        "count": len(chosen),
        "exact_match": exact / len(chosen),
        "word_accuracy": max(0.0, 1 - word_errors / word_count),
        "cer": char_errors / char_count,
        "chrf": sum(chrf_scores) / len(chrf_scores),
    }


def evaluate_csv(path: str | Path, include_llm: bool = False) -> dict[str, object]:
    """Evaluate only held-out, real collected rows; refuse synthetic or official rows."""
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    invalid = [row for row in rows if row.get("source") != "collected" or row.get("synthetic", "").lower() != "false"]
    if invalid:
        raise ValueError("Evaluation accepts only source=collected, synthetic=false rows from the held-out split")
    dialects = sorted({row.get("dialect", "") for row in rows if row.get("dialect")})
    result: dict[str, object] = {
        "sample_size": len(rows),
        "overall": metrics(rows),
        "by_dialect": {name: metrics(rows, name) for name in dialects},
        "ablations": {
            "copy_input_no_rules": metrics(rows, mode="copy"),
            "rules_only": metrics(rows, mode="rules"),
            "rules_plus_llm": metrics(rows, mode="rules+llm") if include_llm else None,
        },
        "llm_ablation_run": include_llm,
    }
    return result


def write_error_analysis(path: str | Path, destination: str | Path, include_llm: bool = False) -> int:
    """Write mismatches for human review; meaning_ok intentionally remains blank."""
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    invalid = [row for row in rows if row.get("source") != "collected" or row.get("synthetic", "").lower() != "false"]
    if invalid:
        raise ValueError("Error analysis accepts only held-out real collected rows")

    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ERROR_FIELDS)
        writer.writeheader()
        for row in rows:
            result = convert(row["dialect_text"], row["dialect"], use_llm=include_llm)
            if include_llm and result["llm_note"] not in {"LLM refined", "LLM cached result"}:
                raise RuntimeError(f"LLM error analysis did not complete: {result['llm_note']}")
            if result["output"] == row["standard_text"]:
                continue
            writer.writerow({
                "sentence_id": row.get("sentence_id", ""),
                "dialect": row.get("dialect", ""),
                "town": row.get("town", ""),
                "topic": row.get("topic", ""),
                "dialect_text": row.get("dialect_text", ""),
                "reference": row.get("standard_text", ""),
                "rule_output": convert(row["dialect_text"], row["dialect"])["output"],
                "llm_output": result["output"] if include_llm else "",
                "applied_rules": ";".join(result["rules"]),
                "glossary_entries": ";".join(str(hit.get("entry_id", "")) for hit in result["hits"]),
                "meaning_ok": "",
                "reviewer_notes": "",
            })
            count += 1
    return count
