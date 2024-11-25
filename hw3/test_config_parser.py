import unittest
import os
from config_parser import parse_file, write_toml
import toml

class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.test_output = "test_output.toml"
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        
    def tearDown(self):
        if os.path.exists(self.test_output):
            os.remove(self.test_output)

    def test_network_config(self):
        # Test input-output conversion for network configuration
        config_path = os.path.join(self.test_dir, 'examples', 'network_config.txt')
        data = parse_file(config_path)
        write_toml(data, self.test_output)
        
        # Read generated TOML and verify contents
        with open(self.test_output, 'r') as f:
            toml_data = toml.load(f)
            
        # Verify basic values
        self.assertEqual(toml_data['port'], 8080)
        self.assertEqual(toml_data['timeout'], 30)
        self.assertEqual(toml_data['max_connections'], 100)
        
        # Verify struct
        self.assertEqual(toml_data['struct']['ip'], '192.168.1.1')
        self.assertEqual(toml_data['struct']['mask'], '255.255.255.0')
        self.assertEqual(toml_data['struct']['gateway'], '192.168.1.254')
        
        # Verify array
        self.assertEqual(toml_data['allowed_ips'], ['192.168.1.2', '192.168.1.3', '192.168.1.4'])
        
        # Verify constant evaluation
        self.assertEqual(toml_data['backup_port'], 8080)

    def test_game_config(self):
        # Test input-output conversion for game configuration
        config_path = os.path.join(self.test_dir, 'examples', 'game_config.txt')
        data = parse_file(config_path)
        write_toml(data, self.test_output)
        
        # Read generated TOML and verify contents
        with open(self.test_output, 'r') as f:
            toml_data = toml.load(f)
            
        # Verify basic values
        self.assertEqual(toml_data['screen_width'], 1920)
        self.assertEqual(toml_data['screen_height'], 1080)
        
        # Verify audio struct
        self.assertEqual(toml_data['struct']['sound_volume'], 80)
        self.assertEqual(toml_data['struct']['music_volume'], 60)
        self.assertEqual(toml_data['struct']['effects_volume'], 100)
        
        # Verify array
        self.assertEqual(toml_data['key_bindings'], ['w', 'a', 's', 'd', 'space', 'shift'])
        
        # Verify graphics struct
        self.assertEqual(toml_data['struct1']['vsync'], 1)
        self.assertEqual(toml_data['struct1']['antialiasing'], 4)
        self.assertEqual(toml_data['struct1']['shadows'], 'high')
        self.assertEqual(toml_data['struct1']['textures'], 'ultra')

    def test_syntax_errors(self):
        # Create a temporary file for testing syntax errors
        test_file = os.path.join(self.test_dir, 'test_syntax.txt')
        
        # Test missing semicolon in constant declaration
        with open(test_file, 'w') as f:
            f.write('invalid_constant <- 42')
        with self.assertRaises(SyntaxError):
            parse_file(test_file)
            
        # Test unclosed struct
        with open(test_file, 'w') as f:
            f.write('struct { a = 1,')
        with self.assertRaises(SyntaxError):
            parse_file(test_file)
            
        # Test invalid array syntax
        with open(test_file, 'w') as f:
            f.write('arr <- [ 1 2 3')
        with self.assertRaises(SyntaxError):
            parse_file(test_file)
            
        # Clean up
        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
