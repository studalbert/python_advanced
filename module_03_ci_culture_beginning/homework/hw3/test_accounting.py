from module_02_linux.homework.hw7.accounting import app, storage
import unittest


class TestAccounting(unittest.TestCase):
    @classmethod
    def setUp(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        storage.update({2024: {11: 5000, 1: 6000, 9: 7000},
                        2023: {10: 7000, 11: 8000, 'total': 15000}})

    def test_endpoint_add(self):
        base_url = '/add/'
        date = 'fgfdg/'
        number = '8000'
        with self.subTest(1), self.assertRaises(ValueError):
            # Проверка, что endpoint /add/ может принять дату только в формате YYYYMMDD,
            # а при подаче невалидного значения вызовется исключение ValueError.
            response = self.app.get(base_url + date + number)

        date = '20220212/'
        with self.subTest(2):
            # Проверка, что словарь storage действительно заполнился необходимыми данными
            response = self.app.get(base_url + date + number)
            res = storage.setdefault(2022, {}).setdefault(2)
            self.assertEqual(res, int(number))

        with self.subTest(3):
            # Проверка, что в словаре хранятся суммарные затраты по каждому году
            response = self.app.get(base_url + '20240612/' + '10000')
            res = storage.setdefault(2024, {}).setdefault('total')
            self.assertEqual(res, 28000)

    def test_endpoint_calculate_month(self):
        base_url = '/calculate/'
        year = '2024/'
        month = '09'
        res = '7000'
        with self.subTest(year):
            # Тест, когда в словаре есть такой год и месяц
            response = self.app.get(base_url + year + month)
            response_text = response.data.decode()
            self.assertEqual(res, response_text)

        month = '02'
        with self.subTest(year):
            # Тест, когда в словаре нет такого месяца
            res = 'None'
            response = self.app.get(base_url + year + month)
            response_text = response.data.decode()
            self.assertEqual(res, response_text)

        invalid_month = 'qwerty'
        with self.subTest(invalid_month):
            # Тест, при некорректном вводе месяца
            response = self.app.get(base_url + year + invalid_month)
            self.assertEqual(response.status_code, 404)

    def test_endpoint_calculate(self):
        base_url = '/calculate/'
        year = '2023'
        res = '15000'
        with self.subTest(year):
            # Тест, когда в словаре есть такой год
            response = self.app.get(base_url + year)
            response_text = response.data.decode()
            self.assertEqual(res, response_text)

        year = '2026'
        with self.subTest(year):
            # Тест, когда в словаре нет такого года
            res = 'None'
            response = self.app.get(base_url + year)
            response_text = response.data.decode()
            self.assertEqual(res, response_text)

        invalid_year = 'qwerty'
        with self.subTest(invalid_year):
            # Тест, при некорректном вводе года
            response = self.app.get(base_url + invalid_year)
            self.assertEqual(response.status_code, 404)
