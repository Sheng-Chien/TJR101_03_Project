import json
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from sqlalchemy.sql import and_

DATABASE_URL = "mysql+pymysql://test:PassWord_1@104.199.214.113:3307/eta"
engine = create_engine(DATABASE_URL, echo=False)
conn = engine.connect()
metadata = MetaData()
equipment_table = Table('equipment', metadata, autoload_with=engine)
service_table = Table('service', metadata, autoload_with=engine)

def update_table_with_filters(table, filters: dict, update_values: dict):

    # 組合 WHERE 條件
    conditions = [table.c[k] == v for k, v in filters.items()]
    stmt = update(table).where(and_(*conditions)).values(update_values)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        affacted = result.rowcount
        if affacted == 1:
            conn.commit()
        elif affacted > 1:
            conn.rollback()
            print("資料更改過多")
        else:
            conn.rollback()
            # print("沒有更改資料")

    return affacted  # 回傳受影響的列數

def insert_table(table, values:dict):
    stmt = insert(table).values(values)
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


def replace_substrings(s, replace_list, replacement):
    for substr in replace_list:
        s = s.replace(substr, replacement)
    return s

def replace_if_contains(A: list[str], B: str, C: str, exception="!") -> list[str]:
    return [s if exception in s else (C if B in s else s) for s in A]

def remove_values(lst: list, values_to_remove: list) -> list:
    return [x for x in lst if x not in values_to_remove]


def NFitems(data:list)->list:
    # 去除地名
    to_remove = ["台北", "新北", "基隆", "桃園",
               "苗栗", "新竹", "宜蘭", "台中",
                 "彰化", "南投", "雲林", "嘉義",
                   "台南", "高雄", "屏東", "花蓮", "台東"]
    data = [replace_substrings(s, to_remove, "" ) for s in data]
    data = replace_if_contains(data, "玩水", "")

    data = replace_if_contains(data, "遊樂", "兒童遊樂設施")
    to_replace = ["溜滑梯", "盪鞦韆"]
    data = [replace_substrings(s, to_replace, "兒童遊樂設施" ) for s in data]
    to_replace = ["洗髮乳", "沐浴乳"]
    data = [replace_substrings(s, to_replace, "沐浴髮品" ) for s in data]

    data = replace_if_contains(data, "WIFI", "有wifi")
    data = replace_if_contains(data, "溪", "近溪流")
    data = replace_if_contains(data, "手做", "DIY活動")
    data = replace_if_contains(data, "手作", "DIY活動")


    data = replace_if_contains(data, "包", "少帳包區", "包區專用衛浴")
    data = replace_if_contains(data, "男女廁所", "男女浴廁分開")
    data = replace_if_contains(data, "在地好味", "在地美味")
    data = replace_if_contains(data, "訊號", "無線通訊有訊號")
    data = replace_if_contains(data, "冰", "冰箱")
    data = replace_if_contains(data, "凍", "冰箱")
    data = replace_if_contains(data, "螢", "賞螢")
    data = replace_if_contains(data, "步道", "步道")
    data = replace_if_contains(data, "櫻", "賞櫻")
    data = replace_if_contains(data, "餐", "餐飲服務")
    data = replace_if_contains(data, "森林", "森林")
    data = replace_if_contains(data, "泡湯", "泡湯")
    data = replace_if_contains(data, "租", "裝備出租")
    data = replace_if_contains(data, "沙坑", "兒童遊樂設施")
    data = replace_if_contains(data, "戲水池", "兒童遊樂設施")
    data = replace_if_contains(data, "草莓", "採草莓")
    data = replace_if_contains(data, "車露", "可車露")

    # 移除特定值
    value_to_remove = [
        "", "泰安", "大興村", "埔里", "和平",
          "國姓", "關西", "南庄", "日月潭"
    ]
    data = remove_values(data, value_to_remove)

    # 去除重複
    data = list(set(data))

    return data


def classification(data:list):
    equipment = []
    special = []
    file_path = Path(__file__).parent/"data/equipment.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        filter_list = [line.strip() for line in f]
    
    equipment = [x for x in data if x in filter_list]         # 交集
    special = [x for x in data if x not in filter_list]     # 差集
    
    result = {
        "equipment": equipment,
        "special": special,
    }
    return result


def main():
    # 讀取設備以及特色
    file_path = Path(__file__).parent/"data/E_campground_info.json"
    with open(file_path, "r", encoding="utf-8") as file:
        camp_data = json.load(file)

    # 提取營區名稱以及設備特色
    facility = dict()
    for camp in camp_data:
        store_name = camp["items"]["store_name"]
        store_alias = camp["items"]["store_alias"]
        store_facility = camp["items"]["facility"]
        facility[store_name] = {
            "campground": store_alias,
            "facility": store_facility,
        }
    
    # 分類
    data = dict()
    for key, value in facility.items():

        fac = NFitems(value["facility"])
        result = classification(fac)
        data[key] = {
            "camping_site_name": value["campground"],
            "equipment_details": result["equipment"],
            "service_details": result["special"],
        }
    
    # 分別取出 設備 及 特色
    df = pd.DataFrame(data).T
    df_equipment = df[["camping_site_name", "equipment_details"]]
    df_equipment = df_equipment.explode("equipment_details")
    df_special = df[["camping_site_name", "service_details"]]
    df_special = df_special.explode("service_details")

    # df_equipment.to_sql("eta_equipment", con=engine, if_exists="replace", index=False)
    # df_special.to_sql("eta_special", con=engine, if_exists="replace", index=False)

    # 讀取 campground_merge 以取得 campground_ID
    df_campground_merge = pd.read_sql("select * from campground_merge", con=engine)
    df_campground_merge = df_campground_merge[["name", "camping_site_name", "campground_ID"]]
    # 保證是ETA的營地
    df_campground_merge = df_campground_merge[df_campground_merge["name"] == "Eta"]
    
    # EQUIPMENT
    # 把campground_ID 合併
    df_insert = df_equipment.merge(df_campground_merge, how="left", on="camping_site_name")
    df_insert.dropna(inplace=True)
    df_insert.drop(["name", "camping_site_name"], axis=1, inplace=True)
    df_insert["campground_ID"] = df_insert["campground_ID"].astype(int)
    df_insert.reset_index(inplace=True, drop=True)

    print("inserting equipments")
    for idx, row in df_insert.iterrows():
        if idx % 20 == 0:
            print(f"insert equipment {idx} / {len(df_insert)}")
        row_dict = row.to_dict()
        if update_table_with_filters(equipment_table, row_dict, row_dict) == 0:
            insert_table(equipment_table, row_dict)

    
    # SPECIAL
    # 把campground_ID 合併
    df_insert = df_special.merge(df_campground_merge, how="left", on="camping_site_name")
    df_insert.dropna(inplace=True)
    df_insert.drop(["name", "camping_site_name"], axis=1, inplace=True)
    df_insert["campground_ID"] = df_insert["campground_ID"].astype(int)
    df_insert.reset_index(inplace=True, drop=True)
    print(df_insert)
    # return
    
    print("inserting specials")
    for idx, row in df_insert.iterrows():
        if idx % 20 == 0:
            print(f"insert specials {idx} / {len(df_insert)}")
        row_dict = row.to_dict()
        if update_table_with_filters(service_table, row_dict, row_dict) == 0:
            insert_table(service_table, row_dict)


if __name__ == "__main__":
    main()