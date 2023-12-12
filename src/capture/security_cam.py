import logging
from src.capture.record import main
from src.capture.arg_parser import ArgParser, Args
from src.capture.log_config import LogConfig

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser: ArgParser = ArgParser()
    args: Args = parser.parse_args()
    LogConfig(args.verbose, args.logdir)

    try:
        main(
            args.snapshot_dir,
            args.dropbox_uploader,
            args.window,
            args.crop,
            args.period,
            args.sensitivity,
            args.upload_path,
        )
    except Exception as e:
        logging.error(e)
        raise e

    logger.info("Program Done")
