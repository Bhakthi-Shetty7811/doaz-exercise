from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import io, os, re, tempfile
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, UnidentifiedImageError
from backend.extractor import preprocess, detect_text_regions, ocr_read, postprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    print("\n===== /extract called =====")
    print(f"Filename received: {file.filename}")
    print(f"Content-Type: {file.content_type}")

    # --- Read file bytes once ---
    data = await file.read()
    print(f"File size: {len(data)} bytes")

    # --- Sanitize filename ---
    filename = os.path.splitext(file.filename)[0]
    filename = re.sub(r"[^\w\-]+", "_", filename)
    drawing_id = filename[:50]

    # --- Handle PDF or Image ---
    pil_image = None
    try:
        if ".pdf" in file.filename.lower():
            print("Detected PDF file — starting conversion...")
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(data)
                    tmp.flush()
                    tmp_path = tmp.name
                    print(f"Temporary PDF path: {tmp_path}")

                pages = convert_from_path(tmp_path, dpi=300)
                print(f"PDF converted successfully. Total pages: {len(pages)}")

                if not pages:
                    raise ValueError("No pages found in PDF.")
                pil_image = pages[0]
            except Exception as e:
                print(f"[ERROR] PDF conversion failed: {e}")
                raise HTTPException(status_code=400, detail=f"PDF conversion failed: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    print("Temporary file removed.")
        else:
            print("Detected image file — trying to open with PIL...")
            try:
                pil_image = Image.open(io.BytesIO(data))
                print("Image opened successfully.")
            except UnidentifiedImageError:
                print("[ERROR] UnidentifiedImageError — invalid image format")
                raise HTTPException(status_code=400, detail="Invalid image format.")
    except Exception as e:
        print(f"[ERROR] General file conversion failure: {e}")
        raise HTTPException(status_code=400, detail=f"File conversion failed: {str(e)}")

    # --- Convert PIL → numpy ---
    try:
        img = np.array(pil_image)
        print("Image converted to NumPy array successfully.")
    except Exception as e:
        print(f"[ERROR] PIL to NumPy conversion failed: {e}")
        raise HTTPException(status_code=400, detail=f"Image conversion failed: {str(e)}")

    # --- Core Extraction Pipeline ---
    print("Starting OCR pipeline...")
    start = time.time()
    gray, proc = preprocess.preprocess_gray(img)
    boxes = detect_text_regions(gray, proc)
    ocrs = ocr_read.ocr_on_boxes(img, boxes)
    entities = [postprocess.build_entity(o) for o in ocrs]

    out = {
        "drawing_id": drawing_id,
        "page": 1,
        "image_size_px": {"width": img.shape[1], "height": img.shape[0]},
        "scale_note": None,
        "entities": entities,
        "meta": {
            "extraction_time_ms": int((time.time() - start) * 1000),
            "engine_versions": {
                "ocr": ocr_read.get_tesseract_version(),
                "detector": "opencv-contours",
            },
        },
    }

    print("Extraction completed successfully ✅")
    return out


if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)

