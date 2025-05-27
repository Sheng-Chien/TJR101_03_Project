import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin

#from base import get_city_links
from utils.YaHsuan.E.base import get_city_links

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

def get_campsite_links(city_links, headers):
    """取得一個縣市頁面中所有露營場連結""" 
    campsite_links = []
    base_url = "https://www.easycamp.com.tw"

    for city_url in city_links:# 拿到從各縣市網址逐一去爬清單
        next_page = city_url
        while next_page:
            try:
                response = requests.get(next_page, headers = headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.select("h2 > a[href^='/Store_']"):
                    campsite_links.append(urljoin(base_url, link["href"]))
                time.sleep(random.uniform(1, 3))

                # 檢查是否有下一頁
                pagination = soup.select("ul.pagination li a")
                next_page = None
                for page in pagination:
                    if page.text.strip() == "下一頁 »":
                        href = page.get("href")
                        next_page = urljoin(base_url, href)  # 自動處理完整/相對路徑
                        break
            except Exception as e:
                print(f"抓取 {next_page} 時發生錯誤：{e}")
                break 
                
    print(f"總共有{len(campsite_links)}個露營場網址")
    return campsite_links #/Store的完整網址


if __name__ == "__main__":
    url = "https://www.easycamp.com.tw/store/store_list"  # base.py 中的網址
    # 先從 base.py 中取得所有縣市的連結
    city_links = get_city_links(url, headers)
    get_campsite_links(city_links, headers)
