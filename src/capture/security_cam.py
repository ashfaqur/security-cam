import os
import logging
from src.capture.util import get_log_file_name
from src.capture.record import main
from argparse import ArgumentParser, ArgumentTypeError
from typing import Tuple


logger = logging.getLogger(__name__)


def args_parser() -> ArgumentParser:
    """
    Parses command line arguments.

    :return: An ArgumentParser object containing parsed command line arguments.
    :rtype: ArgumentParser
    """
    arg_parser: ArgumentParser = ArgumentParser(
        description="Captures images and videos from camera based on person detection"
    )
    arg_parser.add_argument(
        "snapshot_dir",
        metavar="snapshot_dir",
        type=str,
        help="directory for saving snapshots",
    )
    arg_parser.add_argument(
        "-d",
        "--dropbox_uploader",
        metavar="dropbox_uploader",
        type=str,
        help="Path to dropbox uploader script",
    )
    arg_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
    )
    arg_parser.add_argument(
        "-w", "--window", action="store_true", help="Show video window"
    )
    arg_parser.add_argument(
        "-l", "--logdir", metavar="logdir", type=str, help="Path to the log directory"
    )
    arg_parser.add_argument(
        "-c",
        "--crop",
        metavar="crop",
        type=tuple_check,
        help="A tuple of four integers for cropping frame",
    )
    arg_parser.add_argument(
        "-p",
        "--period",
        metavar="period",
        type=int,
        help="Period in seconds for analysing video frame",
    )
    return arg_parser


def set_log_config(verbose: bool, logdir: str) -> None:
    """
    Sets the logging configuration for the application.

    This function sets the logging level and log file path based on the input parameters.

    :param verbose: A boolean indicating whether to set the logging level to `DEBUG`.
    :param logdir: The path to the directory where the log file should be written. If `None`, log messages are printed to the console.
    :return: None
    """
    log_level: int = logging.INFO
    log_level_detail: str = "INFO"
    if verbose:
        log_level = logging.DEBUG
        log_level_detail = "DEBUG"
    if logdir:
        if os.path.isdir(logdir):
            log_file_path = os.path.join(logdir, get_log_file_name())
            logging.basicConfig(
                filename=log_file_path,
                filemode="w",
                format="%(asctime)s %(levelname)-8s %(message)s",
                level=log_level,
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            logging.info(f"Logs are written to file '{log_file_path}'")
        else:
            raise ValueError(f"Given log file directory '{logdir}' is invalid")
    else:
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=log_level,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    logging.debug(f"Log level set to {log_level_detail}")


def tuple_check(s: str) -> Tuple[int, ...]:
    try:
        values = tuple(map(int, s.split(",")))
        if len(values) != 4:
            raise ArgumentTypeError("Tuple must contain exactly four integers.")
        return values
    except ValueError:
        raise ArgumentTypeError("Tuple must contain integers only.")


if __name__ == "__main__":
    parser: ArgumentParser = args_parser()
    args = parser.parse_args()
    set_log_config(args.verbose, args.logdir)

    try:
        main(
            args.snapshot_dir,
            args.dropbox_uploader,
            args.window,
            args.crop,
            args.period,
        )
    except Exception as e:
        logging.error(e)
        raise e
