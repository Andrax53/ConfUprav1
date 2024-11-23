import unittest
from uvm import assembler, interpreter

class TestUVM(unittest.TestCase):

    def test_interpreter_move(self):
        code = [("move", 352, 346)]
        expected = [{'op': 'move', 'A': '0x52', 'B': '0x160', 'C': '0x15A'}]
        self.assertEqual(interpreter(code), expected)

    def test_interpreter_read(self):
        code = [("read", 511, 112, 71)]
        expected = [{'op': 'read', 'A': '0x13', 'B': '0x1FF', 'C': '0x70', 'D': '0x47'}]
        self.assertEqual(interpreter(code), expected)

    def test_interpreter_write(self):
        code = [("write", 27, 148, 883)]
        expected = [{'op': 'write', 'A': '0x1F', 'B': '0x1B', 'C': '0x94', 'D': '0x373'}]
        self.assertEqual(interpreter(code), expected)

    def test_interpreter_bswap(self):
        code = [("bswap", 810, 188)]
        expected = [{'op': 'bswap', 'A': '0x16', 'B': '0x32A', 'C': '0xBC'}]
        self.assertEqual(interpreter(code), expected)

if __name__ == '__main__':
    unittest.main()
