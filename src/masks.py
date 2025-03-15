"""IT-отдел крупного банка делает новую фичу для личного кабинета клиента. Это виджет,
который показывает несколько последних успешных банковских операций клиента. Вам доверили реализовать
этот проект, который на бэкенде будет готовить данные для отображения в новом виджете."""


def get_mask_card_number(card_number: int) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован и
    отображается в формате XXXX XX** **** XXXX, где X — это цифра номера. То есть видны первые 6 цифр и
    последние 4 цифры, остальные символы отображаются звездочками, номер разбит по блокам по 4 цифры,
    разделенным пробелами."""

    for arg in [card_number]:
        if not isinstance(arg, int):
            raise TypeError("Ошибка типа данных")

    # Длина номера карты (обычно 16)
    length = int(len(str(card_number)))

    if length != 16:
        raise ValueError("Неверный номер карты")

    if card_number == int():
        raise ValueError("Отсутствует номер карты")

    # Определяю количество скрытых символов и обозначаю символ
    n = length - (6 + 4)
    symbol = "*"

    # Выделяю первые 6 и последние 4 цифры карты
    new_card_number = str(card_number)[:6] + n * symbol + str(card_number)[-4:]

    # Делю номер карты на группы по 4 цифры
    groups = [new_card_number[i: i + 4] for i in range(0, length, 4)]
    mask_card_number = " ".join(groups)

    return mask_card_number


def get_mask_account(account: int) -> str:
    """Функция принимает на вход номер счета и возвращает его маску. Номер счета замаскирован и
    отображается в формате **XXXX, где X — это цифра номера."""

    for arg in [account]:
        if not isinstance(arg, int):
            raise TypeError("Ошибка типа данных")

    # Длина номера карты (обычно 20)
    length_account = int(len(str(account)))

    if length_account != 20:
        raise ValueError("Неверный номер счета")

    if account == int():
        raise ValueError("Отсутствует номер счета")

    # Выделяю последние 4 цифры счета
    mask_account = "**" + str(account)[-4:]

    return mask_account
