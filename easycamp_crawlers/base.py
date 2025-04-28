
import requests
from bs4 import BeautifulSoup



def get_city_links():
    """抓出所有縣市的頁面連結"""
    url = "https://www.easycamp.com.tw/store/store_list"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    city_links = []
    Base_url = "https://www.easycamp.com.tw"
   
    for link in soup.select("h2 a[href^='/Camp_']"):
        city_links.append(Base_url + link["href"])
        
    return city_links


#[Base_url + link["href"] for link in links]