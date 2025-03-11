from typing import Dict, List, Optional


def filter_by_state(transactions: List[Dict], state: Optional[str] = "EXECUTED") -> List[Dict]:
    """Функция принимает список словарей и опционально значение для ключа state. Возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует указанному значению.
    """
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию -
    убывание). Возвращает новый список, отсортированный по дате (date).
    """
    return sorted(transactions, key=lambda x: (x["date"], "%Y-%m-%dT%H:%M-%S.%f"), reverse=reverse)


if __name__ == "__main__":
    transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(filter_by_state(transactions, state="EXECUTED"))
    print(sort_by_date(transactions, reverse=True))
