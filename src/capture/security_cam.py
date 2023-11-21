import logging
from src.capture.record import main
from src.capture.arg_parser import ArgParser
from src.capture.log_config import LogConfig

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser: ArgParser = ArgParser()
    args = parser.parse_args()
    LogConfig(args.verbose, args.logdir)

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

    logger.info("Program Done")
