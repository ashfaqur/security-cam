from argparse import ArgumentParser, ArgumentTypeError
from typing import Tuple, cast


class Args:
    snapshot_dir: str
    dropbox_uploader: str
    verbose: bool
    window: bool
    logdir: str
    crop: Tuple[int, int, int, int]
    period: int
    sensitivity: int
    upload_path: str


class ArgParser:
    def __init__(self) -> None:
        self.parser = ArgumentParser(
            description="Captures images and videos from camera based on person detection"
        )
        self.add_arguments()

    def add_arguments(self) -> None:
        self.parser.add_argument(
            "snapshot_dir",
            type=str,
            help="directory for saving captured images",
        )
        self.parser.add_argument(
            "-d",
            "--dropbox_uploader",
            type=str,
            help="Path to dropbox uploader script",
        )
        self.parser.add_argument(
            "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
        )
        self.parser.add_argument(
            "-w", "--window", action="store_true", help="Show video window"
        )
        self.parser.add_argument(
            "-l",
            "--logdir",
            type=str,
            help="Path to the log directory",
        )
        self.parser.add_argument(
            "-c",
            "--crop",
            type=tuple_check,
            help="A tuple of four integers for cropping frame",
        )
        self.parser.add_argument(
            "-p",
            "--period",
            type=int,
            help="Period in seconds for analysing video frame",
        )
        self.parser.add_argument(
            "-s",
            "--sensitivity",
            type=check_sensitivity,
            help="Sensitivity value between 2 and 6",
        )
        self.parser.add_argument(
            "-u",
            "--upload_path",
            type=str,
            help="Upload path",
        )

    def parse_args(self) -> Args:
        return cast(Args, self.parser.parse_args())


def tuple_check(s: str) -> Tuple[int, ...]:
    try:
        values = tuple(map(int, s.split(",")))
        if len(values) != 4:
            raise ArgumentTypeError("Tuple must contain exactly four integers.")
        return values
    except ValueError:
        raise ArgumentTypeError("Tuple must contain integers only.")


def check_sensitivity(value: str) -> int:
    ivalue = int(value)
    if ivalue < 2 or ivalue > 6:
        raise ArgumentTypeError(
            "%s is an invalid sensitivity value. It should be between 2 and 6." % value
        )
    return ivalue
