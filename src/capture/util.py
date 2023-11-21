import time
import socket
import cv2
from typing import Tuple, Any


def get_log_file_name() -> str:
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
    file_name = f"{formatted_time}_security_cam_log.txt"
    return file_name


def is_connected() -> bool:
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("www.dropbox.com", 80))
        return True
    except OSError:
        pass
    return False


def validate_crop_frame_parameters(
    crop_frame: Tuple[int, int, int, int], height: int, width: int
) -> None:
    if crop_frame[0] < 0 or crop_frame[0] > height or crop_frame[0] > crop_frame[1]:
        ValueError(f"Crop frame invalid x parameter {crop_frame[0]}")
    if crop_frame[1] < 0 or crop_frame[1] > height or crop_frame[1] < crop_frame[0]:
        ValueError(f"Crop frame invalid x parameter {crop_frame[1]}")
    if crop_frame[2] < 0 or crop_frame[2] > width or crop_frame[2] > crop_frame[3]:
        ValueError(f"Crop frame invalid y parameter {crop_frame[2]}")
    if crop_frame[3] < 0 or crop_frame[3] > width or crop_frame[3] < crop_frame[2]:
        ValueError(f"Crop frame invalid y parameter {crop_frame[3]}")


def put_text(
    frame: Any, date_time: Any, width: int, stamp_color: Tuple[int, int, int]
) -> None:
    img_date = date_time.strftime("%d/%m/%Y")
    img_time = date_time.strftime("%H:%M:%S")
    cv2.putText(
        frame,
        img_date,
        (10, 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        stamp_color,
        2,
        2,
    )
    cv2.putText(
        frame,
        img_time,
        (width - 80, 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        stamp_color,
        2,
        2,
    )
