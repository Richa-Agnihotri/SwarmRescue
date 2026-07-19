from src.models.detection import Detection
from src.tracking.temporal_filter import TemporalConfirmationFilter


def make_detection(class_name: str) -> Detection:
    return Detection(
        class_name=class_name,
        confidence=0.90,
        x1=10.0,
        y1=10.0,
        x2=100.0,
        y2=100.0,
    )


def main() -> None:
    temporal_filter = TemporalConfirmationFilter(
        window_size=5,
        minimum_positive_frames=3,
    )

    frame_detections = [
        [make_detection("fire")],
        [],
        [make_detection("fire")],
        [make_detection("fire")],
        [],
        [],
    ]

    print("=" * 70)

    for frame_index, detections in enumerate(frame_detections):
        state = temporal_filter.update(detections)

        print(
            f"Frame {frame_index}"
            f" | fire evidence="
            f"{state.fire_positive_frames}/{state.window_size}"
            f" | confirmed={state.fire_detected}"
        )

    print("=" * 70)


if __name__ == "__main__":
    main()