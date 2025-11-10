# Doaz Mini Viewer

**Doaz Mini Viewer** is a lightweight web-based tool for extracting textual and dimensional data from engineering drawings (PDFs or images) and comparing different versions to detect changes. It’s ideal for quickly identifying modifications, additions, or removals in drawings without manual inspection.

---

## Features

- **OCR-based extraction** of dimensions and annotations from PDF or image files.
- **Symbol & unit recognition** including `Ø`, `±`, `φ`, and metric units like `mm`.
- **Bounding box detection** for precise entity locations on the drawing.
- **Diff comparison** between two drawings:
  - Detects **added**, **removed**, **modified**, and **moved** entities.
  - Shows similarity scores and positional differences.
- **Fast performance**:
  - Extraction: ≤ 3 seconds (depending on image size)
  - Diff computation: ≤ 1 second
- **Simple frontend** interface for uploading drawings and viewing extracted JSON and diffs.

---

## Backend

- **Framework:** FastAPI  
- **OCR Engine:** Tesseract (`pytesseract`)  
- **Image Processing:** OpenCV & PIL  
- **PDF Conversion:** `pdf2image`  
- **Endpoints:**
  - `GET /healthz` – Health check
  - `POST /extract` – Extracts entities from a PDF/image file
  - `POST /diff` – Compares two extracted JSON outputs for changes

### Example `/extract` Response

```json
{
  "drawing_id": "A3-JGS1EP-HAN-DD-E-0414R-001_R0",
  "page": 1,
  "image_size_px": {"width": 3509, "height": 2480},
  "scale_note": null,
  "entities": [
    {
      "id": "ent_0000",
      "type": "dimension",
      "text": "2",
      "numeric_value": 2,
      "unit": null,
      "tolerance": null,
      "bbox_px": [375, 2444, 8, 12],
      "anchor_points_px": null,
      "confidence": 0.9
    }
  ],
  "meta": {
    "extraction_time_ms": 2334,
    "engine_versions": {
      "ocr": "5.5.0.20241111",
      "detector": "opencv-contours"
    }
  }
}
````

### Example `/diff` Response

```json
{
  "base_drawing_id": "A3-JGS1EP-HAN-DD-E-0414R-001_R0",
  "revised_drawing_id": "A3-JGS1EP-HAN-DD-E-0408B-001_RC",
  "changes": [
    {
      "change_id": "chg_0001",
      "type": "removed",
      "entity_ref_before": "ent_0000",
      "entity_ref_after": null,
      "before": {"text": "2", "numeric_value": 2, "bbox_px": [375, 2444, 8, 12]},
      "after": null,
      "similarity": 0
    }
  ],
  "summary": {
    "added": 14,
    "removed": 14,
    "modified": 0,
    "moved": 0
  }
}
```

---

## Frontend

* **Framework:** React + TypeScript
* Simple UI to:

  * Upload **Base (A)** and **Revised (B)** drawings
  * Extract JSON for each file
  * Run a diff comparison to visualize changes
* JSON outputs and diffs are shown in formatted, scrollable `<pre>` blocks.

---

## Installation

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate         
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

* Frontend runs at `http://localhost:3000`
* Backend runs at `http://localhost:8000`

---

## Usage

1. Open the frontend in your browser.
2. Upload your **Base** drawing (A) and click **Extract A**.
3. Upload your **Revised** drawing (B) and click **Extract B**.
4. Click **Run Diff** to see added, removed, modified, or moved entities between the two drawings.

---

## Notes

* Current implementation supports **single-page extraction**.
* Recognizes common **dimension symbols** and **units**, but may need fine-tuning for complex layouts.
* Anchor points and scale notes are placeholders (`null`) — can be implemented in future updates.
* Extraction times vary with image resolution and PDF size (≈2–3s for standard drawings).

---

## Future Improvements

* Multi-page PDF support
* Scale note extraction
* Anchor point detection for entities
* Performance optimization for large drawings
* Highlight changes visually on the frontend


