import time

from selenium import webdriver

from src.config import YANDEX_IMAGE_SEARCH_URL


options = webdriver.FirefoxOptions()
options.set_preference("dom.webdriver.enabled", False)

browser = webdriver.Firefox(options=options)

browser.get(YANDEX_IMAGE_SEARCH_URL)

time.sleep(10)
