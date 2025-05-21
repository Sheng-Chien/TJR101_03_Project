# 把直接提取(extract)和AI分析(ai)的結果合併
import os
from pathlib import Path
import json
import re

def replaceItem(input:list, target:list, replacement:str):
    for idx in range(len(input)):
        for el in target:
            if el in input[idx]:
                input[idx] = replacement
    
    return input


def main():
    # 讀取ai分析結果

    # 取得所有已分析檔案
    ai_file_dir = Path(__file__).parent/"results/temp"
    ai_files = [file for file in os.listdir(ai_file_dir) if os.path.isfile(ai_file_dir/file)]
    extract_path = Path(__file__).parent / "results/classfied_extract.json"
    ai_path = Path(__file__).parent / "results/classfied_ai.json"
    save_path = Path(__file__).parent / "results/classfied_all.json"
    # print(ai_files)

    ai_data = dict()
    for file_name in ai_files:
        file_path = ai_file_dir/file_name
        with open(file_path, "r", encoding="utf-8") as f:
            response = json.load(f)
        
        camp_related = response["candidates"][0]["content"]["parts"][0]["text"]
        # 只擷取json檔案部分
        start = camp_related.find("{")
        end = camp_related.rfind("}")
        print(file_name)
        if start != -1 and end != -1 and start < end:
            camp_related = camp_related[start : end+1]
            camp_related = json.loads(camp_related)
            # print(camp_related)
        else:
            print(f"{file_name} 檔案格式錯誤！")
            continue

        # 特殊處理
        # 冰箱條款
        equipmint_list = ["冰", "凍"]
        camp_related["equipment"] = replaceItem(camp_related["equipment"], equipmint_list, "冰箱")
        # 美味條款
        service_list = ["好味"]
        camp_related["special"] = replaceItem(camp_related["special"], service_list, "在地美味")
        # # 寵物條款
        # if "寵物友善" in camp_related["equipment"]:
        #     camp_related["equipment"].remove("寵物友善")
        #     camp_related["special"].append("寵物友善")
        


        
        # 加入營地名稱以供辨識
        ai_data[file_name.split(".")[0]] = camp_related
    
    # 存檔(可有可無，方便查看以及回憶資料結構)
    with open(ai_path, "w", encoding="utf-8") as file:
        json.dump(ai_data, file, indent=2, ensure_ascii=False)

    # 讀取一般擷取結果
    with open(extract_path, "r", encoding="utf-8") as file:
        extract_data = json.load(file)


    data = []
    for camp in extract_data:
        if camp["name"] in ai_data.keys():
            print(camp["name"])
            camp["equipment"] = ai_data[camp["name"]]["equipment"]
            camp["special"] = ai_data[camp["name"]]["special"]
        data.append(camp)

    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
