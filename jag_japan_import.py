import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime
import collections,re
df = pd.read_csv("COVID-19.csv",
                 parse_dates=['確定日', '発症日'], low_memory=False)

# 再陽性を削除
df = df[['再陽性' not in x for x in df['備考'].astype(str)]].copy()

cdic=collections.Counter(df["確定日"])
_date=cdic.keys()
confirm=[cdic[key] for key in _date]


def adapt_zero(str1):
        if len(str1)==1:
                str1="0"+str1
        return str1

date=[adapt_zero(str(day.day))+"/"+adapt_zero(str(day.month))+"/"+str(day.year) for day in _date]

print(date)
#print(confirm)





