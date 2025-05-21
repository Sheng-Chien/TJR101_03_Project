import json
from pathlib import Path

def readJson(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    return data

def main():
    data_dir = Path(__file__).parent/"data"
    file_path = data_dir/"E_icamping_all_camps.json"
    all_camps_data = readJson(file_path)
    file_path = data_dir/"E_camp_site.json"
    camp_site_data = readJson(file_path)
    file_path = data_dir/"E_campground_info.json"
    campground_data = readJson(file_path)
    
    # 每個json的item才是真正內容
    all_camps_data = all_camps_data["items"]

    data = []
    for camp in camp_site_data:
        data.append(camp["items"])
    camp_site_data = data

    data = []
    for camp in campground_data:
        data.append(camp["items"])
    campground_data = data

    
    # 每個營區都是一個字典
    # 把 store name (pk) 當作字典的key
        





if __name__ == "__main__":
    main()