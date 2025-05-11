import os
import sys


from pathlib import Path
from datetime import datetime
import json
import os
import time

def findParentDirPath(current_path, target_dir):
    current = Path(current_path).resolve()
    while current != current.parent:  # 直到根目錄
        target = current / target_dir
        if target.exists() and target.is_dir():
            return target
        current = current.parent
    return None

# 需要用到AI的部分
def main():
    # 加入lib路徑到環境變數
    root_dir = findParentDirPath(Path(__file__),"eta")
    sys.path.insert(0,str(root_dir) )
    from ai.gemini.chatWithGemini import ChatWithGemini

    
    key_path = root_dir / Path("ai/gemini/KEY/AI_Project_User.json")
    file_path = root_dir / Path("crawler/icamping/jsons/camps.jsonl")
    save_dir = Path(__file__).parent / Path("results")
    # key_path = Path(__file__).parent /Path("ai/gemini/KEY/AI_Project_User.json")
    # file_path = Path(__file__).parent / Path("crawler/icamping/jsons/camps.jsonl")
    # save_dir = Path(__file__).parent / Path("results")
    temp_dir = save_dir/"temp"
    # 取得已經處理過的檔名
    files = [f.split(".")[0] for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
    # 召喚AI小幫手
    ai = ChatWithGemini(
        key_path=key_path, # 填入金鑰json檔的路徑(選填))
        max_tonkens=500,
        temperature=0.5,
        top_k=40,
        top_p=0.9,
    )

    i=0 # 計數器
    j=0
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            i += 1
            
            # # 測試用，跳著選，不要每次都選一樣的
            # if i % 3 !=0:
            #     continue
            # else:
            #     j += 1

            # 測試用，只執行幾次
            # if i == 100:
            #     break


            # 每個營區都是一行
            camp = json.loads(line)

            # checkpoint, 如果檔案已存在則跳過, 執行下一個營區執行下一個營區
            if camp["name"] in files:
                pass # 如果不重複執行已有的檔案，取消continue的註解
                continue
            time.sleep(0.5)

            # 取出所有設備並清理空白節省token
            related= dict()
            related["設備名稱"] = [ item.strip() for item in camp["related"]]
            # print(related)
            
            # 載入命令提詞
            prompt_path = Path(__file__).parent/"prompt.txt"
            with open(prompt_path, "r", encoding="utf-8") as file:
                prompt = file.read()

            response = ""
            response = ai.chat(prompt+str(related)) # 取得AI回應(分類)

            # 存檔路徑
            json_dir = save_dir / "temp"
            json_dir.mkdir(exist_ok=True, parents=True)
            json_path = json_dir / f"{camp["name"]}.json"
            # 存檔
            with open( json_path, "w", encoding="utf-8") as f:
                json.dump(response, f, indent=2, ensure_ascii=False)
                print(f"{camp["name"]} 回應寫入成功！")


if __name__ == "__main__":
    main()