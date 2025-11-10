from backend.differ.matcher import text_similarity

def test_text_sim():
    assert text_similarity('Ø150 mm','Ø150mm') > 0.9
    assert text_similarity('100','200') < 0.6
