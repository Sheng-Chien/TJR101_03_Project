# import os
# import sys
# current_dir = os.path.dirname(os.path.abspath(__file__))
# external_lib_path = os.path.join(current_dir, "ai/gimini")
# sys.path.insert(0, external_lib_path)

from ai.gemini.chatWithGemini import ChatWithGemini
from pathlib import Path
from datetime import datetime
import json
import re

def extract_leading_chinese(text):
    match = re.match(r'^[\u4e00-\u9fff]+', text)
    return match.group(0) if match else None


def main():

    file_path = Path(__file__).parent / Path("crawler/icamping/jsons/camps.jsonl")
    save_path = Path(__file__).parent / Path("results/classfied.json")

    final_data=[]
    # 不必用AI, 字串分析部分
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            data = dict()
            camp = json.loads(line)
            # 取得縣市
            data["county"] = camp["info"][-1].split(" ")[-2]
            # 取得名稱
            data["name"] = camp["name"]
            # 取得高度
            data["altitude"] = camp["info"][1].split(" ")[2]

            # 取額營位
            location = list()
            for key, values in camp["services"].items():
                pattern =  r"NT\$\d{1,3}(?:,\d{3})*"
                price = re.search(pattern, values["price"]).group()
                price = price.replace(",", "").replace("NT$", "")
                pattern = r"\d*[\u4e00-\u9fff]+"
                type = re.search(pattern, values["details"]).group()
                location.append(list([key, price, type]))
            # print(location)
            data["location"] = location
            # print(data)
            final_data.append(data)
            # break
    
    # return
    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(final_data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()