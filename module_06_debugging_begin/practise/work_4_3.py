"""
Представим, что мы работаем в IT отделе крупной компании.
У HR отдела появилась гениальная идея - поздравлять сотрудников
в день рождения однодневным отгулом.

Для этого HR отделу надо предоставить данные на всех
сотрудников вместе с их датами рождения.
Сотрудники у нас работают либо в IT-, либо в PROD-отделе.
Идентификационным номером сотрудника является число,
анкеты сотрудников в формате json вы можете найти в папке fixtures.
В написанное приложение добавьте логи так,
чтобы они помогли найти ошибки со следующими сотрудниками
    отдел IT, сотрудники 1, 2, 3, 4, 5
    отдел PROD, сотрудники 1, 2, 3, 4, 5
"""

import json
import logging
import os
from json import JSONDecodeError
from typing import Optional

from flask import Flask
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)

logger = logging.getLogger("account_book")

current_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(current_dir, "fixtures")

departments = {"IT": "it_dept", "PROD": "production_dept"}


@app.route("/account/<department>/<int:account_number>/")
def account(department: str, account_number: int):

    dept_directory_name = departments.get(department)

    if dept_directory_name is None:
        return "Department not found", 404

    full_department_path = os.path.join(fixtures_dir, dept_directory_name)

    account_data_file = os.path.join(full_department_path, f"{account_number}.json")
    try:
        with open(account_data_file, "r") as fi:
            account_data_txt = fi.read()

        account_data_json = json.loads(account_data_txt)

        name, birth_date = account_data_json["name"], account_data_json["birth_date"]
        day, month, _ = birth_date.split(".")
        logger.debug(f"{name} was born on {day}.{month}")
        return f"{name} was born on {day}.{month}"
    except Exception as exc:

        logger.exception(f"Error. json file: {account_data_file}", exc_info=exc)
        return "Ошибка от сервера", 500


@app.errorhandler(FileNotFoundError)
def handle_error(e):
    logger.error(f"Error: {e}")
    return f"Error: {e}", 400


@app.errorhandler(KeyError)
def handle_key_error(e):
    logger.error(f"KeyError: {e}")
    return f"KeyError: {e}", 400


@app.errorhandler(JSONDecodeError)
def handle_decode(e):
    logger.error(f"JSONDecodeError: {e}")
    return f"JSONDecodeError: {e}", 400


@app.errorhandler(ValueError)
@app.errorhandler(InternalServerError)
def handle_exc(e):
    logger.info("Произошла ошибка от сервера")
    original: Optional[Exception] = getattr(e, "original_exception", None)

    if isinstance(original, FileNotFoundError):
        logger.error(
            f"Tried to access {original.filename}. Exception info: {original.strerror}"
        )
        return (
            f"Tried to access {original.filename}. Exception info: {original.strerror}"
        )

    elif isinstance(original, OSError):
        logger.error(f"Unable to access a card. Exception info: {original.strerror}")
        return f"Unable to access a card. Exception info: {original.strerror}"

    return "Internal server error", 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Started account server")
    app.run(debug=True)
