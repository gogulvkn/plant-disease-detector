import io
import os
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from PIL import Image
from ultralytics import YOLO

BASE = Path(__file__).parent
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE / "weights" / "plant_best.pt"))
MAX_BYTES = 10 * 1024 * 1024

app = FastAPI(title="Verdant Plant Disease Detector")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

model = YOLO(MODEL_PATH)


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "classes": list(model.names.values())}


@app.post("/detect")
async def detect(file: UploadFile = File(...), conf: float = 0.25):
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Image too large (max 10 MB).")
    try:
        img = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        raise HTTPException(400, "Could not read the image.")
    result = model.predict(img, conf=conf, verbose=False)[0]
    dets = [
        {
            "class": model.names[int(b.cls)],
            "conf": round(float(b.conf), 4),
            "box": [round(v, 1) for v in b.xyxy[0].tolist()],
        }
        for b in result.boxes
    ]
    return sorted(dets, key=lambda d: d["conf"], reverse=True)
