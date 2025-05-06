import jieba
from rapidfuzz import fuzz
import pandas as pd
from pathlib import Path

def getAllCSVtoDF()->pd.DataFrame:
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



def findTopSimilar(s:pd.Series, func):
    idx_similar = []

    # 依序取出每一個名字
    for i, name in s.items():
        # 比對每一個名字並計算出相似度
        ratio = s.apply(lambda x: func(name, x))
        # 只取前 5個，並轉成list
        # top 的index 對應於最大的index
        top = ratio.nlargest(5).to_dict()
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


def similarJieba():
    pass

def saveFile(df:pd.DataFrame, path:Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(
        path,
        encoding="utf-8",
    )

def main():
    df_merged = getAllCSVtoDF()
    df_merged = df_merged.head(30)
    df = findTopSimilar(df_merged["Campsite"], fuzz.partial_ratio)
    
    with open()
    
    print(df)

if __name__ == "__main__":
    main()