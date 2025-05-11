import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium_driver import SeleniumDriver
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class KlookCrawer(SeleniumDriver):
    pass

if __name__ == "__main__":
    # klook 台灣 露營 的搜尋結果
    root = Path(__file__).parent

    klook = KlookCrawer()
    time.sleep(1)

    # 先擷取搜尋頁面
    # https://www.klook.com/zh-TW/destination/co1014-taiwan/?frontend_id_list=19&start=1
    # frontend_id_list=19  19是露營
    # start=1   1 是第 1 頁

    with open(root/"test/搜尋第一頁.html", "r", encoding="utf-8") as file:
        page = file.read()

    
    page = 1
    while True:
        # break
        search_url = f"https://www.klook.com/zh-TW/destination/co1014-taiwan/?frontend_id_list=19&start={page}"
        search_url = "https://www.klook.com/zh-TW/"
        klook.gotoURL(search_url)
        time.sleep(3)
        # links = klook.driver.find_elements(By.CSS_SELECTOR, 'a.title[target="_blank"]')
        # element = klook.driver.find_element(By.CLASS_NAME, "country_block")
        # print("網頁加載中，請稍候...")
        # # 等待該元素消失（最多等 20 秒）
        # WebDriverWait(klook.driver, 20).until(
        #     EC.invisibility_of_element(element)
        # )
        break

