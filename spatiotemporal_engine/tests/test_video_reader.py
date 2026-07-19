from pathlib import Path

from src.simulation.video_reader import VideoReader


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    video_path = (
        repo_root
        / "spatiotemporal_engine"
        / "trajectories"
        / "test_video.mp4"
    )

    with VideoReader(str(video_path)) as reader:
        print("=" * 60)
        print(f"Video: {video_path.name}")
        print(f"FPS: {reader.fps:.2f}")
        print(f"Frame count: {reader.frame_count}")
        print(f"Resolution: {reader.width}x{reader.height}")
        print("=" * 60)

        processed_frames = 0

        for frame_index, timestamp_seconds, frame in reader.frames():
            print(
                f"Frame {frame_index:4d}"
                f" | Timestamp: {timestamp_seconds:7.2f}s"
                f" | Shape: {frame.shape}"
            )

            processed_frames += 1

            # Only inspect the first five frames for this test.
            if processed_frames == 5:
                break

        print("=" * 60)
        print(f"Successfully read {processed_frames} frames.")
        print("=" * 60)


if __name__ == "__main__":
    main()