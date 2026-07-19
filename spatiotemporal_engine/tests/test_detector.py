import cv2
from pathlib import Path

from src.vision.detector import VisionDetector


def main():

    # Repository root
    repo_root = Path(__file__).resolve().parents[2]

    model_path = repo_root / "person_fire" / "weights" / "best.pt"
    image_path = repo_root / "person_fire" / "test.jpg"

    detector = VisionDetector(str(model_path))

    frame = cv2.imread(str(image_path))

    if frame is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    detections = detector.detect(frame)

    print("=" * 50)

print(f"Detected Objects: {len(detections)}")

for detection in detections:

    print(

        f"{detection.class_name:10s}"
        f" | Confidence: {detection.confidence:.3f}"

    )

print("=" * 50)


if __name__ == "__main__":
    main()