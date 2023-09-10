import os
import logging
from util import get_log_file_name
from argparse import ArgumentParser

logger = logging.getLogger(__name__)


def args_parser() -> ArgumentParser:
    """
    Parses command line arguments.

    :return: An ArgumentParser object containing parsed command line arguments.
    :rtype: ArgumentParser
    """
    arg_parser: ArgumentParser = ArgumentParser(
        description="Captures images and videos from camera based on motion detection"
    )
    arg_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Set the log level to DEBUG"
    )
    arg_parser.add_argument("--logdir", type=str, help="Path to the log directory")
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


if __name__ == "__main__":
    parser: ArgumentParser = args_parser()
    args = parser.parse_args()
    set_log_config(args.verbose, args.logdir)
