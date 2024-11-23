# TODO переписать реализацию ini-файла в формате dict-конфигурации.
import configparser
import sys


def ini_to_dict(ini_file):
    config = configparser.ConfigParser(interpolation=None)
    config.read(ini_file)

    dict_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {},
        "handlers": {},
        "loggers": {},
    }

    # Обрабатываем форматтеры
    if "formatters" in config:
        for key in config["formatters"]["keys"].split(","):
            section = f"formatter_{key}"
            if section in config:
                dict_config["formatters"][key] = {
                    "format": config[section].get("format"),
                    "datefmt": config[section].get("datefmt"),
                }

    # Обрабатываем обработчики
    if "handlers" in config:
        for key in config["handlers"]["keys"].split(","):
            section = f"handler_{key}"
            if section in config:
                handler_args = eval(config[section].get("args"))
                dict_config["handlers"][key] = {
                    "class": f'logging.{config[section]["class"]}',
                    "level": config[section].get("level"),
                    "formatter": config[section].get("formatter"),
                }
                # Добавляем аргументы
                if "StreamHandler" in config[section]["class"]:
                    dict_config["handlers"][key]["stream"] = handler_args[0]
                elif "FileHandler" in config[section]["class"]:
                    dict_config["handlers"][key]["filename"] = handler_args[0]

    # Обрабатываем логгеры
    if "loggers" in config:
        for key in config["loggers"]["keys"].split(","):
            section = f"logger_{key}"
            if section in config:
                dict_config["loggers"][key] = {
                    "level": config[section].get("level"),
                    "handlers": config[section].get("handlers").split(","),
                    "propagate": config[section].getboolean("propagate", True),
                }

    return dict_config


ini_file = "logging_conf.ini"
dict_config = ini_to_dict(ini_file)
print(dict_config)
