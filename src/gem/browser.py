import json
import requests


def image_search(url):
    url = f"https://yandex.ru/images/search?source=collections&text=site:ozon.ru&rpt=imageview&url={url}"
    response = requests.get(url)
    print(response)
    print(response.content)


image_search("https://raskraskiplus.ru/wp-content/uploads/7/8/6/786f0f50636ffc16755be43a3f1da8f2.jpeg")
