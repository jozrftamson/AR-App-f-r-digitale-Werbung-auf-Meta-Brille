"""Shared fixtures for benchmarks."""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

# Ensure the python-backend package root is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def small_frame() -> np.ndarray:
    """A small 320x240 BGR frame with a red and a blue rectangle."""
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    # Red rectangle (BGR: 0,0,200)
    cv2.rectangle(frame, (20, 20), (100, 100), (0, 0, 200), -1)
    # Blue rectangle (BGR: 200,0,0)
    cv2.rectangle(frame, (150, 50), (280, 180), (200, 0, 0), -1)
    return frame


@pytest.fixture
def medium_frame() -> np.ndarray:
    """A 640x480 BGR frame with multiple coloured regions."""
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Several red patches
    cv2.rectangle(frame, (10, 10), (150, 120), (0, 0, 210), -1)
    cv2.rectangle(frame, (400, 300), (600, 450), (0, 0, 190), -1)
    # Several blue patches
    cv2.rectangle(frame, (200, 50), (350, 200), (210, 0, 0), -1)
    cv2.rectangle(frame, (50, 300), (180, 440), (190, 0, 0), -1)
    return frame
