"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""
from datetime import datetime
from flask import Flask

app = Flask(__name__)

weekdays_tuple = ('хорошего понедельника', 'хорошего вторника', 'хорошей среды', 'хорошего четверга', 'хорошей пятницы',
                  'хорошей субботы', 'хорошего воскресенья')


@app.route('/hello-world/<string:username>')
def hello_world(username):
    weekday = datetime.today().weekday()
    return f'Привет, {username}. {weekdays_tuple[weekday]}'


if __name__ == '__main__':
    app.run(debug=True)
