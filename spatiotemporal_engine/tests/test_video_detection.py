from pathlib import Path

from src.simulation.video_reader import VideoReader
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

    max_frames = 10

    with VideoReader(str(video_path)) as reader:
        print("=" * 70)
        print(f"Video: {video_path.name}")
        print(f"FPS: {reader.fps:.2f}")
        print(f"Testing first {max_frames} frames")
        print("=" * 70)

        for frame_index, timestamp_seconds, frame in reader.frames():
            detections = detector.detect(frame)

            print(
                f"Frame {frame_index:4d}"
                f" | Time: {timestamp_seconds:6.2f}s"
                f" | Detections: {len(detections)}"
            )

            for detection in detections:
                print(
                    f"    {detection.class_name:10s}"
                    f" | confidence={detection.confidence:.3f}"
                    f" | bbox=("
                    f"{detection.x1:.0f}, "
                    f"{detection.y1:.0f}, "
                    f"{detection.x2:.0f}, "
                    f"{detection.y2:.0f})"
                )

            if frame_index + 1 >= max_frames:
                break

        print("=" * 70)
        print("Video detection test completed.")
        print("=" * 70)


if __name__ == "__main__":
    main()