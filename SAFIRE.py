#######################################################
## Name: JahkRCode
## Title: SAFIRE.py
## Description: SAFIRE -> Sunshine And Freedom Innovative Research & Engineering
## Date Created: June 4th, 2018
#######################################################
import decimal

class MovingAverageCrossAlgorithm(QCAlgorithm):

    def __init__(self):
            self.symbols = ["BTCUSD"]
            self.previous = None
            self.fast = {}
            self.slow = {}
            self.MACD_period = {}
            self.bought_price = None
            self.take_profits = None
            self.percentage_unreal = None
            self.percentage_buy = None
            self.percentage_sell = None
    
    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash 
        and start-end dates for your algorithm. All algorithms must initialized.'''
        
        self.SetStartDate(2018, 7, 1)  #Set Start Date
        self.SetEndDate(2018, 7, 22)   #Set End Date
        self.SetCash(4100)           #Set Strategy Cash
        
        # create a 15 day exponential moving average
        for symbol in self.symbols:
            self.AddCrypto(symbol, Resolution.Hour, Market.GDAX)
            self.SetBrokerageModel(BrokerageName.GDAX, AccountType.Cash)
            self.MACD_period[symbol] = (self.MACD(symbol, 12, 26, 9, MovingAverageType.Exponential, Resolution.Hour))
            self.fast[symbol] = self.MACD_period[symbol].Fast
            self.slow[symbol] = self.MACD_period[symbol].Slow
            
        self.Debug("HIT HERE B4: {}".format(self.symbols))
        x = 0
        '''
        while(x < len(self.MACD_period)):
            
            self.fast[symbol] = self.MACD_period[symbol]
        # create a 30 day exponential moving average
            self.slow[symbol] = (self.MACD_period[x])
            x += 1
        '''
        self.SetWarmUp(26)
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        
        Arguments:
            data: TradeBars IDictionary object with your stock data
        '''
        self.DefaultOrderProperties = GDAXOrderProperties()
        self.DefaultOrderProperties.PostOnly = True

        # wait for our slow ema to fully initialize
        # define a small tolerance on our checks to avoid bouncing
        if self.IsWarmingUp: return
        for symbol in self.symbols:
            if not self.slow[symbol].IsReady:
                return 
            self.SetRuntimeStatistic("MACD SCORE: ", str((self.fast[symbol].Current.Value - self.slow[symbol].Current.Value)))

            #self.Transactions.CancelOpenOrders(symbol)
            self.currency = symbol.replace("USD", "")
            holdings = self.Portfolio.CashBook[self.currency].Amount

            # we only want to go long if we're currently short or flat
            if self.Portfolio.CashBook[self.currency].Amount == 0:
                # if the fast is greater than the slow, we'll go long
                if (self.fast[symbol].Current.Value - self.slow[symbol].Current.Value) < 0:
                    self.Debug("BUY  >> {0}".format(self.Securities[symbol].Price))
                    self.SetHoldings(str(symbol), 0.9, "BUY")
            # we only want to liquidate if we're currently long
            # if the fast is less than the slow we'll liquidate our long
            elif self.Portfolio.CashBook[self.currency].Amount > 0:
                if (self.Securities[symbol].Price > (self.Portfolio[symbol].HoldingsCost * decimal.Decimal(1.005))):
                    self.Debug("SELL for Take Profit >> {0}".format(self.Securities[symbol].Price))
                    self.SetHoldings(str(symbol), 0.9, "SELL")
                elif (self.fast[symbol].Current.Value - self.slow[symbol].Current.Value) > 0:
                    self.Debug("SELL for Average Profit >> {0}".format(self.Securities[symbol].Price))
                    self.SetHoldings(str(symbol), 0.9, "SELL_LOSS")
     # Override SetHoldings to use limit orders (ratio is of totalPortfolioValue.)
    def SetHoldings(self, symbol, ratio, position):
        #self.Debug("POSITION: {} - SYMBOL: {} - RATIO: {}".format(position, symbol, ratio))
        security = self.Securities[symbol]
        if not security.IsTradable:
            self.Debug("{} is not tradable.".format(symbol))
            return    # passive fail
        ratio = decimal.Decimal(ratio)
        price, quantity = security.Price, self.Portfolio[symbol].Quantity
        
        # Keep 5% Cash    (for the limit order, rounding errors, and safety)
        totalPortfolioValue = self.Portfolio.CashBook["USD"].Amount * decimal.Decimal(0.95)
        
        # +0.5% Limit Order
        # (to make sure it executes quickly and without much loss)
        # (if you set the limit large it will act like a market order)
        limit = 1.005
        quantity = decimal.Decimal(quantity)
        desiredQuantity = (totalPortfolioValue * ratio) / price
        orderQuantity = desiredQuantity - quantity
        self.Debug("DesiredQuant: {} - quantity: {} - PortValue: {} Price: {}".format(desiredQuantity, quantity, totalPortfolioValue, price))
        # limit needs to be inverse when selling
        self.Debug("Number of Open Orders: {}".format(len(self.Transactions.GetOpenOrders(symbol))))
        if position == "SELL":
            limitPrice = price * decimal.Decimal(limit)
            limitPrice = decimal.Decimal(limitPrice)
            self.LimitOrder(symbol, -quantity, round(limitPrice,2))
            self.Debug("SELL Open Orders: {}".format(self.Transactions.GetOpenOrders(symbol)))
        if position == "SELL_LOSS":
            limitPrice = price * decimal.Decimal(1.0001)
            limitPrice = decimal.Decimal(price)
            self.LimitOrder(symbol, -quantity, round(limitPrice,2))
            self.Debug("SELL Open Orders: {}".format(self.Transactions.GetOpenOrders(symbol)))
        if position == "BUY":
                limitPrice = price * decimal.Decimal(.9999)
                limitPrice = decimal.Decimal(limitPrice)
                self.LimitOrder(symbol, orderQuantity, round(limitPrice, 2))
                self.Debug("BUY Open Orders: {}".format(self.Transactions.GetOpenOrders(symbol)))
