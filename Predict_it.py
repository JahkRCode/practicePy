import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression

class Predict_it(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018,2, 1)  #Set Start Date for Nahdya's Birthday
        self.SetEndDate(2018,4, 10)    #Set End Date for Nahdya's Birthday
        self.SetCash(100000)           #Set Strategy Cash for Nahdya's Birthday
        
        self.crypto = self.AddCrypto("BTCUSD", Resolution.Daily).Symbol # What we're buying
        self.sto = self.STO(self.crypto, 7, Resolution.Daily)
        
        self.df = self.History(self.crypto, 31, Resolution.Hour) # Dataframe storing historical data of previous hour
        self.X = self.df[list(self.df.columns)[:-1]]
        y = self.df["close"]
        
        X_train, self.X_test, y_train, y_test = train_test_split(np.array(self.X), np.array(y))
        self.regressor = LinearRegression()
        self.regressor.fit(X_train, y_train)
        
        # Creates List to store Close price from previous hour
        
        y_predictions = self.regressor.predict(self.X)
        #self.counter += 1
        self.Debug("y_test: \n{}".format(self.X))

        #cvp = cross_val_predict(self.regressor, self.X, y, cv=5)
        #self.Debug("X-Test Value: \n{}".format(X_test.iloc[0]))
        self.Debug("predict type: {}".format(y_predictions))
        self.Debug("Actual Close Price: {}\nPredicted Close Price: {}\nConfidence Score: {}".format(y[0], y_predictions[0], self.regressor.score(np.array(self.X), y_predictions)))

        #x = 0
        #while x < len(self.y_predictions):
        #    self.Debug("Actual Price Close: {}\nPrice Close Predictions: {}".format(y_test.iloc[x], cvp[x]))
        #    x += 1
        #self.counter = 0
        
    def OnData(self, data):
        self.df2 = self.History(self.crypto, 3, Resolution.Daily) # Dataframe storing historical data of previous hour
        self.X2 = self.df2[list(self.df2.columns)[:-1]]
        last_hour_price = self.df2.iloc[len(self.df2)-2]["close"]
        
        close_price = self.df2.iloc[len(self.df2)-2]["close"]
        high_price = self.df2.iloc[len(self.df2)-2]["high"]
        low_price = self.df2.iloc[len(self.df2)-2]["low"]
        open_price = self.df2.iloc[len(self.df2)-2]["open"]
        percentage = float(.10)
        actual_price = data[self.crypto].Close
        stop_loss = last_hour_price - (last_hour_price * percentage)
        trade_profit = last_hour_price + (last_hour_price * percentage)
        
        data_array = np.array([close_price, high_price, low_price, open_price])
        '''
        self.Debug("Trade Profit: {}".format(trade_profit))
        self.Debug("Time of Price: {}".format(data[self.crypto].Time))
        self.Debug("Actual Close: {}".format(data[self.crypto].Close))
        self.Debug("Stop Loss Limit: {}".format(stop_loss))
        self.Debug("Last Hour Close: {}".format(last_hour_price))
        '''
        self.Debug("Is Invested: {}".format(self.Portfolio.Invested))
        ## Enters Buy Phase
        if (self.sto.Current.Value < 20):
            if ((actual_price > stop_loss) and (actual_price < last_hour_price) and (self.Portfolio.Invested == False)):
                self.MarketOrder(self.crypto, 1)
                self.Debug("My Bought Price: {} | Actual Price: {} | Stochastic Value: {}\n"
                .format(self.Portfolio["LTEUSD"].HoldingsCost, actual_price, self.sto.Current.Value))
        ## Enter Sell Phase
        if((self.Portfolio["LTEUSD"].HoldingsCost > actual_price or self.Portfolio["LTEUSD"].HoldingsCost > trade_profit) and (self.Portfolio.Invested == True)):
            #self.MarketOrder(self.crypto, -1)
            self.Liquidate()
            self.Debug("My Sell Price: {} | Actual Price: {} | Stochastic Value: {}\n"
            .format(self.Portfolio["LTEUSD"].HoldingsCost, actual_price, self.sto.Current.Value))
            
            
            
            
            #End Code Line
