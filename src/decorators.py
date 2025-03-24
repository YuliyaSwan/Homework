from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор, который логирует вызовы функций в файл или выводит в консоль, если файл не указан.
    Возвращает - обернутая функция с возможностью логирования."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка для выполнения декорированной функции и логирования результата. Возвращает результат выполнения
            декорированной функции или None в случае ошибки."""
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok\n"
            except Exception as e:
                result = None
                log_message = (
                    f"{func.__name__} error: {type(e).__name__}. Explanation: {e}." f"Inputs: {args}, {kwargs}\n"
                )
            if filename:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(log_message)
            else:
                print(log_message)
            return result

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    return x + y


@log()
def my_function_no_log(x: int, y: int) -> int:
    return x + y


my_function(1, 2)
