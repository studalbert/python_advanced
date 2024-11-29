"""
Напишите Flask POST endpoint /calculate,
который принимает на вход арифметическое выражение и
вычисляет его с помощью eval (о безопасности думать не нужно,
работайте только над фукнционалом).

Поскольку наш Flask endpoint работает с арифметическими выражениями,
напишите 4 error_handler-а, которые будет обрабатывать
ArithmeticError, ZeroDivisionError, FloatingPointError и OverflowError
(о значении этих исключений вы можете посмотреть
вот на этой страничке https://docs.python.org/3/library/exceptions.html ).

Напишите по unit-тесту на каждую ошибку: тест должен проверять, что ошибка обрабатывается

Примечание: рекомендуется обрабатывать  ArithmeticError,
перехватывая InternalServerError ,
остальные классы ошибок можно обрабатывать напрямую.
"""

from decimal import Overflow
from typing import Optional

from flask import Flask
from werkzeug.exceptions import InternalServerError
import math

app = Flask(__name__)


@app.route("/calculate/<path:expression>")
def calculate(expression):
    result = eval(expression)
    return f"{result}"


@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(e: ZeroDivisionError):
    return "We are unable to divide by zero!", 400


@app.errorhandler(FloatingPointError)
def handle_arithmetic_error(e):
    return f"{e}", 400


@app.errorhandler(OverflowError)
def handle_general_exception(e):
    return f"{e}", 400


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
    original: Optional[Exception] = getattr(e, "original_exception", None)
    if isinstance(original, ArithmeticError):
        return "e", 400

    return "Internal server error", 500


if __name__ == "__main__":
    app.run()
