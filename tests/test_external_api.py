import unittest
from decimal import Decimal
from typing import Optional
from unittest.mock import Mock, patch

from src.external_api import convert_to_rub, get_exchange_rate


class TestCurrencyConversion(unittest.TestCase):

    # Тесты для get_exchange_rate

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_success(self, mock_get: Mock) -> None:
        # Мокаем успешный ответ API для валюты, отличной от RUB
        mock_response = Mock()
        mock_response.json.return_value = {"result": 75.0}  # Пример: 1 USD = 75 RUB
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Проверка, что курс для USD возвращается корректно
        result = get_exchange_rate("USD")
        self.assertEqual(result, Decimal("75.0"))

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_rub(self, mock_get: Mock) -> None:
        # Мокаем успешный ответ для RUB, который должен всегда возвращать 1.0
        mock_response = Mock()
        mock_response.json.return_value = {"result": 1.0}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Проверка, что для RUB курс всегда равен 1.0
        result: Optional[Decimal] = get_exchange_rate("RUB")
        self.assertEqual(result, Decimal("1.0"))

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_api_failure(self, mock_get: Mock) -> None:
        # Мокаем ошибку API
        mock_get.side_effect = Exception("API error")

        # Проверка, что курс возвращает None при ошибке API
        result = get_exchange_rate("USD")
        self.assertIsNone(result)

    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_invalid_currency(self, mock_get: Mock) -> None:
        # Мокаем ответ без курса для этой валюты
        mock_response = Mock()
        mock_response.json.return_value = {}  # Пример: отсутствует курс для валюты
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Проверка, что курс возвращает None, если валюта отсутствует
        result = get_exchange_rate("XYZ")
        self.assertIsNone(result)

    # Тесты для convert_to_rub

    @patch("src.external_api.get_exchange_rate", return_value=Decimal("75.0"))
    def test_convert_to_rub_valid_transaction(self, mock_rate: Mock) -> None:
        transaction = {"id": 1, "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
        # Проверка, что сумма в рублях вычисляется корректно
        result = convert_to_rub(transaction)
        self.assertEqual(result, 7500.0)

    @patch("src.external_api.get_exchange_rate", return_value=Decimal("75.0"))
    def test_convert_to_rub_invalid_amount(self, mock_rate: Mock) -> None:
        transaction = {"id": 1, "operationAmount": {"amount": "not-a-number", "currency": {"code": "USD"}}}
        # Проверка, что при некорректной сумме возвращается None
        result = convert_to_rub(transaction)
        self.assertIsNone(result)

    @patch("src.external_api.get_exchange_rate", return_value=Decimal("75.0"))
    def test_convert_to_rub_missing_currency(self, mock_rate: Mock) -> None:
        transaction = {"id": 1, "operationAmount": {"amount": "100.00"}}
        # Проверка, что при отсутствии валюты возвращается None
        result = convert_to_rub(transaction)
        self.assertIsNone(result)

    @patch("src.external_api.get_exchange_rate", return_value=None)
    def test_convert_to_rub_rate_not_found(self, mock_rate: Mock) -> None:
        transaction = {"id": 1, "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
        # Проверка, что при отсутствии курса возвращается None
        result = convert_to_rub(transaction)
        self.assertIsNone(result)
