"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: list) -> float:
    summ = 0
    count_file = 0
    for line in ls_output:
        columns = line.split()
        if not columns[0].startswith('d'):
            summ += int(columns[4])
            count_file += 1
    try:
        return summ/count_file
    except ZeroDivisionError:
        return 0


if __name__ == '__main__':
    lines: list = sys.stdin.readlines()[1:]
    mean_size: float = get_mean_size(lines)
    print(mean_size)

