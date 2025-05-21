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

    # 🔽 加入標準化處理
    replacements = {
        "寵物同行": "寵物友善",
        "寵物友善免裝備露營": "寵物友善",
        "生態導覽": "導覽解說",
        "部落導覽": "導覽解說",
        "旅遊導覽": "導覽解說",
        "導覽解說": "導覽解說",
        "雲海": "雲海",
        "有雲海": "雲海",
        "有夜景": "夜景",
        "登山步道": "步道",
        "步道": "步道",
        "一帳包區": "少帳包區",
        "小包區": "少帳包區",
        "少帳包場": "少帳包區",
        "機車露營": "可車露",
        "可車露": "可車露",
        "營區賞螢": "賞螢",
        "周邊賞螢": "賞螢",
        "螢火蟲季": "賞螢",
        "營區採草莓": "果菜採收",
        "週邊採草莓": "果菜採收",
        "季節採果": "果菜採收",
        "餐點/咖啡":"餐飲服務"
    }

    to_remove = {"需注意清潔", "需綁鍊或放置籠內", "需先取得營主同意", "大型狗禁止", "入園需另購門票", "需收寵物清潔費","旅遊基地/景點"}

    # 標準化 service_items
    standardized_service = []
    for item in service_items:
        if item in to_remove:
            continue
        # 替換成標準化名稱（若在 mapping 中）
        standardized_value = replacements.get(item, item)
        if standardized_value not in standardized_service:
            standardized_service.append(standardized_value)
    
    # 將「衛浴配置」、「無線通訊」、「附屬設施」合併為 equipment list
    equipment_fields = ["衛浴配置", "無線通訊", "附屬設施"]
    raw_equipment_items = []
    for field in equipment_fields:
        text = camp_intro.get(field, "")
        items = [s.strip() for s in text.replace("\n", "").split("、") if s.strip()]
        raw_equipment_items.extend(items)

    # 標準化與過濾條件
    equipment_standardized = []
    added_set = set()  # 用來避免重複加入

    signal_keywords = [
        "3G/4G訊號", "中華電信有訊號", "遠傳有訊號", "台哥大有訊號",
        "台灣之星有訊號", "亞太有訊號", "其他家訊號不穩"
    ]
    #販賣部/販賣機
    #selling_keywords = ["販賣部/販賣機"]
    fridge_keywords = ["有冰箱", "冷藏", "冷凍"]
    play_keywords = ["溜滑梯", "鞦韆","玩沙池","戲水池"]
    remove_keywords = ["季節賞花", "開心農場", "攀岩", "攀樹", "山訓","塗鴨板"]

    for item in raw_equipment_items:
        if any(word in item for word in remove_keywords):
            continue
        elif item in fridge_keywords:
            if "冰箱" not in added_set:
                equipment_standardized.append("冰箱")
                added_set.add("冰箱")
        elif item in signal_keywords:
            if "無線通訊有訊號" not in added_set:
                equipment_standardized.append("無線通訊有訊號")
                added_set.add("無線通訊有訊號")
        elif item == "男女廁所":
            if "男女浴廁分開" not in added_set:
                equipment_standardized.append("男女浴廁分開")
                added_set.add("男女浴廁分開")
        elif item == "販賣部/販賣機":
            if "販賣部" not in added_set:
                equipment_standardized.append("販賣部")
                added_set.add("男女浴廁分開")
        elif item in play_keywords:
            if "兒童遊樂設施" not in added_set:
                equipment_standardized.append("兒童遊樂設施")
                added_set.add("兒童遊樂設施")
        else:
            if item not in added_set:
                equipment_standardized.append(item)
                added_set.add(item)

    #  移動 "有遊戲設施" 到 equipment 並標準化為 "兒童遊樂設施"
    if "有遊戲設施" in standardized_service:
        standardized_service.remove("有遊戲設施")
        if "兒童遊樂設施" not in added_set:
            equipment_standardized.append("兒童遊樂設施")
            added_set.add("兒童遊樂設施")

    #"有雨棚": "雨棚"
    if "有雨棚" in standardized_service:
        standardized_service.remove("有雨棚")
        if "雨棚" not in added_set:
            equipment_standardized.append("雨棚")
            added_set.add("雨棚")
    if "餐點/咖啡" in equipment_standardized:
        equipment_standardized.remove("餐點/咖啡")
        if "餐飲服務" not in standardized_service:
            standardized_service.append("餐飲服務")
            added_set.add("餐飲服務")


    # 回傳轉換後結果
    result = {
        "營地名稱": camp_name,
        "營地價格": price_table,
        "海拔": altitude,
        "service":  standardized_service,
        "equipment": equipment_standardized
    }
    return result

def main():
    current_dir = Path(__file__).parent
    input_path = current_dir / "easycamp_info_cleaned.json"
    with open(input_path, "r", encoding="utf-8") as file:
        cleaned_data = json.load(file)

    transformed_all = [transform_data(camp) for camp in cleaned_data]
    output_path = current_dir / "info_ready_for_db.json"
    with open(output_path, "w", encoding="utf-8") as f :
        json.dump(transformed_all, f, ensure_ascii=False, indent=2)

    print("✅")

if __name__ == "__main__":
    main()