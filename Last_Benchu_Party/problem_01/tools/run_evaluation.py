"""Generate honest held-out metrics, ablations, and human-review errors."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nudisetu.evaluate import evaluate_csv, write_error_analysis


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test", default="data/splits/test.csv")
    parser.add_argument("--results", default="docs/results.md")
    parser.add_argument("--errors", default="docs/error_analysis.csv")
    parser.add_argument("--with-llm", action="store_true", help="Explicitly send test sentences to the configured Gemini API")
    args = parser.parse_args()

    try:
        report = evaluate_csv(args.test, include_llm=args.with_llm)
        errors = write_error_analysis(args.test, args.errors, include_llm=args.with_llm)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Evaluation stopped: {exc}")
        return 1
    size = int(report["sample_size"])
    lines = [
        "# Held-out evaluation results",
        "",
        f"Test rows: **{size}** (only collected, non-synthetic rows are accepted).",
        "",
    ]
    if size:
        lines.extend([
            "| System | Exact match | Word accuracy (1-WER) | CER | chrF |",
            "|---|---:|---:|---:|---:|",
        ])
        for label, key in [("Copy input (no rules)", "copy_input_no_rules"), ("Rules only", "rules_only")]:
            m = report["ablations"][key]
            lines.append(f"| {label} | {pct(m['exact_match'])} | {pct(m['word_accuracy'])} | {pct(m['cer'])} | {pct(m['chrf'])} |")
        if args.with_llm:
            m = report["ablations"]["rules_plus_llm"]
            lines.append(f"| Rules + Gemini (free-text API; enabled explicitly) | {pct(m['exact_match'])} | {pct(m['word_accuracy'])} | {pct(m['cer'])} | {pct(m['chrf'])} |")
        lines.extend(["", "## Per-dialect results", "", "| Dialect | N | Exact match | Word accuracy | CER | chrF |", "|---|---:|---:|---:|---:|---:|"])
        for dialect, m in report["by_dialect"].items():
            lines.append(f"| {dialect} | {m['count']} | {pct(m['exact_match'])} | {pct(m['word_accuracy'])} | {pct(m['cer'])} | {pct(m['chrf'])} |")
        lines.extend(["", f"Mismatches requiring review: **{errors}**. See `{args.errors}`; `meaning_ok` is intentionally blank for a human reviewer."])
    else:
        lines.extend([
            "No metrics are reported because there are no eligible collected rows in the held-out split.",
            "Synthetic bootstraps and official examples are excluded from reported evaluation.",
            "The error-analysis CSV contains headers only. Add consented, independently reviewed data, rebuild speaker-separated splits, then rerun this command.",
        ])
    lines.extend([
        "",
        "## Method and limits",
        "",
        "Word accuracy is 1-WER using the project's Unicode word tokenizer. CER is character edit distance divided by reference length. chrF is sacreBLEU chrF (character order 6, beta 2), averaged per sentence.",
        "",
        "The optional Gemini ablation sends each held-out sentence to Google's API. Run only when the consent/usage basis permits external processing; otherwise leave `--with-llm` off. The rules-only engine remains offline.",
        "",
    ])
    Path(args.results).write_text("\n".join(lines), encoding="utf-8")
    print(f"Held-out rows: {size}; mismatches: {errors}; report: {args.results}; error analysis: {args.errors}")
    if not size:
        print("No performance score can be claimed until real reviewed speaker rows are collected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
