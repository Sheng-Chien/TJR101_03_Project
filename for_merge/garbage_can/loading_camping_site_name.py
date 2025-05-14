from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import pandas as pd
from merge_v3 import campsiteNF, addressNF, findTopSimilar, addressRatio
from rapidfuzz import fuzz
import re
# 連接到已存在的 MySQL 資料庫
# 請根據實際資料庫設定，替換 user, password, localhost, dbname
DATABASE_URL = "mysql+pymysql://test:PassWord_1@104.199.214.113:3307/test2_db"

# 建立 SQLAlchemy 引擎
engine = create_engine(DATABASE_URL, echo=False)

# 建立 Session 連線
Session = sessionmaker(bind=engine)
session = Session()

# 定義資料表結構（可以透過 MetaData 類別來反射已存在的表格）
metadata = MetaData()
merge_table = Table('campground_merge', metadata, autoload_with=engine)
campground_table = Table('campground', metadata, autoload_with=engine)
county_table = Table('county', metadata, autoload_with=engine)

def findTopSimilar(s:pd.Series, self_idx:int)->int:
    new_site = s.iloc[-1]
    max_core = -1
    best_idx = -1
    for idx, site in s.items():
        # 如果是自己則不執行
        if idx == self_idx:
            continue
        # 比較，如果分數高則記錄高分idx
        score = fuzz.partial_ratio(new_site, site)
        if score > max_core:
            max_core = score
            best_idx = idx
    
    return best_idx

def insertMergeTable(s:pd.Series):
    new_values = {
        "name": s["Name"],
        "camping_site_name": s["Campsite"],
        "address": s["Address"],
    }
    print()
    print(new_values)
    with engine.connect() as conn:
        try:
            stmt = insert(merge_table).values( new_values )
            conn.execute(stmt)    
            conn.commit()
            # 至此插入新資料成功，表示新增一筆對照資料

            # 讀取表格，因為剛剛有insert成功，所以必定有資料
            df = selectTable(merge_table)
            s_site = df["camping_site_name"].map(campsiteNF)
            s_address = df["address"].map(addressNF)
            # 找到自己的idx 迴避比較
            condition = (
                (df['name'] == new_values["name"]) & 
                (df['camping_site_name'] == new_values["camping_site_name"]) & 
                (df['address'] == new_values["address"])
            )
            self_idx = df[condition].index[0]
            # 找到最像的
            best_idx = findTopSimilar(s_site, self_idx)
            
            # 第一筆資料會是-1
            if best_idx >= 0:
                score_site = fuzz.partial_ratio(s_site.iloc[self_idx], s_site[best_idx])
                score_address = addressRatio(s_address.iloc[self_idx], s_address.iloc[best_idx])
                print(s_site.iloc[self_idx], s_site[best_idx])
            else:
                score_site = 0
                score_address = 0
            print("分數")
            print(score_site, score_address)
            print("地址")
            print(s_address.iloc[self_idx])

            # 挑出行政區
            county = re.search(r'([\u4e00-\u9fa5]{2}(縣|市))', s_address.iloc[self_idx])
            # print(county)
            if county is not None:
                county = county.group(0)
                df_county = selectTable(county_table)
                # print(df_county)
                try:
                    # 搜尋符合條件的第一行
                    matching_row = df_county.loc[df_county['county_name'] == county].iloc[0]  # .iloc[0] 獲取第一行  
                    # print(county, matching_row)
                    county_id = matching_row["county_ID"]
                    print(county, county_id)
                except:
                    # 沒有在conty table裡的會報錯，手動歸類模糊不清
                    score_site = 90
                    score_address = 60   
                
                
                # 沒有行政區的人為操作為模糊不清
            else:
                score_site = 90
                score_address = 60               

            # 相同的營區
            if score_site > 80 and score_address > 70:
                print("相同的✅✅")
                fk = df["campground_ID"].iloc[best_idx]
                # 因為有可能相似資料尚未載入而造成模糊不清
                # 此時對照的fk 為none
                if fk is None:
                    print("更新merge✅✅✅✅")
                    best_value = {
                        "name": df["Name"].iloc[best_idx],
                        "camping_site_name": df["Campsite"].iloc[best_idx],
                        "address": df["Address"].iloc[best_idx],                  
                    }
                    # 插入camping ground 以取得 fk
                    fk = insertCampground(best_value)
                    # 更新fk
                    updateMergeFK(best_value, fk)
            
            # 模糊並不清的
            elif score_site > 80 and score_address > 50:
                fk = None
                print("模糊不清的✴️")
            # 完全不同的
            else:
                print("不同的營區✳️")
                values = {
                    "county_ID": county_id,
                    "camping_site_name": s["Campsite"],
                    "address": s["Address"],
                }
                fk = insertCampground(values)
            
            # 更新 fk
            if fk is not None:
                updateMergeFK(new_values, fk)


        except IntegrityError as e:
            print("主鍵重複，不插入資料")

def updateMergeFK(value, fk):
    update_values = {"campground_ID": fk}
    # 執行更新
    session.query(merge_table).filter_by(**value).update(
        update_values,
        synchronize_session=False  # 設定為 False 通常會加速更新，視情況而定
    )
    session.commit()

def insertCampground(values):
    with engine.connect() as conn:
        # 插入資料，並使用 returning() 取得自動增量的值
        stmt = insert(campground_table).values(values)
        result = conn.execute(stmt)
        conn.commit()
        # 取得自動增量的 id
        inserted_id = result.inserted_primary_key[0]
        print(f"插入後的自動增量 ID: {inserted_id}")
        return inserted_id

def selectTable(table):
    # 使用 SQLAlchemy 查詢並將結果轉換成 DataFrame
    with engine.connect() as conn:
        stmt = select(table) 
        df = pd.read_sql(stmt, conn)
        return df


def main():
    file_path = Path(__file__).parent/"result.csv"
    df = pd.read_csv(file_path, encoding="utf-8", engine="python")
    df = df.iloc[1500:]
    for _, row in df.iterrows():
        # print(row.to_dict())
        insertMergeTable(row)


if __name__ == "__main__":
    main()

session.close()