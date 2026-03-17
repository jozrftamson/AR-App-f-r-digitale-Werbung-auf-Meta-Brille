"""Performance benchmarks for logo detection and tracking."""
from __future__ import annotations

import numpy as np
import pytest

from detector import detect_logos
from domain import LogoDetection
from tracking import SimpleTracker, _iou


# ---------------------------------------------------------------------------
# detector benchmarks
# ---------------------------------------------------------------------------

@pytest.mark.benchmark
def test_detect_logos_small_frame(small_frame: np.ndarray) -> None:
    """Benchmark logo detection on a 320x240 frame."""
    detect_logos(small_frame)


@pytest.mark.benchmark
def test_detect_logos_medium_frame(medium_frame: np.ndarray) -> None:
    """Benchmark logo detection on a 640x480 frame."""
    detect_logos(medium_frame)


# ---------------------------------------------------------------------------
# tracking benchmarks
# ---------------------------------------------------------------------------

@pytest.mark.benchmark
def test_iou_overlapping() -> None:
    """Benchmark IoU computation for two overlapping detections."""
    a = LogoDetection(label="A", confidence=0.9, x=10, y=10, width=100, height=100)
    b = LogoDetection(label="A", confidence=0.9, x=50, y=50, width=100, height=100)
    _iou(a, b)


@pytest.mark.benchmark
def test_tracker_update_cycle(small_frame: np.ndarray) -> None:
    """Benchmark a tracker update cycle with detections from a frame."""
    tracker = SimpleTracker()
    detections = detect_logos(small_frame)
    tracker.update(detections)


@pytest.mark.benchmark
def test_tracker_sequential_updates(small_frame: np.ndarray) -> None:
    """Benchmark multiple sequential tracker updates (simulates a video stream)."""
    tracker = SimpleTracker()
    for _ in range(10):
        detections = detect_logos(small_frame)
        tracker.update(detections)
