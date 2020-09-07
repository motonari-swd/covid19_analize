import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime,sys
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#df = pd.read_csv("https://dl.dropboxusercontent.com/s/6mztoeb6xf78g5w/COVID-19.csv",
df = pd.read_csv("COVID-19_old.csv",
                 parse_dates=['確定日', '発症日'], low_memory=False)
#print(df['確定日']- df['発症日'])
#for i in df:
#    print(i)
# 再陽性を削除
df = df[['再陽性' not in x for x in df['備考'].astype(str)]].copy()
#df = df[df['受診都道府県'] != '東京都']
#df = df[[ x>3000 for x in df['通し']]].copy()
dtx = type(pd.to_datetime('2014-11-09 10:00'))
df = df[ [isinstance(x,dtx) for x in df['発症日']] ].copy()

df.info()
#sys.exit()
#print(['再陽性' in x for x in df['備考'].astype(str)])

b = np.arange(min(min(df['確定日']), min(df['発症日'])),
              max(max(df['確定日']), max(df['発症日'])) + datetime.timedelta(days=2),
              datetime.timedelta(days=1))
fig, ax   = plt.subplots()
locator   = mdates.AutoDateLocator()
formatter = mdates.AutoDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
#for i in df['発症日']:
#    if isinstance(i,dtx): print(i,type(i))
#sys.exit()
   
dt = (df['確定日'] - df['発症日']).dt.days
data,bin,ccc=ax.hist(dt, bins=np.arange(0, 40), color="lightgray", edgecolor="black")
print('xxxxxxxxxxxxxxxxxxxxxx')
print(data)
print(bin)
ax.legend(['days (confirmed date - onset date)'])
ax.text(0.98, 0.87, 'median: ' + str(np.median(dt.dropna())),
        horizontalalignment='right', transform=ax.transAxes)
#ax.set_xlim(datetime.datetime(2020,2,1), b[-1])
#fig.savefig('200312b.svg', bbox_inches="tight")
#sys.exit()

