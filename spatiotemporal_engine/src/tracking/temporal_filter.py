from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable

from src.models.detection import Detection


@dataclass(frozen=True)
class TemporalState:
    """
    Confirmed event state produced by the temporal filter.
    """

    human_detected: bool
    fire_detected: bool

    human_positive_frames: int
    fire_positive_frames: int

    window_size: int


class TemporalConfirmationFilter:
    """
    Confirms detection events using evidence from a sliding frame window.

    An event is considered confirmed when it appears in at least
    `minimum_positive_frames` frames within the most recent `window_size`
    processed frames.
    """

    def __init__(
        self,
        window_size: int = 5,
        minimum_positive_frames: int = 3,
    ) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be greater than zero.")

        if minimum_positive_frames <= 0:
            raise ValueError(
                "minimum_positive_frames must be greater than zero."
            )

        if minimum_positive_frames > window_size:
            raise ValueError(
                "minimum_positive_frames cannot exceed window_size."
            )

        self.window_size = window_size
        self.minimum_positive_frames = minimum_positive_frames

        self._human_history: Deque[bool] = deque(maxlen=window_size)
        self._fire_history: Deque[bool] = deque(maxlen=window_size)

    def update(
        self,
        detections: Iterable[Detection],
    ) -> TemporalState:
        """
        Process detections from one frame and return the updated state.
        """

        detections = list(detections)

        human_present = any(
            detection.class_name.lower() in {"person", "human"}
            for detection in detections
        )

        fire_present = any(
            detection.class_name.lower() == "fire"
            for detection in detections
        )

        self._human_history.append(human_present)
        self._fire_history.append(fire_present)

        human_positive_frames = sum(self._human_history)
        fire_positive_frames = sum(self._fire_history)

        return TemporalState(
            human_detected=(
                human_positive_frames
                >= self.minimum_positive_frames
            ),
            fire_detected=(
                fire_positive_frames
                >= self.minimum_positive_frames
            ),
            human_positive_frames=human_positive_frames,
            fire_positive_frames=fire_positive_frames,
            window_size=self.window_size,
        )

    def reset(self) -> None:
        """
        Clear all accumulated temporal evidence.
        """

        self._human_history.clear()
        self._fire_history.clear()