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
    

def main():
    file_path = Path(__file__).parent/"results/results.csv"
    df = pd.read_csv(file_path, encoding="utf-8", engine="python")
    df_merge = df[["Name", "Campsite", "Address", "similar_idx"]]
    df_merge.reset_index(names="idx", inplace=True)
    # 是否重複
    result_series = df.apply(lambda row: ifRepeat(row), axis=1)
    df_merge["repeat"] = result_series

    

    print(df)

if __name__ == "__main__":
    main()