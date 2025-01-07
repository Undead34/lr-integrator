import logging
from logging.handlers import RotatingFileHandler
import os

from .constants import APP_LOGGER_PATH

def setup_logger(log_file: str = APP_LOGGER_PATH):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    logger.propagate = False

    return logger

logger = setup_logger()
