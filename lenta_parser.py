import requests  # Импортируем библиотеку для отправки HTTP-запросов к сайтам
from bs4 import BeautifulSoup  # Импортируем инструмент для парсинга (разбора) HTML-кода
import os  # Импортируем модуль для работы с операционной системой и файловыми путями

def get_lenta_news(url="https://lenta.ru"):
    # Создаем заголовок User-Agent, чтобы сайт думал, что запрос идет от обычного браузера
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Отправляем GET-запрос на сайт с указанными заголовками и временем ожидания 10 секунд
        response = requests.get(url, headers=headers, timeout=10)

        # Проверяем, не вернул ли сервер ошибку (например, 404 или 500)
        response.raise_for_status()

        # Если всё хорошо, возвращаем текст (HTML-код) страницы
        return response.text

    except requests.RequestException:
        # Если произошла ошибка при запросе (нет интернета и т.д.), возвращаем None
        return None

def parse_titles(html):
    # Если HTML пустой или запрос не удался, возвращаем пустой список
    if not html:
        return []

    # Создаем объект BeautifulSoup для удобного поиска элементов в HTML-коде
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем все теги span и h3, которые имеют классы заголовков новостей Lenta.ru
    items = soup.find_all(['span', 'h3'], class_=['card-mini__title', 'card-big__title', 'card-container__title'])

    # Если по конкретным классам ничего не нашли, пробуем найти все span, где в названии класса есть "title"
    if not items:
        items = soup.select('span[class*="title"]')

    titles = []  # Создаем пустой список для хранения очищенных заголовков
    for item in items:

        # Извлекаем текст из тега и убираем лишние пробелы по краям
        text = item.get_text(strip=True)

        # Если текст не пустой и мы его еще не добавляли (защита от дублей)
        if text and text not in titles:
            titles.append(text)  # Добавляем заголовок в наш список
    # Возвращаем первые 10 заголовков из списка
    return titles[:10]

def save_to_local_folder(titles, filename="news.txt"):
    if not titles:
        print("Нет данных для сохранения.")
        return False

    # Получаем полный путь к папке, в которой находится текущий запущенный скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Соединяем путь к папке с именем файла, создавая корректный путь для любой ОС
    file_path = os.path.join(current_dir, filename)

    try:
        # Открываем файл для записи ("w") в кодировке utf-8, чтобы корректно отображался русский язык
        with open(file_path, "w", encoding="utf-8") as f:
            # Перебираем заголовки, используя enumerate для получения порядкового номера (начиная с 1)
            for i, title in enumerate(titles, 1):
                # Записываем в файл строку в формате "номер. заголовок" и переходим на новую строку
                f.write(f"{i}. {title}\n")
        # Выводим сообщение об успешном сохранении и показываем путь к файлу
        print(f"Файл сохранен здесь: {file_path}")
        return True
    except IOError as e:
        # Если возникла ошибка при записи (например, нет прав доступа), выводим её в консоль
        print(f"Ошибка записи: {e}")
        return False

# Эта часть кода выполнится только если запустить этот файл, а не импортировать его
if __name__ == "__main__":
    # Вызываем функцию получения HTML-кода страницы
    html_content = get_lenta_news()
    # Вызываем функцию парсинга для получения списка заголовков
    news_titles = parse_titles(html_content)
    # Печатаем в консоль количество найденных заголовков
    print(f"Найдено новостей: {len(news_titles)}")
    # Пытаемся сохранить заголовки в файл и выводим финальный результат работы
    if save_to_local_folder(news_titles):
        print("Успешно!")
    else:
        print("Ошибка при сохранении.")