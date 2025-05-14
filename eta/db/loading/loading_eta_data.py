from pathlib import Path
import json
# from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from sqlalchemy.sql import and_


DATABASE_URL = "mysql+pymysql://test:PassWord_1@104.199.214.113:3307/test2_db"
engine = create_engine(DATABASE_URL, echo=False)
conn = engine.connect()
metadata = MetaData()

merge_table = Table('campground_merge', metadata, autoload_with=engine)
campground_table = Table('campground', metadata, autoload_with=engine)
county_table = Table('county', metadata, autoload_with=engine)
equipment_table = Table('equipment', metadata, autoload_with=engine)
service_table = Table('service', metadata, autoload_with=engine)
camping_site_table = Table('camping_site', metadata, autoload_with=engine)


def selectTargetPK(camp_name):
    uploder = "Eta"
    stmt = select(merge_table.c.campground_ID).where(
        merge_table.c.name == uploder,
        merge_table.c.camping_site_name == camp_name,
    )

    with engine.connect() as conn:
        pk = conn.execute(stmt).fetchall()

    # 理應精準比對只回傳 1筆資料
    if len(pk) > 1:
        print("檢索錯誤")
        for line in pk:
            print(camp_name)
            print(line)
            return None
    return pk[0][0]



def query_table_with_filters(table: str, filters: dict):
    """回傳一筆精準查詢，查到多筆回傳None，沒有資料回傳{}"""
    # 組合 where 條件
    conditions = [table.c[k] == v for k, v in filters.items()]
    stmt = select(table).where(and_(*conditions)) if conditions else select(table)

    # 執行查詢並轉成 list of dicts
    with engine.connect() as conn:
        results = conn.execute(stmt)
    
    # 轉成字典以利程式
    rows_as_dicts = [dict(row._mapping) for row in results]
    
    # 檢查查詢是否正確
    if len(rows_as_dicts) > 1:
        print("檢索錯誤，查到多筆資料")
        for row in rows_as_dicts:
            print(row)
        return None
    elif len(rows_as_dicts) == 0:
        # print("檢索資料不存在")
        return dict()
    
    # 確認只有一筆資料後
    data = rows_as_dicts[0]
    return data

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


def updateCampground(campground_ID, camp):
    # 查詢條件：營區ID
    filters = {"campground_ID": campground_ID}
    data = query_table_with_filters(campground_table, filters)

    # 不得新增營區，必須有查詢結果
    if data is None or not data:
        print(f"{campground_ID} 錯誤的檢索")
        return
    # print(data)
    # print(len(data))

    # 更新我的資料
    # 更新名稱
    data["camping_site_name"] = camp["name"]
    # 更新高度
    altitude = int(camp["altitude"])
    if data["altitude"] is None:
        data["altitude"] = altitude
    elif altitude > data["altitude"]:
        data["altitude"] = altitude
    
    # print(data)
    # print(len(data))

    # 更新campground資料
    stmt = update(campground_table).where(
        campground_table.c.campground_ID == campground_ID
    ).values(data)
    
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()
    
def updateEquipment(campground_ID, camp):
    equipments = camp["equipment"]
    for equipment in equipments:
        filters = {
        "campground_ID": campground_ID,
        "equipment_details": equipment,          
        }
        # 因為只有 2欄，只有"重複"和"沒有"這種選項
        # 重複則更新相同資料(等同沒做事)
        # 沒有則改為新增資料
        if update_table_with_filters(equipment_table, filters, filters) == 0:
            insert_table(equipment_table, filters)



def updateService(campground_ID, camp):
    services = camp["special"]
    for ser in services:
        filters = {
        "campground_ID": campground_ID,
        "service_details": ser,          
        }
        # 因為只有 2欄，只有"重複"和"沒有"這種選項
        # 重複則更新相同資料(等同沒做事)
        # 沒有則改為新增資料
        if update_table_with_filters(service_table, filters, filters) == 0:
            insert_table(service_table, filters)        


def updateSite(campground_ID, camp):
    # 處理資料為site_type
    # site_ID(PK), ground_ID(FK), type, price
    # 除了PK 對照資料，不存在則寫入，存在則更新
    sites = camp["location"]
    for site in sites:
        price = int(site[1])
        site_type = site[2]
        if len(site_type) > 10:
            # 資料表結構限制
            continue
        filters = {
            "campground_ID": campground_ID,
            "camping_site_type_name": site_type,
        }
        data = query_table_with_filters(camping_site_table, filters)
        if data is None:
            # 查詢到多筆重複資料
            print(f"{campground_ID} Site 資料檢索出錯")
            return
        elif not data:
            # 沒有查詢到資料，新增
            data = {
                "campground_ID": campground_ID,
                "camping_site_type_name": site_type,
                "price": price,                
            }
            stmt = insert(camping_site_table).values(data)
            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()
        else:
            # 有資料，作比對後更新
            if data["price"] > price:
                # 資料價格較高則不更新
                continue
            data["price"] = price
            update_table_with_filters(camping_site_table, filters, data)


def main():
    file_path = Path(__file__).parent/"classfied_all.json"
    with open(file_path, "r", encoding="utf-8") as file:
        camps = json.load(file)
    
    # 依序處理每個營區
    i = 0
    for camp in camps:
        i+=1
        if i < 75:
            continue
        print(f"正在處理第 {i} 筆資料")
        camp_name = camp["name"]
        print(camp_name)

        # 取的該營區的 campground_ID
        campground_ID = selectTargetPK(camp_name)
        # print(campground_ID)
        if campground_ID is None:
            print("檢索錯誤或不匯入資料")
            continue
        
        # 有 3 個資料格式錯誤無法讀取，先跳過
        try:
            _ = camp["equipment"]
        except:
            continue


        # updateCampground(campground_ID, camp)

        updateSite(campground_ID, camp)

        # updateEquipment(campground_ID, camp)

        # updateService(campground_ID, camp)

        # break



if __name__ == "__main__":
    main()

conn.close()