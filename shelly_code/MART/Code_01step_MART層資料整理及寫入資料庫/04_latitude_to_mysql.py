# 把經緯度資訊寫入MySQL
# 已寫入，勿再重複執行
# 已寫入，勿再重複執行
# 已寫入，勿再重複執行

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DECIMAL
import pandas as pd
from pathlib import Path

# # 建立連線-------------------
# host='104.199.214.113' # 主機位置
# user='test' # 使用者名稱
# port="3307" # 埠號
# password='PassWord_1' # 密碼
# url = f"mysql+pymysql://{user}:{password}@{host}:{port}/test2_db"

# engine = create_engine(url, echo=True)

# Base = declarative_base()
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# 資料處理-------------------

file_path = Path(".venv", "MART", "result_csv")
info_file = file_path / "MART03_address_change_to_latitude.csv"
df = pd.read_csv(info_file, encoding="utf-8-sig")

# MySQL要先建好表單
class address_to_lat_lng(Base):
    __tablename__ = 'address_to_latitude_longitude'
    add_to_lat_lng_ID = Column(Integer, primary_key=True)
    campground_ID = Column(Integer, nullable=False)
    latitude = Column(DECIMAL(10,7), nullable=False)
    longitude = Column(DECIMAL(10,7), nullable=False)


# 寫入-------------------
records = []

for i in range(len(df)):
    row = df.iloc[i]
    record = address_to_lat_lng(
        campground_ID=int(row["campground_ID"]),
        latitude=float(row["lat"]),
        longitude=float(row["lng"])
    )
    records.append(record)

# 一次寫入全部
try:
    session.add_all(records)
    session.commit()
    print(f"資料寫入成功，共寫入{len(records)}筆")
except Exception as e:
    session.rollback()
    print("資料寫入失敗:", e)
finally:
    session.close()


