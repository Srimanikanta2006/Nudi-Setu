from pathlib import Path

from nudisetu.glossary import load_glossary, map_words
from nudisetu.rules import apply_rules

ROOT = Path(__file__).resolve().parents[1]


def test_hubballi_word_mapping_does_not_corrupt_standard_substrings():
    rows = load_glossary(ROOT / "data" / "glossary.csv")
    output, hits = map_words("ಅದರ ಬಣ್ಣ ಚೆನ್ನಾಗಿದೆ", "Hubballi-Dharwad", rows)
    assert output == "ಅದರ ಬಣ್ಣ ಚೆನ್ನಾಗಿದೆ"
    assert not hits


def test_mangaluru_word_mapping_does_not_match_inside_loanword():
    rows = load_glossary(ROOT / "data" / "glossary.csv")
    output, hits = map_words("ಸ್ಕ್ಯಾನ್ ಮಾಡಿ ಕಳುಹಿಸಿ", "Mangaluru", rows)
    assert output == "ಸ್ಕ್ಯಾನ್ ಮಾಡಿ ಕಳುಹಿಸಿ"
    assert not hits


def test_grammar_rules_do_not_match_inside_unrelated_words():
    output, hits = apply_rules("ಮ್ಯಾಕ್ ಮತ್ತು ವಿಂಡೋಸ್")
    assert output == "ಮ್ಯಾಕ್ ಮತ್ತು ವಿಂಡೋಸ್"
    assert not hits
