import unittest
from unittest.mock import patch, MagicMock
from visualizer import get_commits_before_date, build_dependency_graph, generate_plantuml_code, main
from datetime import datetime

class TestDependencyVisualizer(unittest.TestCase):

    @patch('visualizer.git.Repo')  # Мокируем git.Repo
    def test_get_commits_before_date(self, mock_repo):
        mock_commit = MagicMock()
        mock_commit.hexsha = "abcd1234"
        mock_repo.return_value.iter_commits.return_value = [mock_commit]

        date_str = '2023-12-01'
        result = get_commits_before_date('/fake/repo', date_str)

        self.assertEqual(result, ["abcd1234"])
        mock_repo.return_value.iter_commits.assert_called_with('main', since=datetime.strptime(date_str, '%Y-%m-%d'))

    def test_build_dependency_graph(self):
        commits = ["abcd1234", "efgh5678"]
        result = build_dependency_graph('/fake/repo', commits)  # Передаем оба аргумента
        expected_graph = {
            "abcd1234": ["efgh5678"],
            "efgh5678": []
        }
        self.assertEqual(result, expected_graph)

    def test_generate_plantuml_code(self):
        graph = {
            "abcd1234": ["efgh5678"],
            "efgh5678": []
        }
        result = generate_plantuml_code(graph)
        expected_code = '@startuml\n"efgh5678" --> "abcd1234"\n@enduml'
        self.assertEqual(result.strip(), expected_code.strip())

    @patch('visualizer.get_commits_before_date')
    @patch('visualizer.read_config')
    @patch('visualizer.git.Repo')  # Патч для git.Repo
    def test_main(self, mock_repo, mock_read_config, mock_get_commits):
        mock_read_config.return_value = {
            "repository_path": "/fake/repo",
            "date": "2023-12-01",
            "result_file_path": "/fake/result.txt"
        }
        mock_get_commits.return_value = ["abcd1234", "efgh5678"]

        # Мокаем репозиторий и его коммиты
        mock_commit = MagicMock()
        mock_commit.hexsha = "abcd1234"
        mock_repo.return_value.iter_commits.return_value = [mock_commit]

        with patch('visualizer.save_result') as mock_save_result, patch('visualizer.print_result') as mock_print_result:
            main('/fake/config.json')

            mock_get_commits.assert_called_with("/fake/repo", "2023-12-01")
            mock_save_result.assert_called()
            mock_print_result.assert_called()

if __name__ == '__main__':
    unittest.main()
