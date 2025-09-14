import cv2
import numpy as np

def enhance_clahe(frame):
    """Enhance low-light road frame using CLAHE + gamma correction."""
    # Convert to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE to L channel (reduce clipLimit for roads)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)

    # Merge channels and convert back to BGR
    lab = cv2.merge((cl, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def apply_gamma(frame, gamma=1.4):
    """Apply gamma correction."""
    invGamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** invGamma * 255
                      for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(frame, table)