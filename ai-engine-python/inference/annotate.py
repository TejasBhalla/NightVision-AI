import cv2
import numpy as np

# Colors per class (BGR format for OpenCV)
COLORS = {
    0: (255, 255, 255), # person - white
    2: (0, 255, 0),     # car - green
    3: (0, 200, 255),   # motorcycle - yellow-ish
    5: (255, 0, 0),     # bus - blue
    7: (255, 0, 255),   # truck - magenta
    15: (0, 165, 255),  # cat - orange
    16: (0, 0, 255),    # dog - red
}

# Human-readable labels
LABELS = {
    0: 'person',
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck',
    15: 'cat',
    16: 'dog'
}

def draw_glow_boxes(frame, boxes):
    """
    Draws glowing rectangles and labels for detected objects.
    - frame: numpy image (BGR)
    - boxes: list of dicts with {x1,y1,x2,y2,cls,conf}
    """
    overlay = frame.copy()

    for b in boxes:
        color = COLORS.get(b['cls'], (0, 255, 255))  # default yellow
        # Outer glow effect (thick fading rectangles)
        for t in [8, 6, 4, 2]:
            cv2.rectangle(
                overlay,
                (b['x1'], b['y1']),
                (b['x2'], b['y2']),
                color,
                thickness=t
            )

        # Label text (class + confidence)
        label = f"{LABELS.get(b['cls'], 'obj')} {b['conf']:.2f}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        x, y = b['x1'], max(0, b['y1'] - th - 6)

        # Label background box
        cv2.rectangle(
            overlay,
            (x, y),
            (x + tw + 6, y + th + 6),
            color,
            thickness=-1
        )

        # Label text itself
        cv2.putText(
            overlay,
            label,
            (x + 3, y + th + 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),  # black text
            thickness=1,
            lineType=cv2.LINE_AA
        )

    # Blend overlay with original to make glow soft
    return cv2.addWeighted(overlay, 0.35, frame, 0.65, 0)
