import requests
from bs4 import BeautifulSoup


def get_campsite_links(city_url):
    """抓出一個縣市頁面中所有露營場連結"""
    response = requests.get(city_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    campsite_links = []
    Base_url = "https://www.easycamp.com.tw"

    for link in soup.select("h2 a[href^='/Store_']"):
        campsite_links.append(Base_url + link["href"])

    return campsite_links

   