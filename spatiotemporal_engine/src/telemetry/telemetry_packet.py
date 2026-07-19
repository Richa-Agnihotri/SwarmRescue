"""
Telemetry packet model.

This module defines the telemetry payload exchanged between the
spatiotemporal engine and the backend service.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.simulation.drone_trajectory import Position


@dataclass(frozen=True)
class TelemetryPacket:
    """
    Represents a single telemetry update produced by one drone.
    """

    drone_id: int
    timestamp: float
    position: Position
    human_detected: bool
    fire_detected: bool

    def to_dict(self) -> dict:
        """
        Convert the packet into the JSON structure expected by
        the backend API.
        """

        return {
            "drone_id": self.drone_id,
            "timestamp": self.timestamp,
            "coords": [
                self.position.x,
                self.position.y,
                self.position.z,
            ],
            "human_detected": self.human_detected,
            "fire_detected": self.fire_detected,
        }