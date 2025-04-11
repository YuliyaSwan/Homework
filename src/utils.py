import json
import logging
import os
from typing import Any, List

# from pprint import pprint


logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[dict[str, Any]]:
    """
    Функция, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых
    транзакциях. Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    logger.info(f"Проверка наличия и содержимого файла: {file_path}")
    if not os.path.exists(file_path):
        logger.warning(f"Файл {file_path} не найден.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f"Считываем данные из файла {file_path}")
            data = json.load(file)
            if isinstance(data, list):
                logger.debug(f"Успешно загружено {len(data)} записей из {file_path}")
                return data
            else:
                logger.warning(f"Файл {file_path} не содержит список.")
    except json.JSONDecodeError as ex:
        logger.error(f"Произошла ошибка: {ex}")

    return []


# pprint(load_transactions("./data/operations.json"))
