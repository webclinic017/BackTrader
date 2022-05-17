import backtrader as bt
import backtrader.indicators as btind
from datetime import datetime
import pandas as pd
import pandas_datareader.data as web
import random
from copy import deepcopy


class SMAC(bt.Strategy):
    """
    A Simple Moving Average Cross Over Strategy
    """
    params = {
        'fast': 20,
        'slow': 50,
        'optim':False,
        'optim_fs':(20,50)
    }

    def __init__(self) -> None:
        """Initialize the Strategy"""
        self.fastma = dict()
        self.slowma = dict()
        self.regime = dict()

        if self.params.optim: # Use a tuple during optiomization
            self.params.fast, self.params.slow = self.params.optim_fs

        if self.params.fast > self.params.slow:
            raise ValueError(
                "A SMAC Strategy with Fast > Slow MA"
            )

        for d in self.getdatanames():
            # Moving Averages
            self.fastma[d] = btind.EMA(
                self.getdatabyname(d),
                period=self.params.fast,
                plotname="FastMA: "+d
            )

            self.slowma[d] = btind.EMA(
                self.getdatabyname(d),
                period=self.params.slow,
                plotname="SlowMA: "+d
            )

            # GET REGIME
            self.regime[d] = self.fastma[d]-self.slowma[d] # positive when bullish

    def next(self):
        """Iteration over each row of data"""
        for d in self.getdatanames(): #Looping through all symbols
            pos = self.getpositionbyname(d).size or 0
            if pos==0:
                # Considering the possibility of entering the market
                if self.regime[d][0] > 0 and self.regime[d][-1] <=0: # A buy signal
                    self.buy(data=self.getdatabyname(d))
            else:
                if self.regime[d][0] <= 0 and self.regime[d][-1] > 0: # A sell signal
                    self.sell(data=self.getdatabyname(d))
