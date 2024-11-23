import logging
import sys
from utils import string_to_operator

logger = logging.getLogger(__name__)


def config_logging():
    logger_base = logging.getLogger()
    logger_base.setLevel("DEBUG")
    custom_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
    )
    custom_handler.setFormatter(formatter)
    logger_base.addHandler(custom_handler)


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
    config_logging()
    # calc(sys.argv[1:])
    calc("2+3")
