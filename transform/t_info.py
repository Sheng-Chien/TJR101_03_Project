import json
import re

#讀取檔案
with open("easycamp_info.json", "r", encoding="utf-8") as file:
    data = json.load(file)

#清理營地名稱（去除地名和括號內的內容）
def clean_name(data):
    for item in data:      
        name = item["營地資訊"]["營地名稱"]
        #把「前面那段非空白字」和「括號前的其他資訊」分開
        match = re.match(r"([^\s]+)([^\(]+)", name)
        if match:
            cleaned_name = match.group(2).strip() #成功比對，就用 group(2) 的內容當營地名稱
            item["營地資訊"]["營地名稱"] = cleaned_name


#清理地址
def clean_address(data):
    for item in data: 
        address = item["營地地址"]
        name = item["營地資訊"]["營地名稱"]
        match = re.match(r"([^\s]+)([^\(]+)", name)
        
        pattern = r"([\u4e00-\u9fa5]{2,}(縣|市)[\u4e00-\u9fa5]{1,}(鄉|鎮|市|區|村)(?:[\u4e00-\u9fa5-\d]{0,}(?:段|路|巷|弄|號))*)"
        result = re.search(pattern, address)
        if result:
            item["營地地址"] = result.group(0)
        elif match:
            item["營地地址"] = match.group(1)#營地名稱的前段部分作為無實際地址時的替代
    
#清理海拔
def clean_altitude(data):
    for item in data:
        altitude = item["營區介紹"].get("海拔", None)  # 使用 .get() 避免 KeyError
        if not altitude:
            item["營區介紹"]["海拔"] = None 
        elif '以下' in altitude:
            item["營區介紹"]["海拔"] = 150
        elif '301-500m' in altitude:
            item["營區介紹"]["海拔"] = 400
        elif '501-800m' in altitude:
            item["營區介紹"]["海拔"] = 650
        elif '801-1000m' in altitude:
            item["營區介紹"]["海拔"] = 900
        elif '1001-1500m' in altitude:
            item["營區介紹"]["海拔"] = 1250
        elif '1501m以上' in altitude:
            item["營區介紹"]["海拔"] = 1700

clean_name(data)
clean_address(data)
clean_altitude(data)

with open("easycamp_info_cleaned.json", "w", encoding="utf-8") as f :
    json.dump(data, f, ensure_ascii=False, indent=2)