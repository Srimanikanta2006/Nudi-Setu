"""Optional Gemini REST refinement with safe offline fallback."""
from __future__ import annotations
import os,re,time,hashlib,json
from pathlib import Path
import requests
from .retrieval import get_similar_examples

DEFAULT_MODEL = "gemini-3.6-flash"

def refine(dialect:str,draft:str,examples:list[dict[str,str]]|None=None,api_key:str|None=None,model_override:str|None=None,source_text:str="")->tuple[str,str]:
    """Refine via Gemini if configured; return unchanged draft for any failure."""
    key=api_key or os.getenv("GEMINI_API_KEY","")
    if not key:return draft,"LLM unavailable: GEMINI_API_KEY not configured"
    cache_root=Path(os.getenv("NUDISETU_CACHE_DIR",str(Path(__file__).resolve().parent.parent/".cache")))
    cache_file=cache_root/"llm_cache.json"; cache_file.parent.mkdir(parents=True,exist_ok=True)
    try:cache=json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    except Exception:cache={}
    cache_material=json.dumps([dialect,source_text,draft,model_override or DEFAULT_MODEL,examples or []],ensure_ascii=False,sort_keys=True)
    cache_key=hashlib.sha256(cache_material.encode()).hexdigest()
    if cache_key in cache:return cache[cache_key],"LLM cached result"
    few="\n".join(f"{x.get('dialect_text','')} → {x.get('standard_text','')}" for x in (examples or [])[:5]) or "(No verified examples available.)"
    prompt=(
        f"Rewrite this {dialect} dialect Kannada as a minimal-edit textbook Kannada sentence. "
        "Preserve meaning, person, politeness, tense, and question/statement form. Use examples only "
        "as guidance; do not copy their content. Prefer the rule-based draft when uncertain. Output "
        "only one Kannada sentence, without labels or explanations.\n"
        f"Examples:\n{few}\nDialect input: {source_text}\nRule-based draft: {draft}\nTextbook Kannada:"
    )
    model=model_override or os.getenv("GEMINI_MODEL",DEFAULT_MODEL)
    if not re.fullmatch(r"[a-zA-Z0-9.-]+",model):
        return draft,"LLM fallback: invalid GEMINI_MODEL"
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key="+key
    for attempt in range(2):
        try:
            response=requests.post(url,json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0,"maxOutputTokens":256}},timeout=12); response.raise_for_status()
            value=response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            if len(re.findall(r"[\u0C80-\u0CFF]",value))/max(1,len(value))<.45 or len(value)>2*max(1,len(draft)) or "\n" in value:return draft,"LLM rejected by output guard"
            cache[cache_key]=value; cache_file.write_text(json.dumps(cache,ensure_ascii=False),encoding="utf-8"); return value,"LLM refined"
        except Exception as exc:
            if attempt==0:time.sleep(.25)
            else:return draft,f"LLM fallback: {type(exc).__name__}"
    return draft,"LLM fallback"
