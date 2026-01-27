1. 規定欄位要是int但是裡面已經有文字在裡面沒辦法直接轉
    ，遇到不能轉的如何處理(row資料完全刪除)
```python
    df[pd.to_numeric(df.iloc[:, 0], errors="coerce").notna()]
```
to_numeric(要處理的範圍[row, columns], errors=遇到不能處理的要做甚麼處理.notna())notna回傳True和False，False是轉失敗的row整筆資料刪除

2. 將date和time結合成一個datetime欄位
- astype多次可以寫在同一行
- drop多個欄位可以用list
- drop要記得assing回去

修正版:
```python
def toDatetime(df):
    df['accident_time'] = df["accident_time"].astype(int).astype(str).str.zfill(6)
    df['accident_date'] = df["accident_date"].astype(int).astype(str)
    df['accident_datetime'] = df['accident_date'] + df['accident_time']
    df = df.drop(["accident_date", "accident_time", 
                  "accident_year", "accident_month"], axis=1)
    return df
```
