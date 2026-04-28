# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
from bs4 import BeautifulSoup
from google.colab import files

# Получаем страницу
response = requests.get('https://lenta.ru')
soup = BeautifulSoup(response.text, 'html.parser')

# создаем пустой список news, в который будем добавлять заголовки и ссылки
news = []
# ищем все HTML-элементы 'a' (ссылки) с классом '_topnews' на странице
# каждый элемент содержит заголовок новости и ссылку на неё.
for item in soup.find_all('a', class_='_topnews'):
  # внутри найденной ссылки ищем либо заголовок 'h3', либо 'span'
  # если поиск 'h3' вернет None, то выполнится поиск 'span'
  title = item.find('h3') or item.find('span')
  # Проверяем два условия: нашли ли мы заголовок title b ссылку (атрибут href)
  if title and item.get('href'):
    # если оба условия True, то извлекаем ссылку из атрибута href
    link = item['href']
    # Если ссылка НЕ начинается с http
    if not link.startswith('http'):
      # Добавляем домен
      link = 'https://lenta.ru' + link
      # Добавляем в список news строку из заголовка + ссылки
      news.append(f"{title.text.strip()}: {link}")

# Количество новостей
n = 10
# Делаем срез, выводит последние 'n' новостей
text_news = news[:n]
for item in text_news:
    print(item)

# Задаем имя файла, в который будем сохранять новости
filename = 'news.txt'
# Открываем файл для записи ('w' - режим записи)
# encoding='utf-8' - указываем кодировку для корректного отображения русских букв
# with open(...) as f - автоматически закроет файл после завершения блока
with open(filename, 'w', encoding='utf-8') as f:
    # '\n'.join(text_news) - объединяем все элементы списка text_news в одну строку,
    # разделяя их символом переноса строки '\n'
    f.write('\n'.join(text_news))

# Скачиваем файл на компьютер
files.download(filename)

print(f"\nСохранено {len(text_news)} новостей в файл {filename} и скачано на компьютер")
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
