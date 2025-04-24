import json
import csv
from pathlib import Path

def parse_file_to_str(file_path)->str:
    """
    將檔案轉為可以傳送的字串
    .csv / .json / .txt
    """
    # 取得副檔名
    file_extension = Path(file_path).suffix

    data = ""
    # 分解.csv
    if file_extension == ".csv":
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            csv_data = [row for row in reader]
            data = json.dumps(csv_data, ensure_ascii=False, indent=2)

    # 分解.json
    elif file_extension == ".json":
        with open(file_path, mode="r", encoding="utf-8") as file:
            json_file = json.load(file)
            data = json.dumps(json_file, ensure_ascii=False, indent=2)

    # 分解.txt
    elif file_extension == ".txt":
        with open(file_path, mode="w", encoding="utf-8") as file:
            data = file.read()
    
    else:
        print("不支援的檔案格式")
            
    if data:
        print("檔案讀取成功")
    
    return data