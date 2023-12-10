import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def check_product_ozon(links: list[dict[str, str]]) -> list[dict[str, str]]:
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    s = Service()
    driver = webdriver.Chrome(service=s, options=options)

    driver.execute_cdp_cmd(
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
    checked_links = []
    try:
        driver.maximize_window()
        for url in links:
            driver.get(url["link"])
            sum_detected = detect_words(driver, words)
            if sum_detected > 1:
                checked_links.append(url)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    return checked_links


words = ["Добавить в корзину"]


def detect_words(driver: webdriver.Chrome, words_: list[str]):
    lens = []
    for word in words_:
        text = driver.find_elements("xpath", f"//*[contains(text(), '{word}')]")
        lens.append(len(text))

    return sum(lens)
