import logging
import cv2
from typing import Any, Optional

VIDEO_DEVICE_ID = 0

logger = logging.getLogger(__name__)


def main() -> None:
    cap = cv2.VideoCapture(VIDEO_DEVICE_ID)
    check_camera_open(cap)
    try:
        recording(capture=cap, show_window=False, crop_frame=None)
    except KeyboardInterrupt:
        logger.warn("Stopping script with keyboard interrupt")
    finally:
        # Release handle to the camera
        cap.release()
        cv2.destroyAllWindows()


def recording(
    capture: Any,
    show_window: bool = False,
    crop_frame: Optional[tuple[int, int, int, int]] = None,
) -> None:
    while True:
        _, frame = capture.read()
        if crop_frame and len(crop_frame) == 4:
            frame = frame[crop_frame[0] : crop_frame[1], crop_frame[2] : crop_frame[3]]
        height, width = frame.shape[:2]

        if show_window:
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break


def check_camera_open(cap: Any) -> None:
    if cap is None or not cap.isOpened():
        raise ValueError(f"Unable to open video source at '{VIDEO_DEVICE_ID}'")
    else:
        logging.debug(f"Using video source at id '{VIDEO_DEVICE_ID}'")
