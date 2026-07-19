"""
Logging utilities for the mission engine.
"""

import logging


def create_logger() -> logging.Logger:
    logger = logging.getLogger("mission_engine")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        "%H:%M:%S",
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger