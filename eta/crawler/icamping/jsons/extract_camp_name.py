import json
from pathlib import Path
import re

def has_full_taiwan_address_part(text):
    has_county_or_city = any(kw in text for kw in ["縣", "市"])
    has_township = any(kw in text for kw in ["鄉", "鎮", "區"])
    return has_county_or_city and has_township

def truncat_address(text):
    # pattern = r"[\u4e00-\u9fa5]{2,}(縣|市)[\u4e00-\u9fa5]{1,}(鄉|鎮|市|區)[\u4e00-\u9fa50-9-號路巷弄段]*"
    # pattern = r"[\u4e00-\u9fa5]{2,}(縣|市)[\u4e00-\u9fa5]{1,}(鄉|鎮|市|區).*[號路巷弄段]?$"
    pattern = r"([\u4e00-\u9fa5]{2,}(縣|市)[\u4e00-\u9fa5]{1,}(鄉|鎮|市|區|村)(?:[\u4e00-\u9fa5-\d]{0,}(?:段|路|巷|弄|號))*)"
    result = re.search(pattern, text)
    if result:
        return result.group(0)
    return ""

file_path = Path(__file__).parent / "camps.jsonl"
save_path = Path(__file__).parent / "camps_mapping.csv"
new_data=["Name,Campsite,Address"]
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)
        address = data["info"][0]
        address = truncat_address(address)
        # 如果地址不完整, 以地區取代
        if not has_full_taiwan_address_part(address):
            address = "".join(data["info"][-1].split(" ")[-2:])
        string ="Eta," + data["name"] + "," + address
        new_data.append(string)
        # break

with open(save_path, "w", encoding="utf-8") as file:
    for line in new_data:
        file.write(line+"\n")