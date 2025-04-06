import unittest
from unittest.mock import patch, Mock
from decimal import Decimal
from src.external_api import get_exchange_rate, convert_to_rub, exchange_rate_cache


class TestCurrencyConversion(unittest.TestCase):

    def setUp(self):
        exchange_rate_cache.clear()

    # === Tests for get_exchange_rate ===

    def test_returns_1_for_rub(self):
        self.assertEqual(get_exchange_rate("RUB"), Decimal("1.0"))

    def test_returns_cached_rate(self):
        exchange_rate_cache["USD"] = Decimal("90.0")
        result = get_exchange_rate("USD")
        self.assertEqual(result, Decimal("90.0"))

    @patch("src.external_api.requests.get")
    def test_fetches_and_caches_rate(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 95.5}
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_exchange_rate("USD")
        self.assertEqual(result, Decimal("95.5"))
        self.assertIn("USD", exchange_rate_cache)

    @patch("src.external_api.requests.get")
    def test_returns_none_if_currency_missing(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Valute": {}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_exchange_rate("CHF")
        self.assertIsNone(result)

    @patch("src.external_api.requests.get")
    def test_returns_none_on_api_error(self, mock_get):
        mock_get.side_effect = Exception("API error")
        result = get_exchange_rate("USD")
        self.assertIsNone(result)

    # === Tests for convert_to_rub ===

    @patch("src.external_api.get_exchange_rate", return_value=Decimal("100.0"))
    def test_convert_valid_transaction(self, mock_rate):
        transaction = {
            "id": 1,
            "operationAmount": {
                "amount": "1.5",
                "currency": {"code": "USD"}
            }
        }
        result = convert_to_rub(transaction)
        self.assertEqual(result, 150.0)

    def test_transaction_missing_amount(self):
        tx = {"operationAmount": {"currency": {"code": "USD"}}}
        self.assertIsNone(convert_to_rub(tx))

    def test_transaction_missing_currency(self):
        tx = {"operationAmount": {"amount": "100"}}
        self.assertIsNone(convert_to_rub(tx))

    @patch("src.external_api.get_exchange_rate", return_value=None)
    def test_exchange_rate_none(self, mock_rate):
        tx = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }
        self.assertIsNone(convert_to_rub(tx))

    def test_transaction_with_invalid_amount(self):
        tx = {
            "id": 2,
            "operationAmount": {
                "amount": "not-a-number",
                "currency": {"code": "USD"}
            }
        }
        self.assertIsNone(convert_to_rub(tx))