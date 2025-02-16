"""Продолжаем работу над виджетом банковских операций клиента"""
from datetime import datetime

from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(name_card_account: str) -> str:
    """Функция принимает на вход тип и номер карты или счета. Возвращает строку с замаскированным номером."""
    if "Счет" in name_card_account:
        number = int(name_card_account.replace("Счет", "").strip())
        return "Счет " + get_mask_account(number)
    else:
        numbers = get_mask_card_number(int(name_card_account[-16:]))
        update_card = " ".join(name_card_account.split()[:-1]) + " " + numbers
        return update_card


def get_date(date: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407" и возвращает строку
    с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""
    date_for_print = datetime.fromisoformat(date)
    return date_for_print.strftime("%d.%m.%Y")


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # выход функции Visa Platinum 7000 79** **** 6361
    print(mask_account_card("Счет 73654108430135874305"))  # выход функции Счет **4305
    print(get_date("2024-03-11T02:26:18.671407"))  # выход функции "ДД.ММ.ГГГГ" ("11.03.2024")
