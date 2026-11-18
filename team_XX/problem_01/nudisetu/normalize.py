"""Unicode and spelling normalization helpers."""
from __future__ import annotations
import re
import unicodedata

_ZERO_WIDTH = "\u200b\u200c\u200d\ufeff"

def normalize_text(text: str) -> str:
    """Return Kannada text normalized to NFC with tidy whitespace and punctuation."""
    value = unicodedata.normalize("NFC", text or "")
    value = value.translate({ord(ch): None for ch in _ZERO_WIDTH})
    value = re.sub(r"([!?.,।])\1+", r"\1", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s+([,!?।.])", r"\1", value)
    value = re.sub(r"([,!?।.])(?=\S)", r"\1 ", value)
    return value

def tokenize(text: str) -> list[str]:
    """Split text into Kannada/Latin word tokens and punctuation."""
    return re.findall(r"[\u0C80-\u0CFF]+|[A-Za-z0-9]+|[^\w\s]", text, re.UNICODE)
