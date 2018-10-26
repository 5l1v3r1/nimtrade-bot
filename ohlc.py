import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio
import requests

from datetime import datetime
import time

open_data = []
high_data = []
low_data = []
close_data = []
volume_nim = []
dates = []

periods = ["M1", "M3", "M15", "H1", "H4", "D1"]
limits = [180, 120, 96, 168, 180, 90] #How many periods per 1d/1w/1m
names = ["3h.png","6h.png","1d.png","1w.png","1m.png","3m.png"]
refresh = [1, 1, 1, 2, 4, 8]
delay = 300 # 5 minutes
s = 1e8 #scaling

count = 1

while True:
    for i in range(0,len(periods)):
        if refresh[i] % count != 0:
            continue

        try:
            r = requests.get("https://api.hitbtc.com/api/2/public/candles/NIMBTC", params = {'period': periods[i], 'limit': limits[i]})
        except:
            print("Error fetching {}".format(r.url))
            time.sleep(15)
            continue
        r = r.json()

        for v in r:
            dates.append(datetime.strptime(v["timestamp"], '%Y-%m-%dT%H:%M:%S.000Z'))
            open_data.append(float(v["open"])*s)
            high_data.append(float(v["max"])*s)
            low_data.append(float(v["min"])*s)
            close_data.append(float(v["close"])*s)
            volume_nim.append(int(v["volume"]))

        trace = go.Candlestick(x=dates,
                        open=open_data,
                        high=high_data,
                        low=low_data,
                        close=close_data,
                        yaxis = 'y2')

        layout = go.Layout(
            width = 900,
            height = 600,
            xaxis = dict(
                rangeslider = dict(visible = False),
                title = "time (utc)"),
            yaxis = dict(
                domain = [0, 0.2],
                showticklabels = False
            ),
            yaxis2 = dict(
                title = "price (sat)",
                domain = [0.2, 0.8]
            ),
            margin = dict( t=40, b=40, r=40, l=40 )
        )

        data = [trace]
        data.append(dict(x=dates, y=volume_nim, type='bar', yaxis='y', name='Volume'))

        trace = go.Figure(data=data,layout=layout)
        pio.write_image(trace, names[i])
        print("Saved {} @ {}".format(names[i], time.asctime(time.localtime(time.time()))))

        open_data,high_data,low_data,close_data,volume_nim,dates = [],[],[],[],[],[]

    time.sleep(delay)
