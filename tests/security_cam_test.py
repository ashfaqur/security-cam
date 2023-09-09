import pytest
from src.capture.security_cam import set_log_config
from src.capture.security_cam import args_parser


def test_set_log_config() -> None:
    # Test with invalid log file path
    with pytest.raises(ValueError):
        set_log_config(True, "/invalid/path/to/logfile")


def test_args_parser() -> None:
    # Test with verbose flag and logpath argument
    test_args = ["-v", "--logpath", "logs/app.log"]
    args = args_parser().parse_args(test_args)
    assert args.verbose == True, "Verbose flag set correctly"
    assert args.logpath == "logs/app.log", "Log path set correctly"

    # Test without verbose flag and logpath argument
    test_args = []
    args = args_parser().parse_args(test_args)
    assert args.verbose == False, "Verbose flag not set correctly"
    assert args.logpath == None, "Log path not set correctly"
