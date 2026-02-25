import pandas as pd
import ast

df = pd.read_csv("nightmarket.csv")
df['wt'] = df['wt'].str.replace(r'\s+', '', regex=True)
df['wt'] = df['wt'].apply(ast.literal_eval) # 把字串"[1,2,3]"轉成list
df = df.explode("wt") # 將字串所有元素垂直拆開，並將其他欄位複製
df["wt"] = df["wt"].str.replace("Open24hours", "00:00-11:59PM") # 把open24hours取代成時間
df["wt"] = df["wt"].str.replace("Closed", "")

# 把 wt 欄位 依照 ":" 前後各自切割成temp_split
temp_split = df["wt"].str.split(":", n=1 ,expand=True)
df['weekday'] = temp_split[0]
df['time_info'] = temp_split[1]

# 把所有長dash變成短dash
df['time_info'] = df['time_info'].str.replace("–", "-")

# 去所有空白
df['time_info'] = df['time_info'].str.replace(r'\s+', '', regex=True)
df['weekday'] = df['weekday'].str.replace(r'\s+', '', regex=True)

# 將一個欄位裡面有多個營業時間的分割
df['time_info'] = df['time_info'].str.split(',')
df = df.explode("time_info")

# 把 time_info 欄位 依照 "-" 前後各自切割成temp_split
temp_split = df["time_info"].str.split("-", n=1 ,expand=True)
df["open"] = temp_split[0]
df["close"] = temp_split[1]

# 把 open、close 欄位轉成時間格式
time_temp = pd.to_datetime(df['close'], format='mixed')
df["close"] = time_temp.dt.strftime("%H:%M")
time_temp = pd.to_datetime(df['open'], format='mixed')
df["open"] = time_temp.dt.strftime("%H:%M")
df = df.drop(columns="wt")
df = df.drop(columns="time_info")

df.to_csv("clear_nightmarket.csv", index=False, encoding='utf-8-sig')