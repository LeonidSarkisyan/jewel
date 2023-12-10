import json
import requests


def image_search(url):
    url = f"https://yandex.ru/images/search?source=collections&text=site:ozon.ru&rpt=imageview&url={url}"
    response = requests.get(url)
    print(response)
    print(response.content)


image_search("https://www.ozon.ru/search/?deny_category_prediction=true&from_global=true&text=Печенье&product_id=791684246")
