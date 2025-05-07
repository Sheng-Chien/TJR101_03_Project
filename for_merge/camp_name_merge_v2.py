import jieba
from rapidfuzz import fuzz
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine


def getAllCSVtoDF()->pd.DataFrame:
    """取得同資料夾下的所有.cxv檔，合併為一張總表，並以DataFrame回傳"""
    # 要排除的檔名集合
    exclude_files = {"result.csv", "same.csv"}

    # 取得所有.csv檔
    csv_paths = [
        f for f in Path(__file__).parent.glob('*.csv')
        if f.name not in exclude_files
    ]
    df_list = [pd.read_csv(file) for file in csv_paths]
    # 組成 dataframe
    df_merge = pd.concat(df_list, ignore_index=True)
    return df_merge


def jaccard_similarity(text1, text2):
    words1 = set(jieba.cut(text1))
    words2 = set(jieba.cut(text2))
    
    intersection = words1 & words2
    union = words1 | words2
    
    if not union:
        return 0.0
    return len(intersection) / len(union)

def sklearn_similarity(text1, text2):
    # 自訂 jieba 分詞給 CountVectorizer 使用
    def jieba_tokenizer(text):
        return list(jieba.cut(text))

    # 初始化 CountVectorizer（用 jieba 當 tokenizer）
    vectorizer = CountVectorizer(tokenizer=jieba_tokenizer)

    # 將兩段文字轉成詞頻向量
    X = vectorizer.fit_transform([text1, text2])

    # 計算餘弦相似度
    cos_sim = cosine_similarity(X[0], X[1]).item()
    return cos_sim

def findTopSimilar(s:pd.Series, func):
    """
    找出最相似的n 個字串, 做出展平的對照表\n
    原始字串idx, 相似字串idx, 分數 
    """
    idx_similar = []

    # 依序取出每一個名字
    for i, name in s.items():
        # 比對每一個名字並計算出相似度
        ratio = s.apply(lambda x: func(name, x))
        # 只取前 5個，並轉成list
        # top 的index 對應於分數最高的index{ 378: 0.73, 224: 0.66, ....}
        n=5
        top = ratio.nlargest(n).to_dict()
        idx_similar.append(top)
        # idx_similar.append()
    
    # 合併為 營區名字 {相似營區idx} 的 df
    df = pd.concat([s, pd.Series(idx_similar, name = "similars")], axis=1)


    # 展平 dict: 每個 dict 轉成 list of tuples，然後 explode
    df_exploded = df.copy()
    df_exploded['similars'] = df['similars'].apply(lambda d: list(d.items()))
    df_exploded = df_exploded.explode('similars')

    # 拆成兩欄 key 和 value
    df_exploded[['fk', 'ratio']] = pd.DataFrame(df_exploded['similars'].tolist(), index=df_exploded.index)

    # 移除原始 dict 欄
    df_exploded = df_exploded.drop(columns='similars')

    df_exploded.drop(columns="Campsite", inplace=True)
    df_exploded.reset_index(names="idx", inplace=True)
    return df_exploded


def saveFile(df:pd.DataFrame, path:Path):
    """儲存.csv 到本機"""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(
        path,
        encoding="utf-8",
    )

def uploadMYSQL(df:pd.DataFrame, table:str):
    """上傳到mysql server 取代原本table"""
    engine = create_engine("mysql+pymysql://test:PassWord_1@104.199.214.113:3307/eta", echo=True)
    df.to_sql(name=table, con=engine, if_exists='replace', index=False)


def scoring(df_merged:pd.DataFrame):
    # 存檔資料夾
    file_dir = Path(__file__).parent/"results"

    # 儲存基底檔案
    saveFile(df_merged, file_dir/"base.csv")
    uploadMYSQL(df_merged.reset_index(names="idx"), "base")
    
    # 分別計算分數後寫入檔案並上傳
    print("fuzz")
    df = findTopSimilar(df_merged["Campsite"], fuzz.partial_ratio)
    saveFile(df, file_dir/"fuzz.csv")
    uploadMYSQL(df, "fuzz")

    print("jaccard")
    df = findTopSimilar(df_merged["Campsite"], jaccard_similarity)
    saveFile(df, file_dir/"jaccard.csv")
    uploadMYSQL(df, "jaccard")

    print("sklearn")
    df = findTopSimilar(df_merged["Campsite"], sklearn_similarity)
    saveFile(df, file_dir/"sklearn.csv")
    uploadMYSQL(df, "sklearn")    

def main():
    df_merged = getAllCSVtoDF()
    # df_merged = df_merged.head(30)

    # 計算分數並存檔
    scoring(df_merged)
    

if __name__ == "__main__":
    main()