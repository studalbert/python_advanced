import datetime
import os
import random
import re

from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def test_function():
    return 'Привет, мир!'

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']

@app.route('/cars')
def cars_function():
    return ', '.join(cars_list)

cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

@app.route('/cats')
def cats_function():
    return random.choice(cats)



@app.route('/get_time/now')
def time_function():
    current_time = datetime.datetime.now()
    return f'Точное время: {current_time}'


@app.route('/get_time/future')
def time_plus_function():
    current_time = datetime.datetime.now()
    current_time_after_hour = current_time + datetime.timedelta(hours=1)
    return f'Точное время через час будет {current_time_after_hour}'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
with open(BOOK_FILE, 'r', encoding='utf-8') as book:
    res_book = book.read()
    result = re.findall(r'\b\w+\b', res_book)


@app.route('/get_random_word')
def word_function():
    return random.choice(result)


@app.route('/counter')
def counter():
    counter.vizits += 1
    return f'Эта страничка открывалась {counter.vizits} раз'

counter.vizits = 0

if __name__ == '__main__':
    app.run(debug=True)
