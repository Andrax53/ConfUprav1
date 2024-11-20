import unittest
from config_parser import parse_file

class TestConfigParser(unittest.TestCase):
    def test_parse_file(self):
        data = parse_file('example_config.txt')
        self.assertEqual(data['port'], 8080)
        self.assertEqual(data['timeout'], 30)
        self.assertEqual(data['max_connections'], 100)
        self.assertEqual(data['server_name'], "example.com")
        self.assertEqual(data['array'], ["192.168.1.1", "192.168.1.2", "192.168.1.3"])
        self.assertEqual(data['table']['ip'], "192.168.1.1")
        self.assertEqual(data['table']['mask'], "255.255.255.0")
        self.assertEqual(data['table']['gateway'], "192.168.1.254")

if __name__ == '__main__':
    unittest.main()
