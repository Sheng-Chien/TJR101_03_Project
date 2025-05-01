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
import os

# 需要用到AI的部分
def main():
    key_path = Path(__file__).parent /Path("ai/gemini/KEY/AI_Project_User.json")
    file_path = Path(__file__).parent / Path("crawler/icamping/jsons/camps.jsonl")
    save_dir = Path(__file__).parent / Path("results")
    temp_dir = save_dir/"temp"
    # 取得已經處理過的檔名
    files = [f.split(".")[0] for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]

    data=[]
    element=dict()

    i=0 # 計數器
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            i += 1
            # 每個營區都是一行
            camp = json.loads(line)

            # checkpoint, 如果檔案已存在則跳過, 執行下一個營區執行下一個營區
            if camp["name"] in files:
                pass
                # continue

            # 取出所有設備並清理空白節省token
            related = [ item.strip() for item in camp["related"]]
            # print(related)
            element[camp["name"]] = related
            # print(element)
            
            # 疊加一定量的營區後當作一筆資料送出
            if i % 5 == 0:
                data.append(element)
                element=dict()
        
        # 沒有整數倍數的也要加進去
        data.append(element)




    # 召喚AI小幫手
    ai = ChatWithGemini(
        key_path=key_path, # 填入金鑰json檔的路徑(選填))
        max_tonkens=500,
        temperature=0.5,
        top_k=40,
        top_p=0.9,
    )

    # 載入命令提詞
    prompt_path = Path(__file__).parent/"prompt.txt"
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read()

    for element in data:
        response = ""
        response = ai.chat(prompt+str(element)) # 取得AI回應(分類)
        # 以現在時間戳記為檔案名稱
        now = datetime.now()
        formated_time = now.strftime("%Y_%m%d_%H%M_%S")+f"{int(now.microsecond/10000)}"
        print(formated_time)
        # 創建資料夾並指定檔案名稱
        json_dir = save_dir / "temp_ai"
        json_dir.mkdir(exist_ok=True, parents=True)
        json_path = json_dir / f"{formated_time}.json"
        # 存檔
        with open( json_path, "w", encoding="utf-8") as f:
            json.dump(response, f, indent=2, ensure_ascii=False)
            print("回應寫入成功！")
        break


if __name__ == "__main__":
    main()