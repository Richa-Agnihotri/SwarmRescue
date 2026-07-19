from ultralytics import YOLO

from src.models.detection import Detection


class VisionDetector:
    """
    Wrapper around the YOLO model developed by the Vision Team.

    Responsibilities:
    - Load the trained model once.
    - Run inference on a frame.
    - Return raw YOLO results.

    NOTE:
    This class intentionally does NOT perform:
    - tracking
    - temporal reasoning
    - API communication
    """

    def __init__(self, model_path: str):

        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=0.25,
            verbose=False
        )

        detections = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])

                detections.append(

                    Detection(

                        class_name=result.names[class_id],

                        confidence=float(box.conf[0]),

                        x1=float(box.xyxy[0][0]),
                        y1=float(box.xyxy[0][1]),
                        x2=float(box.xyxy[0][2]),
                        y2=float(box.xyxy[0][3]),
                    )

                )

        return detections