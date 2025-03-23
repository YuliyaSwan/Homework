from typing import Dict, Generator, List


def filter_by_currency(transactions: List[Dict], code: str) -> Generator[Dict, None, None]:
    """Функция принимает на вход список словарей, представляющих транзакции. Возвращает итератор, который поочередно
    выдает транзакции, где валюта операции соответствует заданной (UCD)."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == code:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """Функция-генератор принимает список словарей с транзакциями и возвращает описание каждой операции поочереди."""
    if not transactions:
        raise ValueError("Список транзакций пуст")
    if not any("description" in x for x in transactions):
        raise ValueError("Описание транзакции отсутствует")
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генератор выдает номера карт в формате ХХХХ ХХХХ ХХХХ ХХХХ, где Х - цифра номера карты. Может сгенерировать
    номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999."""
    for i in range(start, stop + 1):
        card_number = f"{i:016}"
        formatted_card_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_card_number
