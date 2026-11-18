"""Validate dataset structure, privacy, consent, Unicode, and collection targets."""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

REQUIRED = ["dialect", "town", "dialect_text", "standard_text", "age_band"]
EXTRA = ["sentence_id", "topic", "speaker_id", "synthetic", "verified_by", "source", "audio_file"]
DIALECTS = ["Uttara Kannada", "Mangaluru", "Hubballi-Dharwad"]
TOPICS = ["home", "market", "school", "travel", "festivals"]
AGES = ["18-25", "26-40", "41-60", "60+"]
TARGET_PER_DIALECT = 100
MIN_PER_TOPIC = TARGET_PER_DIALECT // len(TOPICS)
SOURCES = {"official_example", "synthetic", "collected"}


def read_csv(path: str | Path) -> tuple[list[str], list[dict[str, str]]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/dataset.csv")
    parser.add_argument("--consent", default="consent/consent_log.csv")
    args = parser.parse_args()

    issues: list[str] = []
    try:
        fields, rows = read_csv(args.dataset)
        consent_fields, consent_rows = read_csv(args.consent)
    except (OSError, csv.Error, UnicodeError) as exc:
        print(f"Cannot read input CSV: {exc}")
        return 1

    for name, actual, required in [
        ("dataset", fields, REQUIRED + EXTRA),
        ("consent log", consent_fields, ["speaker_id", "dialect", "date", "consent_given", "age_band", "text_release", "audio_recording_consent", "audio_release"]),
    ]:
        missing = [column for column in required if column not in actual]
        if missing:
            issues.append(f"{name} missing columns: {', '.join(missing)}")
    if not rows:
        issues.append("Dataset has no rows")

    consent_by_speaker = {
        row.get("speaker_id", ""): row
        for row in consent_rows
        if row.get("speaker_id")
        and row.get("consent_given", "").strip().lower() == "yes"
        and row.get("text_release", "").strip().lower() == "yes"
    }
    collected = {dialect: 0 for dialect in DIALECTS}
    topic_counts = {dialect: {topic: 0 for topic in TOPICS} for dialect in DIALECTS}
    seen: set[tuple[str, str]] = set()

    for line, row in enumerate(rows, start=2):
        source = row.get("source", "").strip()
        synthetic = row.get("synthetic", "").strip().lower()
        dialect = row.get("dialect", "").strip()
        topic = row.get("topic", "").strip()
        if dialect not in DIALECTS:
            issues.append(f"Row {line}: unsupported dialect {dialect!r}")
        if source not in SOURCES:
            issues.append(f"Row {line}: unsupported source {source!r}")
        if synthetic not in {"true", "false"}:
            issues.append(f"Row {line}: synthetic must be true or false")
        if (source == "synthetic") != (synthetic == "true"):
            issues.append(f"Row {line}: source and synthetic flag disagree")
        if source == "collected" and synthetic != "false":
            issues.append(f"Row {line}: collected data must be marked synthetic=false")

        for field in REQUIRED + EXTRA:
            if field == "audio_file":
                continue
            if not (row.get(field, "") or "").strip():
                issues.append(f"Row {line}: {field} is empty")
        if dialect in DIALECTS and topic not in TOPICS:
            issues.append(f"Row {line}: topic must be one of {', '.join(TOPICS)}")

        text = row.get("dialect_text", "")
        key = (dialect, text)
        if key in seen:
            issues.append(f"Row {line}: duplicate dialect_text for {dialect}")
        seen.add(key)

        for field in ("dialect_text", "standard_text"):
            value = row.get(field, "")
            if unicodedata.normalize("NFC", value) != value:
                issues.append(f"Row {line}: {field} is not Unicode NFC")
            if re.search(r"\b\d{10}\b|@|\bph\b", value, re.IGNORECASE):
                issues.append(f"Row {line}: possible contact information in {field}")
            if value and sum("\u0c80" <= char <= "\u0cff" for char in value) / len(value) < 0.35:
                issues.append(f"Row {line}: low Kannada-script ratio in {field}")

        if source == "collected" and synthetic == "false" and dialect in DIALECTS:
            collected[dialect] += 1
            if topic in TOPICS:
                topic_counts[dialect][topic] += 1
            speaker = row.get("speaker_id", "").strip()
            reviewer = row.get("verified_by", "").strip()
            if not speaker:
                issues.append(f"Row {line}: collected row has no speaker_id")
            if not reviewer or reviewer == speaker:
                issues.append(f"Row {line}: second reviewer must be present and differ from speaker_id")
            if row.get("age_band", "").strip() not in AGES:
                issues.append(f"Row {line}: collected row has invalid age_band")
            consent = consent_by_speaker.get(speaker)
            if not consent:
                issues.append(f"Row {line}: speaker has no consent_given=yes record")
            elif consent.get("dialect") != dialect:
                issues.append(f"Row {line}: consent log dialect does not match")
            elif consent.get("age_band") != row.get("age_band"):
                issues.append(f"Row {line}: consent log age_band does not match")
            if row.get("audio_file", "").strip() and (
                not consent
                or consent.get("audio_recording_consent", "").strip().lower() != "yes"
                or consent.get("audio_release", "").strip().lower() != "yes"
            ):
                issues.append(f"Row {line}: audio is present without separate recording and release consent")

    print("DATA STATUS - real collected rows only (target 100 per dialect)")
    for dialect in DIALECTS:
        count = collected[dialect]
        print(f"{dialect}: {count}/{TARGET_PER_DIALECT} real")
        for topic in TOPICS:
            print(f"  {topic}: {topic_counts[dialect][topic]}/{MIN_PER_TOPIC} real")
        if count < TARGET_PER_DIALECT:
            issues.append(f"{dialect}: collection target short by {TARGET_PER_DIALECT - count} real rows")
        for topic in TOPICS:
            if topic_counts[dialect][topic] < MIN_PER_TOPIC:
                issues.append(f"{dialect}: {topic} topic short by {MIN_PER_TOPIC - topic_counts[dialect][topic]} real rows")
    print(f"Total real: {sum(collected.values())}/300")

    if issues:
        print(f"Validation found {len(issues)} issue(s):")
        print("\n".join(f"- {issue}" for issue in issues))
        return 1
    print("Dataset validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
