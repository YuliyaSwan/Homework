import os
from decimal import Decimal

import requests
from dotenv import load_dotenv

# from pprint import pprint

# Загружаем переменные окружения из файла .env
load_dotenv(".env")
API_KEY = os.getenv("API_KEY")


def get_exchange_rate(currency_code: str) -> Decimal | None:
    """
    Получает текущий курс обмена для заданной валюты к рублю.

    :param currency_code: Код валюты (например, 'USD' или 'EUR').
    :return: Курс обмена как Decimal. Если курс не найден, возвращает None.
    """
    if currency_code == "RUB":
        return Decimal("1.0")

    url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount=1"

    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        rate = data.get("result")
        if rate:
            return Decimal(str(rate))
    except Exception as e:
        print(f"Ошибка при получении курса валют: {e}")
    return None


# pprint(get_exchange_rate('USD'))


def convert_to_rub(transaction: dict) -> float | None:
    """
    Конвертирует сумму каждой транзакции в рубли.

    :param transaction: Словарь с ключами 'amount' и 'currency'.
    :return: Сумма в рублях как float. Если конвертация невозможна, возвращает None.
    """

    try:
        op_amount = transaction.get("operationAmount", {})
        amount_str = op_amount.get("amount")
        currency_code = op_amount.get("currency", {}).get("code")

        if not amount_str or not currency_code:
            return None

        amount = Decimal(str(amount_str))
        rate = get_exchange_rate(currency_code)
        if rate is None:
            return None

        amount_rub = amount * rate
        return float(round(amount_rub, 2))
    except Exception as e:
        print(f"Ошибка в транзакции {transaction.get('id')}: {e}")
        return None


# transactions = load_transactions("./data/operations.json")
# for tx in transactions:
#     amount_rub = convert_to_rub(tx)
#     if amount_rub is not None:
#         print(f"ID: {tx.get('id')} | RUB Amount: {amount_rub}")
