import requests
from bs4 import BeautifulSoup


response = requests.get("https://yandex.ru/images/search?from=tabbar&text=site:ozon.ru")

print(response.content1)
