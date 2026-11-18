"""Optional local Ollama refinement with no network transmission."""
from __future__ import annotations

import os
import re

import requests

DEFAULT_MODEL = "gemma4:latest"
DEFAULT_HOST = "http://127.0.0.1:11434"


def _host() -> str:
    return os.getenv("OLLAMA_HOST", DEFAULT_HOST).rstrip("/")


def available_models(timeout: float = 0.45) -> list[str]:
    """Return installed local model names, or an empty list if Ollama is offline."""
    try:
        response = requests.get(f"{_host()}/api/tags", timeout=timeout)
        response.raise_for_status()
        return [str(item.get("name", "")) for item in response.json().get("models", []) if item.get("name")]
    except (requests.RequestException, ValueError, TypeError):
        return []


def refine(
    dialect: str,
    source_text: str,
    draft: str,
    examples: list[dict[str, str]] | None = None,
    model: str | None = None,
) -> tuple[str, str]:
    """Use an already-installed local model; keep the rule draft on every failure."""
    chosen_model = model or os.getenv("NUDISETU_OLLAMA_MODEL", DEFAULT_MODEL)
    if chosen_model not in available_models():
        return draft, "Local model unavailable; kept offline rules draft"

    example_lines = [
        f"{item.get('dialect_text', '').strip()} → {item.get('standard_text', '').strip()}"
        for item in (examples or [])[:5]
        if item.get("dialect_text", "").strip() and item.get("standard_text", "").strip()
    ]
    examples_block = "\n".join(example_lines) if example_lines else "(No verified examples available.)"
    prompt = (
        f"Convert one {dialect} Kannada sentence into textbook Kannada. Preserve the exact meaning, "
        "person, politeness, tense, and question/statement form. Use only the examples as guidance; "
        "do not copy their content. Prefer the rule-based draft when uncertain. Return exactly one "
        "Kannada sentence with no label or explanation.\n\n"
        f"Examples:\n{examples_block}\n\n"
        f"Dialect input: {source_text}\n"
        f"Rule-based draft: {draft}\n"
        "Textbook Kannada:"
    )
    try:
        response = requests.post(
            f"{_host()}/api/chat",
            json={
                "model": chosen_model,
                "messages": [
                    {"role": "system", "content": "You rewrite Kannada dialect text conservatively."},
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
                "options": {"temperature": 0, "num_predict": 160},
            },
            timeout=120,
        )
        response.raise_for_status()
        value = str(response.json().get("message", {}).get("content", "")).strip().strip('"“”')
        kannada_chars = len(re.findall(r"[\u0C80-\u0CFF]", value))
        script_ratio = kannada_chars / max(1, len(value.replace(" ", "")))
        if (
            not value
            or "\n" in value
            or script_ratio < 0.55
            or len(value) > 2 * max(1, len(source_text))
            or re.search(r"(?i)(textbook kannada|answer|translation|explanation)\s*:", value)
        ):
            return draft, "Local model output rejected; kept offline rules draft"
        return value, f"Local {chosen_model} draft; review meaning before use"
    except (requests.RequestException, ValueError, TypeError, KeyError):
        return draft, "Local model failed; kept offline rules draft"
