import io
from PIL import Image
import numpy as np
import cv2

def read_imagefile(filebytes) -> 'np.ndarray':
    img = Image.open(io.BytesIO(filebytes))
    img = img.convert('RGB')
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def preprocess_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV,15,9)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=1)
    return gray, closed
