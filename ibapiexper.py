import datetime
from ib_insync import *

import pandas as pd
import mplfinance as mpf
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib.animation as animation
from matplotlib import style

from datetime import datetime

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)



#gets the total account and the availible funds
for v in ib.accountValues():
    if v.tag == 'NetLiquidationByCurrency' and v.currency == 'USD':
        netLiquidationValue = float(v.value)
        print('Net Liquidation Value: ', netLiquidationValue)
    elif  v.tag == 'AvailableFunds' and v.currency == 'USD':
        availableFunds = float(v.value)
        print('Account Cash Value: ', availableFunds)

#create a method that makes a contract from user input



contract1 = Stock('TSLA', 'SMART', 'USD')



# do stock analysis with pandas here #######################################################################

#use this eventually to get current price
#ticker = ib.ticker(contract1)
#ticker.marketPrice()

#1 pull data from here

bars = ib.reqHistoricalData(
        contract1,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1,
        keepUpToDate=False)

#print(bars)
#2 create empty df outside with orignal columns preset 
df1 = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

#3 loop to get individual bar and parse data and put accordingly into df columns 

#get the amount of bars of data curently
lenBars = len(bars)

for b in range(lenBars):
    b = int(b)
    df1.at[b, 'Date'] = bars[b].date
    df1.at[b, 'Open'] = bars[b].open
    df1.at[b, 'High'] = bars[b].high
    df1.at[b, 'Low'] = bars[b].low
    df1.at[b, 'Close'] = bars[b].close
    df1.at[b, 'Volume'] = bars[b].volume


#4 store df into a csv

df1 = df1.set_index(['Date'])

df1.to_csv('test1.csv')
 
print(df1)
#data = pd.read_csv('test.csv', index_col = 'Date')
#print(data)



############################################(%b %d %y %H %M')






