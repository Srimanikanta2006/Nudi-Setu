"""Build deterministic speaker-separated splits from reviewed collected rows only."""
import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path

REQUIRED_FIELDS = ["dialect", "town", "dialect_text", "standard_text", "age_band"]
EXTRA_FIELDS = ["sentence_id", "topic", "speaker_id", "synthetic", "verified_by", "source", "audio_file"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="data/dataset.csv")
    parser.add_argument("--output-dir", default="data/splits")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    with Path(args.dataset).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or []) or REQUIRED_FIELDS + EXTRA_FIELDS
    rows = [row for row in rows if row.get("source") == "collected" and row.get("synthetic", "").lower() == "false"]

    by_dialect_speaker: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        speaker = row.get("speaker_id", "").strip()
        if not speaker:
            raise ValueError(f"Collected sentence {row.get('sentence_id', '')!r} has no speaker_id")
        by_dialect_speaker[row.get("dialect", "")][speaker].append(row)

    splits: dict[str, list[dict[str, str]]] = {"train": [], "dev": [], "test": []}
    rng = random.Random(args.seed)
    for speakers in by_dialect_speaker.values():
        speaker_ids = sorted(speakers)
        rng.shuffle(speaker_ids)
        train_cut = int(len(speaker_ids) * 0.8)
        dev_cut = int(len(speaker_ids) * 0.9)
        # With fewer than 3 speakers, keep all rows in train rather than leak speakers.
        if len(speaker_ids) < 3:
            train_cut, dev_cut = len(speaker_ids), len(speaker_ids)
        assignment = {
            **{speaker: "train" for speaker in speaker_ids[:train_cut]},
            **{speaker: "dev" for speaker in speaker_ids[train_cut:dev_cut]},
            **{speaker: "test" for speaker in speaker_ids[dev_cut:]},
        }
        for speaker, speaker_rows in speakers.items():
            splits[assignment[speaker]].extend(speaker_rows)

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for name, split_rows in splits.items():
        with (output / f"{name}.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(split_rows)

    print(f"Reviewed collected rows: {len(rows)}")
    print("Speaker-separated split rows:", ", ".join(f"{name}={len(items)}" for name, items in splits.items()))
    if not rows:
        print("No eligible collected rows; splits are empty and evaluation metrics are unavailable.")
    elif not splits["test"]:
        print("No test rows yet; add more independent speakers per dialect before reporting metrics.")
    print("Synthetic and official examples were excluded. Keep the glossary built from train rows only.")


if __name__ == "__main__":
    main()
