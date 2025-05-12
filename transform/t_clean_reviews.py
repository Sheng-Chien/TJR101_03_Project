import pandas as pd
import json
import re

with open("easycamp_reviews.json", "r", encoding="utf-8") as file:
    data = json.load(file)

#營地名稱也要清洗
def clean_name(data):
    for item in data:      
        name = item["營地名稱"]
        #把「前面那段非空白字」和「括號前的其他資訊」分開
        match = re.match(r"([^\s]+)([^\(]+)", name)
        if match:
            cleaned_name = match.group(2).strip() #成功比對，就用 group(2) 的內容當營地名稱
            item["營地名稱"] = cleaned_name

clean_name(data)


with open("easycamp_reviews_cleaned.json", "w", encoding="utf-8") as f :
    json.dump(data, f, ensure_ascii=False, indent=2)