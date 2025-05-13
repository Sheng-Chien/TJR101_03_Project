import json
import re
from pathlib import Path

current_dir = Path(__file__).parent
# 載入原始資料
input_path = current_dir / "easycamp_reviews_cleaned.json"
with open(input_path, 'r', encoding='utf-8') as f:
    cleaned_data = json.load(f)

# 清洗姓名：去除先生或小姐
def clean_name(name):
    return re.sub(r'(先生|小姐)$', '', name)

# 合併評論標題與內容，在標題後加一格空白
def merge_content(title, content):
    return f"{title} {content}" if content else title

# 開始清洗
for camp in cleaned_data:
    new_reviews = []
    for review in camp.get("顧客評論", []):
        cleaned_review = {
            "姓名": clean_name(review["姓名"]),
            "評論日期": review["評論日期"],
            "評分": review["評分"],
            "content": merge_content(review["評論標題"], review["評論內容"])
        }
        new_reviews.append(cleaned_review)
    camp["顧客評論"] = new_reviews

# 儲存清洗後的資料
output_path = current_dir / "reviews_ready_for_db.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
