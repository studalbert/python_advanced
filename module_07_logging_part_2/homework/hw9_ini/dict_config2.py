import sys

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "fileFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
        "consoleFormatter": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z",
        },
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "consoleFormatter",
            "stream": sys.stdout,
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "fileFormatter",
            "filename": "logfile.log",
        },
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["consoleHandler"]},
        "appLogger": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False,
        },
    },
}
