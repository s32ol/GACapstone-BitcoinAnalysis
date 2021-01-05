import pandas as pd
import datetime as dt
  
class df_calculations:
    '''
    This class calculates the moving average & typical price from market
    trade data and returns a df object. This can be used in creation of
    analytical indicators eg. Bollinger Bands      
    '''
    def __init__(self, data):
        '''
        Constuctor
        Parameters:
            data (pandas.DataFrame): intakes a df
            day (datetime.timedelta): class instance variable
        '''
        self.data = data 
        
    def moving_avg(self, typical_price, time_range):
        '''
        The method calucates the moving average from market data, given that
        a df containing typical price/time is given. *Note time in unix time 
        Parameters
        ----------
        typical_price : df
            see typical_price()
        time_range : int (days)
            Time bin which serve as the bases from when the mean is calucated. 
            Eg time_range = 10 provides a trailing moving average of 10 days
            which is used in FOREX techinal analysis.
        Returns
        -------
        ma : df
            this method will produce an moving average df
        '''
        days = int(dt.timedelta(days=time_range).total_seconds()/60)
        ma = pd.DataFrame()
        ma['moving_avg'] = typical_price['typical_price'].rolling(days).mean()
        return ma
                        
    def typical_price(self, high, low, close):
        '''
        mean(high, low, close) for a given period.
        Parameters
        ----------
        high, low, close : str , 
            insert corresponding name of df column in string format
        Returns
        -------
        tp : df
            this method will produce an typical df
        '''
        high = self.data['{}'.format(high)]
        low = self.data['{}'.format(low)]
        close = self.data['{}'.format(close)]       
        tp = pd.DataFrame()
        tp['typical_price'] = round((high + low + close) /3, 4) 
        return tp

#test_methods
#btc_data = pd.read_csv('./raw_data/coinbaseUSD2014_2018.csv')  
#btc_trades = df_calculations(btc_data)
#btc_tp = btc_trades.typical_price('High', 'Low', 'Close')
#btc_ma = btc_trades.moving_avg(btc_tp, 1)




