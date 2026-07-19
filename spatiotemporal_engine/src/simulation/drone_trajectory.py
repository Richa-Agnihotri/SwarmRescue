"""
Drone trajectory simulation.

This module generates deterministic drone positions based on
elapsed mission time.

The simulated trajectory can later be replaced with real GPS
coordinates without affecting the rest of the pipeline.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """
    Represents the drone position in metres.
    """

    x: float
    y: float
    z: float


class DroneTrajectory:
    """
    Simulates a drone flying at constant speed,
    constant altitude and constant heading.
    """

    def __init__(
        self,
        speed_mps: float = 3.0,
        altitude_m: float = 20.0,
        heading_deg: float = 0.0,
    ) -> None:
        if speed_mps < 0:
            raise ValueError("speed_mps must be non-negative.")

        if altitude_m < 0:
            raise ValueError("altitude_m must be non-negative.")

        self.speed_mps = speed_mps
        self.altitude_m = altitude_m
        self.heading_deg = heading_deg

        heading_rad = math.radians(heading_deg)

        self._cos_heading = math.cos(heading_rad)
        self._sin_heading = math.sin(heading_rad)

    def position_at(self, timestamp_seconds: float) -> Position:
        """
        Returns the simulated drone position
        at the given timestamp.
        """

        if timestamp_seconds < 0:
            raise ValueError("timestamp_seconds must be non-negative.")

        distance = self.speed_mps * timestamp_seconds

        x = distance * self._cos_heading
        y = distance * self._sin_heading
        z = self.altitude_m

        return Position(
            x=x,
            y=y,
            z=z,
        )