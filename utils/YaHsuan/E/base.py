import requests
from bs4 import BeautifulSoup

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

def get_city_links(url, headers):
    """抓出所有縣市的頁面連結"""
    city_links = []
    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        print(f"請求失敗，status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    base_url = "https://www.easycamp.com.tw"

    h2_list = soup.find_all("h2", class_="store")
    for h2 in h2_list:
        if "縣市" in h2.text:
            city_div = h2.find_next_sibling("div", class_="kw-h")
            for a in city_div.find_all("a"):
                href = a.get("href") 
                if href:
                    city_links.append(base_url + href )  
    return city_links

def main():
    url = "https://www.easycamp.com.tw/store/store_list"
    links = get_city_links(url, headers)
    for link in links:
        print(link)
if __name__ == "__main__":
    main()


