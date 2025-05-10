import json
import os
import pandas as pd
#將easycamp_reviews_cleaned.json轉為dataframe

# 讀取 JSON 檔案 (*檔案路徑)
def create_rating_df():
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'easycamp_reviews_cleaned.json')
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

# 將 JSON 轉成 DataFrame
    rows = []
    for item in data:
        rows.append({
            "name": item.get("營地名稱", ""),
            "total_rank": item.get("營地總星等", None),#
            "total_comments_count": item.get("評論總數", None),#
            "traffic_rating": item.get("交通便利度", None),#若有缺值寫none(NaN)
            "bathroom_rating": item.get("衛浴整潔度", None),
            "view_rating": item.get("景觀滿意度", None),
            "service_rating": item.get("服務品質", None),
            "facility_rating": item.get("設施完善度", None)
        })
    rating_df = pd.DataFrame(rows)
     # 將 NaN 轉換為 None，並確保數值可以處理
    rating_df = rating_df.where(pd.notnull(rating_df), None)
    #轉換為Int64(支援 NaN)
    int_columns = ["traffic_rating", "bathroom_rating", "view_rating", "service_rating", "facility_rating"]
    for col in int_columns:
        #rating_df[col] = rating_df[col].apply(lambda x: int(x) if pd.notnull(x) and str(x).strip() != '' else None)
        rating_df[col] = pd.to_numeric(rating_df[col], errors='coerce')  # 將無法轉換的值轉成 NaN
        rating_df[col] = rating_df[col].astype('Int64')  # 轉換為 Int64，這樣就能支援 NaN

    #print(rating_df.head())
    #print(rating_df.dtypes)  # 檢查是否正確為 object

    return rating_df


create_rating_df()