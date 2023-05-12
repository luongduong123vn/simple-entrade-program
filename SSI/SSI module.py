import pandas as pd
from ssi_fc_data import fc_md_client
from ssi_fc_data import md_client_main
from ssi_fc_data import config

ticker='VN30F1M'
class SSI_API(object):
    def __init__(self,token=1,ticker=2):
        self.token=token
        self.ticker=ticker
        self.df=[]
        self.daily_ohlc_data=[]
        self.intra_ohlc_data=[]
        self.save_address='C:/Users/luong/Desktop/scrape data'
    
    def access_token(self): 
        self.token=md_client_main.access_token(config)
        config.access_jwt = self.token['data']['accessToken']

    def get_df(self, raw_data):
        df=pd.DataFrame(raw_data)
        df=df.drop(columns=['message','status','totalRecord'])
        df=df.drop('data', 1).assign(**pd.DataFrame(df.data.values.tolist()))
        return df
 
    def get_daily_ohlc(self,ticker):
        self.daily_ohlc_data.append(md_client_main.daily_ohlc(config, ticker,'12/12/2022','01/01/2023',1,10, True))
        for i in range(len(self.daily_ohlc_data)):
            self.daily_ohlc_data[i] = self.get_df(self.daily_ohlc_data[i])
        return self.daily_ohlc_data
        #self.daily_ohlc_data.to_csv(f'{self.save_address}/{ticker}_ssi.csv', index=False)
        

    def get_intra_ohlc(self):
        intra_ohlc_data=md_client_main.intraday_ohlc(config, 'HDB','02/12/2022','01/01/2023',1, 9999, True, 1)
        df_intra_ohlc = self.get_df(intra_ohlc_data)
        df_intra_ohlc.to_csv(f'{self.save_address}/hdb_ssi.csv', index=False)

    def securities_details(self):
        HDB_details = self.get_df(md_client_main.securities_details(config, 'HOSE', 'HDB', 1, 10))
        HDB_details=HDB_details.drop('RepeatedInfo', 1).assign(**pd.DataFrame(HDB_details.RepeatedInfo.values.tolist()))
        HDB_details.to_csv(f'{self.save_address}/hdb_info',index=False)

a=SSI_API()
b=a.access_token()
#print(config.access_jwt)
c=a.get_daily_ohlc('VN30F2306')
print(a.daily_ohlc_data[0])






