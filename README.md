---
title: Verdant Plant Disease Detector
emoji: 🌿
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# Verdant: Plant Disease Detector

Upload a leaf photo and a YOLO11s model draws bounding boxes around diseased regions.
Trained on the [Plant Disease Detection Bounding Box Dataset](https://www.kaggle.com/datasets/mahin661/plant-disease-detection-bounding-box-dataset).

## Project layout

```
app.py              FastAPI server (API + serves the web page)
static/index.html   Front-end
weights/            Put plant_best.pt here
Dockerfile          For Hugging Face Spaces / any Docker host
requirements.txt
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# copy your trained weights to weights/plant_best.pt
uvicorn app:app --reload
```

Open http://127.0.0.1:8000 for the UI or http://127.0.0.1:8000/docs for the API.

## API

`POST /detect?conf=0.25` with multipart field `file`:

```json
[{"class": "Tomato_Late_blight", "conf": 0.91, "box": [34.0, 50.2, 210.5, 190.8]}]
```

`GET /health` lists the model's classes.

## Deploy

**Hugging Face Spaces (free, Docker)**

1. Create a new Space, choose SDK **Docker**.
2. Clone it and copy all files here into it.
3. Weights are over 10 MB, so use Git LFS: `git lfs install` (the `.gitattributes` already tracks `*.pt`).
4. `git add . && git commit -m "deploy" && git push`

**Render / Railway / any Docker host**

Build the Dockerfile and expose the port. Set the port to 7860, or change it in the `CMD` line.

## Notes

Detections are a screening aid. Confirm with an agronomist before treating a crop.
