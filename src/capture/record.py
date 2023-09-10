import logging
import cv2
from typing import Any

VIDEO_DEVICE_ID = 0

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("main")
    cap = cv2.VideoCapture(VIDEO_DEVICE_ID)
    check_camera_open(cap)


def check_camera_open(cap: Any) -> None:
    if cap is None or not cap.isOpened():
        raise ValueError(f"Unable to open video source at '{VIDEO_DEVICE_ID}'")
