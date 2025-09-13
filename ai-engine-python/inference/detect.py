from ultralytics import YOLO
import numpy as np
import cv2

# Classes we care about (COCO)
INTERESTING = {0, 1, 2, 3, 5, 7, 15, 16, 19}
COCO_CLASSES = {
    0:'person', 1:'bicycle', 2:'car', 3:'motorcycle', 5:'bus', 7:'truck',
    15:'cat', 16:'dog', 19:'cow'
}

_model = None

def init_model():
    """Load YOLOv8 once globally (small & fast)."""
    global _model
    if _model is None:
        _model = YOLO("yolov8n.pt")  # replace with your model path if custom
        _model.to("cuda:0")           # optional, remove if using CPU
    return _model


def detect_objects(model, frame, conf=0.35):
    """
    Detect objects in a single frame (numpy BGR image).
    Returns list of boxes in format:
    [{'x1':..,'y1':..,'x2':..,'y2':..,'cls':..,'name':..,'conf':..}, ...]
    """
    results = model.predict(source=frame, conf=conf, verbose=False)
    return _extract_boxes(results)


# ---------------- Helpers ----------------
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
                "name": COCO_CLASSES.get(cls, "unknown"),
                "conf": float(b.conf.item())
            })
    return boxes
