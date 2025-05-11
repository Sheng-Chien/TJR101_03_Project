import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定義爬蟲函式
def scrape_article(url: str) -> pd.DataFrame:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 嘗試從不同網站抓取資料
    title = ""
    date = ""
    content = ""

    if "travel.ettoday.net" in url:
        # ETtoday 網站爬取邏輯
        title = soup.find('h1', class_='title').text.strip() if soup.find('h1', class_='title') else "找不到標題"
        
        publish_time = soup.find('time', class_='date')
        date = publish_time.get_text(separator=' ', strip=True) if publish_time else "找不到發文日期"

        content_div = soup.find('div', class_='story')
        if content_div:
            p_tags = content_div.find_all('p')
            content = "\n".join(p_tag.text.strip() for p_tag in p_tags) if p_tags else "找不到內容"
        else:
            content = "找不到內容區塊"


    else:
        title = "不支援此網站"
        date = "不支援此網站"
        content = "不支援此網站"

    return pd.DataFrame([[title, date, content]], columns=["title", "date", "content"])

# 主程式：多網址、多CSV檔案
if __name__ == "__main__":
    urls = [
        "https://travel.ettoday.net/article/2889505.htm",
        "https://travel.ettoday.net/article/2833926.htm",
        "https://travel.ettoday.net/article/2798215.htm",
        "https://travel.ettoday.net/article/2802591.htm",
        "https://travel.ettoday.net/article/2693281.htm",
        "https://travel.ettoday.net/article/2688753.htm",
        "https://travel.ettoday.net/article/2685229.htm",
        "https://travel.ettoday.net/article/1051960.htm",
        "https://travel.ettoday.net/article/2598643.htm",
        "https://travel.ettoday.net/article/2213061.htm",
        "https://travel.ettoday.net/article/2936180.htm"
        
        # 你可以繼續加入更多網址
    ]

    start_index = 1  # 從 articles1.csv 開始命名

    for i, url in enumerate(urls, start=start_index):
        try:
            df = scrape_article(url)
            filename = f"articles{i}.csv"
            df.to_csv(filename, encoding="utf-8", index=False)
            print(f"✅ 儲存成功：{filename}")
        except Exception as e:
            print(f"❌ 錯誤：{url} -> {e}")


        df.str.replace("#"," ")
