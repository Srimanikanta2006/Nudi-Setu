"""Five-stage Nudi Setu conversion pipeline."""
from __future__ import annotations
from pathlib import Path
from .normalize import normalize_text
from .glossary import load_glossary,match_phrase,map_words
from .rules import apply_rules
from .diffing import align_words
from .retrieval import find_exact_public_pair, get_similar_examples

ROOT=Path(__file__).resolve().parent.parent

def convert(text:str,dialect:str,use_llm:bool=False,glossary_path:str|Path|None=None,api_key:str|None=None,llm_model:str|None=None,use_local_llm:bool=False,local_model:str|None=None)->dict[str,object]:
    """Convert dialect text and expose every stage, hits, rules and alignment."""
    normalized=normalize_text(text); rows=load_glossary(glossary_path or ROOT/"data"/"glossary.csv")
    mapped,phrase_hits=match_phrase(normalized,dialect,rows); mapped,word_hits=map_words(mapped,dialect,rows)
    ruled,rule_hits=apply_rules(mapped); output=ruled; llm_note="LLM not requested"
    public_pair = find_exact_public_pair(normalized, dialect)
    if public_pair:
        mapped = ruled = output = public_pair["standard_text"]
        phrase_hits = [{"entry_id": f"public-{dialect}-exact", "source_title": public_pair.get("source_title", ""), "confidence": "needs_native_review"}]
        word_hits = []
        rule_hits = ["exact_public_source_pair"]
        llm_note = "Exact public-source match; native review still needed"
    examples = get_similar_examples(normalized, dialect) if (use_llm or use_local_llm) and not public_pair else []
    if use_local_llm and not public_pair:
        from .ollama import refine
        output,llm_note=refine(dialect,normalized,ruled,examples=examples,model=local_model)
    elif use_llm and not public_pair:
        from .llm import refine
        output,llm_note=refine(dialect,ruled,examples=examples,api_key=api_key,model_override=llm_model,source_text=normalized)
    return {"output":output,"stages":{"input":text,"normalized":normalized,"mapped":mapped,"grammar":ruled,"final":output},"hits":phrase_hits+word_hits,"rules":rule_hits,"alignment":align_words(text,output),"llm_note":llm_note,"public_source_reference":public_pair}
