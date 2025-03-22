"""Продолжаем работу над виджетом банковских операций клиента"""

from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(name_card_account: str) -> str:
    """Функция принимает на вход тип и номер карты или счета. Возвращает строку с замаскированным номером.
    Пример: Visa Platinum 7000 79** **** 6361, Счет **4305"""
    if not name_card_account:  # Проверка на пустую строку
        return "Неверный формат карты"

    if "Счет" in name_card_account:
        try:
            number = int(name_card_account.replace("Счет", "").strip())  # Преобразуем в число
            return str("Счет " + get_mask_account(number))
        except ValueError:  # Если не удалось преобразовать в число
            return "Неверный формат счета"
    else:  # Проверка формата карты
        card_number = name_card_account[-16:]
        if not card_number.isdigit() or len(card_number) != 16:
            return "Неверный формат карты"
        numbers = get_mask_card_number(int(card_number))  # Маскировка номера карты
        update_card = " ".join(name_card_account.split()[:-1]) + " " + numbers
        return str(update_card)


def get_date(date: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407" и возвращает строку
    с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""
    try:
        date_for_print = datetime.fromisoformat(date)
        return date_for_print.strftime("%d.%m.%Y")
    except ValueError:
        return "Неверный формат даты"
