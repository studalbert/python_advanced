import logging
import sys
from utils import string_to_operator
from logging_config import get_logger
import logging_tree

logger = get_logger("app")


def calc(args):
    logger.info(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error("Error while converting number 1", exc_info=e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error("Error while converting number 1", exc_info=e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.info(f"Result: {result}")
    logger.info(f"{num_1} {operator} {num_2} = {result}")


if __name__ == "__main__":
    # calc(sys.argv[1:])
    with open("logging_tree.txt", "w") as f:
        f.write(logging_tree.format.build_description())
    calc("2+3")
