from dataclasses import dataclass
from typing import Optional


@dataclass
class LogoDetection:
    """Domain object shared between detector and tracker layers."""

    label: str
    confidence: float
    x: float
    y: float
    width: float
    height: float
    track_id: Optional[str] = None

    def to_bbox_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
