"""Word-level alignment used for UI highlighting."""
from __future__ import annotations
from difflib import SequenceMatcher
from .normalize import tokenize

def align_words(source: str,target: str)->list[dict[str,object]]:
    """Return source/target token groups tagged as equal, replace, insert, delete."""
    a,b=tokenize(source),tokenize(target)
    return [{"tag":tag,"source":a[i1:i2],"target":b[j1:j2],"changed":tag!="equal"} for tag,i1,i2,j1,j2 in SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes()]
