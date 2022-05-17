import backtrader as bt

class AcctValue(bt.Observer):
    alias = ("Value",)
    lines =('value',)

    plotinfo = {
        'plot':True,
        'subplot':True
    }

    def next(self):
        """Get total account value (cash +stocks)"""
        self.lines.value[0] = self._owner.broker.getvalue()

class AcctStats(bt.Analyzer):

    def __init__(self) -> None:
        self.start_val = self.strategy.broker.getvalue()
        self.end_val = None

    def stop(self):
        self.end_val = self.strategy.broker.getvalue()

    def get_analysis(self):
        return {
            'start':self.start_val,
            'end': self.end_val,
            'growth':self.end_val-self.start_val,
            'return':self.end_val/self.start_val
        }