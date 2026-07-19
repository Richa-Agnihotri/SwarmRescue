from pathlib import Path

from src.mission.config import MissionConfig
from src.mission.mission_engine import MissionEngine


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    swarmrescue_root = project_root.parent

    model_path = (
        swarmrescue_root
        / "person_fire"
        / "weights"
        / "best.pt"
    )

    video_path = (
        project_root
        / "trajectories"
        / "test_video.mp4"
    )

    config = MissionConfig(
        model_path=str(model_path),
        video_path=str(video_path),
        backend_url="http://127.0.0.1:8000",
    )

    MissionEngine(config).run()


if __name__ == "__main__":
    main()