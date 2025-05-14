import requests
from bs4 import BeautifulSoup


def main():
    url = "https://www.leagueoflegends.com/zh-tw/champions/?_gl=1*1a09ifb*_gcl_au*MTYwOTQwNjQxNi4xNzQ2NDE5OTI1*_ga*MTAyOTQ0ODg4Mi4xNzQ2NDE5OTI2*_ga_FXBJE5DEDD*MTc0NjQ1MzIxNi4zLjAuMTc0NjQ1MzIxNi4wLjAuMA.."
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    response = requests.get(url,headers = headers)
    if response.status_code != 200:
        print(f"請求失敗,請顯示{response.status_code}")
        return
    soup = BeautifulSoup(response.text,"html.parser")
    article = soup.select_one("div.sc-946e2cfc-0.dvjuUX")
    
    if not article:  # 檢查是否找到任何符合的元素
        print("沒有找到匹配的元素")
        return

    content = article.select("a")  # 從 article 中選擇所有的 <a> 標籤
    if not content:
        print("沒有找到任何鏈接")
        return
    # print(content)
    for x in content:
        print(x.get("href"))  # 使用 get() 可以防止 KeyError 如果 <a> 沒有 href 屬性



if __name__ == "__main__":
    print("===================================")
    main()
    print("===================================")