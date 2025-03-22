from datetime import datetime
from typing import Dict, List, Optional


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
