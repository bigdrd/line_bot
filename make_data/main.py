from csv import reader
import csv
from datetime import datetime
import pandas as pd
import time
column_names = ["time", "open", "high","low","close","volume","close_time","q","n","t","tt","ttt"]
df = pd.read_csv("BTCUSDT-5m-2021-11-21.csv", names=column_names)
print(df.head(2))
a = df.close.tolist()

with open('5m_ma.csv', mode='w+') as out:
    out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


for i, j in df.iterrows():
    if i == 25:

        print(j.time,j.close)
    try:
        ma = sum(a[i-23:i+1])/24
    except:
        ma = None
    row = [j.time,j.close,ma]
    with open('5m_ma.csv', mode='a') as out:
        out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        out.writerow(row)

exit()
print("ok,fix start")
time.sleep(10)

column_names = ["time", "open", "ma"]
df = pd.read_csv("5m_ma.csv", names=column_names)

column_names = ["id", "price", "q","qq","i","time","ii"]
df2 = pd.read_csv("BTCUSDT-aggTrades-2021-11-21.csv", names=column_names)



with open('out.csv', mode='w+') as out:
    out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)



index = len(df2.index)
counter = 0
for i, j in df.iterrows():
    if (counter == len(df2.index)):
        break
    with open('out.csv', mode='a') as out:
        out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        out.writerow([j.time,j.open,j.ma])
    print(index)
    for n,m in df2.tail(index).iterrows():
        if int(m.time) > int(j.time) + 300000:
            print("OK")
            index = len(df2.index) - counter
            break
        with open('out.csv', mode='a') as out2:
            out2 = csv.writer(out2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            out2.writerow([m.time,m.price,j.ma])
        counter += 1



# # open file in read mode
# with open('out.csv', mode='w+') as out:
#     out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     out.writerow(["start"])

# with open('5m.csv', 'r') as read_obj:
#     candle = reader(read_obj)
#     for row in candle:
#         try:
#             ma = sum()
        
#         row2 = row.extend([ma])
#         with open('out.csv', mode='a+') as out:
#             out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             out.writerow(row2)

# with open('5m.csv', 'r') as read_obj:
#     candle = reader(read_obj)
#     for row in candle:
#         time = int(row[0]) + 300000
#         print(time)
#         l = [row[0],row[4]]
#         with open('out.csv', mode='a+') as out:
#             out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             out.writerow(l)

#         with open('ticks.csv', 'r') as read_obj2:
#             ticks = reader(read_obj2)
#             for row2 in ticks:
#                 l2 = [row2[4],row2[1]]
#                 time2 = int(row2[4])
#                 with open('out.csv', mode='a+') as out:
#                     out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                     out.writerow(l2)
#                 if time2 > time:
#                     break
