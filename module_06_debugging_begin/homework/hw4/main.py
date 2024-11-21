"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""

import json
import shlex
import subprocess
from typing import Dict
from itertools import groupby


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    result = dict()
    with open("skillbox_json_messages.log", "r") as file:
        for line in file:
            line_dict = json.loads(line)
            line_level = line_dict["level"]
            if result.get(line_level) is None:
                result[line_level] = 1
            else:
                result[line_level] += 1
    return result


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    result = dict()
    with open("skillbox_json_messages.log", "r") as file:
        for line in file:
            line_dict = json.loads(line)
            line_time = line_dict["time"]
            hour = line_time[:2]
            if result.get(hour) is None:
                result[hour] = 1
            else:
                result[hour] += 1

    result_num = max(result.values())
    for hour in result:
        if result[hour] == result_num:
            return hour


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    counter = 0
    cmd_str = 'grep \'"level": "CRITICAL"\' skillbox_json_messages.log'
    cmd = shlex.split(cmd_str)
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    stdout, stderr = proc.communicate()
    logs = stdout.split("\n")
    logs = (json.loads(log) for log in logs if log)
    start_time = "05:00:00"
    end_time = "05:20:00"
    for log in logs:
        if start_time <= log["time"] <= end_time:
            counter += 1
    return counter


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    counter = 0
    cmd_str = r"grep '\bdog\b' skillbox_json_messages.log"
    cmd = shlex.split(cmd_str)
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    stdout, stderr = proc.communicate()
    logs = stdout.split("\n")
    logs = (json.loads(log) for log in logs if log)
    for log in logs:
        if "dog's" not in log["message"]:
            counter += 1
    return counter


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    words_dict = dict()
    cmd_str = 'grep \'"level": "WARNING"\' skillbox_json_messages.log'
    cmd = shlex.split(cmd_str)
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    stdout, stderr = proc.communicate()
    logs = (json.loads(log) for log in stdout.splitlines())
    for log in logs:
        for word in log["message"].split():
            if words_dict.get(word) is None:
                words_dict[word] = 1
            else:
                words_dict[word] += 1
    res_count = max(words_dict.values())
    for word in words_dict:
        if words_dict[word] == res_count:
            return word


if __name__ == "__main__":
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f"{i}. {task_answer}")
