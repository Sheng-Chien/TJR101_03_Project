import jieba
import pandas as pd

# 讀取 CSV 文件
result_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\result.csv')
articles1_df = pd.read_csv(r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles1.csv")
articles2_df = pd.read_csv(r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles2.csv")
articles3_df = pd.read_csv(r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles3.csv")
articles4_df = pd.read_csv(r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles4.csv")
articles5_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles5.csv')
articles6_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles6.csv')
articles7_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles7.csv')
articles8_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles8.csv')
articles9_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles9.csv')
articles10_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles10.csv')
articles11_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles11.csv')

# 提取 result.csv 中的 Campsite 和 Address 作為自訂詞典
custom_words = set(result_df['Campsite'].dropna()).union(set(result_df['Address'].dropna()))

# 提取各個 articles 中的 title 和 content
articles_titles = (articles1_df['title'].dropna().tolist() +
                   articles2_df['title'].dropna().tolist() +
                   articles3_df['title'].dropna().tolist() +
                   articles4_df['title'].dropna().tolist() +
                   articles5_df['title'].dropna().tolist() +
                   articles6_df['title'].dropna().tolist() +
                   articles7_df['title'].dropna().tolist() +
                   articles8_df['title'].dropna().tolist() +
                   articles9_df['title'].dropna().tolist() +
                   articles10_df['title'].dropna().tolist() +
                   articles11_df['title'].dropna().tolist())

articles_content = (articles1_df['content'].dropna().tolist() +
                    articles2_df['content'].dropna().tolist() +
                    articles3_df['content'].dropna().tolist() +
                    articles4_df['content'].dropna().tolist() +
                    articles5_df['content'].dropna().tolist() +
                    articles6_df['content'].dropna().tolist() +
                    articles7_df['content'].dropna().tolist() +
                    articles8_df['content'].dropna().tolist() +
                    articles9_df['content'].dropna().tolist() +
                    articles10_df['content'].dropna().tolist() +
                    articles11_df['content'].dropna().tolist())

# 合併所有標題和內容
all_texts = articles_titles + articles_content

# 將提取出的詞語加入 jieba 的自訂詞典
for word in custom_words:
    jieba.add_word(word)

# 測試斷詞
sample_text = " ".join(all_texts[:])  # 用所有文章內容作為範例

# 使用 jieba 進行斷詞
seg_list = jieba.cut(sample_text)

# 將斷詞結果轉為集合以便後續比對
seg_set = set(seg_list)

# 比對斷詞結果與自訂詞典中的詞語
matched_words = [word for word in seg_set if word in custom_words]

# 顯示匹配的詞語
print("匹配的自訂詞語：")
print(matched_words)


print("********************************************")

namelist = []
addresslist = []
for i in matched_words:
    if i in result_df['Campsite'].values:
        print(i)
        namelist.append(i)

    print("********************************************")

    if i in result_df['Address'].values:
        print(i)
        addresslist.append(i)

print("----------------------------------------------------------")


# 讀取 CSV 文件
result_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\result.csv')
camping_news_1_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\camping_news_1.csv')
camping_news_2_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\camping_news_2.csv')

# 提取 result.csv 中的 Name 和 Campsite 作為自訂詞典
custom_words = set(result_df['Campsite'].dropna()).union(set(result_df['Address'].dropna()))

# 提取各個 articles 中的 content
camping_news_title = camping_news_1_df['露營名稱'].dropna().tolist()
camping_news_content = (camping_news_1_df['露營內容'].dropna().tolist()+camping_news_2_df['Content'].dropna().tolist())
camping_news_address = camping_news_1_df['露營地址'].dropna().tolist()

# 合併所有內容
all_camping_news_texts = camping_news_title + camping_news_content + camping_news_address

# 將提取出的詞語加入 jieba 的自訂詞典
for word in custom_words:
    jieba.add_word(word)

# 測試斷詞
sample_camping_text = " ".join(all_camping_news_texts[:])  # 用所有露營新聞內容作為範例

# 使用 jieba 進行斷詞
seg_list_camping = jieba.cut(sample_camping_text)

# 將斷詞結果轉為集合以便後續比對
seg_set_camping = set(seg_list_camping)

# 比對斷詞結果與自訂詞典中的詞語
matched_words_camping = [word for word in seg_set_camping if word in custom_words]

# 顯示匹配的詞語
print("匹配的自訂詞語：")
print(matched_words_camping)
