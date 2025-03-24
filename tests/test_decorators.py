from unittest.mock import mock_open, patch

from src.decorators import log, my_function, my_function_no_log


# Тест на корректное логирование успешного выполнения функции в файл.
def test_log_success() -> None:
    with patch("builtins.open", mock_open()) as mock_file:
        my_function(1, 2)
        mock_file().write.assert_called_with("my_function ok\n")


# Тест на корректное логирование исключений в файл.
def test_log_exception() -> None:
    @log(filename="testlog.txt")
    def faulty_function() -> None:
        raise ValueError("Test error")

    with patch("builtins.open", mock_open()) as mock_file:
        faulty_function()
        assert "faulty_function error: ValueError." in mock_file().write.call_args[0][0]


# Тест на корректное логирование успешного выполнения функции в консоль при отсутствии файла.
def test_log_no_file(capsys) -> None:
    my_function_no_log(1, 2)
    captured = capsys.readouterr()
    assert captured.out == "my_function_no_log ok\n\n"
