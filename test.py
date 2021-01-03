import pandas as pd
import datetime as dt
import statistics as stats
from tqdm import tqdm 
   
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
        self.day = dt.timedelta(days=1) 
        
    def moving_avg(self, typical_price, timestamp_col, time_range):
        '''
        The method calucates the moving average from market data, given that
        a df containing typical price/time is given. *Note time is calcuated
        in unix time and time range bin 
        Parameters
        ----------
        typical_price : df
            see typical_price()
        timestamp_col : string
            df['example name'] Name of the column where you would find time
        time_range : int (days)
            Time bin which serve as the bases from when the mean is calucated. 
            Eg time_range = 10 provides a trailing moving average of 10 days
            which is used in FOREX techinal analysis.
        Returns
        -------
        ma : df
            this method will produce an moving average df
        '''
        timestamp = self.data[['{}'.format(timestamp_col)]]
        day = self.day.total_seconds()
        empty_set = int(timestamp.iloc[0] + (day * time_range)) #time_range
        time_bin = []
        ma_bin = []
        percentage_counter = 0
        while percentage_counter < len(timestamp): #loop to track progress 
            for index, row in timestamp.iterrows():
                time_bin.append(typical_price.iloc[index][0]) 
                #Adding all time values
                if int(row) < empty_set:
                    ma_bin.append(0)
                else: #mean calucation can begin after time_range has been passed
                    ma_bin.append(stats.mean(time_bin).round(4))
                percentage_counter += 1
                print('{}%  @{} only {} left to go *cry in lack of optimization*'\
                      .format(round(percentage_counter/len(timestamp)*100, 4),
                              index, len(timestamp) - percentage_counter ))
        ma = pd.DataFrame()
        ma['moving_avg'] = ma_bin
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

btc_data = pd.read_csv('./raw_data/toy_set.csv')        
btc_trades = df_calculations(btc_data)
btc_tp = btc_trades.typical_price('High', 'Low', 'Close')
btc_ma = btc_trades.moving_avg(btc_tp, 'Timestamp', 1)



