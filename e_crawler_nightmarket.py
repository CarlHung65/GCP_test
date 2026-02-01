import requests
from bs4 import BeautifulSoup
import time
import pandas as pd



def crawler_nightmarket():
    """抓取夜市的wiki網址，回傳網頁文字"""

    url = "https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A3%E5%A4%9C%E5%B8%82%E5%88%97%E8%A1%A8#"
    headers = {
    "User-Agent": "WikiDataPipelineBot/1.0"
    "(data engineering practice on Wikipedia; contact: eszaqw6207@gmail.com)"
    }
    max_retries = 3 # 設定重抓網址的上限次數
    retries = 0

    while retries < max_retries:
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            return soup
        except Exception as e:
            retries += 1
            print(f"第{retries}次抓取失敗，原因: {e}")
            time.sleep(5)
        return None
            

def crawler_city(soup):
    """抓取城市名稱，回傳list"""
    citys = []
    for div in soup.find_all("div", class_="mw-heading mw-heading3"):
        city = div.select_one("h3 a").get("title")
        citys.append(city)
    return citys

def crawler_nightmarket_name(soup):
    """抓取夜市名稱，回傳list"""
    all_table = soup.find_all("table", class_="wikitable")
    nightmarkets = []
    for table in all_table:
        trs = table.find_all("tr")
        nightmarket_name = []
        for tr in trs:
            first_td = tr.find("td")
            if first_td:
                a_tag = first_td.find("a")
                if a_tag:
                    name = a_tag.get_text(strip=True)
                else:
                    name = first_td.get_text(strip=True)

                nightmarket_name.append(name)
        nightmarkets.append(nightmarket_name)
    return nightmarkets

def map_to_df(citys, nightmarkets):
    """把城市名稱和夜市名稱轉為df"""
    count = 0
    city = []
    nms = []
    for nightmarket in nightmarkets:
        for nm in nightmarket:
            city.append(citys[count])
            nms.append(nm)
        count += 1
    df = pd.DataFrame({
    "city" : city,
    "nightmarket_name" : nms,
    })
    return df

def main():
    soup = crawler_nightmarket()
    citys = crawler_city(soup)
    nightmarkets = crawler_nightmarket_name(soup)
    df = map_to_df(citys, nightmarkets)
    print(df)


if __name__ == ("__main__"):
    main()