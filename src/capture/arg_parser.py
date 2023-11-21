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


class ArgParser:
    def __init__(self) -> None:
        self.parser = ArgumentParser(
            description="Captures images and videos from camera based on person detection"
        )
        self.add_arguments()

    def add_arguments(self) -> None:
        self.parser.add_argument(
            "snapshot_dir",
            metavar="snapshot_dir",
            type=str,
            help="directory for saving captured images",
        )
        self.parser.add_argument(
            "-d",
            "--dropbox_uploader",
            metavar="dropbox_uploader",
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
            metavar="logdir",
            type=str,
            help="Path to the log directory",
        )
        self.parser.add_argument(
            "-c",
            "--crop",
            metavar="crop",
            type=tuple_check,
            help="A tuple of four integers for cropping frame",
        )
        self.parser.add_argument(
            "-p",
            "--period",
            metavar="period",
            type=int,
            help="Period in seconds for analysing video frame",
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
