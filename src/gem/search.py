import time
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException, StaleElementReferenceException

from fake_useragent import UserAgent

from src.config import YANDEX_IMAGE_SEARCH_URL
from src.gem.protect import check_product_ozon


def get_yandex_image_url(url: str):
    return f'https://yandex.ru/images/searchbyimage?rpt=imageview&url={url}'


photo_choose_x_path = "/html/body/div[1]/header/div/div[2]/div[1]/form/div[1]/span/span/button/div"
input_search_x_path = "/html/body/div[1]/header/div/div[3]/div[1]/form/span/input"
search_button_x_path = "/html/body/div[1]/header/div/div[3]/div[1]/form/button"
yandex_input_search_x_path = "/html/body/div[1]/div/div[1]/header/form/div[1]/input"
yandex_button_x_path = "/html/body/div[1]/div/div[1]/header/form/button/div[2]"
yandex_default_x_path = "/html/body/div[6]/div/div/div[3]/div[3]/a[1]"
search_results_list_x_path = "/html/body/div[4]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div"


def init_browser() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    options.add_argument("--disable-blink-features=AutomationControlled")

    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(
        options=options,
    )
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {"source": "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});"})
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        "source": "Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {get: () => 1});"})
    res = browser.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument", {
            'source': """
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """
        }
    )

    browser.get("https://bot.sannysoft.com/")
    time.sleep(100)
    print(res)
    return browser


def get_started_yandex(browser: webdriver.Chrome):
    browser.get(YANDEX_IMAGE_SEARCH_URL)
    while True:
        try:
            yandex_default_element = browser.find_element("xpath", yandex_default_x_path)
            yandex_default_element.click()
        except (ElementNotInteractableException, NoSuchElementException):
            print("Загружается...")
            browser.save_screenshot("yandex_screenshot.png")
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
            print("Пробуем яндекс...")
            continue
        else:
            yandex_input_search_element.click()
            yandex_input_search_element.send_keys("site:ozon.ru")
            yandex_button_element = browser.find_element("xpath", yandex_button_x_path)
            yandex_button_element.click()
            break


product_link_x_path = "/html/body/div[14]/div[2]/div/div/div/div[3]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/a"


def collect_data(browser: webdriver.Chrome) -> list[str]:
    result_links = []
    while True:
        try:
            search_result_list_element = browser.find_element("xpath", search_results_list_x_path)
        except NoSuchElementException:
            pass
        else:
            while True:
                try:
                    rows = search_result_list_element.find_elements("class name", "JustifierRowLayout-Row")
                except StaleElementReferenceException:
                    print("Беру картинки")
                    continue
                else:
                    for row in rows:
                        items = row.find_elements("class name", "JustifierRowLayout-Item")
                        for item in items:
                            item.click()
                            while True:
                                try:
                                    product_link_element = browser.find_element("xpath", product_link_x_path)
                                    link = product_link_element.get_attribute("href")
                                    result_links.append(link)
                                    close_button = browser.find_element("class name", "MMViewerModal-Close")
                                    close_button.click()
                                except NoSuchElementException:
                                    print("Ссылка на продукт пока не загружена")
                                else:
                                    break
                    break
            break
    return result_links


def collect_data_new(browser: webdriver.Chrome, limit: int = 20) -> list[dict[str, str]]:
    links = []
    first_image = browser.find_element("class name", "SimpleImage-Image")
    first_image.click()
    items = browser.find_elements("class name", "MMGallery-Item")

    for index, item in enumerate(items):
        if index < 20:
            item.click()
            link = (
                browser.find_element("class name", "MMOrganicSnippet-TitleWrap")
                .find_element("tag name", "a").get_attribute("href")
            )
            image_link = browser.find_element("class name", "MMImage-Origin").get_attribute("src")

            links.append({"link": link, "image_link": image_link})
        else:
            break

    return links


def get_product_links(links: list[dict[str, str]]) -> list[dict[str, str]]:
    product_links = []
    for link in links:
        if "/product/" in link["link"]:
            product_links.append(link)
    return product_links


def get_similar_links(url_image: str, limit: int = 5):
    print("НАЧИНАЕМ ПАРСИНГ")
    browser = init_browser()
    print("ЗАПУСКАЮ ЯНДЕКС")
    get_started_yandex(browser)
    print("ВВОЖУ ДАННЫЕ URL IMAGE")
    photo_prepared(browser, url_image)
    print("ВВОЖУ ДАННЫЕ URL IMAGE")
    try_search(browser)
    print("ПРОБУЕМ ЯНДЕКС ПОИСК")
    try_yandex_search(browser)
    time.sleep(2)
    browser.save_screenshot('screenie.png')
    try:
        links = collect_data_new(browser)
        browser.close()
        browser.quit()
    except NoSuchElementException:
        return []
    else:
        product_links = get_product_links(links)
        print("ВСЕ ЛИНКИ:", product_links)
        checked_links = check_product_ozon(product_links)
        checked_links_limited = checked_links[:5] if len(checked_links) > 5 else checked_links
        return checked_links_limited
