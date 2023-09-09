import os
import logging
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
    arg_parser.add_argument("--logpath", type=str, help="Path to the log file")
    return arg_parser


def set_log_config(verbose: bool, logpath: str) -> None:
    log_level: int = logging.INFO
    log_level_detail: str = "INFO"
    if verbose:
        log_level = logging.DEBUG
        log_level_detail = "DEBUG"
    if logpath and os.path.exists(os.path.dirname(logpath)):
        logging.basicConfig(
            filename=logpath,
            filemode="w",
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=log_level,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info(f"Logs are written to file {logpath}")
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
    set_log_config(args.verbose, args.logpath)
