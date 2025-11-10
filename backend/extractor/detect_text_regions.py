import cv2

def detect_text_regions(gray, closed):
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    h, w = gray.shape
    for c in contours:
        x,y,ww,hh = cv2.boundingRect(c)
        if ww < 8 or hh < 8: continue
        if ww > w*0.9 and hh > h*0.9: continue
        boxes.append((x,y,ww,hh))
    boxes = sorted(boxes, key=lambda b: (b[0],b[1]))
    merged = []
    for b in boxes:
        if not merged:
            merged.append(b)
            continue
        x,y,ww,hh = b
        px,py,pw,ph = merged[-1]
        if x < px+pw and y < py+ph:
            nx = min(x,px)
            ny = min(y,py)
            nr = max(px+pw, x+ww) - nx
            nb = max(py+ph, y+hh) - ny
            merged[-1] = (nx,ny,nr,nb)
        else:
            merged.append(b)
    return merged
