import pandas as pd
from datetime import time,date,datetime,timedelta
import requests
import numpy as np
import trade_package

def get_etf_data():
    etf_file_names = trade_package.get_file_name('C:/Users/duongluong/Desktop/finpros/tiingo/data')
    etf_data = pd.DataFrame()
    for etf_file_str in etf_file_names:
        etf_temp = pd.read_parquet(f"C:/Users/duongluong/Desktop/finpros/tiingo/data/{etf_file_str}")
        etf_name = etf_file_str.split("_")[1]
        etf_temp = etf_temp.set_index(["Timestamp"], drop=True)
        etf_temp.rename(columns= lambda col: col +" "+ etf_name, inplace=True)
        etf_data = pd.concat([etf_data, etf_temp], axis=1)
    return etf_data

def get_vn30_etf():
    etf_df = pd.read_csv(r'C:/Users/duongluong/Desktop/finpros/tiingo/etf_data.csv')
    def format_date_pd(series):
        #series in the form : pandas date range
        yymmdd = list(map(lambda x: int(x), str(series).split(" ")[0].split("-")))
        return datetime(int(yymmdd[0]),int(yymmdd[1]),int(yymmdd[2]))
    etf_df["Timestamp"] = pd.Series(etf_df["Timestamp"]).apply(lambda x: format_date_pd(x))

    etf_df.set_index(etf_df["Timestamp"], inplace=True)
    etf_df.drop(columns=['Timestamp'], inplace=True)
    etf_df = etf_df[datetime(2018,8,12):]

    vn30f = trade_package.get_vn30f_df()
    abc = vn30f[['Volume VN30F1M', 'Volume VN30F2M']].resample('D', closed='right').sum()
    vn30f_df = vn30f.resample('D', closed='right').last()
    vn30f_df.drop(columns=['Volume VN30F1M', 'Volume VN30F2M'], inplace=True)
    vn30f_df = pd.concat([vn30f_df, abc], axis=1)

    etf_df = pd.concat([etf_df, vn30f_df], axis=1)
    etf_df = etf_df.ffill()
    print(etf_df)
    etf_df.to_csv(r"C:/Users/duongluong/Desktop/finpros/data/vn30_etf_data.csv")






