import logging.config
import logging

import requests

from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import (
    LevelFileHandler,
)
from logging.handlers import HTTPHandler


class AsciiFilter(logging.Filter):
    def filter(self, record):
        return str.isascii(record.msg)


class CustomHTTPHandler(HTTPHandler):
    def emit(self, record):
        log_entry = self.mapLogRecord(record)
        # Отправляем лог в формате JSON
        requests.post(f"http://{self.host}{self.url}", json=log_entry)


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
        "http_handler": {
            "()": CustomHTTPHandler,
            "level": "DEBUG",
            "formatter": "base",
            "host": "localhost:5000",
            "url": "/log",
            "method": "POST",
        },
    },
    "loggers": {
        "app": {
            "level": "DEBUG",
            "handlers": ["http_handler"],
            "propagate": False,
        },
        "utils": {
            "level": "DEBUG",
            "handlers": ["http_handler"],
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
