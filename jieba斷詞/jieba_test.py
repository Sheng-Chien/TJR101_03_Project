import jieba
import pandas as pd

# 讀取 result.csv 中的 Campsite 和 Address 作為自訂詞典
result_df = pd.read_csv(r'C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\result.csv')
custom_words = set(result_df['Campsite'].dropna()).union(set(result_df['Address'].dropna()))

# 讀取所有 articles 的 CSV 檔案
file_paths = [
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles1.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles2.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles3.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles4.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles5.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles6.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles7.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles8.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles9.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles10.csv",
    r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\articles11.csv"
]

# 儲存匹配的結果
namelist_all = []
addresslist_all = []

# 將每個檔案進行處理
for file_path in file_paths:
    # 讀取 CSV 檔案
    df = pd.read_csv(file_path)

    # 提取 'title' 和 'content' 欄位
    articles_titles = df['title'].dropna().tolist()
    articles_content = df['content'].dropna().tolist()

    # 合併所有標題和內容
    all_texts = articles_titles + articles_content

    # 將提取出的詞語加入 jieba 的自訂詞典
    for word in custom_words:
        jieba.add_word(word)

    # 使用 jieba 進行斷詞
    seg_list = jieba.cut(" ".join(all_texts))

    # 儲存匹配結果
    namelist = set()  # 使用 set 去除重複項
    addresslist = set()

    # 逐個詞語進行比對
    for i in seg_list:
        if i in result_df['Campsite'].values:
            namelist.add(i)

        if i in result_df['Address'].values:
            addresslist.add(i)

    # 儲存該檔案的結果
    namelist_all.append(list(namelist))  # 轉回 list 以便在 DataFrame 中顯示
    addresslist_all.append(list(addresslist))

# 使用字典將 namelist_all 和 addresslist_all 轉換成 DataFrame
df_result = pd.DataFrame({
    'Matched Campsite': namelist_all,
    'Matched Address': addresslist_all
})

# 顯示結果
print(df_result)
