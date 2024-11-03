import unittest
from datetime import datetime

from module_03_ci_culture_beginning.homework.hw4.person import Person


class TestPerson(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.person = Person('Вася', 2000, 'Russia')

    def test_get_age(self):
        res = datetime.now().year - self.person.yob
        method_res = self.person.get_age()
        self.assertEqual(res, method_res)

    def test_get_name(self):
        res = self.person.name
        method_res = self.person.get_name()
        self.assertEqual(res, method_res)

    def test_set_name(self):
        new_name = 'Вова'
        self.person.set_name(new_name)
        self.assertEqual(new_name, self.person.name)

    def test_get_address(self):
        res = self.person.address
        method_res = self.person.get_address()
        self.assertEqual(res, method_res)

    def test_set_address(self):
        new_address = 'China'
        self.person.set_address(new_address)
        self.assertEqual(new_address, self.person.address)

    def test_is_homeless(self):
        res = False if self.person.address else True
        method_res = self.person.is_homeless()
        self.assertEqual(res, method_res)