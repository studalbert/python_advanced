import unittest
from block_errors import BlockErrors

class TestBlockErrors(unittest.TestCase):
    def test_error_ignored(self):
        err_types = {ZeroDivisionError}
        try:
            with BlockErrors(err_types):
                a = 1 / 0
        except:
            self.fail()

    def test_error(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0

    def test_error_is_thrown_higher_ignored(self):
        outer_err_types = {TypeError}
        try:
            with BlockErrors(outer_err_types):
                inner_err_types = {ZeroDivisionError}
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
        except:
            self.fail()

    def test_subclass_ignored(self):
        err_types = {Exception}
        try:
            with BlockErrors(err_types):
                a = 1 / '0'
        except:
            self.fail()

if __name__ == '__main__':
    unittest.main()
