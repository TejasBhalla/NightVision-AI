import cv2
import numpy as np

# --- Colors per class (BGR) ---
# Now reindexed for 16 classes (auto rickshaw removed)
COLORS = {
    0: (0, 255, 0),       # bus - green
    1: (0, 200, 255),     # car - yellow-ish
    2: (255, 0, 0),       # motorbike - blue
    3: (255, 0, 255),     # truck - magenta
    4: (0, 165, 255),     # pothole - orange
    5: (0, 0, 255),       # person - red
    6: (128, 0, 128),     # cat - purple
    7: (0, 128, 128),     # chicken - teal
    8: (128, 128, 0),     # cow - olive
    9: (0, 128, 0),       # dog - dark green
    10: (128, 0, 0),      # fox - maroon
    11: (0, 0, 128),      # goat - navy
    12: (128, 128, 128),  # horse - gray
    13: (64, 64, 64),     # racoon - dark gray
    14: (0, 255, 255),    # skunk - cyan
    15: (255, 255, 0),    # SpeedBreaker - light blue
}

# --- Human-readable labels ---
LABELS = [
    'bus', 'car', 'motorbike', 'truck', 'pothole',
    'person', 'cat', 'chicken', 'cow', 'dog',
    'fox', 'goat', 'horse', 'racoon', 'skunk', 'SpeedBreaker'
]


def draw_glow_boxes(frame, boxes):
    """
    Draws glowing rectangles and labels for detected objects.
    - frame: numpy image (BGR)
    - boxes: list of dicts with {x1,y1,x2,y2,cls,conf}
    """
    overlay = frame.copy()

    for b in boxes:
        color = COLORS.get(b['cls'], (0, 255, 255))  # fallback yellow

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
        cls_name = LABELS[b['cls']] if b['cls'] < len(LABELS) else 'obj'
        label = f"{cls_name} {b['conf']:.2f}"
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

        # Label text
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
