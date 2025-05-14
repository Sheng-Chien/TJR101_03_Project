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
    df_fuzz = pd.read_csv(file_dir/"fuzz.csv", encoding="utf-8", engine="python")
    df_jaccard = pd.read_csv(file_dir/"jaccard.csv", encoding="utf-8", engine="python")
    df_sklearn = pd.read_csv(file_dir/"sklearn.csv", encoding="utf-8", engine="python")

    df = pd.concat([df_fuzz, df_jaccard, df_sklearn], axis=1, ignore_index=True)
    df = df.iloc[:,[1,2,3,6,7,10,11]]

    df.columns = ["base_idx", "f_idx", "f_ratio", "j_idx", "j_ratio", "s_idx", "s_ratio"]
    
    # 在這裡做營地名稱相似度篩選
    df_filtered = df[
        (df["base_idx"] != df["f_idx"]) # 因為程式邏輯, 結果包含自己, 排除
        & (df["f_ratio"]>80)
        & (df["j_ratio"]>0.5)
        & (df["s_ratio"]>0.5)
    ]

    id_to_name = df_base["Campsite"]
    # df_filtered["base_idx"] = df_filtered["base_idx"].map(id_to_name)
    # df_filtered["f_idx"] = df_filtered["f_idx"].map(id_to_name)
    # df_filtered["j_idx"] = df_filtered["j_idx"].map(id_to_name)
    # df_filtered["s_idx"] = df_filtered["s_idx"].map(id_to_name)

    # 魔法數字！請注意使用
    df_filtered.insert(1,"Campsite",df_filtered["base_idx"].map(id_to_name))
    df_filtered.insert(3,"f_site",df_filtered["f_idx"].map(id_to_name))
    df_filtered.insert(6,"j_site",df_filtered["j_idx"].map(id_to_name))
    df_filtered.insert(9,"s_site",df_filtered["s_idx"].map(id_to_name))
    
    f_add_score = compareAddress(df_base["Address"][df_filtered["base_idx"]], df_base["Address"][df_filtered["f_idx"]], fuzz.partial_ratio)
    j_add_score = compareAddress(df_base["Address"][df_filtered["base_idx"]], df_base["Address"][df_filtered["f_idx"]], jaccard_similarity)
    set_add_score = compareAddress(df_base["Address"][df_filtered["base_idx"]], df_base["Address"][df_filtered["f_idx"]], sklearn_similarity)

    
    # print(df_filtered)
    df_filtered.to_csv(file_dir/"merged.csv", encoding="utf-8")
    
    

if __name__ == "__main__":
    main()