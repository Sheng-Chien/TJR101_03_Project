import os
from pathlib import Path
import json

dir_path = Path(__file__).parent/"results/temp"
# 取得所有檔案名稱
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

for file in files:
    file_path = dir_path/file
    # print(file_path)
    with open(file_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)
        response = data["candidates"][0]["content"]["parts"][0]["text"]
        print(file)
        print(response)