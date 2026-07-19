from dataclasses import dataclass


@dataclass
class Detection:
    """
    Standard detection object used throughout the project.
    """

    class_name: str
    confidence: float

    x1: float
    y1: float
    x2: float
    y2: float