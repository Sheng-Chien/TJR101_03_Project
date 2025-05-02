# 用SQLAlchemy讀取資料到pandas
from sqlalchemy import create_engine
import pandas as pd

# 建立連線
host='104.199.214.113' # 主機位置
user='test' # 使用者名稱
port="3307" # 埠號
password='PassWord_1' # 密碼
url = f"mysql+pymysql://{user}:{password}@{host}:{port}/test_shema"
print(url)
engine = create_engine(url, echo=True)
connection = engine.connect()

sql = """
select * from sample_data
"""
df = pd.read_sql(sql, connection)
print(df)

connection.close()

