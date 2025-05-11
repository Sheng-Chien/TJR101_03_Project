# 從資料庫下載比對用的露營場表

from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

# 建立連線
host='104.199.214.113' # 主機位置
user='test' # 使用者名稱
port="3307" # 埠號
password='PassWord_1' # 密碼
url = f"mysql+pymysql://{user}:{password}@{host}:{port}/test2_db"
# print(url)
engine = create_engine(url, echo=True)
connection = engine.connect()

# 用pandas讀取

df1 = pd.read_sql("SELECT * FROM campground_merge where name='shelly'", con=engine)

df2 = pd.read_sql("SELECT * FROM county", con=engine)

df3 = pd.read_sql("SELECT * FROM campers", con=engine)

df4 = pd.read_sql("SELECT * FROM platform", con=engine)

# 存檔
save_path = Path(".venv", "project", "l_data_to_mysql")
df1.to_csv(save_path / "ref_campground.csv", index=False, encoding="utf-8-sig")
df2.to_csv(save_path / "ref_county.csv", index=False, encoding="utf-8-sig")
df3.to_csv(save_path / "ref_campers.csv", index=False, encoding="utf-8-sig")
df4.to_csv(save_path / "ref_platform.csv", index=False, encoding="utf-8-sig")

print("存檔成功")

connection.close()

