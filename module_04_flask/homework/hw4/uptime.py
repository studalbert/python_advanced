"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
import subprocess, shlex

from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def _uptime() -> str:
    command_str = f"uptime -p"
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True, encoding='utf-8')
    UPTIME = result.stdout
    return f"Current uptime is {UPTIME}"


if __name__ == '__main__':
    app.run(debug=True)
