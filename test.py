import pandas as pd
import datetime as dt
import statistics as stats
from tqdm import tqdm 
   
class df_calculations:
    def __init__(self, data):
        self.data = data
        self.day = dt.timedelta(days=1)
        
    def moving_avg(self, typical_price, timestamp_col, time_range):
        timestamp = self.data[['{}'.format(timestamp_col)]]
        day = self.day.total_seconds()
        empty_set = int(timestamp.iloc[0] + (day * time_range))
        time_bin = []
        ma_bin = []
        percentage_counter = 0
        while percentage_counter < len(timestamp):
            for index, row in timestamp.iterrows():
                time_bin.append(typical_price.iloc[index][0])
                if int(row) < empty_set:
                    ma_bin.append(0)
                else:
                    ma_bin.append(stats.mean(time_bin).round(4))
                percentage_counter += 1
                print('{}%  @{} only {} left to go *cry in lack of optimization*'\
                      .format(round(percentage_counter/len(timestamp)*100, 4),
                              index, len(timestamp) - percentage_counter ))
        ma = pd.DataFrame()
        ma['moving_avg'] = ma_bin
        return ma
                        
    def typical_price(self, high, low, close):
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



