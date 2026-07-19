from pprint import pprint

import requests

from src.communication.telemetry_sender import TelemetrySender
from src.simulation.drone_trajectory import Position
from src.telemetry.telemetry_packet import TelemetryPacket


def main() -> None:
    sender = TelemetrySender()

    print("=" * 70)

    if not sender.health_check():
        print("Backend is not running.")
        print("Start the FastAPI server first.")
        return

    packet = TelemetryPacket(
        drone_id=1,
        timestamp=12.34,
        position=Position(
            x=5.5,
            y=1.2,
            z=20.0,
        ),
        human_detected=False,
        fire_detected=True,
    )

    try:
        response = sender.send(packet)

        print("Packet successfully sent.")
        print()

        pprint(response.json())

    except requests.RequestException as error:
        print(f"Request failed:\n{error}")

    print("=" * 70)


if __name__ == "__main__":
    main()