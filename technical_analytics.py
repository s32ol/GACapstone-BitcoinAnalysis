import pandas as pd
from df_export import df_calculations as DFC

class technical_analytics(DFC):
    '''
    This class creates techinal analysis indicators. It inherents the 
    df_calculations class for computational methods.       
    '''
    def __init__(self, data):
        '''
        Constuctor
        Parameters
        ----------
        data : df
            Load df containing market trade data
        Returns
        -------
        None.
        '''
        super().__init__(data)
             
    def bollinger_bands(self, time_range, stdev):
        '''
        This class exports a dataframe containing upper & lower band values
        for bollinger bands.
        Parameters
        ----------
        time_range : int
            number that gets converted (in days)
            default value: 10
        stdev : int     
            standard deveations from the typical price
            default value: 2
        Returns
        -------
        df
            This method will produce an bolling band df containing both ranges
        '''
        days = DFC.days_to_window_intervals(time_range)         #Moving range
        tp = DFC.typical_price(self, 'High', 'Low', 'Close')    #typical price df
        ma = DFC.moving_avg(self, tp, time_range)               #moving average df

        std = pd.DataFrame() #Standard Deviation calculator
        std['rSTDEV'] = (tp['typical_price'].rolling(days).std()) * stdev
        
        upper_band = pd.DataFrame()     #BOLU=MA(TP,n)+m∗σ[TP,n]
        upper_band['upper_band'] = round(ma['moving_avg'] + std['rSTDEV'], 4)
        
        lower_band = pd.DataFrame()     #BOLD=MA(TP,n)−m∗σ[TP,n]
        lower_band['lower_band'] = round(ma['moving_avg'] - std['rSTDEV'],4)
        
        return pd.concat([upper_band, lower_band], axis=1)
    
#test_methods    
#btc_data = pd.read_csv('./raw_data/coinbaseUSD2014_2018.csv')
#btc_trades = technical_analytics(btc_data).bollinger_bands(10, 2)