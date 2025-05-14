import jieba
from rapidfuzz import fuzz
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def jaccard_similarity(text1, text2):
    words1 = set(jieba.cut(text1))
    words2 = set(jieba.cut(text2))
    
    intersection = words1 & words2
    union = words1 | words2
    
    if not union:
        return 0.0
    return len(intersection) / len(union) * 100

def sklearn_similarity(text1, text2):
    # 自訂 jieba 分詞給 CountVectorizer 使用
    def jieba_tokenizer(text):
        return list(jieba.cut(text))

    # 初始化 CountVectorizer（用 jieba 當 tokenizer）
    vectorizer = CountVectorizer(tokenizer=jieba_tokenizer)

    # 將兩段文字轉成詞頻向量
    X = vectorizer.fit_transform([text1, text2])

    # 計算餘弦相似度
    cos_sim = cosine_similarity(X[0], X[1]).item() * 100
    return cos_sim


def compareAddress(s1:pd.Series, s2:pd.Series, fun):
    result = pd.Series(map(lambda x: fun(x[0], x[1]), zip(s1, s2)))
    return result

def main():

    # 讀取已分析檔案
    file_dir = Path(__file__).parent/"results"
    df_base = pd.read_csv(file_dir/"base.csv", encoding="utf-8", engine="python")
    df_fuzz = pd.read_csv(file_dir/"fuzz.csv", encoding="utf-8", engine="python", index_col=0)
    df_jaccard = pd.read_csv(file_dir/"jaccard.csv", encoding="utf-8", engine="python", index_col=0)
    df_sklearn = pd.read_csv(file_dir/"sklearn.csv", encoding="utf-8", engine="python", index_col=0)

    # 把三種比對方式 相似度都名列前茅的結果作交集
    df_results = pd.merge(
        df_fuzz, df_jaccard, 
        on=["idx", "fk"], 
        suffixes=('', '_j')
    )
    df_results = pd.merge(
        df_results, df_sklearn, 
        on=["idx", "fk"], 
        suffixes=('_f', '_s')
    )
    # 移除自己的比對(分數必為100)
    df_results = df_results[df_results["idx"] != df_results["fk"]]

    f_add_score = compareAddress(df_base["Address"][df_results["idx"]], df_base["Address"][df_results["fk"]], fuzz.partial_ratio)
    j_add_score = compareAddress(df_base["Address"][df_results["idx"]], df_base["Address"][df_results["fk"]], jaccard_similarity)
    s_add_score = compareAddress(df_base["Address"][df_results["idx"]], df_base["Address"][df_results["fk"]], sklearn_similarity)

    df_add_score = pd.concat([f_add_score, j_add_score, s_add_score], axis=1)
    print(df_add_score)

    print(df_results)
    
    

if __name__ == "__main__":
    main()