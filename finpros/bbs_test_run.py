import pandas as pd
from datetime import time,date,datetime,timedelta
import requests
import numpy as np
import trade_package
 
username = "luongduong123vn@gmail.com"
userpassword = "Ngungon234@"

def get_data(ticker):
    import time 
    today_date = int(time.mktime(pd.Timestamp('2015-01-01').timetuple()))
    end_date = int(time.mktime((date.today() + pd.Timedelta('1D')).timetuple()))
    ticker = ticker
    link = "https://services.entrade.com.vn/chart-api/chart?from={start_date}&resolution=1&symbol={ticker}&to={end_date}".format(start_date=today_date, ticker=ticker,end_date=end_date)
    f = requests.get(link)
    dict_f = f.json()
    import datetime
    df = pd.DataFrame()
    df['Date'] = dict_f['t']
    df['Date'] = pd.to_datetime(df['Date'].astype(int).apply(lambda x: datetime.datetime.fromtimestamp(x)))
    df['Close'] = dict_f['c']
    df['High'] = dict_f['h']
    df['Low'] = dict_f['l']
    df['Open'] = dict_f['o']
    df['Volume'] = dict_f['v']
    #df['day'] = df['Date'].dt.date
    df.set_index('Date', inplace=True)
    df = df.sort_values('Date')
    df.rename(columns= lambda col: col +" "+ ticker, inplace=True)
    return df

vn30f1m_df = get_data("VN30F1M")
vn30f2m_df = get_data("VN30F2M")
vn30f_df = vn30f1m_df.merge(vn30f2m_df, on='Date', how='left')
cols = ['Close VN30F2M', 'High VN30F2M', 'Low VN30F2M', 'Open VN30F2M']
for col in cols:
    vn30f_df[col]= vn30f_df[col].ffill()
vn30f_df['Volume VN30F2M'] = vn30f_df['Volume VN30F2M'].fillna(0)

price_data = vn30f_df
price_data['spread'] = price_data['Close VN30F1M'] - price_data['Close VN30F2M']

price_data['bnh_returns'] = (price_data['spread']-price_data['spread'].shift(1))/(price_data['Close VN30F1M'].shift(1) + price_data['Close VN30F2M'].shift(1))

strat_window = 20
price_data['ma20']=price_data['spread'].rolling(strat_window).mean()
price_data['std'] = price_data['spread'].rolling(strat_window).std()
price_data['upper_band'] = price_data['ma20'] + (2 * price_data['std'])
price_data['lower_band'] = price_data['ma20'] - (2 * price_data['std'])

price_data['signal'] = np.where((price_data['spread'] < price_data['lower_band']) &
                        (price_data['spread'].shift(1) >= price_data['lower_band']),1,0)

price_data['signal'] = np.where( (price_data['spread'] > price_data['upper_band']) &
                          (price_data['spread'].shift(1) <= price_data['upper_band']),-1,price_data['signal'])

def send_order():
    data_feed = price_data.reset_index()
    if data_feed.iloc[-1]['signal'] == 0:
        #need to cancel prev trade 1st
        trade_package.selenium_order(username,userpassword,price = data_feed.iloc[-1]['Close VN30F1M'], lots=1,order='long')
    elif data_feed.iloc[-1]['signal'] == -1:
        #need to cancel prev trade 1st
        trade_package.selenium_order(username,userpassword,price = data_feed.iloc[-1]['Close VN30F1M'], lots=1,order='short')
    else:
        pass

send_order()
