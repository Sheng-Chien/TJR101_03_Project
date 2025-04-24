from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import csv
from pathlib import Path



class CrawlCamp():
    
    def __init__(self):
        # self.startDriver()
        self.driverStatus = False
        # 網址
        self.root_url = "https://m.icamping.app/"
        # 存檔路徑
        self.root = ""
        self.dir_html =  self.root + "htmls/"
        self.dir_csv =  self.root + "csvs/"
        self.dir_camp =  "camps/"
        self.dir_json =  self.root + "jsons/"
        self.file_search_html =  "search_result.html"
        self.file_search_csv =  "search_result.csv"
        # log
        self.error_log = []
    
    def __del__(self):
        if len(self.error_log) == 0:
            return
        print("❌❌❌有錯誤請檢視LOG❌❌❌")
        with open("ErrorLog.txt", mode="w", encoding="utf-8") as file:
            for line in self.error_log:
                file.write(line + "\n")

    def startDriver(self):
        # 設定 chromedriver 路徑（如果已經加入環境變數，可以不寫）
        chromedriver_path = "chromedriver.exe"
        service = Service(chromedriver_path)

        # 設定 Chrome 選項
        options = Options()
        # options.add_argument("--start-maximized")  # 初始最大化，稍後再縮放調整

        # 啟動瀏覽器
        self.driver = webdriver.Chrome(options=options, service=service)

        # # =========================
        # # 設定螢幕大小，非必要
        # # 取得螢幕寬高
        # try:
        #     from screeninfo import get_monitors
        #     screen = get_monitors()[0]  # 取得主螢幕
        #     screen_width = screen.width
        #     screen_height = screen.height
        #     # print("取得螢幕資訊")
        #     # print(f"{screen_height}x{screen_width}")
        # except ImportError:
        #     # 若無 screeninfo 模組，使用預設值
        #     screen_width = 1920
        #     screen_height = 1080

        # # 將視窗移動到左側（左上角），寬度為螢幕一半，高度全高
        # left = 0
        # top = 0
        # width = screen_width / 3
        # height = screen_height

        # # 設定視窗位置與大小
        # self.driver.set_window_position(left, top)
        # self.driver.set_window_size(width, height)
        # # =========================================
        print("啟動完成！")

    def loadData(self, file_path):
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print("❌ 檔案不存在")
        except PermissionError:
            print("❌ 沒有權限讀取檔案")
        except Exception as e:
            print(f"❌ 發生未知錯誤：{e}")
        # 開啟錯誤回傳None
        return None
        
    def getPage(self, url):
        if not self.driverStatus:
            self.startDriver()
        self.driver.get(url)
        time.sleep(2)
        
        try:
            element = self.driver.find_element(By.CLASS_NAME, "mat-progress-bar-secondary")
            print("網頁加載中，請稍候...")
            # 等待該元素消失（最多等 20 秒）
            WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element(element)
            )
            print("網頁加載完成")

        except NoSuchElementException:
            print("這就加載完了？這麼神速？")

        except TimeoutException:
            print("等太久了！我要上啦！")

        except Exception as e:
            print(f"其他加載錯誤：{e}")
            return
    
    def searchPage(self):
        # 愛露營的搜尋頁面，已包含所有營區
        search_url = self.root_url + "store/search-result"
        self.getPage(search_url)
        file_path = self.dir_html + self.file_search_html
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(self.driver.page_source)
            print("✅ 搜尋結果儲存完畢！")

    
    def parseSearch(self):
        file_path = self.dir_html + self.file_search_html
        soup = None
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                soup = BeautifulSoup(file.read(), "html.parser")
        except FileNotFoundError:
            print("❌ 檔案不存在")
        except PermissionError:
            print("❌ 沒有權限讀取檔案")
        except Exception as e:
            print(f"❌ 發生未知錯誤：{e}")
        
        if soup is None:
            print("無法處理檔案")
            return
        
        camps = soup.select("div.row.smallhero")
        data=[]
        title = ["縣市", "行政區", "海拔", "露營地", "網址"]
        data.append(title)

        for camp in camps:
            name = camp.select_one("div.row6 > div.row > a").text.strip()
            url = camp.select_one("div.row6 > div.row > a").get("href")
            location = camp.select_one("div.f13.i-green").text.strip()
            location = location.replace(" ","").split("・")
            location.append(name)
            location.append(url)
            # print(location)
            data.append(location)
            

        # 寫入 CSV 檔案
        file_path = self.dir_html + self.file_search_csv
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)  # 一次寫入多列
            print("✅ 寫入完成")

    def getCampHTML(self):
        root_url = self.root_url
        file_path = self.dir_csv + self.file_search_csv
        
        camp_list = pd.read_csv(
            file_path,
            engine="python",
            encoding="utf-8",
            header=0
        )
        # print(camp_list)

        # 提出網址欄並檢查內容是否正確
        col_name_url = camp_list.columns[-1]
        camp_url = camp_list.loc[0,col_name_url]
        cheack = re.fullmatch(r"[0-9a-zA-Z/]+", camp_url)
        if not cheack:
            print(f"{camp_url}似乎不合格式，請檢查內容")
            return
        

        for index in range(len(camp_list)):
            camp_url = root_url + camp_list.loc[index, col_name_url]
            camp_name = camp_list.iloc[index, -2]
            camp_location = camp_list.iloc[index, 0]
            camp_PK = camp_url.split("/")[-1]
            # print(camp_name, camp_url)

            self.getPage(camp_url)
            # print(self.driver.page_source)
            file_name = camp_location + "_" + camp_PK + "_" + camp_name + ".html"
            file_path = self.dir_html + self.dir_camp + file_name
            with open(file_path, mode="w", encoding="utf-8") as file:
                file.write(self.driver.page_source)
                print(f"{index}: -{camp_name}- ✅ 寫入成功！")            
            
            time.sleep(1)
            # i+=1
            # if i > 3 :
            # break
    
    # 精準定位tag的selector
    def get_full_selector(self, tag):
        path = []
        while tag is not None and tag.name != '[document]':
            selector = tag.name
            if tag.get('id'):
                selector += f"#{tag['id']}"
            if tag.get('class'):
                selector += ''.join(f".{cls}" for cls in tag['class'])
            siblings = tag.find_previous_siblings(tag.name)
            if siblings:
                selector += f":nth-of-type({len(siblings)+1})"
            path.insert(0, selector)
            tag = tag.parent

        return ' > '.join(path)



    # 以其一HTML為範例，提取標籤再套用其他HTML分析
    def parseTags(self):
        # 範例檔案路徑
        file_sample = self.dir_html + "sample_camp.html"
        with open(file_sample, "r", encoding="utf-8") as file:
            content = file.read()
        tags = {}
        soup = BeautifulSoup(content, "html.parser")

        # 營地名稱
        camp_name = "斑比跳跳 頂級豪華露營訂位"
        tag_camp_name = soup.find_all(string=camp_name)[-1]
        # print(tag_camp_name.parent.text)
        tags["name"] = self.get_full_selector(tag_camp_name.parent)

        camp_address = " 苗栗縣三灣鄉北埔村小北埔27號 "
        tag_camp_address = soup.find(string=camp_address)
        tag_camp_info = tag_camp_address.find_parent("div")#.find_all(recursive=False)
        tags["info"] = self.get_full_selector(tag_camp_info)


        # 提取營區介紹
        about_camp = "關於營區"
        tag_about_camp = soup.find_all(string=about_camp)[-1].find_parent("div").find_next_sibling("p")
        # print(tag_about_camp)
        tags["about"] = self.get_full_selector(tag_about_camp)
        
        # 提取相關設施
        related_facilities = "相關設施"
        tag_related = soup.find_all(string=related_facilities)[-1].find_parent("div").find_next_sibling("div")
        # print(tag_related)
        tags["related"] = self.get_full_selector(tag_related)

        # 提取營地須知
        readme = "請至指定區域吸菸，"
        tag_readme = soup.find_all(string=readme)[-1].find_parent("div")
        # print(tag_readme)
        tags["readme"] = self.get_full_selector(tag_readme)

        # 提取區域數量(表格)
        locations = " 營地名稱 "
        tag_locations = soup.find_all(string=locations)[-1].find_parent("table")
        # print(tag_locations)
        tags["locations"] = self.get_full_selector(tag_locations)

        # 提取服務項目
        # services = "A區湖畔豪華露營車"
        # tag_services = soup.select_one("app-stuff")
        # tags["services"] = self.get_full_selector(tag_services)
        
        # 因為有唯一標籤 app-stuff，所以不做字串反查
        tags["services"] = "app-stuff"

        return tags

    def dumpJson(self, file_path_json, data):
            if data: 
                with open(file_path_json, mode="a", encoding="utf-8") as file:
                    for d in data:
                        json.dump(d, file, ensure_ascii=False, indent=4)
        
    def parseCampHTML(self, file_name)->dict:

        # print("開始解析營地內容")
        # 暫存HTML檔路徑
        dir_path = self.dir_html + self.dir_camp
        # 取得所有檔案名稱
        # 解析Sample.mtml提取標籤
        tags = self.tags


        file_path = dir_path + file_name
        content = None
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                print(f"✅ {file_name} 讀取成功！")
        except:
            print(f"❌ {file_name} 讀取失敗！")
            self.error_log.append(f"{file_name} 讀取失敗\n")
        
        if content is None:
            return

        soup = BeautifulSoup(content, "html.parser")

        data = dict()
        # 提取營地名稱
        camp_name = soup.select_one(tags["name"])
        # print(camp_name.text)
        data["name"] = camp_name.get_text()

        # 提取營區資訊
        camp_info = soup.select_one(tags["info"])
        # for el in camp_info.find_all(recursive=False):
        #     print(el.text)
        data["info"] = [el.get_text() for el in camp_info.find_all(recursive=False)]
        
        # 提取營區介紹
        camp_about = soup.select_one(tags["about"])
        # for el in camp_about.select("p"):
        #     print(el.get_text(separator="\n"))
        data["about"] = [el.get_text(separator="\n") for el in camp_about.select("p")]
        
        # 提取相關設施
        camp_related = soup.select_one(tags["related"])
        # for el in camp_related.select("div.facilitielabel"):
        #     print(el.get_text())
        data["related"] = [el.get_text() for el in camp_related.select("div.facilitielabel")]

        # 提取營地須知
        camp_readme = soup.select_one(tags["readme"])
        # for el in camp_readme.select("p"):
        #     print(el.get_text(separator="\n"))
        data["readme"] = [el.get_text(separator="\n") for el in camp_readme.select("p")]
        
        # 提取區域數量(表格)
        camp_locations = soup.select_one(tags["locations"])
        locations = {"locations":"total_count"}
        # 跳過標題，直接擷取表格內容
        for t in camp_locations.select("tbody > tr"):
            key = t.select_one("th").text
            value = t.select_one("td").text
            # print(key,value)
            locations[key] = value
        # print(locations)
        data["locations"] = locations

        # 提取服務項目
        camp_services = soup.select_one(tags["services"])
        services = camp_services.select("mdb-card-body")
        serv = dict()
        for card in services:
            # 找到最底層的div標籤
            divs = [div for div in card.find_all("div") if not div.find("div")]
            # for div in divs:
            #     print(div.get_text(separator="\n"))
            if len(divs) == 3:
                serv[divs[0].get_text()] = {
                    "price" : divs[1].get_text()
                    , "details" : divs[2].get_text()
                }
        if serv:
            data["services"] = serv
        else:
            self.error_log.append("服務卡片錯誤，可能格式有改?")
        # print(data)
        return data


    def campJson(self):
        print("開始解析營地內容")
        # 暫存HTML檔路徑
        dir_path = self.dir_html + self.dir_camp
        # 取得所有檔案名稱
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        # 解析Sample.mtml提取標籤
        self.tags = self.parseTags()

        file_path_json = self.dir_json + "camps.json"
        with open(file_path_json, mode="w", encoding="utf-8") as file:
            pass
        
        
        data = []
        for index in range(len(files)):
            # if index == 40:
            #     break
            data.append(self.parseCampHTML(files[index]))
            if index % 20 == 0:
                self.dumpJson(file_path_json, data)
                data = []
        
        self.dumpJson(file_path_json, data)


def main():
    crawler = CrawlCamp()
    # crawler.searchPage()
    # crawler.parseSearch()
    # crawler.getCampHTML()
    # 解析標籤
    # crawler.parseTags()
    # 解析HTML
    crawler.campJson()
    

if __name__ == "__main__":
    main()