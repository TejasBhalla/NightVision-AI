import os
import cv2
import tempfile
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

    # Save uploaded file to temp
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

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 360)
    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Enhance
        if enhance:
            frame = enhance_clahe(frame)
            frame = apply_gamma(frame, gamma=1.4)

        # Detect
        boxes = detect_objects(model, frame) if detect else []

        # Glow boxes
        if glow and boxes:
            frame = draw_glow_boxes(frame, boxes)

        writer.write(frame)

    cap.release()
    writer.release()

    # ✅ Return the processed file directly instead of JSON
    return FileResponse(
        out_path,
        media_type="video/mp4",
        filename="processed.mp4"
    )
