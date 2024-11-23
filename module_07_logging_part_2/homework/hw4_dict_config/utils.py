import logging
from typing import Union, Callable
from operator import sub, mul, truediv, add
from logging_config import get_logger

logger = get_logger("utils")

OPERATORS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        logger.error(f"wrong operator type, {value}")
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        logger.error(f"wrong operator type, {value}")
        raise ValueError("wrong operator value")

    return OPERATORS[value]
