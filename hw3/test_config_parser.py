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
        self.assertEqual(data['new_port'], 8081)
        self.assertEqual(data['new_timeout'], 25)
        self.assertEqual(data['new_max_connections'], 200)
        self.assertEqual(data['min_value'], 30)
        self.assertEqual(data['max_value'], 8080)

if __name__ == '__main__':
    unittest.main()
