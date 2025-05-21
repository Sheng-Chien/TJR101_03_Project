# 把MySQL的VIEW表下載成csv檔案

from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

host='104.199.214.113' # 主機位置
user='test' # 使用者名稱
port="3307" # 埠號
password='PassWord_1' # 密碼
url = f"mysql+pymysql://{user}:{password}@{host}:{port}/test2_db"
engine = create_engine(url, echo=True, pool_pre_ping=True)



current_dir = Path(__file__).parent

# 用pandas讀取articles表-----------------------
with engine.connect() as connection:
    df = pd.read_sql("SELECT articles_ID,platform_ID,camper_ID,campground_ID,article_type,publish_date,article_rank FROM articles", con=engine)

articles_table = current_dir/ "articles_no_content_table.csv"
df.to_csv(articles_table, encoding="utf-8-sig", index=False)
print("articles_no_content_table.csv下載完成")

# # 用pandas讀取equipment表-----------------------
# with engine.connect() as connection:
#     df = pd.read_sql("SELECT * FROM equipment", con=engine)

# equipment_table = current_dir/ "equipment_table.csv"
# df.to_csv(equipment_table, encoding="utf-8-sig", index=False)
# print("equipment_table.csv下載完成")

# 用pandas讀取campground表-----------------------
# with engine.connect() as connection:
#     df = pd.read_sql("SELECT * FROM campground", con=engine)

# campground_table = current_dir/ "campground_table.csv"
# df.to_csv(campground_table, encoding="utf-8-sig", index=False)
# print("campground_table.csv下載完成")