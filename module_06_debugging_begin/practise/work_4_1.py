"""
Перепишите банковский endpoint, заменив запись сообщений в файл на логирование.
Проверьте работу endpoint-а. Код этого задания мы будем использовать в следующем уроке,
поэтому обязательно выполните его перед изучением следующей темы
"""

import csv


from typing import Optional
import logging
from flask import Flask
from werkzeug.exceptions import InternalServerError


app = Flask(__name__)
logger = logging.getLogger("bank_api")


@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    branch_card_file_name = f"bank_data/{branch}.csv"

    with open(branch_card_file_name, "r") as fi:
        csv_reader = csv.DictReader(fi, delimiter=",")
        logger.info("Открыли csv файл")
        for record in csv_reader:
            if int(record["id"]) == person_id:
                logger.info("Нашли человека с указанным id")
                return record["name"]
        else:
            logger.info("НЕ Нашли человека с указанным id")
            return "Person not found", 404


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        filename="banking.log",
        filemode="w",
        encoding="utf-8",
    )
    app.run()
