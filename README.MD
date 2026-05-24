# NightVision AI Engine

NightVision AI Engine is a full-stack project for enhancing low-light videos and running object detection on night scenes. It combines a FastAPI AI service (OpenCV + YOLO) with a Node.js backend for video upload/streaming and a React + Vite frontend for the UI, plus dataset utilities for building YOLO training sets.

## Features

- Video enhancement with CLAHE and gamma correction
- Object detection using a custom YOLO model
- Glow-style annotations for detected objects
- Video upload API with range streaming support for MP4 playback
- Real-time webcam detection endpoint and UI
- Dataset merge/split utilities for YOLO training

## Architecture

- Frontend (React + Vite): Uploads video, toggles options, shows original video, and triggers processing. Also supports real-time webcam detection.
- Backend (Node.js + Express): Receives video uploads and forwards them to the AI service, then streams back the processed MP4.
- AI Engine (FastAPI + OpenCV + Ultralytics): Enhances frames, runs YOLO, draws glow boxes, and returns a processed MP4 or JSON detections.

## Repository Structure

- ai-engine-python/ - FastAPI service, inference utilities, and dataset scripts
- backend/ - Node.js API server for uploads and streaming
- frontend/ - React UI (Vite + Tailwind)
- runs/ - YOLO training outputs and model weights
- uploads/ - Uploaded videos (backend)

## Quick Start

### 1) AI Engine (FastAPI)

From the project root:

```
cd ai-engine-python
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

The FastAPI service exposes:

- POST /process - Process a video file and return MP4
- POST /detect - Run detection on a single image and return JSON

### 2) Backend (Node.js)

```
cd backend
npm install
npm run dev
```

Backend runs on port 8080 by default and exposes:

- GET /health
- POST /api/process/upload (multipart form-data, field: video)

### 3) Frontend (React)

```
cd frontend
npm install
npm run dev
```

The UI runs on http://localhost:5173 and expects:

- Backend at http://localhost:8080
- AI Engine at http://localhost:8000

## Configuration

Backend environment variables:

- PORT (default 8080)
- MAX_UPLOAD_MB (default 200)

AI Engine model path is configured in ai-engine-python/inference/detect.py:

- _model = YOLO("../runs/detect/merged_V4_11n_finetune/weights/best.pt")

Update this path to your trained model if needed. GPU is enabled by default via model.to("cuda:0").

## API Details

### POST /api/process/upload (backend)

- Form fields:
	- video: MP4 or other video file
	- enhance: true/false (string)
	- detect: true/false (string)
	- glow: true/false (string)
- Response: processed MP4 stream (supports range requests)

### POST /process (AI Engine)

- Form fields:
	- file: video file
	- enhance, detect, glow: true/false (string)
- Response: processed MP4

### POST /detect (AI Engine)

- Form fields:
	- file: image (JPG/PNG)
	- enhance: true/false (string)
- Response: { detections: [ { x1, y1, x2, y2, cls, name, conf } ] }

## Dataset Utilities

The ai-engine-python directory includes scripts for dataset preparation:

- merge_yolo_datasets.py: Merge multiple datasets into a single YOLO dataset with unified classes
- merge_datasetsV2.py: Merge with name normalization and class remapping
- auto.py: Create merged_V3 by reindexing classes and removing auto rickshaw
- split_dataset.py: Split a dataset into train/valid/test

These scripts assume dataset folders under ai-engine-python/datasets and write YOLO-formatted outputs.

## Notes

- Frontend currently triggers download of the processed video (Blob) after processing.
- Real-time detection uses the webcam and calls the AI Engine /detect endpoint every ~500 ms.
- CORS is configured for http://localhost:5173 on both backend and AI engine.

## Tech Stack

- Frontend: React 19, Vite 7, Tailwind 4, Zustand, Framer Motion
- Backend: Node.js, Express 5, Multer, Axios
- AI Engine: FastAPI, OpenCV, Ultralytics YOLO, Torch

## License

ISC (backend package.json)