import unittest
from remote_execution import app

class TestRemoteExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        cls.app = app.test_client()
        cls.base_url = '/run_code'

    def test_timeout(self):
        with self.subTest(1):
            self.data = {'code': 'import time;time.sleep(5)',
                         'timeout': 3}
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Исполнение кода не уложилось в данное время',
                          response.data.decode())
        with self.subTest(2):
            self.data = {'code': 'print("Hello world!")',
                         'timeout': 'asd'}
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid input',
                          response.data.decode())
        with self.subTest(3):
            self.data = {'code': 'print("Hello world!")',
                         'timeout': 35}
            response = self.app.post(self.base_url, data=self.data)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid input',
                          response.data.decode())

    def test_unsafe_input(self):
        self.data = {'code': 'print()"; echo "hacked',
                     'timeout': 3}
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Ошибка при выполнении команды',
                      response.data.decode())

if __name__ == '__main__':
    unittest.main()
