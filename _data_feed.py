import backtrader as bt
from datetime import datetime
import os

def questrade_feed(ticker,time_frame):
    # DATA PATH
    ticker_path = os.path.join(os.getenv("STOCK_DATA_PATH"),'OHLC',time_frame,f'{ticker}.csv')
    # TIME FORMAT
    if time_frame[-1] in ['m','s']:
        _format = '%Y-%m-%d %H:%M:%S'
    elif time_frame[-1] in ['D','W','M']:
        _format = '%Y-%m-%d'
        
    data = bt.feeds.GenericCSVData(
        dataname=ticker_path,
        fromdate = datetime(2019,1,1),
        name=ticker,
        nullvalue=0.0,
        dtformat=_format,
        datetime=0,
        low=3,
        high=4,
        open=5,
        close=6,
        volume=7,
        openinterest=-1,
        vwap=8
    )
    return data