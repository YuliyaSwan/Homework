import json
import os
from typing import Any, List

# from pprint import pprint


def load_transactions(file_path: str) -> List[dict[str, Any]]:
    """
    Функция, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых
    транзакциях. Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass

    return []


# pprint(load_transactions("./data/operations.json"))
