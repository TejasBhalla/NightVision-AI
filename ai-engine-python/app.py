import os
import cv2
import tempfile
import time
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from inference.enhance import enhance_clahe, apply_gamma
from inference.detect import init_model, detect_objects
from inference.annotate import draw_glow_boxes

app = FastAPI(title="Night Vision AI Engine")
model = init_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # --- Save uploaded file to temporary path ---
    suffix = os.path.splitext(file.filename)[-1]
    in_fd, in_path = tempfile.mkstemp(suffix=suffix)
    out_fd, out_path = tempfile.mkstemp(suffix=".mp4")
    os.close(in_fd)
    os.close(out_fd)

    with open(in_path, "wb") as f:
        f.write(await file.read())

    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        return JSONResponse({"error": "Cannot open video file"}, status_code=400)

    # --- Video parameters ---
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 360)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    # --- Processing loop ---
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # --- Optional: print progress every 10 frames ---
        if frame_count % 10 == 0:
            if total_frames > 0:
                percent = (frame_count / total_frames) * 100
                elapsed = time.time() - start_time
                fps_now = frame_count / elapsed
                print(f"🟩 Processed {frame_count}/{total_frames} frames "
                      f"({percent:.1f}%) at {fps_now:.2f} FPS")
            else:
                print(f"🟩 Processed {frame_count} frames...")

        # --- Enhance ---
        if enhance:
            frame = enhance_clahe(frame)
            frame = apply_gamma(frame, gamma=1.4)

        # --- Detect ---
        boxes = detect_objects(model, frame) if detect else []

        # --- Annotate ---
        if glow and boxes:
            frame = draw_glow_boxes(frame, boxes)

        writer.write(frame)

    cap.release()
    writer.release()

    total_time = time.time() - start_time
    print(f"✅ Completed {frame_count} frames in {total_time:.2f}s "
          f"({frame_count / total_time:.2f} FPS avg)")

    # --- Return processed video file ---
    return FileResponse(
        out_path,
        media_type="video/mp4",
        filename="processed.mp4"
    )

@app.post("/detect")
async def detect(file: UploadFile = File(...), enhance: str = Form("true")):
    """
    Receives an uploaded image (JPG/PNG), optionally enhances it,
    runs YOLOv8 inference, and returns detections as JSON.
    """
    try:
        enhance_flag = enhance.lower() == "true"

        # Read image
        contents = await file.read()
        npimg = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Apply enhancement if requested
        if enhance_flag:
            frame = enhance_clahe(frame)
            frame = apply_gamma(frame, gamma=1.4)

        # Detect objects
        detections = detect_objects(model, frame)

        return JSONResponse(content={"detections": detections})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

