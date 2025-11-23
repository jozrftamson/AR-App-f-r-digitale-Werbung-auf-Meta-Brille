"""Simple IoU-based tracker for assigning stable IDs to detections."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from domain import LogoDetection


def _iou(a: LogoDetection, b: LogoDetection) -> float:
    ax2 = a.x + a.width
    ay2 = a.y + a.height
    bx2 = b.x + b.width
    by2 = b.y + b.height
    inter_x1 = max(a.x, b.x)
    inter_y1 = max(a.y, b.y)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h
    union_area = a.width * a.height + b.width * b.height - inter_area
    return 0.0 if union_area <= 0 else inter_area / union_area


@dataclass
class _TrackState:
    detection: LogoDetection
    misses: int = 0


class SimpleTracker:
    """Maintains tracked detections within a stream."""

    def __init__(self, iou_threshold: float = 0.3, max_misses: int = 10):
        self._tracks: Dict[str, _TrackState] = {}
        self._next_id = 1
        self._iou_threshold = iou_threshold
        self._max_misses = max_misses

    def update(self, detections: List[LogoDetection]) -> List[LogoDetection]:
        # mark all as unmatched initially
        unmatched = detections.copy()

        # greedy matching between existing tracks and new detections
        for track_id, state in list(self._tracks.items()):
            best_det = None
            best_score = self._iou_threshold
            for det in detections:
                if det.label != state.detection.label:
                    continue
                score = _iou(state.detection, det)
                if score > best_score:
                    best_score = score
                    best_det = det
            if best_det:
                best_det.track_id = track_id
                self._tracks[track_id] = _TrackState(detection=best_det, misses=0)
                unmatched.remove(best_det)
            else:
                state.misses += 1
                if state.misses > self._max_misses:
                    self._tracks.pop(track_id, None)
                else:
                    self._tracks[track_id] = state

        # create new tracks for unmatched detections
        for det in unmatched:
            track_id = f"brand-{self._next_id}"
            self._next_id += 1
            det.track_id = track_id
            self._tracks[track_id] = _TrackState(detection=det)

        return [state.detection for state in self._tracks.values()]

    def reset(self):
        self._tracks.clear()
        self._next_id = 1


class TrackerRegistry:
    """Stores tracker instances per stream/session."""

    def __init__(self):
        self._trackers: Dict[str, SimpleTracker] = {}

    def get_tracker(self, stream_id: str) -> SimpleTracker:
        if stream_id not in self._trackers:
            self._trackers[stream_id] = SimpleTracker()
        return self._trackers[stream_id]

    def reset_tracker(self, stream_id: str) -> None:
        tracker = self._trackers.get(stream_id)
        if tracker:
            tracker.reset()
