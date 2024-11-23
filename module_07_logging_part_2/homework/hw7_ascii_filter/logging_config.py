import logging.config
import logging
from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import (
    LevelFileHandler,
)


class AsciiFilter(logging.Filter):
    def filter(self, record):
        return str.isascii(record.msg)


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["ascii_filter"],
        },
        "rotate_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename": "utils.log",
            # "mode": "a",
            "when": "h",
            "interval": 10,
            "backupCount": 3,
            "filters": ["ascii_filter"],
        },
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False,
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["rotate_file"],
            "propagate": False,
        },
    },
    "filters": {"ascii_filter": {"()": AsciiFilter}},
    # "root": {} # == "": {}
}


def get_logger(name):
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger(name)
    # logger.setLevel("DEBUG")
    # custom_handler = LevelFileHandler()
    # formatter = logging.Formatter(
    #     fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
    # )
    # custom_handler.setFormatter(formatter)
    # logger.addHandler(custom_handler)

    return logger
