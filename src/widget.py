"""Продолжаем работу над виджетом банковских операций клиента"""

from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(name_card_account: str) -> str:
    """Функция принимает на вход тип и номер карты или счета. Возвращает строку с замаскированным номером.
    Пример: Visa Platinum 7000 79** **** 6361, Счет **4305"""

    # Проверяем, что name_card_account — это строка
    if not isinstance(name_card_account, str):
        return ""

    if not name_card_account:  # Пустая строка
        return "Пустая строка"

    if "Счет" in name_card_account:
        try:
            number = "".join(filter(str.isdigit, name_card_account))
            # number = int(name_card_account.replace("Счет", "").strip())  # Преобразуем в число
            return "Счет " + get_mask_account(int(number))
        except ValueError:
            return "Неверный формат счета"  # Неверный формат счета

    else:
        # Извлекаем только цифры из строки, игнорируя символы и буквы
        card_number = "".join(filter(str.isdigit, name_card_account))

        # Проверяем, что это строка из 16 цифр
        if len(card_number) != 16 or not card_number.isdigit():
            return "Неверный формат карты"  # Неверный формат карты

        try:
            # Маскируем номер карты
            masked = get_mask_card_number(card_number)
            card_type = " ".join(name_card_account.split()[:-1])  # Маскируем только номер карты
            return f"{card_type} {masked}"
        except ValueError:
            return "Неверный формат карты"  # Возвращаем пустую строку, если формат карты неверный

    # if not name_card_account:  # Проверка на пустую строку
    #     return ""
    #
    # if "Счет" in name_card_account:
    #     try:
    #         number = int(name_card_account.replace("Счет", "").strip())  # Преобразуем в число
    #         return "Счет " + get_mask_account(number)
    #     except ValueError:  # Если не удалось преобразовать в число
    #         return ""
    #
    # else:  # Проверка формата карты
    #     card_number = name_card_account[-16:].replace(" ", "")
    #     if not card_number.isdigit() or len(card_number) != 16:
    #         return ""
    #     try:
    #         numbers = get_mask_card_number(int(card_number))  # Маскировка номера карты
    #         update_card = ''.join(name_card_account.split()[:-1])
    #         return f"{update_card} {numbers}"
    #     except ValueError:
    #         return ""


def get_date(date: str) -> str:
    """Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407" и возвращает строку
    с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")."""
    try:
        date_for_print = datetime.fromisoformat(date)
        return date_for_print.strftime("%d.%m.%Y")
    except ValueError:
        return "Неверный формат даты"
