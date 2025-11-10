from backend.extractor.normalize import normalize_text

def test_normalize_basic():
    assert normalize_text('  Ø150  ') == 'Ø150'
    assert 'φ' in normalize_text('phi')
