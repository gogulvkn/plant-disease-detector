# Run once, next to your weights:  python export_model.py
import json
from ultralytics import YOLO

m = YOLO("weights/plant_best.pt")
m.export(format="onnx", imgsz=640, opset=12)          # creates weights/plant_best.onnx
json.dump(list(m.names.values()), open("classes.json", "w"))
print("Done. Copy weights/plant_best.onnx -> best.onnx and classes.json into the Space.")
