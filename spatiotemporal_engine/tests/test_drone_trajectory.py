from src.simulation.drone_trajectory import DroneTrajectory


def main() -> None:
    trajectory = DroneTrajectory(
        speed_mps=3.0,
        altitude_m=20.0,
        heading_deg=0.0,
    )

    print("=" * 70)

    timestamps = [
        0.0,
        1.0,
        2.0,
        3.0,
        4.5,
        10.0,
    ]

    for timestamp in timestamps:
        position = trajectory.position_at(timestamp)

        print(
            f"Time {timestamp:5.2f}s"
            f" -> "
            f"({position.x:.2f}, "
            f"{position.y:.2f}, "
            f"{position.z:.2f})"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()