from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import matplotlib.font_manager as fm

# 讀取關鍵字
file_path = Path(".venv", "MART", "data_from_mysql")
file_path.mkdir(parents=True, exist_ok=True)
text = file_path / "MySQL_MART_各縣市露營場_熱度及TAG表.csv"
df = pd.read_csv(text, encoding="utf-8-sig")

# 匯入中文字形
zh_font_path = "C:/Windows/Fonts/msjh.ttc"
zh_font = fm.FontProperties(fname=zh_font_path)

keywords = df["ref_keywords"].dropna().str.replace("｜", " ", regex=False).str.cat(sep=" ")

# 建立全台文字雲--------------------------
# 全台露營場關鍵字
# wc = WordCloud(
#     font_path="msjh.ttc",  # 指定中文字型，例如微軟正黑體（放在同目錄或用絕對路徑）
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(keywords)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# # 北中南東地區產生文字雲--------------------------

# # 根據 region 分群-------------
# grouped = df.groupby("region")

# for region, group in grouped:
#     keywords_text = group["ref_keywords"].str.cat(sep=" ")
    
#     # 建立文字雲
#     wc = WordCloud(
#         font_path="msjh.ttc",
#         width=800,
#         height=400,
#         background_color="white"
#     ).generate(keywords_text)
    
#     # 顯示圖形
#     plt.figure(figsize=(10, 5))
#     plt.imshow(wc, interpolation="bilinear")
#     plt.axis("off")
#     plt.title(f"{region}", fontproperties=zh_font, fontsize=20)
#     plt.show()

# # ---------------------------------------
# # 篩選負評比例 >= 0.5
# neg_df = df[df["negative_ratio"] > 0.49]

# # 組合關鍵字文字
# neg_keywords = neg_df["ref_keywords"].dropna().str.replace("｜", " ", regex=False).str.cat(sep=" ")

# # 建立文字雲
# wc = WordCloud(
#     font_path="msjh.ttc",
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(neg_keywords)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.title("負評比例>=50% 的露營場關鍵字", fontproperties=zh_font, fontsize=20)
# plt.show()

# # ---------------------------------------
# 親子友善
# family = df[df["Tag"] == "親子友善"]

# # 組合關鍵字文字

# exclude = {"小朋友", "小孩", "親子", "孩子"}

# # 將關鍵字拆開 → 過濾 → 再合併
# filtered_keywords = (
#     family["ref_keywords"]
#     .dropna()
#     .str.replace("｜", " ", regex=False)
#     .str.cat(sep=" ")
#     .split()
# )

# # 移除不想要的關鍵字
# family_filtered_keywords = [word for word in filtered_keywords if word not in exclude]

# # 合併回一個字串給文字雲使用
# family_final_text = " ".join(family_filtered_keywords)

# # 建立文字雲
# wc = WordCloud(
#     font_path="msjh.ttc",
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(family_final_text)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.title("親子友善的露營場關鍵字", fontproperties=zh_font, fontsize=20)
# plt.show()

# 懶人露營文字雲 ---------------------------------------

lazy = df[df["Tag"] == "免搭帳篷(懶人露營)"]

# 組合關鍵字文字
exclude = {"不用", "帳篷", "懶人", "懶人露", "懶人帳", "露營"}

# 將關鍵字拆開 → 過濾 → 再合併
filtered_keywords = (
    lazy["ref_keywords"]
    .dropna()
    .str.replace("｜", " ", regex=False)
    .str.cat(sep=" ")
    .split()
)

# 移除不想要的關鍵字
lazy_filtered_keywords = [word for word in filtered_keywords if word not in exclude]

# 合併回一個字串給文字雲使用
lazy_final_text = " ".join(lazy_filtered_keywords)


# 建立文字雲
wc = WordCloud(
    font_path="msjh.ttc",
    width=1000,
    height=800,
    background_color="white"
).generate(lazy_final_text)

# 顯示圖形
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("免搭帳篷(懶人露營)的露營場關鍵字", fontproperties=zh_font, fontsize=20)
plt.show()

# # 豪華露營文字雲---------------------------------------

# lux = df[df["Tag"] == "豪華露營"]

# # 組合關鍵字文字
# lux_keywords = lux["ref_keywords"].dropna().str.replace("｜", " ", regex=False).str.cat(sep=" ")

# # 建立文字雲
# wc = WordCloud(
#     font_path="msjh.ttc",
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(lux_keywords)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.title("豪華露營的露營場關鍵字", fontproperties=zh_font, fontsize=20)
# plt.show()


# # 營主用心經營文字雲---------------------------------------

# mana = df[df["Tag"] == "營主用心經營"]

# # 組合關鍵字文字
# mana_keywords = mana["ref_keywords"].dropna().str.replace("｜", " ", regex=False).str.cat(sep=" ")

# # 建立文字雲
# wc = WordCloud(
#     font_path="msjh.ttc",
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(mana_keywords)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.title("營主用心經營露營場的關鍵字", fontproperties=zh_font, fontsize=20)
# plt.show()

# # 適合團體或家族出遊文字雲---------------------------------------

# group_play = df[df["Tag"] == "適合團體或家族出遊"]

# exclude = {"團體", "大家", "適合", "團露", "朋友", "家族"}

# # 將關鍵字拆開 → 過濾 → 再合併
# filtered_keywords = (
#     group_play["ref_keywords"]
#     .dropna()
#     .str.replace("｜", " ", regex=False)
#     .str.cat(sep=" ")
#     .split()
# )

# # 移除不想要的關鍵字
# group_play_filtered_keywords = [word for word in filtered_keywords if word not in exclude]

# # 合併回一個字串給文字雲使用
# group_final_text = " ".join(group_play_filtered_keywords)

# # 建立文字雲
# wc = WordCloud(
#     font_path="msjh.ttc",
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(group_final_text)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.title("適合團體或家族出遊露營場的關鍵字", fontproperties=zh_font, fontsize=20)
# plt.show()

# # 營地環境維護佳 文字雲---------------------------------------

# envir = df[df["Tag"] == "營地維護佳"]

# exclude = {"維護", "環境", "營地"}

# # 將關鍵字拆開 → 過濾 → 再合併
# filtered_keywords = (
#     envir["ref_keywords"]
#     .dropna()
#     .str.replace("｜", " ", regex=False)
#     .str.cat(sep=" ")
#     .split()
# )

# # 移除不想要的關鍵字
# envir_filtered_keywords = [word for word in filtered_keywords if word not in exclude]

# # 合併回一個字串給文字雲使用
# envir_final_text = " ".join(envir_filtered_keywords)

# # 建立文字雲
# wc = WordCloud(
#     font_path="msjh.ttc",
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(envir_final_text)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.title("營地環境維護佳露營場的關鍵字", fontproperties=zh_font, fontsize=20)
# plt.show()

# HOT 文字雲---------------------------------------

# hot = df[df["hot"] == "Hot"]

# exclude = {}

# # 將關鍵字拆開 → 過濾 → 再合併
# filtered_keywords = (
#     hot["ref_keywords"]
#     .dropna()
#     .str.replace("｜", " ", regex=False)
#     .str.cat(sep=" ")
#     .split()
# )

# # 移除不想要的關鍵字
# hot_filtered_keywords = [word for word in filtered_keywords if word not in exclude]

# # 合併回一個字串給文字雲使用
# hot_final_text = " ".join(hot_filtered_keywords)

# # 建立文字雲
# wc = WordCloud(
#     font_path="msjh.ttc",
#     width=1000,
#     height=800,
#     background_color="white"
# ).generate(hot_final_text)

# # 顯示圖形
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
# plt.title("hot露營場的關鍵字", fontproperties=zh_font, fontsize=20)
# plt.show()

