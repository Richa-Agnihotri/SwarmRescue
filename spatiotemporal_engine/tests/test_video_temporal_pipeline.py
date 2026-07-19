from pathlib import Path

from src.simulation.video_reader import VideoReader
from src.tracking.temporal_filter import TemporalConfirmationFilter
from src.vision.detector import VisionDetector


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    model_path = repo_root / "person_fire" / "weights" / "best.pt"
    video_path = (
        repo_root
        / "spatiotemporal_engine"
        / "trajectories"
        / "test_video.mp4"
    )

    detector = VisionDetector(str(model_path))

    temporal_filter = TemporalConfirmationFilter(
        window_size=5,
        minimum_positive_frames=3,
    )

    max_frames = 20

    with VideoReader(str(video_path)) as reader:
        print("=" * 90)
        print(f"Video: {video_path.name}")
        print(f"FPS: {reader.fps:.2f}")
        print(f"Processing first {max_frames} frames")
        print("=" * 90)

        for frame_index, timestamp_seconds, frame in reader.frames():
            detections = detector.detect(frame)
            state = temporal_filter.update(detections)

            raw_fire_present = any(
                detection.class_name.lower() == "fire"
                for detection in detections
            )

            raw_human_present = any(
                detection.class_name.lower() in {"person", "human"}
                for detection in detections
            )

            print(
                f"Frame {frame_index:3d}"
                f" | Time={timestamp_seconds:5.2f}s"
                f" | Raw fire={str(raw_fire_present):5s}"
                f" | Confirmed fire={str(state.fire_detected):5s}"
                f" | Fire evidence="
                f"{state.fire_positive_frames}/{state.window_size}"
                f" | Raw human={str(raw_human_present):5s}"
                f" | Confirmed human={str(state.human_detected):5s}"
            )

            if frame_index + 1 >= max_frames:
                break

        print("=" * 90)
        print("Video temporal pipeline test completed.")
        print("=" * 90)


if __name__ == "__main__":
    main()