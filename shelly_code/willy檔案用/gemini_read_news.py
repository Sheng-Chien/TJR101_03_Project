# 使用Gemini ai從新聞中取出露營場資訊
# 要先在GCP上打開vertexai的服務
# 第一次需要先pip install google-generativeai
# 然後去IAM新增一個service account，role要選Vertex AI User，並新增key

from vertexai.generative_models import GenerativeModel
import vertexai
import os
from pathlib import Path
import pandas as pd

# 設定Gemini API資訊----------------------

# 要換成自己key的json檔案的位置
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\TJR101_03_Project\.venv\project\gemini-api-user.json"

# 初始化GCP專案與地區
vertexai.init(
            project="glass-archway-457401-e6", # 要改自己GCP的專案ID
            location="us-central1" # 固定不用改
            )

# Gemini 模型
model = GenerativeModel("gemini-2.0-flash")

# 開始處理文章----------------------

article_path = Path(".venv", "willy", "articles") # 路徑要改

article_names = ["articles1.csv", "articles2.csv", "articles3.csv",
                "articles4.csv", "articles5.csv", "articles6.csv",
                "articles7.csv", "articles8.csv", "articles9.csv",
                "articles10.csv", "articles11.csv"
                ]

results = [] # 儲存AI分析的結果

for file_name in article_names:
    each_article = Path(article_path / file_name)
    df = pd.read_csv(each_article, encoding="utf-8-sig")

    article_content = df["content"].iloc[0]

    # 指令
    prompt = f"""
    這是一篇介紹露營場的文章，裡面有一個或多個露營場的介紹，請幫我從文章中擷取以下三個資訊，如果判斷文章內容與露營場無關，則三個欄位都留空：

    1. 露營場名稱
    2. 地址（如果沒有留空）
    3. 介紹文字

    段落內容如下：
    {article_content}

    請列出多筆資訊，並用這個格式回覆（不要加多餘文字），每一篇以-----------區隔：
    露營場名稱：XXX
    地址：XXX
    介紹：XXX
    """
    # 開始執行
    response = model.generate_content(prompt)
    usage = response.usage_metadata  # Token統計

    print(f"{file_name}分析結束")

    # 分析結果轉存至DataFrame

    entries = response.text.strip().split("-----------")

    for entry in entries:
        lines = entry.strip().splitlines()
        if len(lines) < 3:
            continue
    
        name = lines[0].replace("露營場名稱：", "").strip()
        address = lines[1].replace("地址：", "").strip()
        intro = lines[2].replace("介紹：", "").strip()

        results.append({
                        "露營場名稱": name,
                        "地址": address,
                        "介紹": intro,
                        "來源檔名": file_name,
                        "title": df["title"].iloc[0],
                        "date": df["date"].iloc[0],
                        "input_tokens": usage.prompt_token_count,
                        "output_tokens": usage.candidates_token_count,
                        "total_tokens": usage.total_token_count
                        })

result_df = pd.DataFrame(results)

# 路徑要改
output_path = Path(r"C:\TJR101_03_Project\.venv\willy", "gemini_results.csv")

result_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"分析完成，結果已儲存")

# Token統計------------------
total_input = result_df["input_tokens"].sum()
total_output = result_df["output_tokens"].sum()
total = result_df["total_tokens"].sum()

print(f"Input tokens：{total_input}")
print(f"Output tokens：{total_output}")
print(f"總Token數：{total}")

