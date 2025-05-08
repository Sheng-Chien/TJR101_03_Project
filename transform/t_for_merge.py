import json
import csv
import re

#讀取檔案
with open("easycamp_info.json", "r", encoding="utf-8") as file:
    data = json.load(file)

#存成csv
with open("yh_campground_change_address.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Campsite", "Address"])
    #not_ok_address =[]
    for item in data:      
        # 清理營地名稱（去除地名和括號內的內容）
        full_name = item["營地資訊"]["營地名稱"]
        match = re.match(r"([^\s]+)([^\(]+)", full_name)
        if match:
            campsite_name = match.group(2).strip()  
        else:
            campsite_name = full_name  
        #清理地址
        address = item["營地地址"]
        pattern = r"([\u4e00-\u9fa5]{2,}(縣|市)[\u4e00-\u9fa5]{1,}(鄉|鎮|市|區|村)(?:[\u4e00-\u9fa5-\d]{0,}(?:段|路|巷|弄|號))*)"
        result = re.search(pattern, address)
        if result:
            campsite_address = result.group(0)
        else:
            campsite_address = match.group(1)
            #not_ok_address.append(address)
            #print(campsite_name,"❌ 無法清理的地址:", address)

        #print(f"原名稱: {address} -> 提取名稱: {campsite_address}")
        writer.writerow(["YH", campsite_name, campsite_address])  
    print("✅ 已成功建立csv")

# 待處理
# 台南左鎮 露營樂1號店(狩獵帳)左鎮旗艦店
# 新竹尖石 露營樂3號店(狩獵帳)臻美館
# 南投中寮賞星月慕 露營樂6號店(狩獵帳)
# 宜蘭大同 露營樂7號店(狩獵帳)圓頂館
# 嘉義番路 露營樂9號店(狩獵帳)阿里山草堂


# 溪遊記露營區 ❌ 無法清理的地址: 導航至嘉興國小義興分校後關導航，再依路邊標示前來 (竹59過5.5K後繼續走300m，右邊岔路走到底)，如下圖
# 景色天地露營區 ❌ 無法清理的地址: 從內灣老街導航至營區，沿途有指標(天湖方向道路封閉)
# 明園星空營地 ❌ 無法清理的地址: 新埔鎮鹿鳴里黃梨園52-20號(請導航座標：24.856448,121.135753)
# 夢之谷露營區 ❌ 無法清理的地址: Google Map搜尋夢之谷露營區，依沿路指標即可抵達；其他導航方式如下方圖示
# 朵悠露營區 ❌ 無法清理的地址: Google Map輸入：朵悠露營區入口。入口處依營區指標向上，即可抵達。(如下方圖示)
# 點將家免裝備露營生態園區 ❌ 無法清理的地址: 投縣國姓鄉中寮鄉
# 幸福城景觀露營區 ❌ 無法清理的地址: 宜蘭大同鄉泰雅路二段29巷58-6號(過茶之鄉民宿，往前約20公尺岔路處(台七線98.3公里處)往右走上山)     
# 一零八零1080 ❌ 無法清理的地址: google map直接搜尋 「一零八零1080」即可到達
# 8