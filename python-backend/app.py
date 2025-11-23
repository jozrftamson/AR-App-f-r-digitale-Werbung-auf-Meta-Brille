"""FastAPI backend for logo detection + tracking in video frames."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import List

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from detector import detect_logos
from domain import LogoDetection
from schemas import (
    BoundingBox,
    DetectionResponse,
    FrameResponse,
    FrameSummary,
    VideoAnalysisSummary,
)
from tracking import TrackerRegistry

app = FastAPI(title="Logo Tracker API", description="Video/logo detection demo", version="0.1.0")
tracker_registry = TrackerRegistry()


def _to_schema(det: LogoDetection) -> DetectionResponse:
    return DetectionResponse(
        label=det.label,
        confidence=det.confidence,
        bbox=BoundingBox(**det.to_bbox_dict()),
        id=det.track_id,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze-frame", response_model=FrameResponse)
async def analyze_frame(
    file: UploadFile = File(..., description="JPEG/PNG frame"),
    stream_id: str = Form("default"),
    enable_tracking: bool = Form(True, description="Attach stable IDs across requests"),
) -> FrameResponse:
    data = await file.read()
    np_frame = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Failed to decode image. Ensure it is a valid JPEG/PNG frame.")

    detections = detect_logos(frame)
    if enable_tracking:
        tracker = tracker_registry.get_tracker(stream_id)
        detections = tracker.update(detections)
    else:
        tracker_registry.reset_tracker(stream_id)

    response = FrameResponse(stream_id=stream_id, detections=[_to_schema(det) for det in detections])
    return response


@app.post("/analyze-video", response_model=VideoAnalysisSummary)
async def analyze_video(
    file: UploadFile = File(..., description="MP4/MOV video"),
    stream_id: str = Form("video-1"),
    stride: int = Form(5, ge=1, description="Process every Nth frame to save CPU"),
    max_frames: int = Form(200, ge=1, description="Max frames to process for this demo"),
) -> VideoAnalysisSummary:
    """Naive video ingestion endpoint.

    For production you would offload this job to a worker/queue and optionally return a job id.
    """

    video_bytes = await file.read()
    suffix = Path(file.filename or "upload.mp4").suffix or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(video_bytes)
        temp_path = tmp.name

    tracker_registry.reset_tracker(stream_id)
    tracker = tracker_registry.get_tracker(stream_id)

    cap = cv2.VideoCapture(temp_path)
    if not cap.isOpened():
        os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Could not open uploaded video.")

    frames: List[FrameSummary] = []
    frame_idx = 0
    processed = 0

    while processed < max_frames:
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        if frame_idx % stride == 0:
            detections = tracker.update(detect_logos(frame))
            frames.append(FrameSummary(frame_index=frame_idx, detections=[_to_schema(det) for det in detections]))
            processed += 1
        frame_idx += 1

    cap.release()
    os.remove(temp_path)

    return VideoAnalysisSummary(stream_id=stream_id, frame_count=frame_idx, frames=frames)


# Notes for frontend integration:
# - POST /analyze-frame with multipart form-data ("file" field) from HTML Canvas or <video> snapshot.
# - Receive JSON response and draw the returned bounding boxes using Canvas 2D or WebGL overlays.
# - To visualize processed frames on the backend, extend this service with a /stream endpoint returning MJPEG or WebSocket updates.
