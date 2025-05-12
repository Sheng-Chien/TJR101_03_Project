from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

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


def ifRepeat(row:pd.Series):
    site_ratio = row["site_ratio"]
    address_ratio = row["address_ratio"]
    if site_ratio > 80 and address_ratio > 70:
        return True
    if site_ratio > 80 and address_ratio > 50:
        return None
    return False


def insertMergeTable(df:pd.DataFrame):

    for idx, row in df.iterrows():
        if idx % 20 == 0:
            print(f"正在處理第{idx}筆資料")
        
        new_values = row.to_dict()
        # print(new_value)
        with engine.connect() as conn:
            try:
                stmt = insert(merge_table).values( new_values )
                conn.execute(stmt)    
                conn.commit()
            except IntegrityError:
                print(f"{idx} 主鍵重複，不插入資料")

def updateMergeFK(value, fk):
    update_values = {"campground_ID": fk}
    # 執行更新
    session.query(merge_table).filter_by(**value).update(
        update_values,
        synchronize_session=False  # 設定為 False 通常會加速更新，視情況而定
    )
    session.commit()

def selectTable(table):
    # 使用 SQLAlchemy 查詢並將結果轉換成 DataFrame
    with engine.connect() as conn:
        stmt = select(table) 
        df = pd.read_sql(stmt, conn)
        return df

def insertCampground(values):
    with engine.connect() as conn:
        # 插入資料，並使用 returning() 取得自動增量的值
        stmt = insert(campground_table).values(values)
        result = conn.execute(stmt)
        conn.commit()
        # 取得自動增量的 id
        inserted_id = result.inserted_primary_key[0]
        # print(f"插入後的自動增量 ID: {inserted_id}")
        return inserted_id


def foriegnTables(df:pd.DataFrame):
    # 由資料庫索取資料表
    df = selectTable(merge_table)
    df_county = selectTable(county_table)

    for idx, row in df.iterrows():

        if idx % 20 == 0:
            print(f"正在處理第{idx}筆資料")

        # 模糊不清的跳過, fk 為 null
        if pd.isna(row["repeat"]):
            # print("NAN")
            continue
        # 提取縣市
        county = row["address"][:3]
        # 查詢縣市代號
        try:
            matching_row = df_county.loc[df_county['county_name'] == county].iloc[0]  # .iloc[0] 獲取第一行  
            # print(county, matching_row)
            county_id = matching_row["county_ID"]
        except:
            # 不在縣市清單中的同樣當作模糊不清, fk 為 null
            county_id = -1
            continue

        # print(county, county_id)
        merge_pk_value = {
            "name": row["name"],
            "camping_site_name": row["camping_site_name"],
            "address": row["address"],
        }
        campground_value = {
            "camping_site_name": row["camping_site_name"],
            "address": row["address"],
            "county_ID": county_id,
        }
        
        # 如果不重複，直接插入
        # 如果相似的idx比較大，則必定尚未新增，直接插入不做比較
        if row["repeat"] == False or row["similar_idx"] > idx:
            
            fk = insertCampground(campground_value)
            updateMergeFK(merge_pk_value, fk)

        else:
            # 先更新merge 表的 fk
            stmt = select(merge_table.c.campground_ID).where(merge_table.c.idx == row["similar_idx"])
            with engine.connect() as conn:
                fk = conn.execute(stmt).fetchall()[0][0]
                # print(fk)
            updateMergeFK(merge_pk_value, fk)




def main():
    file_path = Path(__file__).parent/"results/results.csv"
    df = pd.read_csv(file_path, encoding="utf-8", engine="python")
    # 是否重複
    result_series = df.apply(lambda row: ifRepeat(row), axis=1)
    df["repeat"] = result_series
    
    df_merge = df[["Name", "Campsite", "Address", "similar_idx", "repeat"]]
    df_merge.reset_index(names="idx", inplace=True)
    # 把欄位名稱改成和 mysql一致
    df_merge.columns = ["idx", "name", "camping_site_name", "address", "similar_idx", "repeat"]
    save_path = Path(__file__).parent/"results/temp.csv"
    df_merge.to_csv(save_path, encoding="utf-8")

    # 插入對照表
    insertMergeTable(df_merge)
    # 插入campground 並建立 merge 表的fk
    foriegnTables(df_merge)
    

if __name__ == "__main__":
    main()