import atexit
import logging
import cv2
import os
import subprocess
from src.capture.util import (
    validate,
    is_connected,
    validate_crop_frame_parameters,
    put_text,
    process_fp_csv,
)
from typing import Any, Optional, Tuple, List
from time import time
from datetime import datetime


VIDEO_DEVICE_ID = 0

STAMP_COLOR = (0, 0, 255)

DEFAULT_UPLOAD_PATH = "images"

BODY_DETECTION_CONFIG = "haarcascade_upperbody.xml"
BODY_DETECTION_SCALE_FACTOR = 1.1
BODY_DETECTION_MIN_NEIGHBOURS = 6

# All time in seconds
DEFAULT_PERIOD_BETWEEN_PROCESSING = 2
SNAPSHOT_PERIODS = (0, 5, 10, 60, 120, 600)
DETECTION_END_TIME_PERIOD = 60
SAMPLE_TIME_PERIOD = 3600

logger = logging.getLogger(__name__)


def main(
    directory: str,
    dropbox_uploader: str,
    window: bool = False,
    crop_frame: Optional[Tuple[int, int, int, int]] = None,
    period: int = DEFAULT_PERIOD_BETWEEN_PROCESSING,
    sensitivity: int = BODY_DETECTION_MIN_NEIGHBOURS,
    upload_path: str = DEFAULT_UPLOAD_PATH,
) -> None:
    validate(directory, dropbox_uploader)
    if not period or period <= 0:
        period = DEFAULT_PERIOD_BETWEEN_PROCESSING
    if not sensitivity:
        sensitivity = BODY_DETECTION_MIN_NEIGHBOURS
        logger.debug(f"Using default sensitivity: {BODY_DETECTION_MIN_NEIGHBOURS}")
    else:
        logger.debug(f"Using user specified sensitivity: {sensitivity}")
    if dropbox_uploader and not upload_path:
        upload_path = DEFAULT_UPLOAD_PATH
        logger.debug(f"Using default upload path: {upload_path}")
    elif dropbox_uploader:
        logger.debug(f"Using upload path: {upload_path}")
    cap = cv2.VideoCapture(VIDEO_DEVICE_ID)
    check_camera_open(cap)
    # Register cleanup function
    atexit.register(cap.release)
    try:
        recording(
            capture=cap,
            dropbox_uploader=dropbox_uploader,
            snapshot_directory=directory,
            show_window=window,
            draw_outline=True,
            sample_pics=True,
            crop_frame=crop_frame,
            period=period,
            sensitivity=sensitivity,
            upload_path=upload_path,
        )

    except KeyboardInterrupt:
        logger.warn("Stopping script with keyboard interrupt")
    finally:
        # Release handle to the camera
        cap.release()
        cv2.destroyAllWindows()


def recording(
    capture: Any,
    snapshot_directory: str,
    dropbox_uploader: str,
    show_window: bool = False,
    crop_frame: Optional[Tuple[int, int, int, int]] = None,
    draw_outline: bool = False,
    sample_pics: bool = True,
    period: int = DEFAULT_PERIOD_BETWEEN_PROCESSING,
    sensitivity: int = BODY_DETECTION_MIN_NEIGHBOURS,
    upload_path: str = DEFAULT_UPLOAD_PATH,
) -> None:
    upper_body_cascade: Any = cv2.CascadeClassifier(
        cv2.data.haarcascades + BODY_DETECTION_CONFIG
    )
    last_process_time: float = 0
    last_snapshot_time: float = 0
    snapshot_counter: int = 0
    last_sample_time = datetime.now()
    false_positive_locations: List[Tuple[int, int, int, int]] = process_fp_csv(
        snapshot_directory
    )

    while True:
        _, frame = capture.read()
        if not frame.any():
            raise ValueError(
                "Video frame is undefined. Possibly the camera is inaccessible"
            )
        height, width = frame.shape[:2]
        if crop_frame and len(crop_frame) == 4:
            validate_crop_frame_parameters(crop_frame, height, width)
            frame = frame[crop_frame[0] : crop_frame[1], crop_frame[2] : crop_frame[3]]
        height, width = frame.shape[:2]

        if show_window:
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        if sample_pics:
            current_time = datetime.now()
            if (current_time - last_sample_time).seconds >= SAMPLE_TIME_PERIOD:
                last_sample_time = current_time
                logger.debug("Taking a sample pic")
                take_snapshot(
                    frame,
                    width,
                    snapshot_directory,
                    dropbox_uploader,
                    True,
                    upload_path,
                )

        if not do_process(last_process_time, period):
            continue

        last_process_time = time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        upper_body_locations: List[Tuple[int, int, int, int]] = detect(
            gray, upper_body_cascade, sensitivity
        )
        if is_detected(upper_body_locations, false_positive_locations):
            for x, y, w, h in upper_body_locations:
                if draw_outline:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            logger.info("Detected a person")
            detection_ongoing = True
            last_detection_time = time()
            if do_take_snapshot(snapshot_counter, last_snapshot_time):
                snapshot_counter += 1
                last_snapshot_time = time()
                take_snapshot(
                    frame,
                    width,
                    snapshot_directory,
                    dropbox_uploader,
                    False,
                    upload_path,
                )
            elif detection_ongoing:
                if (time() - last_detection_time) > DETECTION_END_TIME_PERIOD:
                    logger.debug("Stopping ongoing detection")
                    detection_ongoing = False
                    snapshot_counter = 0


def is_detected(
    upper_body_locations: List[Tuple[int, int, int, int]],
    false_positive_locations: List[Tuple[int, int, int, int]],
) -> bool:
    detected: bool = False
    if len(upper_body_locations) > 0:
        for x, y, w, h in upper_body_locations:
            if (x, y, w, h) in false_positive_locations:
                continue
            logger.debug(f"Detected x,y,w,h ({x},{y},{w},{h})")
            detected = True
    return detected


def take_snapshot(
    frame: Any,
    width: int,
    snapshot_directory: str,
    dropbox_uploader: str,
    sample: bool,
    upload_path: str,
) -> None:
    date_time = datetime.now()
    file_path_date = date_time.strftime("%Y-%m-%d")
    file_path_time = date_time.strftime("%H-%M-%S")
    put_text(frame, date_time, width, STAMP_COLOR)
    extension = "_sample.jpg" if sample else "_detected.jpg"
    file_name = file_path_date + "_" + file_path_time + extension
    file_path = os.path.join(snapshot_directory, file_name)
    logger.info(f"file_name: {file_path}")
    cv2.imwrite(file_path, frame)
    if dropbox_uploader:
        upload(
            dropbox_uploader,
            file_path,
            file_path_date,
            file_path_time,
            extension,
            upload_path,
        )


def check_camera_open(cap: Any) -> None:
    if cap is None or not cap.isOpened():
        raise ValueError(f"Unable to open video source at '{VIDEO_DEVICE_ID}'")
    else:
        logging.debug(f"Using video source at id '{VIDEO_DEVICE_ID}'")


def do_process(last_time_stamp: float, period: int) -> float:
    return (time() - last_time_stamp) > period


def detect(grey_frame: Any, upper_body_cascade: Any, sensitivity: int) -> Any:
    return upper_body_cascade.detectMultiScale(
        grey_frame, BODY_DETECTION_SCALE_FACTOR, sensitivity
    )


def do_take_snapshot(counter: int, last_time: float) -> bool:
    index: int = len(SNAPSHOT_PERIODS) - 1
    if counter < index:
        index = counter
    return (time() - last_time) > SNAPSHOT_PERIODS[index]


def upload(
    dropbox_uploader: str,
    file_path: str,
    date: Any,
    timestamp: Any,
    extension: str,
    upload_path: str,
) -> None:
    if is_connected():
        logger.debug("Uploading image to dropbox")
        upload_path = os.path.join(upload_path, date, timestamp + extension)
        upload = subprocess.run(
            [dropbox_uploader, "-s", "upload", file_path, upload_path],
            capture_output=True,
            text=True,
        )
        logger.debug(upload.args)
        logger.debug(upload.returncode)
        logger.info(upload.stdout)
        if upload.returncode != 0:
            logger.error("Upload failed")
    else:
        logger.warn("Upload skipped as internet connection to dropbox is unavailable.")
