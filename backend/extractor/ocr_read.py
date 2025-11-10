import pytesseract
import cv2

TESS_CONFIG = r"-l eng --oem 1 --psm 6 -c tessedit_char_whitelist=0123456789.+-xX Øφ/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZmmin"

def get_tesseract_version():
    try:
        return str(pytesseract.get_tesseract_version())
    except:
        return 'unknown'

def ocr_on_boxes(img, boxes):
    results = []
    for i,(x,y,ww,hh) in enumerate(boxes):
        crop = img[y:y+hh, x:x+ww]
        try:
            txt = pytesseract.image_to_string(crop, config=TESS_CONFIG)
        except Exception:
            txt = ''
        txt = txt.strip()
        results.append({'id': f'ent_{i:04d}', 'text': txt, 'bbox': [int(x),int(y),int(ww),int(hh)], 'conf': 0.9})
    return results
