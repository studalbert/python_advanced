"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import subprocess, shlex

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

from module_05_processes_and_threads.homework.hw5_add.self_printing import result

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=30)])


def run_python_code_in_subproccess(code: str, timeout: int):
    cmd_str = f"prlimit --nproc=1:1 python -c '{code}'"
    cmd = shlex.split(cmd_str)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    try:
        process.wait(timeout)
        stdout, stderr = process.communicate()
        if stderr:
            return (f'Ошибка при выполнении команды:'
                    f'<pre>{stderr}</pre>'), 400
        return f'<pre>{stdout}</pre>'

    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        stdout, stderr = process.communicate()
        return (f"<b>Исполнение кода не уложилось в данное время.</b> "
                f"<pre>{stdout}</pre>"
                f"<pre>{stderr}</pre>"), 400


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        res = run_python_code_in_subproccess(code, timeout)
        return res
    else:
        return f'Invalid input, {form.errors}', 400


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
