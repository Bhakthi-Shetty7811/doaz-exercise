from backend.extractor.postprocess import parse_dimension

def test_parse_dimension():
    assert parse_dimension("Ø150 mm ±0.5") == {'text':'Ø150 mm ±0.5','numeric_value':150,'unit':'mm','tolerance':'±0.5'}
    assert parse_dimension("φ12in") == {'text':'φ12in','numeric_value':12,'unit':'in','tolerance':None}
    assert parse_dimension("100 x 200 mm") == {'text':'100 x 200 mm','numeric_value':100,'unit':'mm','tolerance':None}
