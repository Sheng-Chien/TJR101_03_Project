# import os
# import sys
# current_dir = os.path.dirname(os.path.abspath(__file__))
# external_lib_path = os.path.join(current_dir, "ai/gimini")
# sys.path.insert(0, external_lib_path)
import sys
from pathlib import Path
from datetime import datetime
import json
import re

def findParentDirPath(current_path, target_dir):
    current = Path(current_path).resolve()
    while current != current.parent:  # 直到根目錄
        target = current / target_dir
        if target.exists() and target.is_dir():
            return target
        current = current.parent
    return None


def main():

    root_dir = findParentDirPath(Path(__file__),"eta")
    sys.path.insert(0,str(root_dir) )
    file_path = root_dir / Path("crawler/icamping/jsons/camps.jsonl")
    save_path = Path(__file__).parent / Path("results/classfied_extract.json")

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