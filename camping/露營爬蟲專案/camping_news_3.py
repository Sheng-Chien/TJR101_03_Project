# import requests
# import json

# # 設定 API 的 URL 和參數
# api_url = "https://api-guest-prod-tier-1-wwclgij22a-an.a.run.app/api/guest/v1/store/list?only_show_user_like=false&key=AIzaSyAKQXJQUSQUChNI3-RklARZWaIzI5hh3ds"
# params = {
#     "location": "苗栗",
#     "type": "露營",
#     "category": "all"
# }

# # 發送 GET 請求
# response = requests.get(api_url)
# # response = requests.get(api_url, params=params)
# # 檢查回應狀態
# if response.status_code == 200:
#     # 解析 JSON 資料
#     data = response.json()
#     items =data["items"]
    
#     # 這裡假設回應是包含露營地資訊的列表
#     # camping_sites = data.get('g', [])
#     for i in items :
#         print(f"設備: {i['facility']}")
   
#         print("-" * 40)
# else:
#     print(f"無法獲取資料，HTTP 狀態碼: {response.status_code}")


print("----------------------")

import requests
from bs4 import BeautifulSoup
from pathlib import Path 


headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
# 網頁 URL
url = "https://travel.ettoday.net/article/2495141.htm"

# 發送 GET 請求
response = requests.get(url)

# 檢查回應狀態
if response.status_code == 200:
    # 解析 HTML 內容
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    file_path=Path("C:\TJR101_03_Project\camping\露營爬蟲專案\camping.html")
    with open(file_path,"w",encoding="UTF-8") as f:
        f.write(soup.prettify())
    show_items = []
    content = soup.find_all("div",class_="story")
    # print(len(content))
    # for x in content: 
    #     content_1 = x.find_all("p")  
    #     for y in content_1:
    #         show_items.append(y.get_text())
    print("-----------------")
    
    content = soup.find("div",class_="story")
    detail = content.find_all("p")
    for d in detail:
        show_items.append(d.text)
    print(show_items)

else:
    print(f"無法獲取資料，HTTP 狀態碼: {response.status_code}")

#newsContent > div > p:nth-child(8)