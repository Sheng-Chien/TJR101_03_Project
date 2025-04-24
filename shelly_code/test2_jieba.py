# 測試jieba斷詞
# 斷詞後提取關鍵字

import pandas as pd
import jieba
import jieba.analyse

# 載入爬好的資料
df = pd.read_csv("宜蘭 露營場_checkpoint.csv", encoding="utf-8-sig")

# 讀取自訂的停用詞清單
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)

punctuations = set("，。、！？：；（）「」『』《》〈〉【】[]()~～…—-\"\'`!@#$%^&*+=|\\/<>\n ")

# 結果欄位
seg_list = []
keywords_list = []

# 開始逐筆處理
for text in df["評論內容"]:
    if pd.isna(text) or text.strip() == "" or text == "本筆評論無內容":
        seg_list.append("")
        keywords_list.append("")
        continue

    # 斷詞並過濾
    words = jieba.lcut(text)
    words = [w for w in words if w.strip() and w not in stopwords and w not in punctuations]
    seg_list.append(" ".join(words))
    clean_text = " ".join(words)

    # TF-IDF + TextRank 各提前20個關鍵詞
    tfidf_kw = set(jieba.analyse.extract_tags(clean_text, topK=20))
    textrank_kw = set(jieba.analyse.textrank(clean_text, topK=20))

    # 去重整合
    combined_kw = sorted(tfidf_kw | textrank_kw)  # 用 union 去重
    keywords_list.append("/".join(combined_kw))

# 加入欄位
df["斷詞結果"] = seg_list
df["關鍵詞"] = keywords_list

print(df.head())


for keyword in df["關鍵詞"]:
    all_keywords = "".join(keyword)

# 提取 TF-IDF 與 TextRank 關鍵詞
tfidf = jieba.analyse.extract_tags(all_keywords, topK=15, withWeight=True)
textrank = jieba.analyse.textrank(all_keywords, topK=15, withWeight=True)

# 顯示結果
print("TF-IDF 提取關鍵詞：")
for word, weight in tfidf:
    print(f"{word} ({weight:.2f})")

print("\nTextRank 提取關鍵詞：")
for word, weight in textrank:
    print(f"{word} ({weight:.2f})")