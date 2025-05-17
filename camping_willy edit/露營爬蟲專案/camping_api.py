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

headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
# 網頁 URL
url = "https://news.pchome.com.tw/living/lifetoutiao/20250325/index-74289314450983315009.html"

# 發送 GET 請求
response = requests.get(url)

# 檢查回應狀態
if response.status_code == 200:
    # 解析 HTML 內容
    soup = BeautifulSoup(response.text, "html.parser")
    
    show_items = []
    # print(soup.select("div[calss]"))
    # 假設要提取標題和內容
    for i in soup.select("div[calss]"):
        titie= i.select_one("calss > h3").text.strip()  # 假設標題在 <h1> 標籤中
        content = i.select_one("p").text.strip()  # 假設內容在 class="content" 的 div 中
        show_items.append([titie,content])
else:
    print(f"無法獲取資料，HTTP 狀態碼: {response.status_code}")

#newsContent > div > p:nth-child(8)