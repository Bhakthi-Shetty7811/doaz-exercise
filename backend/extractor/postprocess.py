from .normalize import normalize_text
import re

DIM_REGEXES = [
    re.compile(r"(?P<symbol>[\u00D8\u03C6Øφ]?)\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>mm|in)?\s*(?P<tolerance>±\s*\d+(?:\.\d+)?)?", re.I),
    re.compile(r"(?P<value>\d+(?:\.\d+)?)\s*[x×]\s*(?P<value2>\d+(?:\.\d+)?)\s*(?P<unit>mm|in)?", re.I)
]

def parse_dimension(text):
    if not text: return None
    t = text.replace('\n',' ').strip()
    for rx in DIM_REGEXES:
        m = rx.search(t)
        if m:
            gd = m.groupdict()
            num = None
            unit = None
            tol = None
            if gd.get('value'):
                try:
                    num = float(gd['value'])
                except:
                    num = None
            if gd.get('unit'):
                unit = gd['unit']
            if gd.get('tolerance'):
                tol = gd['tolerance']
            return {'text': t, 'numeric_value': num, 'unit': unit, 'tolerance': tol}
    return {'text': t, 'numeric_value': None, 'unit': None, 'tolerance': None}

def build_entity(ocr_result):
    text = normalize_text(ocr_result.get('text',''))
    parsed = parse_dimension(text)
    ent = {
        'id': ocr_result.get('id'),
        'type': 'dimension' if parsed and parsed['numeric_value'] is not None else 'annotation',
        'text': parsed['text'] if parsed else text,
        'numeric_value': parsed['numeric_value'] if parsed else None,
        'unit': parsed['unit'] if parsed else None,
        'tolerance': parsed['tolerance'] if parsed else None,
        'bbox_px': ocr_result.get('bbox'),
        'anchor_points_px': None,
        'confidence': ocr_result.get('conf', 0.0)
    }
    return ent
