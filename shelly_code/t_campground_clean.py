# clean campground name and address

from pathlib import Path
import pandas as pd
import re

filepath = Path("C:\TJR101_03_Project\.venv\project\shelly_merge.csv")
df = pd.read_csv(filepath, encoding="utf-8")

# 處理特定的露營場名稱
df.loc[df["Campsite"].isna(), "Campsite"] = "《綠野雲仙》 露營區"

# 用正規表達式合併為一個 pattern
split_symbols = [
    r"｜", r"\|",   # 全形與半形的直線
    r"－", r"-",   # 全形與半形的 dash
    r"／", r"/",   # 全形與半形的 slash
    r"、", r"‧",   # 中文列點符號
    r"》", r"》",   # 全形右雙括號
    r"】", r"\]",  # 全形右方括號
    r"（",  # 括號
    r"」", r"「", 
    r"《", r"：",
]
pattern = r"|".join(split_symbols)

name_list = []

for _, row in df["Campsite"].items():
    row_str = str(row)
    matches = list(re.finditer(pattern, row_str))
    sharp_matches = list(re.finditer(r"#", row_str))

    if pd.isna(row):
        name_list.append("")
        continue

    # 檢查是否有兩個以上的"#""   
    elif len(sharp_matches) >= 2:
        second_sharp = sharp_matches[1]
        name_list.append(row_str[:second_sharp.start()].strip())

    elif matches:
        match = matches[0]
        # 特殊符號的起始位置>=3才切，避開少數12號露營地等狀況
        if match.start() >= 3:
            name_list.append(row_str[:match.start()].strip())
        else:
            name_list.append(row_str.strip().replace("「", ""))
    else:
        name_list.append(row_str.strip())

df["Campsite"] = name_list

# 處理地址
cleaned_address = []
for _, row in df["Address"].items():
    # 清除開頭郵遞區號
    row = re.sub(r"^\d{3,6}\s*", "", str(row)).replace(" ", "")

    # 清除其他雜字
    row = row.replace("、", "").replace("No.", "").replace("No", "").replace("TW", "")
    
    # 清除座標
    row = re.sub(r"\d{2,3}(?:\.\d+)+", "", row) #小數點座標
    row = re.sub(r"\d{1,3}°\d{1,3}'\d{0,3}(\.\d+)?[NSEW]?", "", row)  # 度分秒座標
    row = re.sub(r"\d{1,3}°\d{1,3}'(\.\d+)?[NSEW]?", "", row)        # 度分座標
    row = re.sub(r"\d+[°\'\"″]{1,2}[NSEW]", "", row)
    row = row.replace("°", "") # 清除可能不會清掉的°

    # 清理地址尾巴的郵遞區號
    row = re.sub(r"\d{1,6}$", "", str(row)).strip()

    # 清除縣市區後面接郵遞區號
    row = re.sub(r"([區鄉鎮])\d{3,5}", r"\1", row)

    if len(row) <= 2 or (len(row) >= 3 and row[2] in ["縣", "市", "鄉"]):
        cleaned_address.append(row)
        continue 

    # 開始清理地址倒反放的狀況
    keywords = ["縣", "市", "區", "段", "鄉", "鎮", "鄰", "鄉道", "路", "巷", "街", "號", "UnnamedRd", "UnnamedRoad", "BaishiChi", "村民石"]

    # 特殊處理：數字放在xx路街巷鄉道前 → 轉為 xx路街巷鄉道 + 數字 + 號
    row = re.sub(r"(\d+)([^\d\s]{1,10}[路街巷鄉道])", r"\2\1號", row)

    # 抓出門牌號碼（放最後用）
    match_house_number = re.search(r"\d+(-\d+)?(號|之\d+)", row)
    house_number = ""
    if match_house_number:
        house_number = match_house_number.group()
        row = re.sub(re.escape(house_number), "", row)

    address_clean = row
    for key in keywords:
        address_clean = re.sub(f"({key})", r"\1 ", address_clean)

    address_parts = address_clean.split()
    t_address = " ".join(address_parts[::-1]).replace(" ", "")

    # 加回門牌
    if house_number and house_number not in t_address:
        t_address += house_number

    print(t_address)
    cleaned_address.append(t_address)

df["Address"] = cleaned_address

df.to_csv("merge_v2", index=False)
