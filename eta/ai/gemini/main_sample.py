from chatWithGemini import ChatWithGemini
from datetime import datetime 
from pathlib import Path
import json

key_path = Path(__file__).parent/"KEY/AI_Project_Admin.json"
# 初始化物件
ask_gemini = ChatWithGemini(
    key_path=key_path, # 填入金鑰json檔的路徑(選填))
    max_tonkens=500,
    temperature=0.5,
    top_k=40,
    top_p=0.9,
)
# 參數都可以用ChatWithGemini.element事後設定
# 但是設置金鑰請用函式方法
# ask_gemini.setKey(key_path)

# 設定傳送訊息
prompt = "請用100個字說個小故事"
# 取得回應
response = ""
response = ask_gemini.chat(prompt)



# ================以下是存檔方式====================
# 以現在時間戳記為檔案名稱
now = datetime.now()
formated_time = now.strftime("%Y_%m%d_%H%M_%S")+f"{int(now.microsecond/10000)}"
print(formated_time)
# 創建資料夾並指定檔案名稱
json_dir = Path(__file__).parent / "results"
json_dir.mkdir(exist_ok=True, parents=True)
json_path = json_dir / f"{formated_time}.json"
# 存檔
with open( json_path, "w", encoding="utf-8") as f:
    json.dump(response, f, indent=2, ensure_ascii=False)
    print("回應寫入成功！")