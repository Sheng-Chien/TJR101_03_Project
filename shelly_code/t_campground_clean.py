# clean campground name and address

from pathlib import Path
import pandas as pd
import re

def clean_campground_name(series: pd.Series):
    """
    處理google map爬下來的露營場名稱
    """
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

    for _, row in series.items():
        if pd.isna(row):
            name_list.append("")
            continue
            
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

    return pd.Series(name_list)


def clean_address(series: pd.Series):
    """
    處理google map的地址
    """
    cleaned_address = []
    for _, row in series.items():
        # 清除開頭郵遞區號
        row = re.sub(r"^\d{3,6}\s*", "", str(row)).replace(" ", "")

        # 清除其他雜字
        row = row.replace("、", "").replace("No.", "").replace("No", "").replace("TW", "").replace("。", "")

        # 先抓出最後的地址號碼
        match_house_number = re.search(r"\d{1,3}(-\d{1,3})?(\d{1,3})?(號|之\d+)號", row)
        house_number = ""
        if match_house_number:
            house_number = match_house_number.group()
            row = re.sub(re.escape(house_number), "", row)

        # 清除座標
        row = re.sub(r"\d{2,3}(?:\.\d+)+", "", row) #小數點座標
        row = re.sub(r"\d{1,3}°\d{1,3}'\d{0,3}(\.\d+)?[NSEW]?", "", row)  # 度分秒座標
        row = re.sub(r"\d{1,3}°\d{1,3}'(\.\d+)?[NSEW]?", "", row)        # 度分座標
        row = re.sub(r"\d+[°\'\"″]{1,2}[NSEW]", "", row)
        row = row.replace("°", "") # 清除可能漏掉的°

        # 清理地址尾巴的郵遞區號
        row = re.sub(r"\d{1,6}$", "", str(row)).strip()
        
        # 清除縣市區後面接郵遞區號
        row = re.sub(r"([區鄉鎮])\d{3,5}", r"\1", row)

        # 寫回格式正常的地址
        if len(row) <= 2 or (row[2] in ["縣", "市", "鄉"]):
            # 加回門牌
            if house_number and house_number not in row:
                row += house_number
            cleaned_address.append(row)
            continue 

        # 開始清理地址倒反放的狀況
        keywords = ["縣", "市", "區", "段", "鄉", "鎮", "鄰", "鄉道", "路", "巷", "街", "號", "樓", "UnnamedRd", "UnnamedRoad", "BaishiChi", "村民石"]

        address_clean = row
        for key in keywords:
            address_clean = re.sub(f"({key})", r"\1 ", address_clean)

        address_parts = address_clean.split()
        t_address = " ".join(address_parts[::-1]).replace(" ", "")

        # 反轉完成後，再檢查「號 + 路街巷」是否顛倒 → 修正
        t_address = re.sub(r"(\d{1,4})([^\d之號]{1,5}[路街巷])", r"\2\1號", t_address)

        # 加回門牌
        if house_number and house_number not in t_address:
            t_address += house_number
        
        cleaned_address.append(t_address)

    return pd.Series(cleaned_address)

def main():
    filepath = Path("C:\TJR101_03_Project\.venv\project\shelly_merge.csv")
    df = pd.read_csv(filepath, encoding="utf-8")

    # 處理特定的露營場名稱
    df.loc[df["Campsite"].isna(), "Campsite"] = "《綠野雲仙》 露營區"
    
    df["Campsite"] = clean_campground_name(df["Campsite"])
    df["Address"] = clean_address(df["Address"])
    dir_path = Path(".venv", "project")
    dir_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(dir_path / "merge_v3.csv", index=False)

    # test_address = pd.Series(["233新北市烏來區西羅岸路132之5號"])
    # result = clean_address(test_address)
    # print(result)

main()
