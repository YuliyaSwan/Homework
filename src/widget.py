"""Продолжаем работу над виджетом банковских операций клиента"""

from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(name_card_account: str) -> str:
    """Функция принимает на вход тип и номер карты или счета. Возвращает строку с замаскированным номером.
    Пример: Visa Platinum 7000 79** **** 6361, Счет **4305"""
    if "Счет" in name_card_account:
        number = int(name_card_account.replace("Счет", "").strip())
        return str("Счет " + get_mask_account(number))
    else:
        numbers = get_mask_card_number(int(name_card_account[-16:]))
        update_card = " ".join(name_card_account.split()[:-1]) + " " + numbers
        return str(update_card)


def get_date(date: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407" и возвращает строку
    с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""
    date_for_print = datetime.fromisoformat(date)
    return date_for_print.strftime("%d.%m.%Y")


if __name__ == "__main__":
    card_nums = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]
    for card in card_nums:
        print(mask_account_card(card))  # выход функции карты или счета
        print(get_date("2024-03-11T02:26:18.671407"))  # выход функции даты
