import requests
from bs4 import BeautifulSoup
import time
import random

from campsite_links import get_campsite_links,get_city_links

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

def get_review_links(campsite_links, headers):
    """取得評論頁完整網址"""
    review_links = [] 
    base_url = "https://www.easycamp.com.tw"
    for link in campsite_links:#從許多露營地完整網址找出評價link
        response = requests.get(link, headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")
        review_link_tag = soup.find("a",string="住過露友評價")                           #會是像<a href="...">住過露友評價</a>的tag物件
        review_links.append (base_url + review_link_tag.get("href"))
        time.sleep(random.uniform(1, 3))                               #每跑完一個露營場頁面、並成功取得它的評論頁網址後，隨機暫停 1～3 秒
    return review_links
        

if __name__ == "__main__":
    url = "https://www.easycamp.com.tw/store/store_list"  # base.py 中的網址
    city_links = get_city_links(url, headers)#先取兩個縣市
    campsite_links = get_campsite_links(city_links, headers)
    get_review_links(campsite_links, headers)