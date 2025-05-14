import json
from pathlib import Path

#CLEANED再清洗


def transform_data(data):
     # 從"營地資訊"抓營地名稱
    camp_info = data.get("營地資訊", {})
    camp_name = camp_info.get("營地名稱", "")
    # 整理價格資訊為二維陣列格式
    original_price_table = data.get("營地價格", [])
    price_table = []
    
    for row in original_price_table[1:]:  # 跳過表頭
        new_row = [row[1], row[4], row[5], row[6], row[7]]
        price_table.append(new_row)

    # 從"營區介紹"抓其他欄位
    camp_intro = data.get("營區介紹", {})
    altitude = camp_intro.get("海拔", "")

    # 將「營區特色」、「攜帶寵物規定」、「附屬服務」合併為 service list
    service_fields = ["營區特色", "攜帶寵物規定", "附屬服務"]
    service_items = []
    for field in service_fields:
        text = camp_intro.get(field, "")
        items = [s.strip() for s in text.replace("\n", "").split("、") if s.strip()]
        service_items.extend(items)

    # 將「衛浴配置」、「無線通訊」、「附屬設施」合併為 equipment list
    equipment_fields = ["衛浴配置", "無線通訊", "附屬設施"]
    equipment_items = []
    for field in equipment_fields:
        text = camp_intro.get(field, "")
        items = [s.strip() for s in text.replace("\n", "").split("、") if s.strip()]
        equipment_items.extend(items)

    # 回傳轉換後結果
    result = {
        "營地名稱": camp_name,
        "營地價格": price_table,
        "海拔": altitude,
        "service": service_items,
        "equipment": equipment_items
    }
    return result

def main():
    current_dir = Path(__file__).parent
    input_path = current_dir / "easycamp_info_cleaned.json"
    with open(input_path, "r", encoding="utf-8") as file:
        cleaned_data = json.load(file)

    transformed_all = [transform_data(camp) for camp in cleaned_data[:3]]
    output_path = current_dir / "info_ready_for_db.json"
    with open(output_path, "w", encoding="utf-8") as f :
        json.dump(transformed_all, f, ensure_ascii=False, indent=2)

    print("✅ 轉換完成")

if __name__ == "__main__":
    main()