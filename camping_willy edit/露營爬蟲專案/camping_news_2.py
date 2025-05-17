from bs4 import BeautifulSoup
import requests 
from pathlib import Path
import pandas as pd 
import re 
def main():
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    url="https://udn.com/news/story/7206/7166586"

    response = requests.get(url,headers = headers)
    if response.status_code!= 200:
        print(f"呼叫失敗,{response.status_code}")
        return
    soup = BeautifulSoup(response.text,"html.parser")
    content=[]
    # paragraph = soup.find_all("section",class_="article-content__editor")
    # if paragraph:
    #     for i in paragraph:
    #         content.append(i.get_text())
    # else:
    #     print("未找到指定的<P>標籤")
    # print(content)

    level1 = soup.find_all("section", class_="article-content__editor")
    for content1 in level1:
        level2 = content1.find_all("p")
        for content2 in level2:
            level3=content2.find_all("b")
            for content3 in level3:
                text = content3.get_text()
                content.append(re.search(r':\s*(.*)', content3) )
    print(content)

     # 將內容轉換為 DataFrame
    df = pd.DataFrame(content, columns=["Content"])  # 每個段落作為一列

    save_dir = Path("camping","露營爬蟲專案")
    df.to_csv(
        save_dir/"camping_news_2.csv",
        header=True,
        index=False
        )
    
    df.to_json(
        save_dir/"camping_news_2.json",
        orient="records", 
        force_ascii=False, 
        indent=4
        )
    

if __name__== "__main__":
    main()