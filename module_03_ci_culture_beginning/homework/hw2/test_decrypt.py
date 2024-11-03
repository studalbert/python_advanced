import unittest
from decrypt import decrypt


class TestDecrypt(unittest.TestCase):

    def test_one(self):
        res = 'абра-кадабра'
        examples = (
            'абра-кадабра.',
            'абраа..-кадабра',
            'абраа..-.кадабра',
            'абра--..кадабра',
            'абрау...-кадабра'
        )
        for example in examples:
            with self.subTest(example):
                func_res = decrypt(example)
                self.assertEqual(res, func_res)

    def test_two(self):
        examples = {
            'абра........': '',
            'абр......a.': 'a',
            '1..2.3': '23',
            '.': '',
            '1.......................': ''
        }
        for key,value in examples.items():
            with self.subTest(key):
                func_res = decrypt(key)
                self.assertEqual(value, func_res)