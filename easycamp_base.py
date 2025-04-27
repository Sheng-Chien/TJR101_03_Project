
import requests
from bs4 import BeautifulSoup

def get_city_links(c):
    """抓出所有縣市的頁面連結"""
    res = requests.get()
    soup = BeautifulSoup(res.text, "html.parser")
    city_links = soup.select("h2 a[href^='/Camp_']")
    #if  else: return[]
    #print("未找到任何營地連結")
    for link in city_links:
        print(link["href"])
    return [Base_url + link["href"] for link in links]