import math
import re
import difflib

def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0]+boxA[2], boxB[0]+boxB[2])
    yB = min(boxA[1]+boxA[3], boxB[1]+boxB[3])
    interW = max(0, xB - xA)
    interH = max(0, yB - yA)
    interArea = interW*interH
    boxAArea = boxA[2]*boxA[3]
    boxBArea = boxB[2]*boxB[3]
    if boxAArea+boxBArea-interArea == 0: return 0
    return interArea / float(boxAArea + boxBArea - interArea)

def text_similarity(a,b):
    if not a or not b: return 0.0
    a = a.lower(); b = b.lower()
    nums_a = re.findall(r"\d+(?:\.\d+)?", a)
    nums_b = re.findall(r"\d+(?:\.\d+)?", b)
    num_score = 0
    if nums_a and nums_b:
        try:
            na = float(nums_a[0]); nb = float(nums_b[0])
            num_score = 1 - min(1, abs(na-nb)/max(1, (na+nb)/2))
        except:
            num_score = 0
    char_score = difflib.SequenceMatcher(None, a, b).ratio()
    if num_score>0:
        return 0.6*num_score + 0.4*char_score
    return char_score

def build_diff(A, B, threshold=0.75):
    entsA = A.get('entities', [])
    entsB = B.get('entities', [])
    usedB = set()
    changes = []
    chg_id = 1
    for ea in entsA:
        best = None
        best_score = 0
        for eb in entsB:
            if eb['id'] in usedB: continue
            sim_text = text_similarity(ea.get('text',''), eb.get('text',''))
            sim_spat = iou(ea.get('bbox_px'), eb.get('bbox_px'))
            score = 0.6*sim_text + 0.4*sim_spat
            if score > best_score:
                best_score = score
                best = eb
        if best and best_score >= threshold:
            usedB.add(best['id'])
            centroidA = (ea['bbox_px'][0]+ea['bbox_px'][2]/2, ea['bbox_px'][1]+ea['bbox_px'][3]/2)
            centroidB = (best['bbox_px'][0]+best['bbox_px'][2]/2, best['bbox_px'][1]+best['bbox_px'][3]/2)
            dist = math.hypot(centroidA[0]-centroidB[0], centroidA[1]-centroidB[1])
            if ea.get('text') and best.get('text') and ea.get('text').strip().lower() == best.get('text').strip().lower() and dist > 20:
                typ = 'moved'
            elif ea.get('text') and best.get('text') and ea.get('text').strip().lower() != best.get('text').strip().lower():
                typ = 'modified'
            else:
                typ = 'modified'
            changes.append({
                'change_id': f'chg_{chg_id:04d}',
                'type': typ,
                'entity_ref_before': ea['id'],
                'entity_ref_after': best['id'],
                'before': {'text': ea.get('text'), 'numeric_value': ea.get('numeric_value'), 'bbox_px': ea.get('bbox_px')},
                'after': {'text': best.get('text'), 'numeric_value': best.get('numeric_value'), 'bbox_px': best.get('bbox_px')},
                'similarity': round(best_score,2)
            })
            chg_id += 1
        else:
            changes.append({
                'change_id': f'chg_{chg_id:04d}',
                'type': 'removed',
                'entity_ref_before': ea['id'],
                'entity_ref_after': None,
                'before': {'text': ea.get('text'), 'numeric_value': ea.get('numeric_value'), 'bbox_px': ea.get('bbox_px')},
                'after': None,
                'similarity': 0.0
            })
            chg_id += 1
    for eb in entsB:
        if eb['id'] in usedB: continue
        changes.append({
            'change_id': f'chg_{chg_id:04d}',
            'type': 'added',
            'entity_ref_before': None,
            'entity_ref_after': eb['id'],
            'before': None,
            'after': {'text': eb.get('text'), 'numeric_value': eb.get('numeric_value'), 'bbox_px': eb.get('bbox_px')},
            'similarity': 0.0
        })
        chg_id += 1
    summary = {'added': sum(1 for c in changes if c['type']=='added'), 'removed': sum(1 for c in changes if c['type']=='removed'), 'modified': sum(1 for c in changes if c['type']=='modified'), 'moved': sum(1 for c in changes if c['type']=='moved')}
    out = {
        'base_drawing_id': A.get('drawing_id'),
        'revised_drawing_id': B.get('drawing_id'),
        'changes': changes,
        'summary': summary
    }
    return out
