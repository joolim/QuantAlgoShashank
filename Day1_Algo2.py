import numpy as np
import pandas as pd
class TransdimensionalNadionCoil(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 14)  # Set Start Date
        self.stocks = ["SPY", "TSLA", "MSFT","DELL"]
        
        for stock in self.stocks:
            self.AddEquity(stock, Resolution.Daily)
            
#   def OnData(self, slice):
        
    def OnEndOfAlgorithm(self):
        
        for item in self.stocks[1:]:
            
            #call historical data from QC database
            history_spy = self.History(self.Symbol("SPY"), 30 , Resolution.Daily)
            #take out the closs price and convert it to list for later using in datframe
            history_spy = history_spy["close"].tolist()
            #calculate absolute return
            spy_abs_return = (history_spy[-1]-history_spy[0]) / history_spy[0]
            
            #same for item
            history = self.History(self.Symbol(item), 30 , Resolution.Daily)
            history = history["close"].tolist()
            abs_return = (history[-1]-history[0]) / history[0]
            
            self.Debug("SPY abs return is " + str(spy_abs_return))
            self.Debug("{} abs return is" .format(item)  + str(abs_return))        
            
            #make a dataframe for easier visual and calculation
            df = pd.DataFrame()
            #store previously obtained spy and tsla prices in dataframe
            df["SPY_Price"]= history_spy
            df["Price"] = history
            
            
            #calculate percentage change ad store in the same database
            df["SPY_returns"] = df["SPY_Price"].pct_change()
            df["returns"] = df["Price"].pct_change()
            
            #self.Debug(df)
            
            #######      Values necessary for BAS Calculations   ##############
            
            # mean of daily returns ( NOT to be confused by abs. monthly returns )
            spy_daily_ret = df["SPY_returns"].mean()
            daily_ret = df["returns"].mean()
            #self.Debug('spy_mean_ret: {}'.format(spy_daily_ret))
            #self.Debug('tsla_mean_ret: {}'.format(tsla_daily_ret))
    
            # variance
            spy_var = df["SPY_returns"].var()
            var = df["returns"].var()
    
            # covariance
            covariance = df["SPY_returns"].cov(df["returns"])
            #self.Debug('covariance: {}'.format(covariance))
            
            # correlation
            correlation = df["SPY_returns"].corr(df["returns"])
            self.Debug('Correlation: {}'.format(correlation))
            
            ###################### BASS Calculation #############################################
            
            # standard deviation
            spy_std = df["SPY_returns"].std()
            std = df["returns"].std()
            self.Debug('Std Deviation of {} : {}'.format(item , std))
            
            
            # TSLA beta
            beta = covariance / spy_var
            self.Debug('{} beta: {}'.format(item, beta))
            
            alpha = abs_return  - beta * spy_abs_return   # making use of annualised mean returns of AAPL and SPY
            self.Debug('{} alpha: {}'.format(item, alpha))
            
            
            monthly_std = std *(20**0.5) 
            SR = abs_return/ monthly_std  # making use of annualised mean returns of AAPL
            self.Debug('{} Sharpe Ratio: {}'.format(item, SR))
