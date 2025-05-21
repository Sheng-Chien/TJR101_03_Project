import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# 建立連線-----------------------
# host='104.199.214.113' # 主機位置
# user='test' # 使用者名稱
# port="3307" # 埠號
# password='PassWord_1' # 密碼
# url = f"mysql+pymysql://{user}:{password}@{host}:{port}/test2_db"
# engine = create_engine(url, echo=True, pool_pre_ping=True)

# with engine.connect() as connection:
#     df = pd.read_sql("SELECT * FROM campground_merge where name='willy'", con=engine)


# df.to_csv("campground_merged_edit.csv",index=False,encoding="UTF-8")
# print(df)

# df1 = df.dropna(subset=["campground_ID"])
# filepath=r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\gemini_results.csv"

# df_AI = pd.read_csv(filepath,encoding="UTF-8")
# df_AI["camper_ID"] = 46993
# df_AI["platform_ID"] = 3


file_path = Path(r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\gemini_results.csv")
df = pd.read_csv(file_path, encoding="utf-8")
df["clean_date"] = pd.to_datetime(
    df["date"].str.replace("  ", " ", regex=False).str.strip(),
    format="%Y年%m月%d日 %H:%M"
    ).dt.date
# print(df["clean_date"])
# print(df)

# 建立連線-----------------------
host='104.199.214.113' # 主機位置
user='test' # 使用者名稱
port="3307" # 埠號
password='PassWord_1' # 密碼
url = f"mysql+pymysql://{user}:{password}@{host}:{port}/test2_db"
engine = create_engine(url, echo=True, pool_pre_ping=True)


with engine.connect() as connection:
    df_sql_campground_merge = pd.read_sql("""
                                          
                                          SELECT name,camping_site_name,address,campground_ID FROM campground_merge where name='willy'
                                          
                                          """, con=engine)

df_merge = df.merge(df_sql_campground_merge,how='left',left_on='露營場名稱',right_on='camping_site_name')
# 若是campground_ID有重複的值就去重複
df_filtered = df_merge.dropna(subset=['campground_ID'])
print(df_filtered)

# 將df_merge裏頭有的欄位名提取出來重新命名匯進sql之articles的table欄位
df_insert_to_sql = df_filtered[['campground_ID','date','介紹']].rename(columns={'date':'publish_date','介紹':'content'})
df_insert_to_sql['article_type'] = '文章'
df_insert_to_sql['camper_ID'] = 46993
df_insert_to_sql['platform_ID'] = 3

df_insert_to_sql.to_sql('article',con=engine,if_exists='append',index=False)

# file_path = Path(r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\camping\露營爬蟲專案\gemini_results.csv")
# df = pd.read_csv(file_path, encoding="utf-8")

# ref_path = Path(r"C:\Users\super\OneDrive\桌面\露營爬蟲專案\camping_willy edit\campground_merged_edit.csv")
# df2 = pd.read_csv(ref_path, encoding="utf-8")

# result_df = df.merge(df2[["camping_site_name", "campground_ID"]], 
#                      left_on="露營場名稱", right_on="camping_site_name", 
#                      how="left")
# print(result_df["campground_ID"])