from pathlib import Path
import json
# from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from sqlalchemy.sql import and_


DATABASE_URL = "mysql+pymysql://test:PassWord_1@104.199.214.113:3307/eta"
engine = create_engine(DATABASE_URL, echo=False)
conn = engine.connect()
metadata = MetaData()

#要寫入的table
merge_table = Table('campground_merge', metadata, autoload_with=engine)
campground_table = Table('campground', metadata, autoload_with=engine)
equipment_table = Table('equipment', metadata, autoload_with=engine)
service_table = Table('service', metadata, autoload_with=engine)
camping_site_table = Table('camping_site', metadata, autoload_with=engine)
campers_table = Table('campers', metadata, autoload_with=engine)
articles_table = Table('articles', metadata, autoload_with=engine)


def selectTargetPK(camp_name):
    #從 merge_table 中查詢露營區的 campground_ID
    uploder = "YH"
    sql = select(merge_table.c.campground_ID).where(
        merge_table.c.name == uploder,
        merge_table.c.camping_site_name == camp_name,
    )

    with engine.connect() as conn:
        pk = conn.execute(sql).fetchall()

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
    conditions = [table.c[k] == v for k, v in filters.items()]#把filters字典中每個key-value轉換成一個條件表達式，如：table.c["name"] == "Alice"
    #如果 conditions 不為空（即有提供過濾條件），就使用 and_(*conditions) 將所有條件以 AND 方式組合起來
    #如果 filters 是空的（也就是 conditions 為空），那就直接執行 select(table)，等於沒有 WHERE 條件，查詢整個資料表
    sql = select(table).where(and_(*conditions)) if conditions else select(table)

    # 執行sql查詢並轉成 list of dicts
    with engine.connect() as conn:
        results = conn.execute(sql)
    
    # 把查詢結果 results 中的每一筆資料列（row），轉換成 Python 字典的形式
    rows_as_dicts = [dict(row._mapping) for row in results]
    
    # 檢查查詢是否正確 (確認只有一筆)
    if len(rows_as_dicts) > 1:
        print("檢索錯誤，查到多筆資料")
        for row in rows_as_dicts:
            print(row)
        return None
    elif len(rows_as_dicts) == 0:
        print("檢索資料不存在: Table: {table.name}, Filters: {filters}")
        return dict()
    
    data = rows_as_dicts[0]#只有一筆資料，把資料從list中拿出來(會是一個dic)
    return data

def update_table_with_filters(table, filters: dict, update_values: dict):
    # 組合 WHERE 條件 (filters)
    conditions = [table.c[k] == v for k, v in filters.items()]
    sql = update(table).where(and_(*conditions)).values(update_values)

    # 執行更新
    with engine.connect() as conn:
        result = conn.execute(sql)
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
    sql = insert(table).values(values)
    with engine.connect() as conn:
        conn.execute(sql)
        conn.commit()
        
def updateCampground(campground_ID, camp, camps_reviews):
    # 查詢條件：營區ID
    filters = {"campground_ID": campground_ID}
    data = query_table_with_filters(campground_table, filters)

    # 必須有查詢結果才新增營區
    if data is None or not data:
        print(f"{campground_ID} 錯誤的檢索")
        return

    # 更新名稱
    data["camping_site_name"] = camp["營地名稱"]
    # 更新高度
    altitude = camp["海拔"]
    if data["altitude"] is None:
        data["altitude"] = altitude
    elif altitude > data["altitude"]:
        data["altitude"] = altitude

    # print(data)
    # print(len(data))
 
    camp_name = camp["營地名稱"]
    #🔍 加入評論資訊 從 camps_reviews 中找出第一筆「營地名稱」等於 camp_name 的評論資料，如果找不到，就回傳 None
    review_data = next((r for r in camps_reviews if r["營地名稱"] == camp_name), None)
    if review_data:
        if "營地總星等" in review_data and review_data["營地總星等"] is not None:
            old_rank = data.get("total_rank")
            new_rank = review_data["營地總星等"]
            if old_rank is not None:
                data["total_rank"] = round((old_rank + new_rank) / 2, 2)
            else:
                data["total_rank"] = new_rank
        #data["total_comments_count"] = review_data.get("評論總數", data.get("total_comments_count"))
        data["traffic_rating"] = review_data.get("交通便利度", data.get("traffic_rating"))
        data["bathroom_rating"] = review_data.get("衛浴整潔度", data.get("bathroom_rating"))
        data["view_rating"] = review_data.get("景觀滿意度", data.get("view_rating"))
        data["service_rating"] = review_data.get("服務品質", data.get("service_rating"))
        data["facility_rating"] = review_data.get("設施完善度", data.get("facility_rating"))
    else:
        print(f"未找到 {camp_name} 的評論資料，略過評論更新")



    # 更新campground資料
    sql = update(campground_table).where(
        campground_table.c.campground_ID == campground_ID
    ).values(data)
    
    with engine.connect() as conn:
        conn.execute(sql)
        conn.commit()

def updateEquipment(campground_ID, camp):
    equipments = camp["equipment"]
    #content = "/".join(equipments)
    for equ in equipments:
        filters = {
            "campground_ID": campground_ID,
            "equipment_details": equ,        
        }
    
    # 查詢 equipment_table有沒有符合條件的資料
    # 如果有 → 嘗試更新
    #    沒有→新增資料

        if update_table_with_filters(equipment_table, filters, filters) == 0:
            insert_table(equipment_table, filters)

def updateService(campground_ID, camp):
    services = camp["service"]
    for ser in services:
        filters = {
        "campground_ID": campground_ID,
        "service_details": ser,          
        }
        if update_table_with_filters(service_table, filters, filters) == 0:
            insert_table(service_table, filters)        


def updateSite(campground_ID, camp):
    # 處理資料為camping_site_type_name
    # site_ID(PK), ground_ID(FK), type, price
    # 除了PK 對照資料，不存在則寫入，存在則更新
    rows = camp["營地價格"]
    # rows = [["碎石","$500","$1000","$1000","$1200"],
    #          ["草皮","$500","$1000","$1000","$1200"],
    #          ["草皮","$700","$1200","$1200","$1200"],
    #          ["草皮","$700","$1200","$1200","$1200"]]
    sites_and_price = []
    #[['碎石', 1200], ['草皮', 1200], ['草皮', 1200], ['草皮', 1200]]
    for row in rows:
        site_type = row[0]
        price_list = [int(p.replace("$", "")) for p in row[1:]if p not in ("-", "", None)]
        if not price_list:
            print(f"{camp['營地名稱']} 的某個營位價格全為空，跳過")
            continue
        max_price = max(price_list)
        sites_and_price.append([site_type, max_price])
         
    for item in sites_and_price:
        site_type = item[0]
        price = item[1]
        if len(site_type) > 10: # 跳過字數太長的
            print(f"跳過：{campground_ID} 的 site_type 超過10字：{site_type}")
            continue  

        filters = {
            "campground_ID": campground_ID,
            "camping_site_type_name": site_type,
        }
        data = query_table_with_filters(camping_site_table, filters)
        if data is None:
            # 查詢到多筆重複資料(依據query函式的邏輯)
            print(f"{campground_ID} Site 資料檢索出錯")
            return
        elif not data:
            # 沒有查詢到資料，新增
            data = {
                "campground_ID": campground_ID,
                "camping_site_type_name": site_type,
                "price": price,                
            }
            sql = insert(camping_site_table).values(data)
            with engine.connect() as conn:
                conn.execute(sql)
                conn.commit()
        else:
            # 有資料，作比對後更新
            if data["price"] > price:# 資料價格較高則不更新
                continue
            data["price"] = price
            update_table_with_filters(camping_site_table, filters, data)

def updateCampers(camp_name, camps_reviews):
    camp_review = next((r for r in camps_reviews if r["營地名稱"] == camp_name), None)
    if not camp_review:
        print(f"未找到 {camp_name} 的評論資料，略過評論更新")
        return
    reviews = camp_review.get("顧客評論", [])
    if not reviews:
        print(f"{camp_name} 沒有顧客評論，略過 campers 寫入")
        return
    
    camper_names = set()
    for r in reviews:
        camper_name = r.get("姓名")
        if not camper_name or camper_name in camper_names:
            continue
        camper_names.add(camper_name)

        filters = {
            "camper_name": camper_name,
            "platform_ID": 4,
        }
        
        if update_table_with_filters(campers_table, filters, filters) == 0:
            insert_table(campers_table, filters) 

def updateArticles(campground_ID, camp_name, camps_reviews):
    camp_review = next((r for r in camps_reviews if r["營地名稱"] == camp_name), None)
    if not camp_review:
        print(f"未找到 {camp_name} 的評論資料，略過評論更新")
        return
    reviews = camp_review.get("顧客評論", [])
    if not reviews:
        print(f"{camp_name} 沒有顧客評論，略過 Articles 寫入")
        return
    
    for review in reviews:
        # 提取評論資料
        publish_date = review.get("評論日期")
        article_rank = review.get("評分")
        content = review.get("content")
        camper_name = review.get("姓名")
        
        # 檢查是否有必要的資料
        if not publish_date or not article_rank or not content or not camper_name:
            print(f"缺少必要資料：{review}，跳過這條評論")
            continue
        
        # 根據姓名和 platform_ID 找到唯一的 camper_ID
        camper_filters = {"camper_name": camper_name, "platform_ID": 4}
        camper_data = query_table_with_filters(campers_table, camper_filters)
        if not camper_data:
            print(f"找不到 camper 資料：{camper_name}，跳過這條評論")
            continue
        camper_ID = camper_data.get("camper_ID")
        
        if not camper_ID:
            print(f"找不到 camper_ID，跳過這條評論：{review}")
            continue

        # 準備寫入資料
        article_data = {
            "platform_ID": 4,
            "camper_ID": camper_ID,
            "campground_ID": campground_ID,
            "publish_date": publish_date,
            "article_rank": article_rank,
            "content": content,
            "article_type": "評論",  # 固定值
        }
        
        # 檢查資料是否已存在
        article_filters = {
            "platform_ID": 4,
            "camper_ID": camper_ID,
            "campground_ID": campground_ID,
            "publish_date": publish_date,  # 假設評論日期唯一，避免重複寫入
        }
        
        if update_table_with_filters(articles_table, article_filters, article_data) == 0:
            insert_table(articles_table, article_data)
        else:
            print(f"已存在相同的評論資料，跳過寫入：{publish_date}")


def main():
    # info檔案
    info_file_path = Path(__file__).parent.parent / "T" /"info_ready_for_db.json"
    # 定位到 T資料夾底下的 json檔
    with open(info_file_path, "r", encoding="utf-8") as file:
        camps_info = json.load(file)
    # review檔案
    reviews_file_path = Path(__file__).parent.parent / "T"/"reviews_ready_for_db.json"
    with open(reviews_file_path, "r", encoding="utf-8") as f:
        camps_reviews = json.load(f)

# 依序處理每個營區
    for camp in camps_info:
        camp_name = camp["營地名稱"]
        # 取的營區的 campground_ID
        campground_ID = selectTargetPK(camp_name)
        print(camp_name,campground_ID)
        if campground_ID is None:
            print("檢索錯誤或不匯入資料")
            continue
        
        # updateCampground(campground_ID, camp, camps_reviews)

        # updateSite(campground_ID, camp)

        updateEquipment(campground_ID, camp)

        updateService(campground_ID, camp)

        # updateCampers(camp_name, camps_reviews)
        
        # updateArticles(campground_ID, camp_name, camps_reviews)

if __name__ == "__main__":
    main()

      