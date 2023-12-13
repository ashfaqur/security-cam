import time
import socket
import cv2
import os
import csv
from typing import List, Tuple, Any


def validate(img_dir: str, uploader: str) -> None:
    if not os.path.isdir(img_dir):
        raise ValueError(f"Given snapshot output path '{img_dir}' is not a directory")

    if uploader and not os.path.isfile(uploader):
        raise ValueError(
            f"Given dropbox uploader script file '{uploader}' does not exist"
        )


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
        raise ValueError(f"Crop frame invalid x parameter {crop_frame[0]}")
    if crop_frame[1] < 0 or crop_frame[1] > height or crop_frame[1] < crop_frame[0]:
        raise ValueError(f"Crop frame invalid x parameter {crop_frame[1]}")
    if crop_frame[2] < 0 or crop_frame[2] > width or crop_frame[2] > crop_frame[3]:
        raise ValueError(f"Crop frame invalid y parameter {crop_frame[2]}")
    if crop_frame[3] < 0 or crop_frame[3] > width or crop_frame[3] < crop_frame[2]:
        raise ValueError(f"Crop frame invalid y parameter {crop_frame[3]}")


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


def process_fp_csv(directory: str) -> List[Tuple[int, int, int, int]]:
    result: List[Tuple[int, int, int, int]] = []
    file_path = os.path.join(directory, "fp.csv")
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 4:
                    raise ValueError("Each line must contain exactly four integers.")
                try:
                    result.append((int(row[0]), int(row[1]), int(row[2]), int(row[3])))
                except ValueError:
                    raise ValueError("All values in each line must be integers.")
    return result
