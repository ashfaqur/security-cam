import logging
import cv2
import os
from typing import Any, Optional
from time import time
from datetime import datetime

VIDEO_DEVICE_ID = 0

STAMP_COLOR = (0, 0, 255)

BODY_DETECTION_CONFIG = "haarcascade_upperbody.xml"
BODY_DETECTION_SCALE_FACTOR = 1.1
BODY_DETECTION_MIN_NEIGHBOURS = 5

# All time in seconds
PERIOD_BETWEEN_PROCESSING = 2
SNAPSHOT_PERIODS = (0, 10, 20, 60, 120, 600)
DETECTION_END_TIME_PERIOD = 60

logger = logging.getLogger(__name__)


def main(directory: str, window: bool) -> None:
    if not os.path.isdir(directory):
        raise ValueError(f"Given snapshot output path '{directory}' is not a directory")

    cap = cv2.VideoCapture(VIDEO_DEVICE_ID)
    check_camera_open(cap)
    try:
        recording(capture=cap, snapshot_directory=directory, show_window=window)
    except KeyboardInterrupt:
        logger.warn("Stopping script with keyboard interrupt")
    finally:
        # Release handle to the camera
        cap.release()
        cv2.destroyAllWindows()


def recording(
    capture: Any,
    snapshot_directory: str,
    show_window: bool = False,
    crop_frame: Optional[tuple[int, int, int, int]] = None,
    draw_outline: bool = False,
) -> None:
    upper_body_cascade: Any = cv2.CascadeClassifier(
        cv2.data.haarcascades + BODY_DETECTION_CONFIG
    )
    last_process_time: float = 0
    last_snapshot_time: float = 0
    snapshot_counter: int = 0
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
            detection_ongoing = True
            last_detection_time = time()
            if draw_outline:
                for x, y, w, h in upper_body_locations:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if take_snapshot(snapshot_counter, last_snapshot_time):
                date_time = datetime.now()
                file_path_date = date_time.strftime("%Y-%m-%d")
                file_path_time = date_time.strftime("%H-%M-%S")
                put_text(frame, date_time, width)
                extension = ".jpg"
                file_name = file_path_date + "_" + file_path_time + extension
                file_path = os.path.join(snapshot_directory, file_name)
                snapshot_counter += 1
                last_snapshot_time = time()
                print(f"file_name: {file_path}, snapshot counter {snapshot_counter}")
                cv2.imwrite(file_path, frame)
            elif detection_ongoing:
                if (time() - last_detection_time) > DETECTION_END_TIME_PERIOD:
                    logger.debug("Stopping ongoing detection")
                    detection_ongoing = False
                    snapshot_counter = 0


def put_text(frame: Any, date_time: Any, width: int) -> None:
    img_date = date_time.strftime("%d/%m/%Y")
    img_time = date_time.strftime("%H:%M:%S")
    cv2.putText(
        frame,
        img_date,
        (10, 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        STAMP_COLOR,
        2,
        2,
    )
    cv2.putText(
        frame,
        img_time,
        (width - 80, 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        STAMP_COLOR,
        2,
        2,
    )


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


def take_snapshot(counter: int, last_time: float) -> bool:
    index: int = len(SNAPSHOT_PERIODS) - 1
    if counter < index:
        index = counter
    return (time() - last_time) > SNAPSHOT_PERIODS[index]
