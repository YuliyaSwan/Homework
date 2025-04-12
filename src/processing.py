import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, Hashable, List, Optional


def filter_by_state(transactions: List[Dict], state: Optional[str] = "EXECUTED") -> List[Dict]:
    """Функция принимает список словарей с данными о банковских операциях и опционально значение для ключа state.
    Возвращает новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному
    значению.
    """
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию -
    убывание). Возвращает новый список, отсортированный по дате (date).
    """
    return sorted(transactions, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S.%f"), reverse=reverse)


def find_by_key(transactions: List[Dict[Hashable, Any]], key: str, query: str) -> List[Dict[Hashable, Any]]:
    """
    Функция ищет строку - `query` с помощью регулярного выражения в поле `key` каждой транзакции.
    Возвращает список словарей, в которых значение по ключу `key` содержит `query`.
    Поиск нечувствителен к регистру.
    """

    result = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for transaction in transactions:
        value = str(transaction.get(key, ""))
        if pattern.search(value):
            result.append(transaction)

    return result


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

    category_counts = []
    categories_lower = [category.lower() for category in categories]

    for transaction in transactions:
        description = str(transaction.get("description", "")).strip().lower()

        # Проверяем, есть ли описание в списке категорий
        for category in categories_lower:
            if category in description:
                category_counts.append(category)
                break

    category_count_dict = dict(Counter(category_counts))

    return {categories[i]: category_count_dict.get(categories_lower[i], 0) for i in range(len(categories))}
