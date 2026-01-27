import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

def AddDT(df):
    """輸入df 將date、time 整合成accident_datetime並刪除year、month、date、time欄位"""
    df['accident_time'] = df["accident_time"].astype(int).astype(str).str.zfill(6)
    df['accident_date'] = df["accident_date"].astype(int).astype(str)
    df['accident_datetime'] = df['accident_date'] + df['accident_time']
    df = df.drop(["accident_date", "accident_time", 
                  "accident_year", "accident_month"], axis=1)
    return df