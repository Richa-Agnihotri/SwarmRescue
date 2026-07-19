from pprint import pprint

from src.simulation.drone_trajectory import Position
from src.telemetry.telemetry_packet import TelemetryPacket


def main() -> None:
    packet = TelemetryPacket(
        drone_id=1,
        timestamp=2.75,
        position=Position(
            x=8.25,
            y=0.0,
            z=20.0,
        ),
        human_detected=False,
        fire_detected=True,
    )

    print("=" * 70)

    pprint(packet.to_dict())

    print("=" * 70)


if __name__ == "__main__":
    main()