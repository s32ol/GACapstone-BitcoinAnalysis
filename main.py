#graphs 
import pandas as pd
import time as t
import datetime as dt
from technical_analytics import technical_analytics_df as taf

#overall goal
#need to make graphs
#randomized trails for values surpasing the bounds of the analytic tool p338
#time_conversion = dt.datetime.fromtimestamp(int("1420444800")).strftime('%Y-%m-%d %H:%M:%S')

#to make graphs, first need time bins
#make a new df containing a specific time

def date_bins_df(df, dates):
    '''
    Creates df from specified dates
    Parameters
    ----------
    df : pandas.dataframe
        DESCRIPTION.
    dates : [str, str] "yyyy/m/d" <- Format
        Date ranges for df creation
    Returns
    -------
    df
        modified df to the date range provided.
    '''
    def unix_time_convert(date):
        '''
        This converts regluar time to unix time @00:00 utc of the date entered
        Parameters
        ----------
        date: str
            A date in following format (yyyy,m,d) <- string
        Returns
        -------
        str
            Date converted
        '''        
        conversion = t.mktime(dt.datetime.strptime(date,"%d/%m/%Y").timetuple())
     
        return conversion
        
    def matching_unixTime(df, unix_stamp):
        '''
        Search algo on finding an exact or closes match of timestamp index
        Parameters
        ----------
        df : pandas.Dataframe
            DESCRIPTION.
        unix_bin : TYPE
            DESCRIPTION.
        Returns
        -------
        TYPE
            DESCRIPTION.
        '''        
        df_sort = df.iloc[(df['Timestamp']-unix_stamp).abs().argsort()[:1]]
        
        return df_sort['Timestamp'].iloc[0] #To retreive the timestamp      
    
    unixStamp_bins = []
    matched_time_bin = []
    
    for idx, dates_list in enumerate(dates):
        unixStamp_bins.append(int(unix_time_convert(dates_list)))
        matched_time_bin.append(matching_unixTime(df, unixStamp_bins[idx]))
        
    timeframe_df = pd.DataFrame()
    timeframe_df = df[df['Timestamp'].between(unixStamp_bins[0], unixStamp_bins[1])]
    
    export_df = timeframe_df.copy() #avoid chain indexing
    export_df['Date'] = pd.to_datetime(timeframe_df['Timestamp'], unit='s')
    export_df = export_df.drop(columns=['Timestamp']) 
    
        
    return export_df

 
btc_data = pd.read_csv('./raw_data/coinbaseUSD2014_2018.csv')
btc_trades = taf(btc_data).bollinger_bands(10, 2)


btc_bb = pd.DataFrame()
btc_bb = pd.concat([btc_data['Timestamp'], btc_trades['moving_avg'], btc_trades['upper_band'], btc_trades['lower_band'], btc_data['Close']], axis=1)

x = date_bins_df(btc_bb, ["01/01/2016", "02/01/2016"])

x.plot()





