# 為了未來部署到GCP
# 改為headless形式(不會跳出視窗)爬資料

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.chrome.options import Options

import random
import pandas as pd
import time
from pathlib import Path
import csv
import glob # 最後整併檔案


def wait(min_sec=2, max_sec=3):
    '''
    隨機等待數秒
    '''
    time.sleep(random.uniform(min_sec, max_sec))

def e_chrome_robot():
    # 讓chrome視窗不要自動關閉
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless=new")              # 使用新版 headless 模式
    options.add_argument("--no-sandbox")                # 雲端環境建議加
    options.add_argument("--disable-dev-shm-usage")     # 防止 /dev/shm 空間不足
    options.add_argument("--window-size=1920,1080")     # 頁面 layout 必備
    options.add_argument("--disable-gpu")               # 某些 Linux 機器建議加（可加可不加）

    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, 
                              options=options)
    driver.set_window_size(1920, 1080) 
    return driver

def e_search_all_links(url, driver, query):

    driver.get(url)
    wait(3, 5)

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
        wait(3, 5)

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
            
            if tag_text in ["露營地點", "旅遊運營商", "營地", "露營車營地", "露營小屋", "農場", "2 星級飯店", "3 星級飯店"]:
                link = card.find_element(By.CLASS_NAME, "hfpxzc").get_attribute("href")
                links.append(link)
            else:
                print(f"第 {i} 張卡片標籤為「{tag_text}」，不符合條件，略過。")
        except:
            print(f"第 {i} 張卡片未找到標籤元素，略過。")
            continue
    return links, query

def e_checkpoint(city):
    # checkpoint檔案
    # 每個縣市的基本資料checkpoint檔案
    checkpoint_folder = Path("output", "checkpoint", f"{city}")
    checkpoint_folder.mkdir(parents=True, exist_ok=True)
    checkpoint_path = checkpoint_folder / f"{city}_basic_info_checkpoint.csv"

    # 評論資料的暫存檔
    review_checkpoint_folder = Path("output", "checkpoint", f"{city}")
    review_checkpoint_folder.mkdir(parents=True, exist_ok=True)
    review_checkpoint_path = review_checkpoint_folder / f"{city}_review_info_checkpoint.csv"

    # 讀取checkpoint檔案內爬過的營地名稱並存成dataframe
    # 後續比對用
    if checkpoint_path.exists():
            done_df = pd.read_csv(checkpoint_path, encoding="utf-8-sig")
            done_names = set(done_df["露營場名稱"].tolist())
    else:
        done_names = set()
    return done_names, checkpoint_path, review_checkpoint_path

def e_crawl_single_campground(driver, links, done_names, checkpoint_path, review_checkpoint_path, city):

    # 開始爬
    for link in links:
        try:
            driver.get(link)
            element = driver.find_element(By.CLASS_NAME, "lMbq3e")
            wait(3, 5)

            # 基本資訊1
            print("爬基本資訊")
            camp_name = element.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text

            # 確認以前checkpoint是否爬過
            if camp_name in done_names:
                print(f"{camp_name}已處理過，略過")
                continue
            
            else:
                rank = element.find_element(By.CSS_SELECTOR, 'span[aria-hidden="true"]').text
                total_rate = element.find_element(By.CSS_SELECTOR, 'span[aria-label$="則評論"]').text.strip("()")
                wait(5, 6)

                # 基本資訊2
                parent_blocks = driver.find_elements(By.CSS_SELECTOR, "div.RcCsl.fVHpi.w4vB1d.NOE9ve.M0S7ae.AG25L")[:3]
                intro_lines = []
                for block in parent_blocks:
                    try:
                        text = block.find_element(By.CSS_SELECTOR, ".Io6YTe.fontBodyMedium").text.strip().replace('"', '').replace(",", "")
                        intro_lines.append(text)
                    except:
                        continue  

                intro = "\n".join(intro_lines)

                # 儲存基本資料
                camp_info = {
                    "露營場名稱": camp_name,
                    "星數": rank,
                    "總評論數": total_rate,
                    "其他資訊": intro,
                    "縣市": city,                          
                }

                e_basicinfo_save_to_checkpoint(checkpoint_path, **camp_info)
                    
                wait()
                print(f"{camp_name}基本資訊爬完&儲存")

            # 準備爬評論
            # 抓所有 tab 按鈕
            tab_wrapper = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".yx21af.lLU2pe.XDi3Bc")))    
            tabs = tab_wrapper.find_elements(By.CSS_SELECTOR, 'button[role="tab"]')
            wait(3, 5)
            
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
                        max_scrolls = 100
                        scroll_count = 0
                        last_count = 0
                        same_count_repeat = 0
                        max_repeat = 10  # 如果連續10次滑動都沒新增評論數就停止

                        while scroll_count < max_scrolls:
                            # 滑動
                            actions.scroll_from_origin(origin, 0, 1200).perform()
                            wait(3, 5)
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

                            # 儲存資料
                            review_info = {
                                "check_ID": f"{camp_name}-{city}-{i}",
                                "露營場名稱": camp_name,
                                "評論者": reviewer,
                                "評論時間": review_time,
                                "評論星數": each_rating,
                                "評論內容": content,                                 
                            }

                            e_save_camp_reviews(review_checkpoint_path, **review_info)

            print(f"已爬完1個露營場資訊: {camp_name}")
        except Exception as e:
            print(f"這筆失敗，錯誤原因：{e.__class__.__name__} - {e}")
            continue


def e_basicinfo_save_to_checkpoint(checkpoint_path, **data):

    # 爬完一個露營場就儲存到checkpoint
    write_header = not checkpoint_path.exists()                        
    with open(checkpoint_path, "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(data)

    wait()

def e_save_camp_reviews(review_checkpoint_path, **data):

    # 爬完一個露營場的100則評論就儲存到checkpoint
    write_header = not review_checkpoint_path.exists()                        
    with open(review_checkpoint_path, "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(data)
    wait()
    
def e_save_to_final_file(driver):
    driver.close()
    
    # 整併全部基本資料的checkpoint檔案
    camp_files = glob.glob("output/checkpoint/*/*_basic_info_checkpoint.csv")

    camp_df = pd.concat([pd.read_csv(f, encoding='utf-8-sig') for f in camp_files], ignore_index=True)
    columns = ["露營場名稱", "縣市", "星數", "總評論數"]
    camp_df = camp_df[columns]
    camp_df = camp_df.drop_duplicates(subset=["露營場名稱", "縣市"])

    final_filename = f"全台露營場_final.csv"
    camp_df.to_csv(final_filename, index=False, encoding="utf-8-sig")

    # 整併全部評論checkpoint資料
    review_files = glob.glob("output/checkpoint/*/*_review_info_checkpoint.csv")

    review_columns = ["check_ID", "露營場名稱", "評論者", "評論時間", "評論星數", "評論內容"]    
    review_df = pd.concat([pd.read_csv(f, encoding='utf-8-sig') for f in review_files], ignore_index=True)
    review_df = review_df[review_columns]
    review_df = review_df.drop_duplicates(subset=["check_ID"])
    
    review_df.to_csv("camp_reviews_final.csv", index=False, encoding="utf-8-sig")

    print(f"\n所有checkpoint檔案已整併儲存")

def e_delete_checkpoint():
    # 刪除所有 checkpoint 資料夾內的 CSV 檔案
    for file in Path("checkpoint").rglob("*_checkpoint.csv"):
        try:
            file.unlink()
            print(f"已刪除：{file.name}")
        except Exception as e:
            print(f"刪除失敗，錯誤原因：{e}")

def main():
    driver = e_chrome_robot()
    # 縣市列表
    taiwan_cities = [
        #"台北", "新北", "基隆", 
        # "桃園", "新竹", "苗栗",
         "台中", "彰化", "南投", "雲林", 
        #"高雄", "嘉義", #"台南",  "屏東", 
        #"宜蘭", #"花蓮", "台東",
    ]
    # 迴圈爬取每個縣市的露營場
    for city in taiwan_cities:

        query = f"{city} 露營場"
        url = f"https://www.google.com/maps/search/{query}"
        # 儲存露營場連結
        links, query = e_search_all_links(url, driver, query)
        # 建立checkpoint資料夾 / 儲存已存在的露營場名稱
        done_names, checkpoint_path, review_checkpoint_path = e_checkpoint(city)
        # 爬露營場資訊，爬一筆即存進checkpoint
        e_crawl_single_campground(driver, links, done_names, checkpoint_path, review_checkpoint_path, city)


    # 整併所有縣市的checkpoint資料
    e_save_to_final_file(driver)
    # 刪除這次的checpoint
    e_delete_checkpoint()

main()