import time
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException

from src.config import YANDEX_IMAGE_SEARCH_URL


def get_yandex_image_url(url: str):
    return f'https://yandex.ru/images/searchbyimage?rpt=imageview&url={url}'


photo_choose_x_path = "/html/body/div[1]/header/div/div[2]/div[1]/form/div[1]/span/span/button/div"
input_search_x_path = "/html/body/div[1]/header/div/div[3]/div[1]/form/span/input"
search_button_x_path = "/html/body/div[1]/header/div/div[3]/div[1]/form/button"
yandex_input_search_x_path = "/html/body/div[1]/div/div[1]/header/form/div[1]/input"
yandex_button_x_path = "/html/body/div[1]/div/div[1]/header/form/button/div[2]"
yandex_default_x_path = "/html/body/div[6]/div/div/div[3]/div[3]/a[1]"


def init_browser() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=chrome_options)
    return browser


def get_started_yandex(browser: webdriver.Chrome):
    browser.get(YANDEX_IMAGE_SEARCH_URL)
    while True:
        try:
            yandex_default_element = browser.find_element("xpath", yandex_default_x_path)
            yandex_default_element.click()
        except ElementNotInteractableException:
            continue
        else:
            break


def photo_prepared(browser: webdriver.Chrome, url_image: str):
    photo_choose_element = browser.find_element("xpath", photo_choose_x_path)
    time.sleep(1)
    photo_choose_element.click()
    input_search_element = browser.find_element("xpath", input_search_x_path)
    input_search_element.click()
    input_search_element.send_keys(url_image)
    time.sleep(1)


def try_search(browser: webdriver.Chrome):
    search_button_element = browser.find_element("xpath", search_button_x_path)
    while True:
        try:
            search_button_element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            print("Пока не кликается...")
        else:
            break


def try_yandex_search(browser: webdriver.Chrome):
    while True:
        try:
            yandex_input_search_element = browser.find_element("xpath", yandex_input_search_x_path)
        except NoSuchElementException:
            print("Пока не загрузилось.")
            continue
        else:
            yandex_input_search_element.click()
            yandex_input_search_element.send_keys("site:ozon.ru")
            yandex_button_element = browser.find_element("xpath", yandex_button_x_path)
            yandex_button_element.click()
            break


def get_similar_links(url_image: str):
    browser = init_browser()
    get_started_yandex(browser)
    photo_prepared(browser, url_image)
    try_search(browser)
    try_yandex_search(browser)


get_similar_links("https://i7.imageban.ru/out/2023/12/09/701697799ca7d7c51c1bf5a5b172556d.jpg")

