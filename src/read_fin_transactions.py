import csv
import os
from typing import Any, Dict, Hashable, List

import pandas as pd


def read_csv_transactions(file_csv: str) -> List[Dict[str, Any]]:
    """
    Функция принимает путь до CSV-файла и возвращает список строк (каждая строка — список значений).
    Если файл не найден или произошла ошибка, возвращает пустой список.
    """

    if not os.path.exists(file_csv):
        print("Файл не найден.")
        return []

    transactions = []

    try:
        with open(file_csv, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                transactions.append(row)

    except FileNotFoundError:
        print("Файл не существует.")
    except UnicodeDecodeError:
        print("Ошибка декодирования. Проверьте кодировку файла.")
    except csv.Error as e:
        print(f"Ошибка CSV: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при чтении CSV: {e}")

    return transactions


def read_excel_transactions(file_excel: str) -> List[Dict[Hashable, Any]]:
    """
    Функция принимает путь до Excel-файла и возвращает список строк (каждая строка — список значений).
    Если файл не найден или произошла ошибка, возвращает пустой список.
    """

    if not os.path.exists(file_excel):
        print("Файл не найден.")
        return []

    try:
        excel_data = pd.read_excel(file_excel)
        print(excel_data.shape)
        print(excel_data.head())
        return excel_data.to_dict(orient="records")
    except FileNotFoundError:
        print("Файл не существует.")
    except ValueError as ve:
        print(f"Ошибка чтения Excel: {ve}")
    except pd.errors.EmptyDataError:
        print("Excel-файл пуст.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

    return []
