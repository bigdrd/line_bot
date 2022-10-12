# pandas for analysis
import pandas as pd
import math
# Plotly for charting
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import random
import matplotlib.patches as mpatches
import numpy as np

start_date = pd.to_datetime('2021-11-01 00:00')
end_date = pd.to_datetime('2021-11-30 23:59')                         

TF = 5
SMA_TF = 5
SMA_LENGHT = 1
SMA = 0
SPREAD = 341
TP = 284
SL = 130
BASE_SPREAD = 35675
TRAILING_STOP = 1



def getLine(n):
    tmp = BASE_SPREAD
    while 1:
        if tmp >= 70000:
            break
        if n < (tmp+SPREAD):
            return tmp,tmp+SPREAD
        tmp += SPREAD

column = ["timestamp","open","high","low","close","volume"]
btc_data = pd.read_csv("p.csv",names=column)

btc_data['timestamp'] = pd.to_datetime(btc_data['timestamp'])

btc_data_new = (btc_data['timestamp']>= start_date) & (btc_data['timestamp']<= end_date)
btc_data = btc_data.loc[btc_data_new]
btc_data = (btc_data.reset_index()
        .drop_duplicates(subset='timestamp', keep='last')
        .set_index('timestamp').sort_index())
btc_data = btc_data.shift(periods=-1)
btc_data.drop(btc_data.tail(1).index,inplace=True)




ohlc = {
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}



print(btc_data.head(20))

fig2 = btc_data.plot( y=["close"])
tmp2 = BASE_SPREAD
while 1:
    if tmp2 >= 70000:
        break
    fig2.hlines(y=tmp2, xmin='2020-09-10', xmax='2021-12-17', color='purple', label='test')
    tmp2 += SPREAD

WIN = 0
LOST = 0
WIN_AMOUNT = 0
LOSS_AMOUNT = 0

i = 1

trade = {"status":"close"}
UP_TRADED = None
BT_TRADED = None
DELAY_TIME = None
CAN_OPEN_TRADE = False
for row in btc_data.itertuples():
    price = row.close

    if i != 0 and i % 5 == 0:
        CAN_OPEN_TRADE = True
    else:
        CAN_OPEN_TRADE = False

    if i == 1:
        bt,up = getLine(price)

    print(price,row.Index,up,bt,CAN_OPEN_TRADE)
    if trade["status"] == "close" and CAN_OPEN_TRADE:
        if price > up and up != UP_TRADED and price <= (up+30):
            print(row.Index,"OPENLONG",price)
            trade["status"] = "open"
            trade["type"] = "long"
            trade["entry"] = price
            trade["trailing"] = price
            trade["entry_cover"] = False
            trade["sl"] = price - SL
            UP_TRADED = up
            DELAY_TIME = row.Index
            plt.scatter(row.Index,price,label="OPEN LONG",color="green",zorder=40)
        
        elif price < bt and bt != BT_TRADED and price >= (bt-30): #or row.Index >= DELAY_TIME+ pd.Timedelta(minutes=1))
            print(row.Index,"OPENSHORT",price)
            trade["status"] = "open"
            trade["type"] = "short"
            trade["sl"] = price + SL
            trade["entry"] = price
            trade["trailing"] = price
            trade["entry_cover"] = False
            BT_TRADED = bt
            DELAY_TIME = row.Index

            plt.scatter(row.Index,price,label="OPEN LONG",color="red",zorder=40)
    
    elif trade["status"] == "open":
        
        if trade["type"] == "long":
            
            if price >= trade["trailing"]:
                if trade["entry_cover"] == False:
                    trade["entry_cover"] = True
                    trade["sl"] = trade["entry"]
                    trade["trailing"] = price
                else:
                    trade["sl"] += (price - trade["trailing"])
                    trade["trailing"] = price
            else:
                if price <= trade["sl"]:
                    if price >= trade["entry"]:
                        print(row.Index,"CLOSELONG WITH PROFIT",price)
                        WIN_AMOUNT += (price - trade["entry"])
                        WIN += 1
                    else:
                        print(row.Index,"CLOSELONG WITH LOSS",price)
                        LOSS_AMOUNT += (trade["entry"] - price )
                        LOST += 1
                    plt.scatter(row.Index,price,label="OPEN LONG",color="orange",zorder=40)
                    trade = {"status":"close"}

        else:

            if price <= trade["trailing"]:
                if trade["entry_cover"] == False:
                    trade["entry_cover"] = True
                    trade["sl"] = trade["entry"]
                    trade["trailing"] = price
                else:
                    trade["sl"] -= (trade["trailing"] - price)
                    trade["trailing"] = price
            
            else:
                if price >= trade["sl"]:
                    if price <= trade["entry"]:
                        print(row.Index,"CLOSESHORT WITH PROFIT",price)
                        WIN_AMOUNT += (trade["entry"] - price)
                        WIN += 1
                    else:
                        print(row.Index,"CLOSESHORT WITH LOSS",price)
                        LOSS_AMOUNT += ( price - trade["entry"])
                        LOST += 1
                    plt.scatter(row.Index,price,label="OPEN LONG",color="black",zorder=40)
                    trade = {"status":"close"}

    if i != 0 and i % 5 == 0:
        bt,up = getLine(price)

    i += 1






TRADE_N = WIN + LOST
LORDO = WIN_AMOUNT-LOSS_AMOUNT
FEES = TRADE_N*(0.04*(60000/100))
NETTO = LORDO - FEES

print("WIN RATE",WIN,"/",LOST)
print("WIN AMOUNT",WIN_AMOUNT)
print("LOST AMOUNT",LOSS_AMOUNT)
print("FEES",FEES)
print("NET x 1BTC",NETTO)

print("START DATE",start_date)
print("END DATE",end_date)

print(f"TF {TF},SPREAD {SPREAD},SL {SL}, TRAILING {TRAILING_STOP},DELAY ON SAME LINE")



red_patch = mpatches.Patch(color='green', label='OPEN LONG')
blue_patch = mpatches.Patch(color='red', label='OPEN SHORT')
blue_patch2 = mpatches.Patch(color='cyan', label='TP LONG')
blue_patch3 = mpatches.Patch(color='orange', label='SL LONG')
blue_patch4 = mpatches.Patch(color='magenta', label='TP SHORT')
blue_patch5 = mpatches.Patch(color='black', label='SL SHORT')





plt.legend(handles=[red_patch, blue_patch,blue_patch2,blue_patch3,blue_patch4,blue_patch5])
plt.show()