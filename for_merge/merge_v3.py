from rapidfuzz import fuzz
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import re

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

def saveFile(df:pd.DataFrame, path:Path):
    """儲存.csv 到本機"""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(
        path,
        encoding="utf-8",
    )

def uploadMYSQL(df:pd.DataFrame, table:str):
    """上傳到mysql server 取代原本table"""
    engine = create_engine("mysql+pymysql://test:PassWord_1@104.199.214.113:3307/eta", echo=False)
    df.to_sql(name=table, con=engine, if_exists='replace', index=False)


def findTopSimilar(s:pd.Series):
    """找出和自己最相似的元素, 並以同等長度的series回傳該元素的所在index"""
    similar_idx = []
    # bubble sort like 雙層迴圈
    for idx, name in s.items():
        max_score = -1
        best_idx = -1
        for j, other_name in s.items():
            # 自己不比較
            if idx == j:
                continue
            score = fuzz.partial_ratio(name, other_name)
            if score > max_score:
                max_score = score
                best_idx = j
        # 找出最佳解後存入 list 中
        similar_idx.append(best_idx)

    return pd.Series(similar_idx)

def idxToCol(s:pd.Series, idx:pd.Series):
    """把索引轉換成索引對應的元素名稱"""
    return s.loc[idx].values
    
def campsiteNF(text:str):
    # 去除不可見字元以及特殊符號
    text = re.sub(r'[\s\u200b\u3000]', '', text)                      # 刪除不可見字元
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)            # 刪除特殊符號

    # 要去除的字典
    dictionary = ["露營地", "露營區", "營地", "營區", 
                  "農場", "民宿", "休閒", "溫泉渡假村", 
                  "露營", "園區", "農莊", "莊園",
                  "農村", "農園", "農庄", "農業"]
    # 重新排序，避免子集合先被刪除(營區&露營區)
    dictionary.sort(key=len, reverse=True)

    pattern = '|'.join(map(re.escape, dictionary))  # 安全建立 regex
    text = re.sub(pattern, "", text)
    return text

def addressNF(text:str):
    # 將門牌正規為阿拉伯數字
    text = re.sub(r'(\d+)-(\d+)', r'\1之\2', text)
    # 繁簡統一
    text = text.replace("台","臺")
    
    return text


def addressRatio(addr1:str, addr2:str):
    # 提取縣市名
    conty1 = re.search(r'([\u4e00-\u9fa5]{2}(縣|市))', addr1)
    conty2 = re.search(r'([\u4e00-\u9fa5]{2}(縣|市))', addr2)
    
    # 如果縣市名不同直接出局
    # 沒有縣市的通常是沒有縣(新竹), 而且名稱很短, 直接進下一輪
    if conty1 and conty2 and conty1.group(0) != conty2.group(0):
        return 0
    
    score =  fuzz.partial_ratio(addr1, addr2)

    return score

def main():
    # 獲取所有
    df_base = getAllCSVtoDF()

    # 分別把 "營區名稱" 以及 "營區地址" 提取出來作正規化及簡化
    s_site = df_base["Campsite"].map(campsiteNF)
    s_address = df_base["Address"].map(addressNF)

    # 取得最相似名稱的對應索引
    print("比較相似度")
    s_similar_idx = findTopSimilar(s_site)

    # 整理資料，不需要的欄位可以註解掉

    # 相似營地索引
    df_base["similar_idx"] = s_similar_idx
    # 簡化營地名稱
    df_base["site_NF"] = s_site
    # 相似營地名稱
    df_base["similar_site"] = idxToCol(s_site, s_similar_idx)
    # 名稱相似度分數
    df_base["site_ratio"] = df_base["site_NF"].combine(df_base["similar_site"], lambda x, y: fuzz.partial_ratio(x,y)).round(2)
    
    
    # 簡化營區地址
    df_base["address_NF"] = s_address
    # 相似營地地址
    df_base["similar_address"] = idxToCol(s_address, s_similar_idx)
    # 相似營區地址分數
    df_base["address_ratio"] = df_base["address_NF"].combine(df_base["similar_address"], lambda x, y: addressRatio(x,y)).round(2)
    
    save_path = Path(__file__).parent/"results/results.csv"
    saveFile(df_base, save_path)
    uploadMYSQL(df_base.reset_index(names="idx"), "mergev3")


    

if __name__ == "__main__":
    main()