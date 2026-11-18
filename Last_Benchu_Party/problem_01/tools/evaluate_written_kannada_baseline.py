"""Check how often Nudi Setu changes a general Kannada text sample.

Reads an external corpus in place and reports aggregate counts only. It never
copies source text into the project or output report.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nudisetu.pipeline import convert

DIALECTS = ["Uttara Kannada", "Mangaluru", "Hubballi-Dharwad"]
SENTENCE_SPLIT = re.compile(r"[\n.!?।]+")
KANNADA = re.compile(r"[\u0c80-\u0cff]")


def segments(corpus: Path):
    """Yield plausible Kannada text segments without retaining file names."""
    for path in corpus.rglob("*.txt"):
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        for raw in SENTENCE_SPLIT.split(content):
            text = " ".join(raw.split())
            if len(text) >= 20 and len(KANNADA.findall(text)) >= 2:
                yield text


def take_reservoir(source, size: int, seed: int) -> tuple[list[str], int]:
    """Take a reproducible sample spread across the corpus, using O(size) memory."""
    rng = random.Random(seed)
    sample: list[str] = []
    total = 0
    for total, text in enumerate(source, start=1):
        if len(sample) < size:
            sample.append(text)
        else:
            index = rng.randrange(total)
            if index < size:
                sample[index] = text
    return sample, total


def analyze(sample: list[str], dialect: str) -> dict[str, object]:
    unchanged = normalization_only = lexical_changes = grammar_changes = 0
    rule_counts: Counter[str] = Counter()
    for text in sample:
        result = convert(text, dialect)
        stages = result["stages"]
        if result["output"] == text:
            unchanged += 1
        if stages["normalized"] != text and stages["mapped"] == stages["normalized"] and stages["grammar"] == stages["mapped"]:
            normalization_only += 1
        if result["hits"]:
            lexical_changes += 1
        if result["rules"]:
            grammar_changes += 1
            rule_counts.update(result["rules"])
    size = len(sample)
    return {
        "segments_sampled": size,
        "unchanged_exactly": unchanged,
        "changed_exactly": size - unchanged,
        "normalization_only_segments": normalization_only,
        "segments_with_glossary_matches": lexical_changes,
        "segments_with_grammar_rules": grammar_changes,
        "grammar_rule_counts": dict(sorted(rule_counts.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="Folder containing the Kannada corpus .txt files")
    parser.add_argument("--sample-size", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=241)
    parser.add_argument("--output", type=Path, help="Optional JSON report path; contains aggregate counts only")
    args = parser.parse_args()
    if args.sample_size < 1:
        parser.error("--sample-size must be greater than zero")
    if not args.corpus.is_dir():
        parser.error(f"Corpus folder does not exist: {args.corpus}")

    sample, total_segments = take_reservoir(segments(args.corpus), args.sample_size, args.seed)
    report = {
        "purpose": "General written-Kannada preservation check; not a dialect accuracy evaluation.",
        "source": {
            "title": "Kannada Text Corpus",
            "url": "https://mozilladatacollective.com/datasets/cmrkqy18t006imm074waw5jbg",
            "dataset_id": "cmrkqy18t006imm074waw5jbg",
            "license": "CC-BY-NC-SA-4.0",
            "attribution": "Compiled by MirasAI; corpus listing identifies Chandrashekara K and other source authors.",
        },
        "method": {
            "corpus_txt_files": sum(1 for _ in args.corpus.rglob("*.txt")),
            "candidate_segments_found": total_segments,
            "sampling": "Reproducible reservoir sample across files; short segments excluded.",
            "sample_size_requested": args.sample_size,
            "seed": args.seed,
            "source_text_written_to_report": False,
        },
        "by_dialect_setting": {dialect: analyze(sample, dialect) for dialect in DIALECTS},
        "interpretation": "Changes reveal possible edits to general written Kannada and should be reviewed. The corpus has no verified target-dialect labels and cannot measure dialect conversion quality.",
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
