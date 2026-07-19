"""
Mission configuration.

Centralizes runtime parameters for the mission engine.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionConfig:
    """
    Configuration used by the MissionEngine.
    """

    model_path: str
    video_path: str
    backend_url: str

    drone_id: int = 1

    speed_mps: float = 3.0
    altitude_m: float = 20.0
    heading_deg: float = 0.0

    temporal_window: int = 5
    temporal_threshold: int = 3

    telemetry_interval_frames: int = 1