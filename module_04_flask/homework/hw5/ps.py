"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import subprocess, shlex
from typing import Tuple

from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str | tuple[str, int]:
    args = request.args.getlist('arg')
    user_cmd = ''.join(args)
    clean_user_cmd = shlex.quote(user_cmd)
    command_str = f"ps {clean_user_cmd}"
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True, encoding='utf-8')
    if result.returncode == 0:
        return f'<pre>{result.stdout}</pre>'
    else:
        return f"Incorrect command: {result.stderr}", 400


if __name__ == "__main__":
    app.run(debug=True)
