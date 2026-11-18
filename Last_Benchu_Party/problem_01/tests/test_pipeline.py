from nudisetu.pipeline import convert

def test_official_hubballi_example():
    assert convert('ಏನ್ರಿ, ಊಟ ಆತೇನ್ರಿ?','Hubballi-Dharwad')['output']=='ಏನು, ಊಟ ಆಯಿತೇ?'
def test_official_mangaluru_example():
    assert convert('ಎಂತ ಮಾಡ್ತಾ ಇದ್ದೀರಿ?','Mangaluru')['output']=='ಏನು ಮಾಡುತ್ತಿದ್ದೀರಿ?'
def test_official_uttara_kannada_example():
    assert convert('ಹೆಂಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರ್ತೀರಾ?','Uttara Kannada')['output']=='ಹೇಗಿದ್ದೀರಿ, ಊಟಕ್ಕೆ ಬರುತ್ತೀರಾ?'

def test_public_mangaluru_source_pair_matches_exactly():
    result=convert('ಬೇಗ ಮಂಗಳೂರಿಗೆ ಎತ್ತಬೇಕು.','Mangaluru')
    assert result['output']=='ಬೇಗ ಮಂಗಳೂರಿಗೆ ತಲುಪಬೇಕು.'
    assert result['public_source_reference']['source_license']=='CC BY-SA 4.0'
    assert result['llm_note']=='Exact public-source match; native review still needed'

