# 增加迴圈爬全台露營場

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

import random
import pandas as pd
import time
import datetime
from pathlib import Path
import csv
import glob # 最後整併檔案

# 紀錄全部時間用
start_time = datetime.datetime.now()
now = datetime.datetime.now().strftime("%Y%m%d_%H%M")

def wait(min_sec=2, max_sec=3):
    '''
    隨機等待數秒
    '''
    time.sleep(random.uniform(min_sec, max_sec))


# 讓chrome視窗不要自動關閉
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# 使用下載好的chromedrive
service = Service(executable_path="./Team_project_coding/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# 縣市列表
taiwan_cities = [
    #"台北", "新北", "基隆", 
    #"桃園", "新竹", "苗栗",
    "台中", #"彰化", "南投", "雲林", 
    # "嘉義", "台南", "高雄", "屏東", 
    # "宜蘭", "花蓮", "台東",
]

# 爬全台露營場
for city in taiwan_cities:
    # map搜尋頁面
    query = f"{city} 露營場"
    url = f"https://www.google.com/maps/search/{query}"
    driver.get(url)
    wait()

    # checkpoint檔案
    # 每個縣市一個checkpoint檔案
    checkpoint_folder = Path("checkpoint")
    checkpoint_folder.mkdir(parents=True, exist_ok=True)
    checkpoint_path = checkpoint_folder / f"{query}_checkpoint.csv"

    # 讀取checkpoint檔案內爬過的營地名稱並存成dataframe
    # 後續比對用
    if checkpoint_path.exists():
            done_df = pd.read_csv(checkpoint_path, encoding="utf-8-sig")
            done_names = set(done_df["露營場名稱"].tolist())
    else:
        done_names = set()

    # google map定位左邊的搜尋欄
    scroll_blocks = driver.find_elements(By.CSS_SELECTOR, ".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd")
    # print("找到區塊數量：", len(scroll_blocks))
    scroll_block = scroll_blocks[-1]

    # 多次滾動左側搜尋結果直到底部
    while True:    
        try:
            done_elem = driver.find_element(By.CSS_SELECTOR, "span.HlvSq")
            done_text = done_elem.text.strip()
            if "你已看完所有搜尋結果" in done_text:
                print("已經滾動到底了")
                break
        except:
            pass

        # 每次滾動一段距離
        driver.execute_script("arguments[0].scrollTop += 800;", scroll_block)
        wait(1, 2)

    # 排除贊助商廣告
    cards = driver.find_elements(By.CLASS_NAME, 'Nv2PK')
    valid_cards = []
    for card in cards:
        try:
            card.find_element(By.XPATH, './/*[contains(text(), "贊助")]')
            continue  
        except:
            valid_cards.append(card)

    print(f"總共搜尋到{len(valid_cards)}個露營場")

    links = []
    # 先挑選Tag是露營場相關的才抓連結 , 其他的都不要
    for i, card in enumerate(valid_cards):
        try:
            tag_text = card.find_element(By.XPATH, './/div[@class="W4Efsd"]/span').text
            
            if tag_text in ["露營地點", "旅遊運營商", "營地"]:
                link = card.find_element(By.CLASS_NAME, "hfpxzc").get_attribute("href")
                links.append(link)
            else:
                print(f"第 {i} 張卡片標籤為「{tag_text}」，不符合條件，略過。")
        except:
            print(f"第 {i} 張卡片未找到標籤元素，略過。")
            continue

    # 後面儲存資料用
    camping_data = []

    # 正式開始爬
    for link in links:
        try:
            driver.get(link)
            element = driver.find_element(By.CLASS_NAME, "lMbq3e")
            wait()

            # 基本資訊1
            print("爬基本資訊")
            camp_name = element.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text

            # 確認以前checkpoint是否爬過
            if camp_name in done_names:
                print(f"{camp_name} 已處理過，略過")
                continue
            
            else:
                rank = element.find_element(By.CSS_SELECTOR, 'span[aria-hidden="true"]').text
                total_rate = element.find_element(By.CSS_SELECTOR, 'span[aria-label$="則評論"]').text.strip("()")
                wait(5, 6)

                # 基本資訊2
                basic_infos = driver.find_elements(By.CSS_SELECTOR, ".Io6YTe.fontBodyMedium")
                intro = f"\n ".join([info.text for info in basic_infos])
                    
                wait()
                print("基本資訊爬完")

                # 準備爬評論
                # 抓所有 tab 按鈕
                tab_wrapper = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".yx21af.lLU2pe.XDi3Bc")))    
                tabs = tab_wrapper.find_elements(By.CSS_SELECTOR, 'button[role="tab"]')
                wait()
                
                if tabs:
                    print(f"tab數量: {len(tabs)}")
                    section_names = driver.find_elements(By.CSS_SELECTOR, ".Gpq6kf.NlVald")

                    for name in section_names:
                            
                            label_text = name.text.strip()
                            wait()

                            # 點擊「評論」分頁
                            if label_text == "評論":
                                name.click()
                                print("進入評論") 
                                wait(5, 7) 

                                # 確認評論區塊
                                scroll_blocks = driver.find_elements(By.CSS_SELECTOR, ".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
                                scroll_block = scroll_blocks[-1]

                                origin = ScrollOrigin.from_element(scroll_block)
                                actions = ActionChains(driver)

                                # 滑動評論到達指定篇數max_reviews
                                max_reviews = 100
                                max_scrolls = 70
                                scroll_count = 0
                                last_count = 0
                                same_count_repeat = 0
                                max_repeat = 10  # 如果連續10次滑動都沒新增評論數就停止

                                while scroll_count < max_scrolls:
                                    # 滑動
                                    actions.scroll_from_origin(origin, 0, 800).perform()
                                    wait(2, 3)
                                    scroll_count += 1

                                    # 確認目前評論數
                                    reviews = driver.find_elements(By.CSS_SELECTOR, ".jftiEf.fontBodyMedium")
                                    review_count = len(reviews)
                                    
                                    print(f"目前載入評論數：{review_count}")

                                    if review_count >= max_reviews:
                                        print("已達目標評論數，停止滑動")
                                        break

                                    # 如果這次滑動後評論數沒增加，記錄次數
                                    if review_count == last_count:
                                        same_count_repeat += 1
                                        if same_count_repeat >= max_repeat:
                                            print("已連續滑動幾次沒有新評論，停止")
                                            break
                                    else:
                                        same_count_repeat = 0  # 有新增就歸零

                                    last_count = review_count                            

                                print("評論區滑動加載完成")
                                wait()

                                # 儲存評論用
                                review_texts = []

                                # 開始爬取評論
                                reviews = driver.find_elements(By.CSS_SELECTOR, ".jftiEf.fontBodyMedium")[:100]
                                print("開始爬評論")
                                for i, review in enumerate(reviews, 1):
                                    
                                    # 先點選「全文」按鈕
                                    more_buttons = review.find_elements(By.XPATH, './/button[contains(text(), "全文")]')
                                    for btn in more_buttons:
                                        driver.execute_script("arguments[0].click();", btn)
                                        wait(1, 2)
                                    
                                    # 爬評論內容                                
                                    reviewer = review.find_element(By.CLASS_NAME, "d4r55").text

                                    # 如果評論架構中有星數就爬
                                    try:
                                        each_rank = review.find_element(By.CSS_SELECTOR, "div.DU9Pgb span[role='img'][aria-label$='顆星']")
                                        each_rating = each_rank.get_attribute("aria-label")
                                    except:
                                        each_rating = "本篇評論無星數"

                                    # 如果有評論內容就爬
                                    try:
                                        content = review.find_element(By.CLASS_NAME, "wiI7pd").text
                                    except:
                                        content = "本筆評論無內容"
                                        
                                    # 評論日期有兩種版型
                                    try:
                                        # 嘗試抓舊版 class
                                        review_time = review.find_element(By.CLASS_NAME, "rsqaWe").text
                                    except:
                                        try:
                                            # 嘗試抓新版 class 結構
                                            review_time_date = review.find_element(By.CSS_SELECTOR, ".fzvQIb").text
                                            review_time_before = review.find_element(By.CSS_SELECTOR, ".xRkPPb").text.replace("Google", "").replace(" (", "").replace(")", "")
                                            review_time = f"{review_time_date}\n{review_time_before}"

                                        except:
                                            review_time = ""  # 無時間資訊
                                    wait()

                                    review_texts.append(f"{reviewer}\n{review_time}\n{each_rating}\n{content}")
                                
                                # 儲存資料
                                camp_info = {
                                    "露營場名稱": camp_name,
                                    "縣市" : city,
                                    "星數": rank,
                                    "總評論數": total_rate,
                                    "其他資訊": intro,                                    
                                }
                                for idx, review in enumerate(review_texts):
                                    camp_info[f"評論{idx+1}"] = review

                                camping_data.append(camp_info)

                                # 爬完一筆就儲存到checkpoint.csv
                                write_header = not checkpoint_path.exists()                        
                                with open(checkpoint_path, "a", encoding="utf-8-sig", newline="") as f:
                                    writer = csv.DictWriter(f, fieldnames=camp_info.keys())
                                    if write_header:
                                        writer.writeheader()
                                    writer.writerow(camp_info)

                print("已爬完1個露營場資訊")
                print(f"目前checkpoint露營場數量: {len(pd.read_csv(checkpoint_path, encoding='utf-8-sig'))}")

        except Exception as e:
            print(f"這筆失敗，錯誤原因：{e.__class__.__name__} - {e}")
            continue

    wait(9, 10)

driver.close()

# 整併全部checkpoint資料
columns = ["露營場名稱", "縣市", "星數", "總評論數", "其他資訊"] + [f"評論{i}" for i in range(1, max_reviews+1)]

all_checkpoints = glob.glob("checkpoint/*_checkpoint.csv", recursive=True)
combined_df = pd.concat([pd.read_csv(f, encoding='utf-8-sig') for f in all_checkpoints], ignore_index=True)

combined_df = combined_df[columns]
combined_df = combined_df.drop_duplicates(subset=["露營場名稱", "縣市"])

final_filename = f"全台露營場_final_{now}.csv"
combined_df.to_csv(final_filename, index=False, encoding="utf-8-sig")
print(f"\n所有checkpoint檔案已整併儲存成：{final_filename}")

# 刪除所有 checkpoint 資料夾內的 CSV 檔案
for file in Path("checkpoint").glob("*_checkpoint.csv"):
    try:
        file.unlink()
        print(f"已刪除：{file.name}")
    except Exception as e:
        print(f"刪除失敗，錯誤原因：{e}")

# 計算花費時間
end_time = datetime.datetime.now()
elapsed = end_time - start_time

print(f"開始時間：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"結束時間：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"總共花費時間：{elapsed}")

