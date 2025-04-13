import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тестирование правильности маскирования номера карты.
def test_get_mask_card_number() -> None:
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


# Проверка работы функции на различных входных форматах номеров карт.
@pytest.mark.parametrize("card_number", [7000792289606361, 7000792289606361.0, {}, [], ()])
def test_get_mask_card_number_wrong_type(card_number: str) -> None:
    with pytest.raises(TypeError):
        get_mask_card_number(card_number)


# Проверка работы функции на нестандартные длины номеров.
@pytest.mark.parametrize("card_number", ["70007922896063610000", "700079228960", "0"])
def test_get_mask_card_number_length_not_16(card_number: str) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


# Тестирование правильности маскирования номера счета.
def test_get_mask_account() -> None:
    assert get_mask_account(73654108430135874305) == "**4305"


# Проверка работы функции с различными форматами номеров счетов.
@pytest.mark.parametrize("account", ["73654108430135874305", 73654108430135874305.0, {}, [], (), " "])
def test_get_mask_account_wrong_type(account: str) -> None:
    with pytest.raises(TypeError):
        get_mask_account(account)


# Проверка работы функции с различными длинами номеров счетов.
@pytest.mark.parametrize("account", [736541084301358743050000, 700079228960, 0])
def test_get_mask_account_length_not_20(account: int) -> None:
    with pytest.raises(ValueError):
        get_mask_account(account)
