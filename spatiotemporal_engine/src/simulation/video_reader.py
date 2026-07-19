from pathlib import Path
from typing import Iterator, Tuple

import cv2
import numpy as np


class VideoReader:
    """
    Reads a video file sequentially and yields frames with metadata.

    Responsibilities:
    - Open the video source.
    - Read frames in order.
    - Expose frame index and video timestamp.
    - Release the underlying OpenCV resource.
    """

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)

        if not self.video_path.exists():
            raise FileNotFoundError(
                f"Video file does not exist: {self.video_path}"
            )

        self.capture = cv2.VideoCapture(str(self.video_path))

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Could not open video file: {self.video_path}"
            )

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)

        if self.fps <= 0:
            raise ValueError(
                f"Invalid video FPS reported for: {self.video_path}"
            )

        self.frame_count = int(
            self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        self.width = int(
            self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        self.height = int(
            self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

    def frames(self) -> Iterator[Tuple[int, float, np.ndarray]]:
        """
        Yield frames from the video.

        Yields:
            Tuple containing:
            - frame_index: zero-based frame number
            - timestamp_seconds: position in the video
            - frame: OpenCV BGR image
        """

        frame_index = 0

        while True:
            success, frame = self.capture.read()

            if not success:
                break

            timestamp_seconds = frame_index / self.fps

            yield frame_index, timestamp_seconds, frame

            frame_index += 1

    def release(self) -> None:
        """
        Release the video capture resource.
        """

        if self.capture.isOpened():
            self.capture.release()

    def __enter__(self) -> "VideoReader":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.release()