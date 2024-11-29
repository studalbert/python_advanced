import logging.config

from module_07_logging_part_2.homework.hw3_level_file_handler.logger_helper import (
    LevelFileHandler,
)

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "file": {"()": LevelFileHandler, "level": "DEBUG", "formatter": "base"}
    },
    "loggers": {
        "app": {"level": "DEBUG", "handlers": ["file"], "propagate": False},
        "utils": {"level": "DEBUG", "handlers": ["file"], "propagate": False},
    },
    # "filters": {},
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
