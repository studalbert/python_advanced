import unittest
from redirect import Redirect

class TestRedirect(unittest.TestCase):

    def test_stdout_stderr_was_indeed(self):
        with open('stdout.txt', 'w') as stdout_file, open('stderr.txt', 'w') as stderr_file:
            with Redirect(stdout=stdout_file, stderr=stderr_file):
                print('Hello stdout.txt')
                raise Exception('Hello stderr.txt')
        with open('stdout.txt', 'r') as stdout_file:
            self.assertIn('Hello stdout.txt', stdout_file.read())
        with open('stderr.txt', 'r') as stderr_file:
            self.assertIn('Exception: Hello stderr.txt', stderr_file.read())

    def test_stdout_stderr_redirected_in_class(self):
        with self.assertRaises(Exception):
            with open('stdout.txt', 'w') as stdout_file, open('stderr.txt', 'w') as stderr_file:
                with Redirect(stdout=stdout_file, stderr=stderr_file):
                    raise Exception('Hello stderr.txt')
                raise Exception('Hello stderr')

    def test_one_arg_stdout(self):
        with open('stdout.txt', 'w') as stdout_file:
            with Redirect(stdout=stdout_file):
                print("This is test with 1 arg stdout")
                raise Exception("This is test with one arg stdout")
        with open('stdout.txt', 'r') as stdout_file:
            self.assertIn('This is test with 1 arg stdout', stdout_file.read())
        with open('stderr.txt', 'r') as stderr_file:
            self.assertNotIn('Exception: This is test with one arg stdout', stderr_file.read())

    def test_one_arg_stderr(self):
        with open('stderr.txt', 'w') as stderr_file:
            with Redirect(stderr=stderr_file):
                print("This is test with 1 arg stderr")
                raise Exception("This is test with one arg stderr")
        with open('stdout.txt', 'r') as stdout_file:
            self.assertNotIn('This is test with 1 arg stderr', stdout_file.read())
        with open('stderr.txt', 'r') as stderr_file:
            self.assertIn('Exception: This is test with one arg stderr', stderr_file.read())




if __name__ == '__main__':
    # unittest.main()
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)
