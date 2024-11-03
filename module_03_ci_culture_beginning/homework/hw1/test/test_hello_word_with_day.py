import unittest
import datetime

from freezegun import freeze_time

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app, GREETINGS


class TestWeekday(unittest.TestCase):

    @classmethod
    def setUp(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.base_url = '/hello-world/'

    @classmethod
    def get_day(cls, i):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        return date

    def test_weekday(self):
        username = 'Хорошей среды'
        for i in range(7):
            date = self.get_day(i)
            with self.subTest(i), freeze_time(date):
                day = date.weekday()
                response = self.app.get(self.base_url + username)
                response_text = response.data.decode()
                res = GREETINGS[day] + "!"
                self.assertTrue(res in response_text)
