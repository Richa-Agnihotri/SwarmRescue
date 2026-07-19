"""
Telemetry sender.

Responsible for sending telemetry packets to the backend API.
"""

from __future__ import annotations

from typing import Optional

import requests

from src.telemetry.telemetry_packet import TelemetryPacket


class TelemetrySender:
    """
    Sends telemetry packets to the backend service.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        timeout_seconds: float = 5.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def send(self, packet: TelemetryPacket) -> requests.Response:
        """
        Send a telemetry packet.

        Raises:
            requests.RequestException
                if communication with the backend fails.
        """

        url = f"{self.base_url}/api/v1/telemetry"

        response = requests.post(
            url,
            json=packet.to_dict(),
            timeout=self.timeout_seconds,
        )

        response.raise_for_status()

        return response

    def health_check(self) -> bool:
        """
        Check whether the backend is reachable.
        """

        try:
            response = requests.get(
                f"{self.base_url}/",
                timeout=self.timeout_seconds,
            )

            return response.status_code == 200

        except requests.RequestException:
            return False