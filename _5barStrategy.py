import os
from datetime import datetime
import backtrader as bt
from _data_feed import questrade_feed

class TestStrategy(bt.Strategy):
    
    """Logging function for this strategy"""
    def log(self, txt,dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()} >> {txt}")
        
    def __init__(self):
        """Keep ref. to close in data[0] series"""
        self.dataclose = self.datas[0].close
        # To keep track of pending orders | buy price | commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.grossprofit = 0
        self.netprofit = 0
        
    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell Order submitted/accepted to/by broker - Nothing to do
            return
        
        # Check if an order has been completed
        # Broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED! Price: {order.executed.price} | Cost: {order.executed.value} | Comm: {order.executed.comm}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(f'SELL EXECUTED! {order.executed.price} | Cost: {order.executed.value} | Comm: {order.executed.comm}')
                
            self.bar_executed = len(self)
        
        elif order.status in [order.Cancelled,order.Margin,order.Rejected]:
            sef.log('Order Cancelled/Margin/Rejected')
            
        self.order = None
        
    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        # self.log(f'OPERATION PROFIT, GROSS: {trade.pnl} | NET: {trade.pnlcomm}')
        self.grossprofit+=trade.pnl
        self.netprofit+=trade.pnlcomm
        print(f"GROSS: {self.grossprofit} | NET: {self.netprofit}")
    def next(self):
        # Log Current Closing Price of the Series
        self.log(f'Close: {self.dataclose[0]}')
        
        # Check if an order is pending >> Not sending another one if yes
        if self.order:
            return
        # Check if we are in the market
        if not self.position:
            # We might buy if conditions are right
            if self.dataclose[0] < self.dataclose[-1] < self.dataclose[-2]:
                # if current close < previous close < previous close (2 candle)
                self.log(f"BUY CREATE: {self.dataclose[0]}")
                self.order = self.buy()
        else:
            # Already in the market >> we might sell
            if len(self)>=(self.bar_executed + 5):
                # SELL WITH DEFAULT PARAMS
                self.log(f"SELL CREATE: {self.dataclose[0]}")
                # Keeping track of created order to avoid the second order
                self.order = self.sell()

if __name__=='__main__':
    ticker = (input("Enter a ticker: ") or 'SPY').upper()
    time_frame = input("Enter a time_frame: ") or '1D'
    data = questrade_feed(ticker,time_frame)

    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    cerebro.adddata(data)

    cerebro.broker.setcommission(commission=0.001)

    print(f"Starting Portfolio value: {cerebro.broker.getvalue()}")
    _starting = cerebro.broker.getvalue()
    cerebro.run()
    print(f"Starting Portfolio value: {_starting}")
    print(f"Final Portfolio Value: {cerebro.broker.getvalue()}")
