"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.fields.numeric import IntegerField
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: IntegerField):
        if isinstance(field.data, int):
            if field.data < min or field.data > max:
                raise ValidationError(message)
        else:
            raise ValidationError('phone must be int')
    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = 1000000000
        self.max = 9999999999
        self.message = message

    def __call__(self, form: FlaskForm, field: IntegerField):
        if isinstance(field.data, int):
            if field.data < self.min or field.data > self.max:
                raise ValidationError(self.message)
        else:
            raise ValidationError('phone must be int')