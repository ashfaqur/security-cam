import time


def get_log_file_name() -> str:
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
    file_name = f"{formatted_time}_security_cam_log.txt"
    return file_name
