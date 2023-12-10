import requests
from selenium import webdriver


response = requests.get("https://yandex.ru/images/search?cbir_id=1537715%2Fo8oKWxts0adsS-hPWAN85g678&cbir_page=similar&from=tabbar&rpt=imageview&text=site%3Aozon.ru&url=https%3A%2F%2Favatars.mds.yandex.net%2Fget-images-cbir%2F1537715%2Fo8oKWxts0adsS-hPWAN85g678%2Forig")

print(response.content)
