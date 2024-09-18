import logging
import logging.handlers
import os

LOG_FILENAME = "kronoterm_cloud_relay.log"


def create_logger(logger_name):
    """Create a logger for use in all cases."""
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=5)
    console_handler = logging.StreamHandler()
    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s [%(levelname)8s] [%(filename)s:%(lineno)4s:%(funcName)20s()]\t%(message)s",
        datefmt="[%d.%m.%Y %H:%M;%S]",
        handlers=[file_handler, console_handler],
    )
    return logging.getLogger(logger_name)
