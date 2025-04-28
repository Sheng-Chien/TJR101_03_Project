import requests
from bs4 import BeautifulSoup



#找<li role="presentation"> 底下有包含"住過露友評價"的a標籤的 href屬性
def get_review_links():
    #從露營頁面(/Store開頭)找到 評價的超連結
    url = 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    review_links = []
    Base_url = "https://www.easycamp.com.tw"
    ##以下待修改
    review_link_tag = soup.find("a",string="住過露友評價") #會是像<a href="...">下一頁</a>的tag物件
    review_links.append (Base_url + review_link_tag.get("href")) #/store/purchase_rank/899


"https://www.easycamp.com.tw/" + review_link #就是下面的url

url = "https://www.easycamp.com.tw/store/purchase_rank/2602" 