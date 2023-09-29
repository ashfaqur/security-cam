import logging
import cv2
from typing import Any, Optional
from time import time

VIDEO_DEVICE_ID = 0
PERIOD_BETWEEN_PROCESSING = 2  # seconds
BODY_DETECTION_CONFIG = "haarcascade_upperbody.xml"
BODY_DETECTION_SCALE_FACTOR = 1.1
BODY_DETECTION_MIN_NEIGHBOURS = 5

logger = logging.getLogger(__name__)


def main(window: bool) -> None:
    cap = cv2.VideoCapture(VIDEO_DEVICE_ID)
    check_camera_open(cap)
    try:
        recording(capture=cap, show_window=window)
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
    upper_body_cascade: Any = cv2.CascadeClassifier(
        cv2.data.haarcascades + BODY_DETECTION_CONFIG
    )
    last_process_time: float = 0

    while True:
        _, frame = capture.read()
        if crop_frame and len(crop_frame) == 4:
            frame = frame[crop_frame[0] : crop_frame[1], crop_frame[2] : crop_frame[3]]
        height, width = frame.shape[:2]

        if show_window:
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        if not do_process(last_process_time):
            continue

        last_process_time = time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        upper_body_locations = detect(gray, upper_body_cascade)
        if len(upper_body_locations) > 0:
            logger.info("Detected a person")
            # detection_ongoing = True
            # last_detection_time = time()
        else:
            logger.info("Not found anyone")


def check_camera_open(cap: Any) -> None:
    if cap is None or not cap.isOpened():
        raise ValueError(f"Unable to open video source at '{VIDEO_DEVICE_ID}'")
    else:
        logging.debug(f"Using video source at id '{VIDEO_DEVICE_ID}'")


def do_process(last_time_stamp: float) -> float:
    return (time() - last_time_stamp) > PERIOD_BETWEEN_PROCESSING


def detect(grey_frame: Any, upper_body_cascade: Any) -> Any:
    return upper_body_cascade.detectMultiScale(
        grey_frame, BODY_DETECTION_SCALE_FACTOR, BODY_DETECTION_MIN_NEIGHBOURS
    )
