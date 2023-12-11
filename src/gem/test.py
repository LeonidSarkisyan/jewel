import time

import requests
from selenium import webdriver


options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('start-maximized')
options.add_argument("--headless")
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
options.add_argument(f'user-agent={user_agent}')

browser = webdriver.Chrome(options=options)

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

time.sleep(2)

browser.get("https://yandex.ru/images/search?cbir_id=2366846%2FtgGy6AmAJpCdMU-JCgonHA9352&from=tabbar&rpt=imageview&url=https%3A%2F%2Favatars.mds.yandex.net%2Fget-images-cbir%2F2366846%2FtgGy6AmAJpCdMU-JCgonHA9352%2Forig")

browser.save_screenshot("SCREEN.png")

time.sleep(100)
