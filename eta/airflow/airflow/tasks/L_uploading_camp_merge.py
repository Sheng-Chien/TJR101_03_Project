from pathlib import Path
from airflow.decorators import task
import pandas as pd
from utils.mysql_lib import MYSQL_CONN, update_with_filter, upsert_with_values, insert_with_values
import utils.mysql_lib as sql_lib

def uploading_camp_merge():
    file_path = Path("data/T_camp_name_merge.csv")
    df = pd.read_csv(file_path, encoding="utf-8", engine="python")

    # 取出相應的值
    data = []
    for idx, row in df.iterrows():
        value = {
            "name": row["Name"],
            "camping_site_name": row["Campsite"],
            "address": row["Address"],
        }
        data.append(value)

    table = sql_lib.merge_table
    stmt = upsert_with_values(table, data)
    trans = MYSQL_CONN.begin()
    result = MYSQL_CONN.execute(stmt)
    print(f"影響的列數：{result.rowcount}")
    trans.commit()

uploading_camp_merge()