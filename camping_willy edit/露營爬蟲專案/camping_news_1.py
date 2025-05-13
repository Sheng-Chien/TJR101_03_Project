from bs4 import BeautifulSoup
import requests 
import pandas as pd 
from pathlib import Path 

def main():
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    url = "https://www.womenshealthmag.com/tw/mental/gotravel/g44657060/six-glamping/"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"請求失敗,{response.status_code}")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 定義檔案路徑
    file_path = Path("C:/Users/super/OneDrive/桌面/PythonCrawler/Exercises/露營專案爬蟲/afile.html")
    
    # 寫入格式化後的 HTML 內容到檔案
    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(soup.prettify())

    # 可選擇性：列印格式化後的 HTML（用於除錯）
    # print(soup.prettify())
    
    content = []
    for i in soup.select("div.css-gd5gam.e16kmapv9"):
        camping_name = i.select_one("h2.css-1czfelb")
        if camping_name is not None:
            camping_name = camping_name.text.split("：")[-1].strip()
        camping_content = i.select_one("p.css-12e28k9.emevuu60").text.strip()
        camping_site = i.select_one("div.css-wutqs3.e16kmapv7 > p:nth-child(2)")
        if camping_site is not None:
            camping_site = camping_site.text.strip()

        # 將抓取到的資料添加到 content 列表
        content.append([camping_name, camping_content, camping_site])
        print(content)
        print("-" * 100)

        

     # 創建 DataFrame
    df = pd.DataFrame(content, columns=["露營名稱", "露營內容", "露營地址"])

    # 處理 "露營名稱" 欄位：取得 ":" 之後的部分
    # df['露營名稱'] = df['露營名稱'].str.split(":")[-1]  # 去除多餘空白

    # print(df)  # 顯示結果


    # 定義資料夾並確保它存在
    save_dir = Path("camping","露營爬蟲專案")
    save_dir.mkdir(parents=True, exist_ok=True)  # 如果資料夾不存在則建立

    # 定義 CSV 檔案路徑
    csv_path = save_dir / "camping_news_1.csv"
    df.to_csv(csv_path, header=True, index=False)

    # 定義 JSON 檔案路徑
    json_path = save_dir / "camping_news_1.json"
    df.to_json(json_path, orient="records", force_ascii=False, indent=4)

if __name__== "__main__":
    main()
