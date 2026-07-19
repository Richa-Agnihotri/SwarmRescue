"""
Mission engine.

Coordinates the complete spatiotemporal processing pipeline.
"""

from __future__ import annotations

from src.communication.telemetry_sender import TelemetrySender
from src.mission.config import MissionConfig
from src.mission.logger import create_logger
from src.simulation.drone_trajectory import DroneTrajectory
from src.simulation.video_reader import VideoReader
from src.telemetry.telemetry_packet import TelemetryPacket
from src.tracking.temporal_filter import TemporalConfirmationFilter
from src.vision.detector import VisionDetector


class MissionEngine:
    """
    Coordinates the complete processing pipeline.
    """

    def __init__(self, config: MissionConfig) -> None:

        self.config = config
        self.logger = create_logger()

        self.detector = VisionDetector(config.model_path)

        self.temporal_filter = TemporalConfirmationFilter(
            window_size=config.temporal_window,
            minimum_positive_frames=config.temporal_threshold,
        )

        self.trajectory = DroneTrajectory(
            speed_mps=config.speed_mps,
            altitude_m=config.altitude_m,
            heading_deg=config.heading_deg,
        )

        self.sender = TelemetrySender(
            base_url=config.backend_url,
        )

    def process_frame(self, timestamp: float, frame):
        """
        Process a single frame.
        """

        detections = self.detector.detect(frame)

        state = self.temporal_filter.update(detections)

        position = self.trajectory.position_at(timestamp)

        packet = TelemetryPacket(
            drone_id=self.config.drone_id,
            timestamp=timestamp,
            position=position,
            human_detected=state.human_detected,
            fire_detected=state.fire_detected,
        )

        return packet

    def run(self) -> None:
        """
        Execute the mission.
        """

        if not self.sender.health_check():
            self.logger.error("Backend is not reachable.")
            return

        self.logger.info("Mission started.")

        with VideoReader(self.config.video_path) as reader:

            for frame_index, timestamp, frame in reader.frames():

                if (
                    frame_index
                    % self.config.telemetry_interval_frames
                    != 0
                ):
                    continue

                packet = self.process_frame(
                    timestamp,
                    frame,
                )

                try:
                    response = self.sender.send(packet)

                    self.logger.info(
                        "Frame %04d | Fire=%s | Human=%s | Position=(%.2f, %.2f, %.2f) | HTTP %d",
                        frame_index,
                        packet.fire_detected,
                        packet.human_detected,
                        packet.position.x,
                        packet.position.y,
                        packet.position.z,
                        response.status_code,
                    )

                except Exception as error:
                    self.logger.error(
                        "Frame %04d | %s",
                        frame_index,
                        error,
                    )

        self.logger.info("Mission completed.")