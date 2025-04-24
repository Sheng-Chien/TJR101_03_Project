from chatWithGPT import ChatWithGPT
from parse_file_to_str import parse_file_to_str
from pathlib import Path
import json
from datetime import datetime

_key=""

askgpt=ChatWithGPT(
    model="gpt-3.5-turbo",
    _key = _key,
    max_tokens=1000,
    temperature=1,
)

# 載入資料
file_path = Path(__file__).parent / "test" / "input.csv"
data = parse_file_to_str(file_path)

# 設定訊息
ai_role = "你是一位文本分析專家，專門從大量評論中找出最常出現的設施、物品或名詞關鍵詞。請以條列方式列出排名前十的詞彙"
command = "以下是收集到的旅遊評論，請找出最常出現的設施與物品，並按照出現次數排序列出前十名。\n"
# ai_role = "你是吟遊由詩人"
# command = "用100個字說個故事"
data = ""
askgpt.set_message("system", ai_role)
askgpt.set_message("user", command + data)

# 可以看看messages有沒有設定錯誤
# print(askgpt._messages)
askgpt.expectBill(True)

# 使用chat() 發送prompt 給GPT，回傳給 response
response = askgpt.chat()

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
    json.dump(response.model_dump(), f, indent=2, ensure_ascii=False)
    print("回應寫入成功！")