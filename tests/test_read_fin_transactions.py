import unittest
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd

from src.read_fin_transactions import read_csv_transactions, read_excel_transactions


class TestFileReaders(unittest.TestCase):

    # Тесты для read_csv_transactions

    @patch(
        "builtins.open",
        mock_open(read_data="Date;Amount;Category\n2024-01-01;100;Groceries\n2024-01-02;200;Transportation"),
    )
    @patch("os.path.exists", return_value=True)
    def test_read_csv_transactions(self, mock_exists: MagicMock) -> None:
        result = read_csv_transactions("dummy.csv")

        expected = [
            {"Date": "2024-01-01", "Amount": "100", "Category": "Groceries"},
            {"Date": "2024-01-02", "Amount": "200", "Category": "Transportation"},
        ]

        self.assertEqual(result, expected)
        mock_exists.assert_called_with("dummy.csv")

    @patch("os.path.exists", return_value=False)
    def test_read_csv_file_not_found(self, mock_exists: MagicMock) -> None:
        result = read_csv_transactions("missing.csv")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    def test_read_csv_decode_error(self, mock_exists: MagicMock) -> None:
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "reason")
            result = read_csv_transactions("bad_encoding.csv")
            self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    def test_read_csv_empty_row(self, mock_exists: MagicMock) -> None:
        # Тестируем пустую строку
        with patch("builtins.open", mock_open(read_data="Date;Amount;Category\n")):
            result = read_csv_transactions("empty_row.csv")
            self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    def test_read_csv_missing_column(self, mock_exists: MagicMock) -> None:
        # Тестируем случай, когда колонка отсутствует
        with patch("builtins.open", mock_open(read_data="Date;Amount\n2024-01-01;100\n2024-01-02;200")):
            result = read_csv_transactions("missing_column.csv")
            self.assertEqual(
                result,
                [
                    {"Date": "2024-01-01", "Amount": "100"},
                    {"Date": "2024-01-02", "Amount": "200"},
                ],
            )

    # Тесты для read_excel_transactions

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel")
    def test_read_excel_transactions_success(self, mock_read_excel: MagicMock, mock_exists: MagicMock) -> None:
        mock_df = pd.DataFrame({"Date": ["2024-01-01", "2024-01-02"], "Amount": [100, 200]})
        mock_read_excel.return_value = mock_df

        result = read_excel_transactions("dummy.xlsx")
        self.assertEqual(result, [{"Date": "2024-01-01", "Amount": 100}, {"Date": "2024-01-02", "Amount": 200}])

    @patch("os.path.exists", return_value=False)
    def test_read_excel_file_not_found(self, mock_exists: MagicMock) -> None:
        result = read_excel_transactions("missing.xlsx")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel", side_effect=ValueError("Ошибка чтения"))
    def test_read_excel_value_error(self, mock_read_excel: MagicMock, mock_exists: MagicMock) -> None:
        result = read_excel_transactions("bad.xlsx")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError("пустой файл"))
    def test_read_excel_empty_file(self, mock_read_excel: MagicMock, mock_exists: MagicMock) -> None:
        result = read_excel_transactions("empty.xlsx")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel", side_effect=TypeError("Ошибка обработки"))
    def test_read_excel_type_error(self, mock_read_excel: MagicMock, mock_exists: MagicMock) -> None:
        result = read_excel_transactions("type_error.xlsx")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_excel", side_effect=KeyError("Ошибка ключа"))
    def test_read_excel_key_error(self, mock_read_excel: MagicMock, mock_exists: MagicMock) -> None:
        result = read_excel_transactions("key_error.xlsx")
        self.assertEqual(result, [])
