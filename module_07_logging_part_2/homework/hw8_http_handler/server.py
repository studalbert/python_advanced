import json
from flask import Flask, request

from logging_config import get_logger

app = Flask(__name__)
logs_list = []


@app.route("/log", methods=["POST"])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    form_data = request.get_data(as_text=True)
    logs_list.append(json.loads(form_data))
    return "OK", 200


@app.route("/logs", methods=["GET"])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    rendered_logs = "\n".join(str(log) for log in logs_list)
    return f"<pre>{rendered_logs}</pre>", 200


# TODO запустить сервер
if __name__ == "__main__":

    app.run(debug=True)
