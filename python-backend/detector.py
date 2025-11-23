"""Logo detection stub.

Replace the body of `detect_logos` with your real model call. When using OpenCV DNN:
- Load the model once (e.g., Net net = cv2.dnn.readNetFromONNX("models/logo-detector.onnx"))
- Preprocess the frame (resize to model input size, convert BGR->RGB, scale/normalize)
- Run the forward pass and parse detections into `LogoDetection` objects.

For cloud APIs (Google Vision, AWS Rekognition, Azure Vision), encode the frame as JPEG/PNG,
call the API, and translate the result bounding boxes back into this project's coordinate format.
"""

from __future__ import annotations

from typing import List

import cv2
import numpy as np

from domain import LogoDetection


# Example placeholder: where you would configure your ONNX/TensorFlow model path
MODEL_PATH = "models/logo-detector.onnx"


def detect_logos(frame: np.ndarray) -> List[LogoDetection]:
    """Return a list of detected logos for the given BGR frame.

    This demo uses basic HSV color segmentation to mimic detections for two brands.
    Replace this logic with DNN inference or an API call.
    """

    detections: List[LogoDetection] = []
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red-ish regions mapped to "Coca-Cola"
    lower_red_1 = np.array([0, 120, 70])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 120, 70])
    upper_red_2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red_1, upper_red_1) | cv2.inRange(hsv, lower_red_2, upper_red_2)

    # Blue-ish regions mapped to "Pepsi"
    lower_blue = np.array([100, 120, 70])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    detections.extend(_contours_to_detections(mask_red, frame_shape=frame.shape, label="Coca-Cola"))
    detections.extend(_contours_to_detections(mask_blue, frame_shape=frame.shape, label="Pepsi"))
    return detections


def _contours_to_detections(mask: np.ndarray, frame_shape, label: str) -> List[LogoDetection]:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = frame_shape[:2]
    detections: List[LogoDetection] = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:  # ignore small blobs
            continue
        x, y, bw, bh = cv2.boundingRect(cnt)
        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))
        bw = min(bw, w - x)
        bh = min(bh, h - y)
        confidence = min(0.99, 0.35 + np.log(area + 1) / 10)
        detections.append(LogoDetection(label=label, confidence=float(confidence), x=float(x), y=float(y), width=float(bw), height=float(bh)))
    return detections
