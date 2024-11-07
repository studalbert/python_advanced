"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app


class TestRegistrationForm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        cls.app = app.test_client()
        cls.base_url = '/registration'

    def setUp(self):
        # Корректные данные
        self.data = {
            'email': 'test@example.com',
            'phone': 1234567890,
            'name': 'Иванов В.Ф.',
            'address': '123 Test St',
            'index': 123456,
            'comment': ''}

    def test_correct_email(self):
        # email, проходящий валидацию
        with self.subTest('correct_email'):
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 200)
        # email, не проходящий валидацию
        with self.subTest('Incorrect_email'):
            self.data['email'] = 'qwerty'
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)

    def test_correct_phone(self):
        # phone, проходящий валидацию
        with self.subTest('correct_phone'):
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 200)
        # phone, не проходящий валидацию
        with self.subTest('Incorrect_phone'):
            self.data['phone'] = 'dasdd'
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)

    def test_correct_name(self):
        # name, проходящий валидацию
        with self.subTest('correct_name'):
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 200)
        # name, не проходящий валидацию
        with self.subTest('Incorrect_name'):
            self.data['name'] = ''
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)

    def test_correct_address(self):
        # address, проходящий валидацию
        with self.subTest('correct_address'):
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 200)
        # address, не проходящий валидацию
        with self.subTest('Incorrect_address'):
            self.data['address'] = ''
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)

    def test_correct_index(self):
        # index, проходящий валидацию
        with self.subTest('correct_index'):
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 200)
        # index, не проходящий валидацию
        with self.subTest('Incorrect_index'):
            self.data['index'] = ''
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
