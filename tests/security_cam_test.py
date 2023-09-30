import pytest
from src.capture.security_cam import set_log_config
from src.capture.security_cam import args_parser


def test_set_log_config() -> None:
    # Test with invalid log file path
    with pytest.raises(ValueError):
        set_log_config(True, "/invalid/path/to/logfile")
