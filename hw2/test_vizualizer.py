import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import zipfile
import xml.etree.ElementTree as ET
from visualizer import download_nupkg, parse_nupkg_dependencies, build_dependency_graph, generate_mermaid_graph

class TestVisualizer(unittest.TestCase):

    @patch('visualizer.requests.get')
    def test_download_nupkg(self, mock_get):
        # Мокируем ответ для получения версий пакета
        mock_response_versions = MagicMock()
        mock_response_versions.json.return_value = {'versions': ['1.0.0', '1.1.0', '1.2.0']}
        mock_get.side_effect = [mock_response_versions, MagicMock()]

        # Мокируем ответ для скачивания пакета
        mock_response_nupkg = MagicMock()
        mock_response_nupkg.content = b'dummy content'
        mock_get.side_effect = [mock_response_versions, mock_response_nupkg]

        base_url = "https://api.nuget.org/v3-flatcontainer"
        package_name = "Newtonsoft.Json"
        nupkg_path = download_nupkg(base_url, package_name)

        self.assertTrue(os.path.exists(nupkg_path))
        os.remove(nupkg_path)

    def test_parse_nupkg_dependencies(self):
        # Создаем временный файл .nupkg
        temp_dir = tempfile.gettempdir()
        nupkg_path = os.path.join(temp_dir, 'test.nupkg')
        nuspec_content = """
        <package xmlns="http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd">
            <metadata>
                <dependencies>
                    <dependency id="Microsoft.CSharp" version="4.0.1" />
                    <dependency id="System.ComponentModel.TypeConverter" version="4.3.0" />
                </dependencies>
            </metadata>
        </package>
        """
        with zipfile.ZipFile(nupkg_path, 'w') as zip_ref:
            zip_ref.writestr('Newtonsoft.Json.nuspec', nuspec_content)

        dependencies = parse_nupkg_dependencies(nupkg_path)
        self.assertEqual(dependencies, ['Microsoft.CSharp', 'System.ComponentModel.TypeConverter'])

        os.remove(nupkg_path)

    @patch('visualizer.download_nupkg')
    @patch('visualizer.parse_nupkg_dependencies')
    def test_build_dependency_graph(self, mock_parse, mock_download):
        mock_download.return_value = 'dummy_path'
        mock_parse.side_effect = [['dep1', 'dep2'], [], []]

        base_url = "https://api.nuget.org/v3-flatcontainer"
        package_name = "Newtonsoft.Json"
        max_depth = 2
        graph = build_dependency_graph(base_url, package_name, max_depth)

        expected_graph = {
            'Newtonsoft.Json': ['dep1', 'dep2'],
            'dep1': [],
            'dep2': []
        }
        self.assertEqual(dict(graph), expected_graph)

    def test_generate_mermaid_graph(self):
        graph = {
            'Newtonsoft.Json': ['dep1', 'dep2'],
            'dep1': ['dep3'],
            'dep2': [],
            'dep3': []
        }
        mermaid_graph = generate_mermaid_graph(graph)
        expected_output = """graph TD
    Newtonsoft.Json --> dep1
    Newtonsoft.Json --> dep2
    dep1 --> dep3
    dep2
    dep3"""
        self.assertEqual(mermaid_graph, expected_output)

if __name__ == '__main__':
    unittest.main()
