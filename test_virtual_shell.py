import unittest
from io import StringIO
import sys
from virtual_shell import VirtualShell

class TestVirtualShell(unittest.TestCase):
    def setUp(self):
        self.shell = VirtualShell('config.csv')

    def test_ls(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.shell.ls(['/'])
        sys.stdout = sys.__stdout__
        self.assertIn('/startup.sh', captured_output.getvalue())

    def test_cd(self):
        self.shell.cd(['/'])
        self.assertEqual(self.shell.current_path, '/')

    def test_uname(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.shell.uname([])
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), 'VirtualOS')

    def test_tac(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.shell.tac(['/testfile.txt'])
        sys.stdout = sys.__stdout__
        self.assertIn('line3', captured_output.getvalue())

    def test_rev(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.shell.rev(['/testfile.txt'])
        sys.stdout = sys.__stdout__
        self.assertIn('3enil', captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
