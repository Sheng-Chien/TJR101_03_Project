import requests
from bs4 import BeautifulSoup
import re
import json
import time

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

urlstart = "https://www.easycamp.com.tw"

#各分頁(各地區的露營場列表) ➜ 露營場 ➜ 詳細內容



# 2. 抓出一個縣市頁面中所有露營場連結
def get_camp_links(city_url):
    """抓出一個縣市頁面中所有露營場連結"""
    res = requests.get(city_url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("h2 a[href^='/Store_']")
    # for link in links:
    #     print(link["href"])
    return [urlstart + link["href"] for link in links]
    
# 3. 擷取個別露營場的詳細資訊 
def get_camp_info(soup):
    """營地基本資訊"""
    h1_tag =  soup.select_one("h1")
    name = h1_tag.contents[0].strip()
    star_count = len(h1_tag.select("i.fa-star"))
    reviews = h1_tag.select_one("h5.icon-font-color").text.strip()
    info = {
        "營地名稱": name,
        "獲得星數": star_count,
        "評價": reviews
    }
    return info

def get_address(soup):
    """營地地址"""
    address_tag = soup.select_one(".inline.block.camp-add")
    return address_tag.text.strip() if address_tag else "無地址資訊"

def get_gps(soup):
    """營地定位"""
    gps_tag = soup.select_one(".inline.camp-gps span")
    return gps_tag.text.strip() if gps_tag else "無GPS資訊"

def get_phone(soup):
    """營地電話"""
    phone_tag = soup.select_one(".inline.camp-phone")
    return phone_tag.text.strip() if phone_tag else "無電話資訊"
    


def get_price(soup):
    """營地價格"""
    table = soup.select_one("table.table.table-hover")
    if table:
        thead = [[th.text.strip() for th in table.select('thead th')] ]
        for tr in table.select('tbody tr'):
            row = [re.sub(r'[\s\u200B\u200C\u200D\uFEFF]', '', td.text.strip()) for td in tr.select('td')]
            thead.append(row)
        return thead
    else:
        print("找不到價格表格")
        return []
    

def get_table_content(soup):#營區資訊介紹表格
    """營區介紹""" 
    results = {}
    for el in soup.select("div.classify"):
        title = el.select_one('div.title').text.strip() 
        values = [li.text.strip() for li in el.select('li')]
        results[title] = "、".join(values)
    return results


def get_campsite_detail(soup):
    """營地須知"""
    h2_tags = soup.find_all('h2',class_='directions')
    detail = h2_tags[1].text.strip()
    return detail


def get_one_place_info(url):
    """獲得單一露營場各項資訊"""
    response = requests.get(url,headers=headers)
    if response.status_code != 200:
        print(f"請求失敗，status code: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")  
    return {
        "營地資訊": get_camp_info(soup),
        "營地地址": get_address(soup),
        "營地gps": get_gps(soup),
        "營地電話": get_phone(soup),
        "營地電話": get_price(soup),
        "營區介紹": get_table_content(soup),
        "營地須知": get_campsite_detail(soup)
    }

   


# ========== 主程式入口 ==========
def main():
    city_url = "https://www.easycamp.com.tw/Camp_0_2_0.html" 
    camp_urls = get_camp_links(city_url)
    all_camps = []
    for camp_url in camp_urls:
        print(f"處理營地：{camp_url}")
        camp_info = get_one_place_info(camp_url) 
        all_camps.append(camp_info)
        time.sleep(1) 

    print(f"共蒐集 {len(all_camps)} 筆營地資料")
    
    with open("xinbei_camp.json", "w", encoding="utf-8") as f:
        json.dump(all_camps, f, indent=4, ensure_ascii=False)
    


if __name__ == "__main__":
    main()


