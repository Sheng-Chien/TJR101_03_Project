# 把地址欄位轉換為經緯度
# 轉換只到鄉鎮市區層級，村|鄰|路可能會失敗

import pandas as pd
from pathlib import Path
import time
from geopy.geocoders import Nominatim
import re

save_path = Path(".venv", "MART", "result_csv")
input_file = Path(save_path / "MART02_campground_add_extra_info.csv")

# 讀取資料
df = pd.read_csv(input_file, encoding="utf-8-sig")

geolocator = Nominatim(user_agent="my_geocoder")

def cut_to_district(address):
    # 地址切到區／鄉／鎮／市，不包含後面的村里鄰...等

    match = re.search(r"^(.*?[縣市].*?[區鄉鎮市])", address)
    if match:
        return "台灣" + match.group(1)
    else:
        # 若格式無法辨識，就直接加上台灣
        return "台灣" + address

# 套用轉換
df["清洗後地址"] = df["address"].apply(cut_to_district)

# 準備儲存經緯度
latitudes = []
longitudes = []

for i, row in df["清洗後地址"].items():
    try:
        location = geolocator.geocode(row, language="zh")
        time.sleep(2)  # 防止 Nominatim 封鎖
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            print(f"{row}轉換完成")
        else:
            latitudes.append(None)
            longitudes.append(None)
            #print(f"{row} 找不到地址")
    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)
        print(f"{row} 查詢錯誤：{e}")

# 存入欄位
df["lat"] = latitudes
df["lng"] = longitudes

input_file = Path(r"C:\TJR101_03_Project\.venv\MART\01\address_change_to_latitude.csv")
df = pd.read_csv(input_file, encoding="utf-8-sig")

# 建立鄉鎮名稱關鍵字對應經緯度的字典
custom_latlng = {
    "五峰鄉": (24.574493, 121.087514),
    "三灣鄉": (24.651154, 120.953763),
    "三星鄉": (24.654330, 121.633110),
    "礁溪鄉": (24.826252, 121.770303),
    "光復鄉": (23.646172, 121.414598),
    "吉安鄉": (23.965529, 121.598162),
    "新城鄉": (24.019738, 121.613146),
    "玉里鎮": (23.336213, 121.311648),
    "富里鄉": (23.194803, 121.296640),
    "大湖鄉": (24.418218, 120.865382),
    "鹿野鄉": (22.912472, 121.136972),
    }

# 遍歷每筆地址
for i, addr in df["清洗後地址"].items():
    found = False
    for keyword, (lat, lng) in custom_latlng.items():
        if keyword in addr:
            df.at[i, "lat"] = lat
            df.at[i, "lng"] = lng
            found = True
            break  # 找到就跳出
    if not found:
        continue


# 存檔-----------------------------------
save_file = save_path / "MART03_address_change_to_latitude.csv"
df.to_csv(save_file, encoding="utf-8-sig", index=False)

print("OK")
