import time
import socket


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
