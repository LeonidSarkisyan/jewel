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
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')

    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('enable-automation')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")

    options.add_argument("--window-size=1920,1080")

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Vivaldi/6.4.3160.34'
    options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(
        options=options
    )
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
    print(res)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    browser.get("https://bot.sannysoft.com/")
    browser.save_screenshot("antibot_screenshot.png")
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
    except NoSuchElementException:
        return []
    else:
        product_links = get_product_links(links)
        print("ВСЕ ЛИНКИ:", product_links)
        checked_links = check_product_ozon(product_links)
        checked_links_limited = checked_links[:5] if len(checked_links) > 5 else checked_links
        return checked_links_limited
