import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.utils import load_transactions


class TestLoadTransactions(unittest.TestCase):

    @patch("os.path.exists", return_value=False)
    def test_file_does_not_exist(self, mock_exists):
        result = load_transactions("fake_path.json")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}, {"id": 2}]')
    @patch("os.path.exists", return_value=True)
    def test_valid_json_list(self, mock_exists, mock_file):
        result = load_transactions("fake_path.json")
        self.assertEqual(result, [{"id": 1}, {"id": 2}])

    @patch("builtins.open", new_callable=mock_open, read_data='{"id": 1}')  # не список
    @patch("os.path.exists", return_value=True)
    def test_json_not_a_list(self, mock_exists, mock_file):
        result = load_transactions("fake_path.json")
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='INVALID_JSON')
    @patch("os.path.exists", return_value=True)
    def test_invalid_json(self, mock_exists, mock_file):
        result = load_transactions("fake_path.json")
        self.assertEqual(result, [])