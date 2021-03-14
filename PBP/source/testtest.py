from __future__ import absolute_import, division, print_function, unicode_literals

import backtrader as bt
import pandas_datareader as web
import datetime
import numpy as np


class St(bt.Strategy):
    def __init__(self):
        pass
        # self.sma = bt.indicators.SimpleMovingAverage(self.data)


# data = bt.feeds.BacktraderCSVData(dataname="../../datas/2005-2006-day-001.txt")
stockData = web.DataReader(
    "^KQ11", "yahoo", datetime.datetime(2020, 2, 20), datetime.datetime(2021, 2, 20)
)[["Open", "Close"]]
dts = bt.feeds.PandasData(dataname=stockData, open="Open", close="Close")

cerebro = bt.Cerebro()
cerebro.adddata(dts)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot(volume=False)