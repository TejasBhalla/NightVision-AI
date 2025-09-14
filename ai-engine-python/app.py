import os
import cv2
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from inference.enhance import enhance_clahe , apply_gamma
from inference.detect import init_model, detect_objects
from inference.annotate import draw_glow_boxes

app = FastAPI(title="Night Vision AI Engine")
model = init_model()


def iterfile(path: str):
    """Stream file in chunks and remove it afterwards."""
    try:
        with open(path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk
    finally:
        try:
            os.remove(path)
        except Exception:
            pass


@app.post("/process")
async def process_video(
    file: UploadFile = File(...),
    enhance: str = Form("true"),
    detect: str = Form("true"),
    glow: str = Form("true"),
):
    enhance = enhance.lower() == "true"
    detect = detect.lower() == "true"
    glow = glow.lower() == "true"

    # Save uploaded file to temp
    suffix = os.path.splitext(file.filename)[-1]
    in_fd, in_path = tempfile.mkstemp(suffix=suffix)
    out_fd, out_path = tempfile.mkstemp(suffix=".mp4")
    os.close(in_fd)
    os.close(out_fd)

    with open(in_path, "wb") as f:
        f.write(await file.read())

    print("[INFO] Processing video...")
    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        return {"error": "Cannot open video file"}

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 360)
    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        print(f"[PROCESS] Frame {frame_idx} -> Enhancing/Detecting...")

        # --- Enhance (CLAHE) ---
        if enhance:
            frame = enhance_clahe(frame)
            frame = apply_gamma(frame, gamma=1.4)

        # --- Detect (YOLO) ---
        if detect:
            boxes = detect_objects(model, frame)
        else:
            boxes = []

        # --- Glow Boxes ---
        if glow and boxes:
            frame = draw_glow_boxes(frame, boxes)

        writer.write(frame)

    cap.release()
    writer.release()
    print("[INFO] Video processing complete ✅")

    return StreamingResponse(iterfile(out_path), media_type="video/mp4")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
