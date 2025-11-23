"""Pydantic models exposed by the FastAPI layer."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x: float = Field(..., ge=0)
    y: float = Field(..., ge=0)
    width: float = Field(..., ge=0)
    height: float = Field(..., ge=0)


class DetectionResponse(BaseModel):
    label: str
    confidence: float = Field(..., ge=0, le=1)
    bbox: BoundingBox
    id: Optional[str]


class FrameResponse(BaseModel):
    stream_id: str
    detections: List[DetectionResponse]


class FrameSummary(BaseModel):
    frame_index: int
    detections: List[DetectionResponse]


class VideoAnalysisSummary(BaseModel):
    stream_id: str
    frame_count: int
    frames: List[FrameSummary]
