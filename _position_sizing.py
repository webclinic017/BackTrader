import backtrader as bt

class PropSizer(bt.Sizer):
    """
    A Sizer that will buy as many as necessary for a certain portion of the portfolio
    to be committed to the position, while allowing stocks to be bought in batches
    """
    params={
        'prop':0.1,
        'batch': 10
    }

    def _getsizing(self, comminfo, cash, data, isbuy):
        """
        Retuns: Proper Sizing
        """
        if isbuy:
            target = self.broker.getvalue() * self.params.prop # Ideal total value of the position
            price = data.close[0]
            shares_ideal = target/price #Total shares needed to get to taker
            batches = int(shares_ideal/self.params.batch) # Total Batches in this trade 
            shares  = batches * self.params.batch
            if shares * price > cash:
               return 0
            else:
                return shares
        else:
            return self.broker.getposition(data).size # Clear the position
        