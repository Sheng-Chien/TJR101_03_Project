import requests
from bs4 import BeautifulSoup
import pandas as pd


def getPageContent():
    
    url = "https://markandhazyl.com/camping-in-miaoli/"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"請求失敗，status code: {response.status_code}")
        return
    # 建立BeautifulSoup物件
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    level1 = soup.select_one("div.entry-content.single-content")
    level2_title = level1.select("a > strong")[:17]
    # print(level2_title)
    for level3 in level2_title:
      title = level3.text.strip()
      link = level3.parent.get("href")
      level3_block = level3.find_parent("h3").next_siblings
      content = ""
      for p in level3_block:
        if p.name == "h3":
          break
        content += p.text

      #content = level3_block.find_next_sibling('p').get_text(strip=True)
      articles.append([title,link,content])

    # 將整頁所有文章轉存放至DataFrame
    df = pd.DataFrame(articles, columns=["title", "link", "content"])
    return df

def dataInfo(df):
    # 列出DataFrame資訊，以查詢哪些欄位有空值
    df.info()
    print(df)


def main():
    df = getPageContent()
    dataInfo(df)
    df.to_csv("articles.csv",encoding="utf-8")


if __name__ == "__main__":

    main()

