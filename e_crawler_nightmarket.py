import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import googlemaps
import os
from dotenv import load_dotenv

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

def get_location(df):
    """把有city和nightmarket_name的df新增location"""
    # 先用dotenv的函式抓取api key 預設會抓當前目錄，若在其他目錄則要給予相對路徑
    # 不會覆蓋已存在的環境變數。
    load_dotenv()
    # 用os套件的getenv來獲取api key
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    full_name = df["city"]+df["nightmarket_name"]
    lats = []
    lngs = []
    place_id = []
    for name in full_name:
        gm = gmaps.geocode(name)
        lat = gm[0]['geometry']['location']['lat']
        lng = gm[0]['geometry']['location']['lng']
        p_id = gm[0]["place_id"]
        lats.append(lat)
        lngs.append(lng)
        place_id.append(p_id)
    df = pd.DataFrame({
    "city" : df["city"],
    "nightmarket_name" : df["nightmarket_name"],
    "latitude": lats,
    "longitude": lngs,
    "place_id": place_id,
    })
    return df

def get_oh_url(df):

    pids = df["place_id"]
    load_dotenv()
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    
    wts = []
    urls = []
    for pid in pids:
        res = gmaps.place(
            place_id=pid,
            fields=["opening_hours", "url"]
            )
        result = res.get("result", {})

        wt = result.get("opening_hours", {}).get("weekday_text",[])
        url = result.get("url")

        wts.append(wt)
        urls.append(url)

    df = pd.DataFrame({
    "city" : df["city"],
    "nightmarket_name" : df["nightmarket_name"],
    "latitude": df["latitude"],
    "longitude": df["longitude"],
    "place_id": df["place_id"],
    "wt": wts,
    "url": urls,
    })
    return df

def main():
    soup = crawler_nightmarket()
    citys = crawler_city(soup)
    nightmarkets = crawler_nightmarket_name(soup)
    df = map_to_df(citys, nightmarkets)
    df_2 = get_location(df)
    df_3 = get_oh_url(df_2)
    df_3.to_csv('nightmarket.csv', index=False, encoding='utf-8-sig')

if __name__ == ("__main__"):
    main()