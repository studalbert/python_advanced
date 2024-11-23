import logging
import sys


class LevelFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        message = self.format(record)
        if record.levelname == "DEBUG":
            with open("calc_debug.log", "a") as f:
                f.write(message + "\n")
        if record.levelname == "INFO":
            with open("calc_info.log", "a") as f:
                f.write(message + "\n")
        if record.levelname == "WARNING":
            with open("calc_warning.log", "a") as f:
                f.write(message + "\n")
        if record.levelname == "ERROR":
            with open("calc_error.log", "a") as f:
                f.write(message + "\n")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel("DEBUG")
    custom_handler = LevelFileHandler()
    formatter = logging.Formatter(
        fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
    )
    custom_handler.setFormatter(formatter)
    logger.addHandler(custom_handler)

    return logger
