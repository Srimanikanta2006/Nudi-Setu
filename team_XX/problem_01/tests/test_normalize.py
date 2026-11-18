from nudisetu.normalize import normalize_text
def test_unicode_cleanup():
    assert normalize_text('  ಕನ್ನಡ\u200d  !! ')=='ಕನ್ನಡ!'
