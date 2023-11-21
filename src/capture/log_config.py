import os
import logging
from src.capture.util import get_log_file_name


class LogConfig:
    def __init__(self, verbose: bool, logdir: str):
        self.verbose = verbose
        self.logdir = logdir
        self.set_log_config()

    def set_log_config(self) -> None:
        """
        Sets the logging configuration for the application.

        This function sets the logging level and log file path based on the input parameters.

        :return: None
        """
        log_level: int = logging.INFO
        log_level_detail: str = "INFO"
        if self.verbose:
            log_level = logging.DEBUG
            log_level_detail = "DEBUG"
        if self.logdir:
            if os.path.isdir(self.logdir):
                log_file_path = os.path.join(self.logdir, get_log_file_name())
                logging.basicConfig(
                    filename=log_file_path,
                    filemode="w",
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    level=log_level,
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
                logging.info(f"Logs are written to file '{log_file_path}'")
            else:
                raise ValueError(f"Given log file directory '{self.logdir}' is invalid")
        else:
            logging.basicConfig(
                format="%(asctime)s %(levelname)-8s %(message)s",
                level=log_level,
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        logging.debug(f"Log level set to {log_level_detail}")
