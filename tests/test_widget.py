import pytest

from src.widget import get_date, mask_account_card


# Тесты для проверки правильных входных данных (карта или счет).
@pytest.mark.parametrize(
    "card, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ],
)
def test_mask_account_card(card: str, expected: str) -> None:
    assert mask_account_card(card) == expected


# Тесты на обработку некорректных входных данных.
@pytest.mark.parametrize(
    "name_card_account, expected",
    [
        ("Visa Platinum 7000 79 1234", "Неверный формат карты"),
        ("Счет abcdefghijklmnop", "Неверный формат счета"),
        ("Visa Platinum 1234abcd 1234", "Неверный формат карты"),
        ("Счет 1234abcd", "Неверный формат счета"),
    ],
)
def test_mask_account_card_invalid_format(name_card_account: str, expected: str) -> None:
    assert mask_account_card(name_card_account) == expected


# Тест для пустой строки
def test_empty_string() -> None:
    assert mask_account_card(" ") == "Неверный формат карты"


# Тестирование правильности преобразования даты.
@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-25T15:30:00.000000", "25.12.2023"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
        ("1999-07-15", "15.07.1999"),
    ],
)
def test_get_date(date: str, expected: str) -> None:
    assert get_date(date) == expected


# Проверка работы функции на различных входных форматах даты, включая граничные случаи и нестандартные строки с датами;
# а также строки, где отсутствует дата.
@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024/03/11 02:26:18", "Неверный формат даты"),
        ("2024-02-30T00:00:00.000000", "Неверный формат даты"),
        ("", "Неверный формат даты"),
        ("abcd-ef-ghTij:kl:mno", "Неверный формат даты"),
    ],
)
def test_get_date_invalid_dates(date: str, expected: str) -> None:
    assert get_date(date) == expected
