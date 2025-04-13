from datetime import datetime

from src.processing import filter_by_state, sort_by_date
from src.read_fin_transactions import read_csv_transactions, read_excel_transactions
from src.utils import load_transactions
from src.widget import mask_account_card

# from pprint import pprint

# from src.external_api import convert_to_rub, get_exchange_rate
# from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
# from src.masks import get_mask_account, get_mask_card_number
# from src.processing import (categorize_operations, extract_unique_categories, find_by_key, filter_by_description)
# from src.widget import get_date


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_path = ""
    file_csv = ""
    file_excel = ""

    while True:
        choice = input("Пользователь: ")
        if choice == "1":
            file_path = "./data/operations.json"
            transactions = load_transactions(file_path)
            # source = "json"
            print("Программа: Для обработки выбран JSON-файл.")
            break
        elif choice == "2":
            file_csv = "./data/transactions.csv"
            transactions = read_csv_transactions(file_csv)
            # source = "csv"
            print("Программа: Для обработки выбран CSV-файл.")
            break
        elif choice == "3":
            file_excel = "./data/transactions_excel.xlsx"
            transactions = read_excel_transactions(file_excel)
            # source = "excel"
            print("Программа: Для обработки выбран XLSX-файл.")
            break
        else:
            print("Пожалуйста, выберите корректный пункт: 1, 2 или 3.")

    if not transactions:
        print("Программа: Не удалось загрузить транзакции.")
        return

    # pprint(transactions)

    # Унификация структуры данных
    for tx in transactions:
        if "operationAmount" in tx:
            tx["amount"] = tx["operationAmount"].get("amount")
            tx["currency_name"] = tx["operationAmount"]["currency"].get("name")
            tx["currency_code"] = tx["operationAmount"]["currency"].get("code")

    # Выбор статуса
    possible_statuses = {"executed", "canceled", "pending"}

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")
        state = input("Пользователь: ").strip().lower()

        if state in possible_statuses:
            filtered_transactions = filter_by_state(transactions, state)
            if not filtered_transactions:
                print(f'Программа: Нет операций со статусом "{state.upper()}". Попробуйте другой статус.')
            else:
                transactions = filtered_transactions
                print(f'Программа: Операции отфильтрованы по статусу "{state.upper()}".')
                # pprint(transactions)
                break
        else:
            print(f'Программа: Статус операции "{state}" недоступен. Попробуйте снова.')

    # Проверяем, пуст ли список транзакций после фильтрации
    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    while True:
        sort_choice = input("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
        if sort_choice in ["да", "нет"]:
            if sort_choice == "да":
                direction = (
                    input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
                )
                ascending = direction == "по убыванию"
                transactions = sort_by_date(transactions, ascending)
                # pprint(transactions)
            break
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'.")

    # Фильтрация по валюте (только RUB)
    while True:
        currency_filter = (
            input("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
        )
        if currency_filter in ["да", "нет"]:
            if currency_filter == "да":
                transactions = [
                    tx
                    for tx in transactions
                    if (
                        tx.get("currency_code") == "RUB"
                        or tx.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
                    )
                ]
                # pprint(transactions)
                break
            else:
                # pprint(transactions)
                break
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'.")

    # Фильтр по ключевому слову в описании
    keyword_filter = (
        input("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if keyword_filter == "да":
        keyword = input("Введите слово для фильтрации по описанию: ").strip().lower()
        transactions = [tx for tx in transactions if keyword in tx.get("description", "").lower()]

    # Вывод финального списка транзакций
    if transactions:
        print("\nПрограмма: Распечатываю итоговый список транзакций...")
        print(f"\nПрограмма: \nВсего банковских операций в выборке: {len(transactions)}")
        for tx in transactions:
            date_str = tx.get("date", "")[:10]
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d.%m.%Y")
            except ValueError:
                formatted_date = date_str  # если дата в неожиданном формате

            # Получаем описание
            description = tx.get("description", "Описание не указано")

            # Маскируем 'from' только если оно есть
            from_info = mask_account_card(tx.get("from", "")) if tx.get("from") else ""

            # Маскируем 'to'
            to_info = mask_account_card(tx.get("to", ""))

            # Маскируем 'from' и 'to' при наличии
            # from_info = mask_account_card(tx.get("from", ""))
            # to_info = mask_account_card(tx.get("to", ""))

            # Сумма и валюта
            amount = tx.get("amount", tx.get("operationAmount", {}).get("amount", "Сумма не указана"))
            currency = tx.get(
                "currency_name", tx.get("operationAmount", {}).get("currency", {}).get("name", "Валюта не указана")
            )

            # Вывод транзакции
            print(f"\n{formatted_date} {description}")
            if from_info and to_info:
                print(f"{from_info} -> {to_info}")
            elif to_info:
                print(f"{to_info}")
            elif from_info:
                print(f"{from_info}")
            else:
                print("")
            print(f"Сумма: {amount} {currency}")
    else:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


if __name__ == "__main__":
    main()

    # print(get_mask_card_number('7000792289606361'))  # выход функции 7000 79** **** 6361
    # print(get_mask_account(73654108430135874305))  # выход функции **4305
    #
    # card_nums = [
    #     "Maestro 1596837868705199",
    #     "Счет 64686473678894779589",
    #     "MasterCard 7158300734726758",
    #     "Счет 35383033474447895560",
    #     "Visa Classic 6831982476737658",
    #     "Visa Platinum 8990922113665229",
    #     "Visa Gold 5999414228426353",
    #     "Счет 73654108430135874305",
    # ]
    # for card in card_nums:
    #     print(mask_account_card(card))  # выход функции карты или счета
    #
    # print(get_date("2024-03-11T02:26:18.671407"))  # выход функции даты
    #
    # transactions = [
    #     {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    #     {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    #     {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    #     {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    # ]
    # pprint(filter_by_state(transactions, state="EXECUTED"))
    # pprint(sort_by_date(transactions, reverse=True))
    #
    # transactions = [
    #     {
    #         "id": 939719570,
    #         "state": "EXECUTED",
    #         "date": "2018-06-30T02:08:58.425572",
    #         "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
    #         "description": "Перевод организации",
    #         "from": "Счет 75106830613657916952",
    #         "to": "Счет 11776614605963066702",
    #     },
    #     {
    #         "id": 142264268,
    #         "state": "EXECUTED",
    #         "date": "2019-04-04T23:20:05.206878",
    #         "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
    #         "description": "Перевод со счета на счет",
    #         "from": "Счет 19708645243227258542",
    #         "to": "Счет 75651667383060284188",
    #     },
    #     {
    #         "id": 873106923,
    #         "state": "EXECUTED",
    #         "date": "2019-03-23T01:09:46.296404",
    #         "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
    #         "description": "Перевод со счета на счет",
    #         "from": "Счет 44812258784861134719",
    #         "to": "Счет 74489636417521191160",
    #     },
    #     {
    #         "id": 895315941,
    #         "state": "EXECUTED",
    #         "date": "2018-08-19T04:27:37.904916",
    #         "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
    #         "description": "Перевод с карты на карту",
    #         "from": "Visa Classic 6831982476737658",
    #         "to": "Visa Platinum 8990922113665229",
    #     },
    #     {
    #         "id": 594226727,
    #         "state": "CANCELED",
    #         "date": "2018-09-12T21:27:25.241689",
    #         "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
    #         "description": "Перевод организации",
    #         "from": "Visa Platinum 1246377376343588",
    #         "to": "Счет 14211924144426031657",
    #     },
    # ]
    #
    # pprint(list(filter_by_currency(transactions, code="USD")))
    # pprint(list(transaction_descriptions(transactions)))
    # pprint(list(card_number_generator(1, 5)))
    #
    # pprint(load_transactions("./data/operations.json"))
    # pprint(get_exchange_rate("USD"))
    #
    # transactions = load_transactions("./data/operations.json")
    # for tx in transactions:
    #     amount_rub = convert_to_rub(tx)
    #     if amount_rub is not None:
    #         pprint(convert_to_rub(tx))
    #     # print(f"ID: {tx.get('id')} | Сумма в рублях: {amount_rub}")
    #
    # pprint(read_csv_transactions("./data/transactions.csv"))
    #
    # pprint(read_excel_transactions("./data/transactions_excel.xlsx"))
    #
    # pprint(find_by_key(load_transactions("./data/operations.json"), "operationAmount", "RUB"))
    # pprint(find_by_key(read_csv_transactions("./data/transactions.csv"), "description", "Перевод организации"))
    # pprint(find_by_key(read_excel_transactions("./data/transactions_excel.xlsx"), "state", "CANCELED"))
    #
    # categories = extract_unique_categories(load_transactions("./data/operations.json"))
    # pprint(categorize_operations(load_transactions("./data/operations.json"), categories))
    #
    # categories = extract_unique_categories(read_csv_transactions("./data/transactions.csv"))
    # pprint(categorize_operations(read_csv_transactions("./data/transactions.csv"), categories))
    #
    # categories = extract_unique_categories(read_excel_transactions("./data/transactions_excel.xlsx"))
    # pprint(categories)
    # pprint(categorize_operations(read_excel_transactions("./data/transactions_excel.xlsx"), categories))
