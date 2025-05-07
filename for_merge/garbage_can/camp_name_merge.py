from pathlib import Path
import pandas as pd
from rapidfuzz import fuzz
import json
import pymysql
from sqlalchemy import create_engine


def findSimilarIdx(s:pd.Series):
    """
    找出同Seires中，和自己最相似的元素 index，以同長度Series回傳
    """
    similar_idx = []
    # 露營地名稱太短又包含露營字樣，會造成比對分數過高
    # 去除露營字樣再行比對
    # s = s.str.replace("露營", "", regex=False)
    s = s.where( s.str.len() > 8, s.str.replace("露營", "", regex=False) )

    # bubble sort like 雙層迴圈
    for i, name in s.items():
        max_score = -1
        best_idx = -1
        for j, other_name in s.items():
            # 自己不比較
            if i == j:
                continue
            score = fuzz.partial_ratio(name, other_name)
            if score > max_score:
                max_score = score
                best_idx = j
        # 找出最佳解後存入 list 中
        similar_idx.append(best_idx)
        
    # print(similar_idx)
    return pd.Series(similar_idx)
    
def uploadMYSQL(df:pd.DataFrame):
    engine = create_engine("mysql+pymysql://test:PassWord_1@104.199.214.113:3307/eta", echo=True)
    df.to_sql(name='camp_merge', con=engine, if_exists='replace', index=False)


def main():
    # 要排除的檔名集合
    exclude_files = {"result.csv", "same.csv"}

    result_path = Path(__file__).parent/"result.csv"
    same_path = Path(__file__).parent/"same.csv"
    # 取得所有.csv檔
    csv_paths = [
        f for f in Path(__file__).parent.glob('*.csv')
        if f.name not in exclude_files
    ]
    df_list = [pd.read_csv(file) for file in csv_paths]
    # 組成 dataframe
    df_merge = pd.concat(df_list, ignore_index=True)
    # print(df_merge)
    camp_name = df_merge["Campsite"]
    similar_camp_idx = findSimilarIdx(camp_name)
    # print(silimar_camp_idx)
    # print(df_merge["Name"].loc[silimar_camp_idx])
    # print(df_merge["Campsite"].loc[silimar_camp_idx])
    # return
    df_merge["Similar_idx"] = similar_camp_idx
    df_merge["Name_similar"] = df_merge["Name"].loc[similar_camp_idx].values
    df_merge["Campsite_similar"] = df_merge["Campsite"].loc[similar_camp_idx].values 
    df_merge["Campsite_ratio"] = df_merge["Campsite"].combine(df_merge["Campsite_similar"], lambda x, y: fuzz.partial_ratio(x,y))
    df_merge["Address_similar"] = df_merge["Address"].loc[similar_camp_idx].values
    df_merge["Address_ratio"] = df_merge["Address"].combine(df_merge["Address_similar"], lambda x, y: fuzz.partial_ratio(x,y))
    
    uploadMYSQL(df_merge)
    df_merge.to_csv(result_path, encoding="utf-8")

    # df_same = df_merge[ (df_merge["Campsite_ratio"] > 60) & (df_merge["Address_ratio"] > 70)    ]
    # df_same = df_same[ (df_same["Campsite_ratio"] < 70 ) & (df_same["Address_ratio"] > 70)    ]
    # df_same.to_csv(same_path, encoding="utf-8")



if __name__ == "__main__":
    main()