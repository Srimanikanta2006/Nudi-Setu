"""Data-driven phrase and word glossary loading."""
from __future__ import annotations
import csv
import re
from pathlib import Path
from typing import Iterable

_WORD_BOUNDARY_LEFT = r"(?<![\w\u0c80-\u0cff])"
_WORD_BOUNDARY_RIGHT = r"(?![\w\u0c80-\u0cff])"

def load_glossary(path: str | Path) -> list[dict[str, str]]:
    """Load glossary rows from UTF-8 CSV; missing files yield an empty glossary."""
    p = Path(path)
    if not p.exists(): return []
    with p.open(encoding="utf-8-sig", newline="") as f: return [dict(r) for r in csv.DictReader(f)]

def match_phrase(text: str, dialect: str, rows: Iterable[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
    """Apply longest phrase matches first, scoped to dialect or shared entries."""
    hits=[]
    eligible=[r for r in rows if r.get("dialect") in (dialect,"Shared") and r.get("type")=="phrase"]
    for row in sorted(eligible,key=lambda r:len(r.get("dialect_form","")),reverse=True):
        src=row.get("dialect_form","").strip()
        if not src: continue
        pattern=f"{_WORD_BOUNDARY_LEFT}{re.escape(src)}{_WORD_BOUNDARY_RIGHT}"
        text,count=re.subn(pattern,lambda _:row.get("standard_form",src),text)
        if count: hits.append(row)
    return text,hits

def map_words(text: str, dialect: str, rows: Iterable[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
    """Replace exact glossary forms, longest first."""
    import re
    hits=[]
    eligible=[r for r in rows if r.get("dialect") in (dialect,"Shared") and r.get("type")!="phrase"]
    for row in sorted(eligible,key=lambda r:len(r.get("dialect_form","")),reverse=True):
        src=row.get("dialect_form","").strip()
        if not src: continue
        pattern=re.escape(src)
        # Word entries should not rewrite a matching substring inside another
        # Kannada word (for example, a dialect form "ಅದ" inside "ಅದರ").
        if row.get("type")=="word":
            pattern=f"{_WORD_BOUNDARY_LEFT}{pattern}{_WORD_BOUNDARY_RIGHT}"
        text,count=re.subn(pattern,lambda _:row.get("standard_form",src),text)
        if count: hits.append(row)
    return text,hits
