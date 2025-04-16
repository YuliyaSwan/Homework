"""IT-отдел крупного банка делает новую фичу для личного кабинета клиента. Это виджет,
который показывает несколько последних успешных банковских операций клиента. Вам доверили реализовать
этот проект, который на бэкенде будет готовить данные для отображения в новом виджете."""

import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован и
    отображается в формате XXXX XX** **** XXXX, где X — это цифра номера. То есть видны первые 6 цифр и
    последние 4 цифры, остальные символы отображаются звездочками, номер разбит по блокам по 4 цифры,
    разделенным пробелами."""

    if not isinstance(card_number, str):
        logger.error("Ошибка типа вводимых данных")
        raise TypeError("Ошибка типа данных")

    # Длина номера карты (обычно 16)
    if len(str(card_number)) != 16:
        logger.error("Неверная длина номера карты")
        raise ValueError("Неверный номер карты")

    # Выделяю первые 6 и последние 4 цифры карты
    logger.debug("Маскируем номер карты")
    new_card_number = str(card_number)[:6] + "******" + str(card_number)[-4:]

    # Делю номер карты на группы по 4 цифры
    groups = [new_card_number[i: i + 4] for i in range(0, len(str(card_number)), 4)]
    mask_card_number = " ".join(groups)

    logger.info("Вывод замаскированного номера карты")
    return mask_card_number


def get_mask_account(account: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску. Номер счета замаскирован и
    отображается в формате **XXXX, где X — это цифра номера."""

    if not isinstance(account, str):
        logger.error("Ошибка типа вводимых данных")
        raise TypeError("Ошибка типа данных")

    # Длина номера карты (обычно 20)
    if len(str(account)) != 20:
        logger.error("Неверная длина номера счёта")
        raise ValueError("Неверный номер счета")

    # Выделяю последние 4 цифры счета
    mask_account = "**" + str(account)[-4:]
    logger.info("Вывод замаскированного номера счета")
    return mask_account
