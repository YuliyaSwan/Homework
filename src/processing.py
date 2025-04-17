import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, Hashable, List


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Функция принимает список словарей с данными о банковских операциях и опционально значение для ключа state.
    Возвращает новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному
    значению.
    """
    # return [transaction for transaction in transactions
    #         if isinstance(transaction.get("state", ""), str) and transaction["state"].strip().lower() == state]

    state = state.lower()
    return [transaction for transaction in transactions if transaction.get("state", "").lower() == state]
    # return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию -
    убывание). Возвращает новый список, отсортированный по дате (date).
    """

    def parse_date(date_str: str) -> datetime:
        # Убираем 'Z' (если есть) и пробуем распарсить дату с миллисекундами
        date_str = date_str.rstrip("Z")
        # Если дата содержит миллисекунды, используем формат с .%f
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            # Если миллисекунд нет, используем формат без .%f
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    return sorted(transactions, key=lambda x: parse_date(x["date"]), reverse=reverse)


def find_by_key(transactions: List[Dict[Hashable, Any]], search_string: str) -> List[Dict[Hashable, Any]]:
    """
    ФФункция ищет строку `search_string` в поле 'description' каждой транзакции.
    Возвращает список словарей, где значение по ключу 'description' содержит строку `search_string`.
    Поиск нечувствителен к регистру.
    """

    result = []
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    for transaction in transactions:
        value = str(transaction.get("description", ""))
        if pattern.search(value):
            result.append(transaction)

    return result


def filter_by_description(transactions: List[Dict[Hashable, Any]], keyword: str) -> List[Dict[Hashable, Any]]:
    """
    Фильтрует список транзакций, оставляя только те, описание которых содержит ключевое слово.
    """
    keyword_lower = keyword.strip().lower()
    return [tx for tx in transactions if keyword_lower in str(tx.get("description", "")).strip().lower()]


def extract_unique_categories(transactions: List[Dict[Hashable, Any]]) -> List[str]:
    """
    Извлекает все уникальные значения из поля 'description' в списке транзакций.
    Возвращает отсортированный список категорий.
    """
    return sorted({str(tx.get("description", "")).strip() for tx in transactions if tx.get("description")})


def categorize_operations(transactions: List[Dict[Hashable, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Функция принимает список транзакций и список категорий.
    Возвращает словарь, где ключи — это категории из поля 'description',
    а значения — количество операций в каждой категории.
    """
    # Преобразуем категории в нижний регистр для сравнения
    categories_lower = [category.lower() for category in categories]

    # Счетчик для подсчета операций по категориям
    category_counts = Counter()

    # Перебираем транзакции и подсчитываем, сколько раз встречается каждая категория
    for transaction in transactions:
        description = str(transaction.get("description", "")).strip().lower()

        # Преобразуем описание в нижний регистр
        for category in categories_lower:
            if category in description:
                category_counts[category] += 1
                break  # Прерываем цикл, чтобы не было нескольких категорий для одного описания

    # Восстанавливаем ключи в исходном регистре
    return {categories[i]: category_counts.get(categories_lower[i], 0) for i in range(len(categories))}
