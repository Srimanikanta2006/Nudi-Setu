from nudisetu.rules import apply_rules
def test_contracted_verb(): assert apply_rules('ನಾನು ಬರ್ತೀನಿ')[0]=='ನಾನು ಬರುತ್ತೇನೆ'
def test_progressive(): assert apply_rules('ನೀವು ಮಾಡ್ತಾ ಇದ್ದೀರಿ')[0]=='ನೀವು ಮಾಡುತ್ತಿದ್ದೀರಿ'
