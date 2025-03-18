from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


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
