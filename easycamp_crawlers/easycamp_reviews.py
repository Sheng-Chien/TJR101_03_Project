import requests
from bs4 import BeautifulSoup
import re
import random
import time
from urllib.parse import urljoin
from pathlib import Path
import json

from reviews_links import get_campsite_links,get_city_links,get_review_links


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}

def get_camp_name(soup):
    """營地基本資訊""" 
    h1_tag =  soup.select_one("h1")
    name = h1_tag.contents[0].strip()
    return name


def get_overall_stars(soup):
    """營地獲得星數"""
    all_stars = soup.select_one("a.icon-star-position.assessment_scroll")#回傳一個tag物件
    if all_stars:
        given_stars = len(all_stars.select("i.fa-star"))
        return given_stars
    return 0
    
def get_review_count(soup):
    """獲得評論數"""
    review_count = soup.select_one("h5.icon-font-color")
    if review_count:
        text = review_count.text.strip()
        match = re.search(r'([\d,]+)', text) #抓出第一個包含數字與逗號的片段
        if match:
            number_str = match.group(1).replace(",", "")  # 不論千分位有無逗號都先移除
            return int(number_str)
    return 0


def get_score(soup):    
    """營地各項得分"""
    scores = []
    score_blocks = soup.select("div.col-md-12.col-sm-12.col-xs-12.evaluation-padding div.text-center")
    if not score_blocks:  # 如果沒有評分區塊，返回五個 None 避免後續出錯
        return [None] * 5 
    for block in score_blocks:
        star_count = len(block.select("i.fa-star"))  # 計算星星數
        scores.append(star_count)  
    return scores


def get_customer_name(soup): 
    """評論者姓名"""
    costumer_name = soup.select_one("div.col-md-12.col-sm-12.col-xs-12 > h3") 
    return re.sub(r'[\s\u200B\u200C\u200D\uFEFF]+', '', costumer_name.text) if costumer_name else None


def get_dates(soup):
    """入住日期&評論日期"""
    all_divs = soup.select("div.col-md-12.col-sm-12.col-xs-12.font-size-16px")
    checkin_date = None
    review_date = None
    for div in all_divs:
        text = div.text.strip()
        date_match = re.search(r"\d{4}/\d{2}/\d{2}", text)  
        if "入住" in text and date_match:
            checkin_date = date_match.group()
        elif "評價" in text and date_match:
            review_date = date_match.group()
    return checkin_date, review_date


def get_customer_rating(soup):
    """評論者給予的星數""" 
    rating_div= soup.select_one("div.col-md-3.col-sm-3.col-xs-3.icon-star-padding")
    customer_rating = len(rating_div.select("i.fa-star"))
    return customer_rating


def get_customer_reviews(block):
    """評論內容""" 
    title_tag = block.select_one("div.title-font-size.english-break-word")
    content_tag = block.select_one("div.content-font-size.english-break-word")    
    review_title = title_tag.text.strip()if title_tag else ""
    review_content = content_tag.text.strip()if content_tag else ""
    return review_title,review_content



def get_one_place_reviews(link, headers):
    """獲得單一露營場評分"""
    #all_reviews = []
    base_url = "https://www.easycamp.com.tw"
    #for link in urls:
    try:
        response = requests.get(link,headers=headers)
        if response.status_code != 200:
            print(f"請求失敗，status code: {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        camp_name = get_camp_name(soup)
        overall_stars = get_overall_stars(soup)
        review_count = get_review_count(soup)
        traffic, bathroom, view, service, facility = get_score(soup)
        all_reviews = []
        # 評論頁翻頁
        current_url = link
        while current_url:
            res = requests.get(current_url, headers=headers)
            if res.status_code != 200:
                print(f"請求失敗，status code: {res.status_code}")
                break
            soup = BeautifulSoup(res.text, "html.parser")
            review_container = soup.select_one("#tab11")

            if review_container: #如果有評論區
                review_blocks = review_container.select("div.row")
                for block in review_blocks:
                    customer_name = get_customer_name(block)
                    checkin_date, review_date = get_dates(block)
                    customer_rating = get_customer_rating(block)
                    review_title, review_content = get_customer_reviews(block)
                    review_data = {
                        "姓名": customer_name,
                        "入住日期": checkin_date,
                        "評論日期": review_date,    
                        "評分": customer_rating,
                        "評論標題": review_title,
                        "評論內容": review_content,    
                    }
                    all_reviews.append(review_data)
                    print(f"有{len(all_reviews)}筆評論")
            #下一頁
            next_page_link = None
            pagination = soup.select_one("ul.pagination")
            if pagination:
                next_links = pagination.select("li a") 
                for link in next_links:
                    if "下一頁" in link.text:
                        href = link.get("href")
                        next_page_link = urljoin(base_url, href)
                        break
            current_url = next_page_link   
            time.sleep(random.uniform(1, 3))          

        #收集一營地之完整評論資訊
        rating_data = {
              "營地名稱": camp_name,
              "營地總星等": overall_stars,
              "評論總數": review_count,
              "交通便利度": traffic,
              "衛浴整潔度": bathroom,
              "景觀滿意度": view,
              "服務品質": service,
              "設施完善度":facility,
              "顧客評論":all_reviews
        }
        return rating_data
    
    except Exception as e:
        print(f"抓取 {link} 時發生錯誤：{e}")
        return None


def save_to_json(data, filename):
    """存入 JSON 檔"""
    with open(filename, "w", encoding="utf-8") as f:
       json.dump(data, f, indent=4, ensure_ascii=False)



def main():
    url = "https://www.easycamp.com.tw/store/store_list"  # base.py 中的網址
    city_links = get_city_links(url, headers)
    campsite_links = get_campsite_links(city_links, headers)
    review_links = get_review_links(campsite_links, headers)

    # 使用 pathlib 定義 checkpoint 檔案路徑
    checkpoint_file = Path("easycamp_reviews.json")
    all_data = []
     # 若已有 checkpoint，先載入已經儲存的資料
    if checkpoint_file.exists():
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            all_data = json.load(f)
   

    processed_names = {camp["營地名稱"] for camp in all_data}
    for i, link in enumerate(review_links):
        print(f"\n🔍 正在處理第 {i+1} 筆，共 {len(review_links)} 筆")
    #for link in review_links:
        # 判斷是否已經處理過這個露營場
        camp_preview = get_camp_name(BeautifulSoup(requests.get(link, headers=headers).text, "html.parser"))
        if camp_preview in processed_names:
            print(f"✅ 已處理過 {camp_preview}，略過")
            continue

        camp_data = get_one_place_reviews(link, headers)
        if camp_data:
            all_data.append(camp_data)

            # 即時寫入 checkpoint
            with open(checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
            print(f"儲存 {camp_data['營地名稱']} 成功")

    # review_data = get_one_place_reviews(review_links, headers)
    #save_to_json(review_data, "easycamp_reviews.json")

if __name__ == "__main__":
    main()




