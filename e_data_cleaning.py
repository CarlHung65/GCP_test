import pandas as pd
import requests 
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np 

def addDT(df):
    """輸入df 將date、time 整合成accident_datetime並刪除year、month、date、time欄位"""
    df['accident_time'] = df["accident_time"].astype(int).astype(str).str.zfill(6)
    df['accident_date'] = df["accident_date"].astype(int).astype(str)
    df['accident_datetime'] = df['accident_date'] + df['accident_time']
    df = df.drop(["accident_date", "accident_time", 
                  "accident_year", "accident_month"], axis=1)
    return df

def clear_age(df):
    """輸入df 將gender不是 "男" 或 "女" 的age改成空值"""
    df.loc[~df["gender"].isin(["男", "女"]), "age"] = np.nan
    return df

