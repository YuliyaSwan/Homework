import pytest

from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number() -> None:
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"


@pytest.mark.parametrize("card_number", ["7000792289606361", 7000792289606361.0, {}, [], ()])
def test_get_mask_card_number_wrong_type(card_number: int) -> None:
    with pytest.raises(TypeError):
        get_mask_card_number(card_number)


@pytest.mark.parametrize("card_number", [70007922896063610000, 700079228960])
def test_get_mask_card_number_length_not_16(card_number: int) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


def test_get_mask_card_number_not_write() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(int())


def test_get_mask_card_number_zero() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(0)


def test_get_mask_account() -> None:
    assert get_mask_account(73654108430135874305) == "**4305"


@pytest.mark.parametrize("account", ["73654108430135874305", 73654108430135874305.0, {}, [], ()])
def test_get_mask_account_wrong_type(account: int) -> None:
    with pytest.raises(TypeError):
        get_mask_account(account)


@pytest.mark.parametrize("account", [736541084301358743050000, 700079228960])
def test_get_mask_account_length_not_20(account: int) -> None:
    with pytest.raises(ValueError):
        get_mask_account(account)


def test_get_mask_account_not_write() -> None:
    with pytest.raises(ValueError):
        get_mask_account(int())


def test_get_mask_account_zero() -> None:
    with pytest.raises(ValueError):
        get_mask_account(0)
