"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""

import re
from typing import List


def my_t9(input_numbers: str) -> List[str]:
    num2 = "[abc]"
    num3 = "[def]"
    num4 = "[ghi]"
    num5 = "[jkl]"
    num6 = "[mno]"
    num7 = "[pqrs]"
    num8 = "[tuv]"
    num9 = "[wxyz]"
    res = ""
    for num in input_numbers:
        if num == "2":
            res += num2
        elif num == "3":
            res += num3
        elif num == "4":
            res += num4
        elif num == "5":
            res += num5
        elif num == "6":
            res += num6
        elif num == "7":
            res += num7
        elif num == "8":
            res += num8
        elif num == "9":
            res += num9

    words = "/home/user/Downloads/words"
    with open(words, "r") as file:
        pattern = re.compile(rf"\b{res}'?\w*\b", re.IGNORECASE)
        result_list = pattern.findall(file.read())
    return result_list


if __name__ == "__main__":
    numbers: str = input()
    words: List[str] = my_t9(numbers)
    print(*words, sep="\n")
