"""Conservative, inspectable Kannada normalization rules."""
from __future__ import annotations
import re

# Seed hypotheses only; uncertain regional forms need native-speaker verification.
RULES=[
 (r"ಮಾಡ್ತಾ\s+ಇದ್ದೀನಿ","ಮಾಡುತ್ತಿದ್ದೇನೆ","progressive_first_person"),
 (r"ಮಾಡ್ತಾ\s+ಇದ್ದೀರಿ","ಮಾಡುತ್ತಿದ್ದೀರಿ","progressive_honorific"),
 (r"ಮಾಡ್ತಾ\s+ಇದ್ದಾನೆ","ಮಾಡುತ್ತಿದ್ದಾನೆ","progressive_masculine"),
 (r"ಮಾಡ್ತಾ\s+ಇದ್ದಾಳೆ","ಮಾಡುತ್ತಿದ್ದಾಳೆ","progressive_feminine"),
 (r"ಮಾಡ್ತಾ\s+ಇದ್ದಾರೆ","ಮಾಡುತ್ತಿದ್ದಾರೆ","progressive_plural"),
 (r"ಬರ್ತೀನಿ","ಬರುತ್ತೇನೆ","present_first_person_baru"),
 (r"ಹೋಗ್ತೀನಿ","ಹೋಗುತ್ತೇನೆ","present_first_person_hogu"),
 (r"ಬರ್ತೀರಾ","ಬರುತ್ತೀರಾ","present_honorific_baru"),
 (r"ಹೋಗ್ತೀರಾ","ಹೋಗುತ್ತೀರಾ","present_honorific_hogu"),
 (r"ಮಾಡ್ತೀನಿ","ಮಾಡುತ್ತೇನೆ","present_first_person_madu"),
 (r"ಮಾಡ್ತೀರಾ","ಮಾಡುತ್ತೀರಾ","present_honorific_madu"),
 (r"ಏನ್ರಿ","ಏನು","hubli_honorific_interrogative"),
 (r"ಏನ್","ಏನು","colloquial_interrogative_en"),
 (r"ಎಂತ","ಏನು","mangaluru_interrogative"),
 (r"ಹೆಂಗಿದ್ದೀರಿ","ಹೇಗಿದ್ದೀರಿ","uttara_how_are_you"),
 (r"ಹೆಂಗ್?","ಹೇಗೆ","colloquial_henge"),
 (r"ಹೆಂಗ","ಹೇಗೆ","colloquial_henga"),
 (r"ಯಾಕ","ಯಾಕೆ","colloquial_yaka"),
 (r"ಆತೇನ್ರಿ","ಆಯಿತೇ","hubli_past_question"),
]

_WORD_BOUNDARY_LEFT = r"(?<![\w\u0c80-\u0cff])"
_WORD_BOUNDARY_RIGHT = r"(?![\w\u0c80-\u0cff])"

def apply_rules(text: str) -> tuple[str,list[str]]:
    """Apply ordered regex rules and return output plus unique rule identifiers."""
    applied=[]
    for pattern,replacement,rule_id in RULES:
        # These are word/phrase substitutions. Keep them from matching inside
        # unrelated words such as "ಯಾಕ" inside a transliterated loanword.
        bounded_pattern=f"{_WORD_BOUNDARY_LEFT}(?:{pattern}){_WORD_BOUNDARY_RIGHT}"
        new,count=re.subn(bounded_pattern,replacement,text)
        if count and new!=text:
            text=new
            if rule_id not in applied: applied.append(rule_id)
    return text,applied
