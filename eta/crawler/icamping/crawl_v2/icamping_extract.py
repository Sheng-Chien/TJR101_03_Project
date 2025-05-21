import json
from pathlib import Path
import requests
import time



def getAllCampInfo(session):
    # 取得全營地基本資料
    url = "https://api-guest-prod-tier-1-wwclgij22a-an.a.run.app/api/guest/v1/store/list?only_show_user_like=false&key=AIzaSyAKQXJQUSQUChNI3-RklARZWaIzI5hh3ds"
    response = session.get(url)

    if response.status_code != 200:
        print("request Fail")
        return

    print("secess")
    # 基本資料存檔
    data = json.loads(response.text)
    data_dir = Path(__file__).parent/"data"
    data_dir.mkdir(exist_ok=True, parents=True)
    file_path = data_dir/"E_icamping_all_camps.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    camps = data["items"]

    camp_site = []
    camp_info = []
    for camp in camps:
        print(f"處理 {camp["store_alias"]}")
        time.sleep(2)
        # 提取子目錄
        store_name = camp["store_name"]
        # 營位資訊
        camp_site.append(getCampSite(session, store_name))
        # 其他各種細項資訊
        camp_info.append(getCampgroundInfo(session, store_name))

    # 存檔
    file_path = data_dir/"E_camp_site.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(camp_site, file, indent=2, ensure_ascii=False)

    file_path = data_dir/"E_campground_info.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(camp_info, file, indent=2, ensure_ascii=False)


def getCampgroundInfo(session: requests.Session, store_name):
    url = f"https://api-guest-prod-tier-1-wwclgij22a-an.a.run.app/api/guest/v1/store/name/get?store_name={store_name}&key=AIzaSyAKQXJQUSQUChNI3-RklARZWaIzI5hh3ds"
    response = session.get(url)
    if response.status_code != 200:
        print(f"{store_name} failed!!!")
        return None

    data = json.loads(response.text)
    return data


def getCampSite(session: requests.Session, store_name):
    url = f"https://api-guest-prod-tier-1-wwclgij22a-an.a.run.app/api/guest/v1/stuff/store_name/list?store_name={store_name}&key=AIzaSyAKQXJQUSQUChNI3-RklARZWaIzI5hh3ds"
    response = session.get(url)
    if response.status_code != 200:
        print(f"{store_name} failed!!!")
        return None

    data = json.loads(response.text)
    return data


def main():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "referer": "https://m.icamping.app/",
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "accept": "application/json",
        "content-type": "application/json"
    }
    session = requests.Session()
    session.headers.update(headers)
    getAllCampInfo(session)


if __name__ == "__main__":
    main()
