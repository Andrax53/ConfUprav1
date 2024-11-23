import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from visualizer import download_nupkg_dependencies, parse_nupkg_dependencies, build_dependency_graph, \
    generate_mermaid_graph


class TestVisualizer(unittest.TestCase):

    @patch('visualizer.requests.get')
    def test_download_nupkg_dependencies(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"name": "package1", "dependencies": [{"id": "dep1"}, {"id": "dep2"}]},
            {"name": "package2", "dependencies": [{"id": "dep3"}]}
        ]
        mock_get.return_value = mock_response

        dependencies_data = download_nupkg_dependencies("http://example.com", "package1")
        self.assertEqual(dependencies_data, [
            {"name": "package1", "dependencies": [{"id": "dep1"}, {"id": "dep2"}]},
            {"name": "package2", "dependencies": [{"id": "dep3"}]}
        ])

    def test_parse_nupkg_dependencies(self):
        dependencies_data = [
            {"name": "package1", "dependencies": [{"id": "dep1"}, {"id": "dep2"}]},
            {"name": "package2", "dependencies": [{"id": "dep3"}]}
        ]
        dependencies = parse_nupkg_dependencies(dependencies_data)
        self.assertEqual(dependencies, {
            "package1": ["dep1", "dep2"],
            "package2": ["dep3"]
        })

    def test_build_dependency_graph(self):
        dependencies = {
            "package1": ["dep1", "dep2"],
            "dep1": ["dep3"],
            "dep2": [],
            "dep3": []
        }
        graph = build_dependency_graph("package1", dependencies, 2)
        self.assertEqual(graph, {
            "package1": ["dep1", "dep2"],
            "dep1": ["dep3"]
        })

    def test_generate_mermaid_graph(self):
        graph = {
            "package1": ["dep1", "dep2"],
            "dep1": ["dep3"]
        }
        mermaid_graph = generate_mermaid_graph(graph)
        expected_output = """graph TD
    package1 --> dep1
    package1 --> dep2
    dep1 --> dep3"""
        self.assertEqual(mermaid_graph, expected_output)

if __name__ == '__main__':
    unittest.main()
