from ultralytics import YOLO
import numpy as np
import cv2

# ✅ Updated class list based on your merged dataset
CLASS_NAMES = [
    'bus', 'car', 'motorbike', 'truck',
    'pothole', 'person', 'cat', 'chicken', 'cow',
    'dog', 'fox', 'goat', 'horse', 'racoon', 'skunk', 'SpeedBreaker'
]

# You can select which ones you want to display/detect
INTERESTING = set(range(len(CLASS_NAMES)))  # all classes

_model = None

def init_model():
    """Load the custom YOLOv8/YOLO11 model (trained on merged dataset)."""
    global _model
    if _model is None:
        # ✅ Replace this path with your trained model's .pt file
        _model = YOLO("../runs/detect/merged_V4_11n_finetune/weights/best.pt")
        # or if training saved somewhere else:
        # _model = YOLO("C:/Users/TEJAS/Documents/NightVision/ai-engine-python/runs/detect/merged_dataset_11n/weights/best.pt")
        _model.to("cuda:0")  # optional GPU acceleration
    return _model


def detect_objects(model, frame, conf=0.35):
    """
    Detect objects in a single frame (numpy BGR image).
    Returns list of boxes in format:
    [{'x1':..,'y1':..,'x2':..,'y2':..,'cls':..,'name':..,'conf':..}, ...]
    """
    results = model.predict(source=frame, conf=conf, verbose=False)
    return _extract_boxes(results)


def _extract_boxes(results):
    """Convert YOLO results -> list of detections for a single frame."""
    boxes = []
    for r in results:
        if r.boxes is None:
            continue
        for b in r.boxes:
            cls = int(b.cls.item())
            if cls not in INTERESTING:
                continue
            x1, y1, x2, y2 = map(lambda x: int(x.item()), b.xyxy[0])
            boxes.append({
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "cls": cls,
                "name": CLASS_NAMES[cls] if cls < len(CLASS_NAMES) else "unknown",
                "conf": float(b.conf.item())
            })
    return boxes
