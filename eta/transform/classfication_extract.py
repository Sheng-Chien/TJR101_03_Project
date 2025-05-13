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
import pandas as pd


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

    peek = []
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
                # 擷取價格
                pattern =  r"NT\$\d{1,3}(?:,\d{3})*"
                price = re.search(pattern, values["price"]).group()
                price = price.replace(",", "").replace("NT$", "")

                # 擷取營位名稱
                # pattern = r"\d*[\u4e00-\u9fff]+"
                # type = re.search(pattern, values["details"]).group()


                # 擷取並清洗營位資訊
                site_type = values["details"]
                pattern = r"(?:(\d)人[\u4e00-\u9fff]+|[\u4e00-\u9fff]+)"
                type = re.search(pattern, site_type).group()
                # 處理特殊狀況

                # 斑比跳跳特別條款
                black_list = ["加購", "每組"]
                white_list = ["每區", "每帳", "每車", "每人"]
                check = False
                for item in white_list:
                    if item in values["price"]+key:
                        check = True
                        break
                # 如果 不在 白名單 中，則跳過資料
                if not check:
                    continue
        
                check = False
                for item in black_list:
                    if item in values["price"]+key:
                        check = True
                        break
                # 如果 在 黑名單 中，則跳過資料
                if check:
                    continue

                # 有些營區會有多餘贅詞，多抓一次
                if len(type) == 1 or len(type)>9:
                    site_type = site_type.replace(type, " ")
                type = re.search(pattern, site_type).group()
                # 真的太奇怪直接以 key 為 type
                if len(type) == 1:
                    type = key
                type = re.search(pattern, site_type).group()

                # 刪除特別字元
                delete_list = ["米", "限", "共"]
                for item in delete_list:
                    type = type.replace(item, "")

                # 露營車直接以key為type
                special_list = ["每車", "Ｆ炊事"]
                content = values["price"] + values["details"] + key
                for item in special_list:
                    if item in content:
                        type = key
                # 雲享清峰,單面露營掛牌
                # 眺浪營地,預訂營位請電話聯絡營主
                # 美富安露營區,F炊事
                # 田心小營地,草地區可搭



                location.append(list([key, price, type]))
                peek.append([camp["name"], type])
            # print(location)
            data["location"] = location
            # print(data)
            final_data.append(data)
            # break
    
    # return
    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(final_data, file, ensure_ascii=False, indent=2)


    df = pd.DataFrame(data = peek, columns=["camp", "type"])
    df.to_csv(Path(__file__).parent/"results/text_type.csv", encoding="utf-8")

if __name__ == "__main__":
    main()