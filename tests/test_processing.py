from typing import Dict, List

import pytest

from src.processing import (categorize_operations, extract_unique_categories, filter_by_description, filter_by_state,
                            find_by_key, sort_by_date)


# Фикстура для подготовки списка транзакций
@pytest.fixture
def transactions() -> list:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Параметризация для различных значений state
@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        ("FAILED", []),  # Когда нет транзакций с таким состоянием
    ],
)
def test_filter_by_state(transactions: list, state: str, expected: str) -> None:
    # Фильтруем список транзакций по состоянию
    assert filter_by_state(transactions, state) == expected


# Тест для случая, когда нет транзакций с заданным статусом
def test_no_matching_state(transactions: list) -> None:
    assert filter_by_state(transactions, "NON_EXISTENT_STATE") == []


# Тестирование сортировки списка словарей по датам в порядке убывания возрастания и при одинаковых датах.
@pytest.mark.parametrize(
    "transactions, reverse, expected_num",
    [
        (
            [
                {"id": 1, "date": "2019-07-03T12:00:00.000"},
                {"id": 2, "date": "2018-06-30T12:00:00.000"},
                {"id": 3, "date": "2018-09-12T12:00:00.000"},
            ],
            True,
            [1, 3, 2],
        ),
        (
            [
                {"id": 1, "date": "2019-07-03T12:00:00.000"},
                {"id": 2, "date": "2018-06-30T12:00:00.000"},
                {"id": 3, "date": "2019-07-03T12:00:00.000"},
            ],
            True,
            [1, 3, 2],
        ),
        ([{"id": 1, "date": "2018-09-12T12:00:00.000"}, {"id": 2, "date": "2018-10-14T12:00:00.000"}], False, [1, 2]),
    ],
)
def test_sort_by_date(transactions: List[Dict], reverse: bool, expected_num: List[int]) -> None:
    assert [transaction["id"] for transaction in sort_by_date(transactions, reverse=reverse)] == expected_num


# Тесты на работу функции с некорректными или нестандартными форматами дат.
@pytest.mark.parametrize(
    "transactions",
    [
        [{"id": 1, "date": "2024/03/18 14:25:43"}, {"id": 2, "date": "2023-06-01T09:15:20.456"}],
        [{"id": 1, "date": "2024-03-18T14:25:43.123"}, {"id": 2, "date": " "}],
    ],
)
def test_sort_by_date_invalid_format(transactions: List[Dict]) -> None:
    with pytest.raises(ValueError):
        sort_by_date(transactions)


# Тесты для функции find_by_key
@pytest.mark.parametrize(
    "transactions, search_string, expected",
    [
        # Тест 1: Поиск по строке в описании с нечувствительностью к регистру
        (
                [
                    {"description": "Перевод с карты на карту", "amount": 100},
                    {"description": "Открытие вклада", "amount": 200},
                ],
                "перевод",
                [
                    {"description": "Перевод с карты на карту", "amount": 100},
                ],
        ),

        # Тест 2: Когда строка не найдена в описаниях
        (
                [
                    {"description": "Перевод с карты на карту", "amount": 100},
                    {"description": "Открытие вклада", "amount": 200},
                ],
                "депозит",  # Строка, которая не существует в описаниях
                [],
        ),

        # Тест 3: Когда поиск нечувствителен к регистру
        (
                [
                    {"description": "Перевод с карты на карту", "amount": 100},
                    {"description": "Открытие вклада", "amount": 200},
                ],
                "открытие",  # Строка в описании, но с другим регистром
                [
                    {"description": "Открытие вклада", "amount": 200},
                ],
        ),

        # Тест 4: Когда описание пустое или отсутствует
        (
                [
                    {"description": "Перевод с карты на карту", "amount": 100},
                    {"description": "", "amount": 200},
                    {"description": "Открытие вклада", "amount": 300},
                ],
                "открытие",  # Строка, которая присутствует в одном из описаний
                [
                    {"description": "Открытие вклада", "amount": 300},
                ],
        ),

        # Тест 5: Пустой список транзакций
        (
                [],
                "перевод",
                [],
        ),
    ],
)
def test_find_by_key(transactions, search_string, expected):
    result = find_by_key(transactions, search_string)
    assert result == expected


# Тестирование функции filter_by_description
@pytest.mark.parametrize(
    "transactions, keyword, expected",
    [
        # Тестируем фильтрацию по описанию
        (
            [
                {"description": "Перевод с карты на карту", "amount": 100},
                {"description": "Открытие вклада", "amount": 200},
                {"description": "Перевод со счета на счет", "amount": 300},
            ],
            "перевод",
            [
                {"description": "Перевод с карты на карту", "amount": 100},
                {"description": "Перевод со счета на счет", "amount": 300},
            ],
        ),
        # Тестируем фильтрацию с учетом регистра
        (
            [
                {"description": "Перевод с карты на карту", "amount": 100},
                {"description": "Открытие вклада", "amount": 200},
            ],
            "открытие",
            [{"description": "Открытие вклада", "amount": 200}],
        ),
        # Тестируем отсутствие совпадений
        (
            [
                {"description": "Перевод с карты на карту", "amount": 100},
                {"description": "Открытие вклада", "amount": 200},
            ],
            "депозит",
            [],
        ),
    ],
)
def test_filter_by_description(transactions, keyword, expected) -> None:
    assert filter_by_description(transactions, keyword) == expected


# Тестирование функции extract_unique_categories
def test_extract_unique_categories() -> None:
    transactions = [
        {"description": "Перевод с карты на карту", "amount": 100},
        {"description": "Открытие вклада", "amount": 200},
        {"description": "Перевод со счета на счет", "amount": 300},
        {"description": "Перевод с карты на карту", "amount": 400},
    ]
    expected = ["Открытие вклада", "Перевод с карты на карту", "Перевод со счета на счет"]
    assert extract_unique_categories(transactions) == expected


# Тестирование функции categorize_operations
def test_categorize_operations() -> None:
    transactions = [
        {"description": "Перевод с карты на карту", "amount": 100},
        {"description": "Открытие вклада", "amount": 200},
        {"description": "Перевод со счета на счет", "amount": 300},
        {"description": "Перевод с карты на карту", "amount": 400},
    ]
    categories = ["Перевод с карты на карту", "Открытие вклада", "Перевод со счета на счет"]
    expected = {
        "Перевод с карты на карту": 2,
        "Открытие вклада": 1,
        "Перевод со счета на счет": 1,
    }
    assert categorize_operations(transactions, categories) == expected


# Дополнительные тесты


def test_empty_transactions() -> None:
    """Тестируем, что будет, если список транзакций пуст."""
    transactions = []
    keyword = "перевод"
    assert find_by_key(transactions, keyword) == []
    assert filter_by_description(transactions, keyword) == []
    assert extract_unique_categories(transactions) == []
    assert categorize_operations(transactions, ["Перевод с карты на карту"]) == {"Перевод с карты на карту": 0}
