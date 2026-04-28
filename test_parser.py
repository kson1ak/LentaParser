import pytest
from unittest.mock import patch, MagicMock
import os
from lenta_parser import get_lenta_news, parse_titles, save_to_local_folder

# 1. ТЕСТ: Проверка успешного запроса к сайту
# @patch временно заменяет реальный requests.get на "пустышку" (mock_get)
@patch('requests.get')
def test_get_lenta_news_success(mock_get):
    # Настраиваем пустышку: имитируем ответ сервера (код 200 и текст страницы)
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><body>Fake News</body></html>"
    result = get_lenta_news()
    # Проверяем, что функция вернула именно тот текст, который мы подложили
    assert result == "<html><body>Fake News</body></html>"

# 2. ТЕСТ: Проверка логики парсинга (извлечения текста из HTML)
def test_parse_titles_valid_html():
    # Создаем кусочек HTML-кода, похожий на структуру Lenta.ru
    sample_html = '<span class="card-mini__title">Тестовая новость</span>'
    titles = parse_titles(sample_html)

    # Проверяем: нашелся ли ровно 1 заголовок и совпадает ли его текст
    assert len(titles) == 1
    assert titles[0] == "Тестовая новость"

# 3. ТЕСТ: Проверка парсинга, если на странице нет нужных тегов
def test_parse_titles_empty():
    empty_html = "<div>Нет новостей</div>"  # Тут нет нужного класса card-mini__title
    titles = parse_titles(empty_html)
    # Ожидаем, что функция вернет пустой список, а не упадет с ошибкой
    assert titles == []

# 4. ТЕСТ: Проверка процесса сохранения в файл
# Подменяем встроенную функцию open и системную os.path.abspath,
# чтобы тест не создавал реальных файлов на твоем компьютере.
@patch('builtins.open', new_callable=MagicMock)
@patch('os.path.abspath', return_value="C:/project/lenta_parser.py")
def test_save_to_local_folder_success(mock_abs, mock_open):
    test_titles = ["Новость 1"]
    result = save_to_local_folder(test_titles)
    # Если функция отработала без ошибок и вернула True — тест пройден
    assert result is True

# 5. ТЕСТ: Проверка граничного случая (сохранение пустого списка)
def test_save_to_local_folder_empty():
    # Логика функции должна запрещать создание файла, если новостей нет
    result = save_to_local_folder([])
    assert result is False

# Блок запуска тестов прямо из Python-файла
if __name__ == "__main__":
    # Запускаем pytest:
    # -v: подробное описание (какой именно тест выполняется)
    # --no-header и --no-summary: убирают лишнюю служебную информацию в консоли
    pytest.main(["-v", "--no-header", "--no-summary", __file__])