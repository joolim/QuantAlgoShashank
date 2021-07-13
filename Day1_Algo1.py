import numpy as np
import pandas as pd
class TransdimensionalNadionCoil(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 14)  # Set Start Date
        self.AddEquity("TSLA", Resolution.Daily) # Initialize tesla
        self.AddEquity("SPY", Resolution.Daily)  # Initialize spy as a refernce for S&P
        
#   def OnData(self, slice):
        
    def OnEndOfAlgorithm(self):
        
        #call historical data from QC database
        history_spy = self.History(self.Symbol("SPY"), 30 , Resolution.Daily)
        #take out the closs price and convert it to list for later using in datframe
        history_spy = history_spy["close"].tolist()
        #calculate absolute return
        spy_abs_return = (history_spy[-1]-history_spy[0]) / history_spy[0]
        
        #same for tsla
        history_tsla = self.History(self.Symbol("TSLA"), 30 , Resolution.Daily)
        history_tsla = history_tsla["close"].tolist()
        tsla_abs_return = (history_tsla[-1]-history_tsla[0]) / history_tsla[0]
        
        self.Debug("SPY abs return is " + str(spy_abs_return))
        self.Debug("TSLA abs return is " + str(tsla_abs_return))        
        
        #make a dataframe for easier visual and calculation
        df = pd.DataFrame()
        #store previously obtained spy and tsla prices in dataframe
        df["SPY_Price"]= history_spy
        df["TSLA_Price"] = history_tsla
        
        
        #calculate percentage change ad store in the same database
        df["SPY_returns"] = df["SPY_Price"].pct_change()
        df["TSLA_returns"] = df["TSLA_Price"].pct_change()
        
        #self.Debug(df)
        
        #######      Values necessary for BAS Calculations   ##############
        
        # mean of daily returns ( NOT to be confused by abs. monthly returns )
        spy_daily_ret = df["SPY_returns"].mean()
        tsla_daily_ret = df["TSLA_returns"].mean()
        #self.Debug('spy_mean_ret: {}'.format(spy_daily_ret))
        #self.Debug('tsla_mean_ret: {}'.format(tsla_daily_ret))

        # variance
        spy_var = df["SPY_returns"].var()
        tsla_var = df["TSLA_returns"].var()

        # covariance
        covariance = df["SPY_returns"].cov(df["TSLA_returns"])
        #self.Debug('covariance: {}'.format(covariance))
        
        # correlation
        correlation = df["SPY_returns"].corr(df["TSLA_returns"])
        self.Debug('Correlation: {}'.format(correlation))
        
        ###################### BASS Calculation #############################################
        
        # standard deviation
        spy_std = df["SPY_returns"].std()
        tsla_std = df["TSLA_returns"].std()
        self.Debug('Std Deviation of TSLA: {}'.format(tsla_std))
        
        
        # TSLA beta
        TSLA_beta = covariance / spy_var
        self.Debug('TSLA beta: {}'.format(TSLA_beta))
        
        TSLA_alpha = tsla_abs_return  - TSLA_beta * spy_abs_return   # making use of annualised mean returns of AAPL and SPY
        self.Debug('TSLA alpha: {}'.format(TSLA_alpha))
        
        
        tsla_monthly_std = tsla_std *(20**0.5) 
        TSLA_SR = tsla_abs_return/ tsla_monthly_std  # making use of annualised mean returns of AAPL
        self.Debug('TSLA Sharpe Ratio: {}'.format(TSLA_SR))
