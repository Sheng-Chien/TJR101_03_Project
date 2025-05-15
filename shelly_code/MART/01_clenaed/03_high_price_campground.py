# 取出高價營位(價格屬於前25%的營位)的露營場
# 再合併其他露營場資訊

import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

# 建立連線-----------------------
host='104.199.214.113' # 主機位置
user='test' # 使用者名稱
port="3307" # 埠號
password='PassWord_1' # 密碼
url = f"mysql+pymysql://{user}:{password}@{host}:{port}/test2_db"
engine = create_engine(url, echo=True, pool_pre_ping=True)

# 用pandas讀取營位表
with engine.connect() as connection:
    df1 = pd.read_sql("SELECT * FROM camping_site", con=engine)

rank_q3 = df1["price"].quantile(0.75) # 75%

df1.loc[df1["price"].notnull() & (df1["price"] >= rank_q3), "high_price_site"] = "高價營位"

# 排除非高價營位的營位資料--------------------------

df1 = df1[df1["high_price_site"] == "高價營位"]

# 合併其他露營場的資訊------------------------------
file_path = Path(".venv", "MART", "result_csv")
ref_file = file_path / "MART03_address_change_to_latitude.csv"

df2 = pd.read_csv(ref_file, encoding="utf-8-sig")

result_df = df1.merge(df2[["campground_ID", "camping_site_name", "address", "total_rank", 
                          "total_comments_count", "campground_category", "hot", 
                          "negative_ratio", "lat", "lng"]], on="campground_ID", how="left")


# 整併各露營場的TAG，從多列變成一列-------------
# 寫入TAG

tag_file = file_path / "MART01_ai_add_campground_tag.csv"
df3 = pd.read_csv(tag_file, encoding="utf-8-sig")
# 改欄位名字
df3.rename(columns={"露營場ID": "campground_ID"}, inplace=True)


# 合併同一露營場的 TAG（以 campground_ID 為主）
df3_grouped = (
    df3.groupby("campground_ID")
    .agg({
        "Tag": lambda x: "｜".join(sorted(set(tag for tags in x for tag in str(tags).split("｜"))))
    })
    .reset_index()
    )

result_df = result_df.merge(df3_grouped, on="campground_ID", how="left")
# # 保留有Tag的露營場
# result_df = result_df[result_df["Tag"].notna()]


save_name = file_path / "MART03_high_price_campground.csv"
result_df.to_csv(save_name, encoding="utf-8-sig", index=False)
print("OK")

