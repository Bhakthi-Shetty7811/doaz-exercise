import unicodedata
import re

def normalize_text(s: str) -> str:
    if not s: return ''
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('phi', 'φ').replace('diam', 'Ø').replace('+/-','±')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

