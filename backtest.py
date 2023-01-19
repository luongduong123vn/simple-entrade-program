# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader.data as web
import get_token

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

#price_data = pd.read_csv(r"C:\Users\luong\price_data.csv")
run_api = get_token.entrade_api()
price_data=run_api.price_data()

price_data['bnh_returns'] = np.log(price_data['close']/price_data['close'].shift(1))

price_data['ma20']=price_data['close'].rolling(window=20).mean()
#price_data['ma50']=price_data['close'].rolling(window=50).mean()
#price_data['ma100']=price_data['close'].rolling(window=100).mean()


price_data['std'] = price_data['close'].rolling(window=20).std()
price_data['upper_band'] = price_data['ma20'] + (2 * price_data['std'])
price_data['lower_band'] = price_data['ma20'] - (2 * price_data['std'])
price_data.drop(['open','high','low','nextTime'],axis=1,inplace=True,errors='ignore')

price_data['signal'] = np.where((price_data['close'] < price_data['lower_band']) &
                        (price_data['close'].shift(1) >= price_data['lower_band']),1,0)

price_data['signal'] = np.where( (price_data['close'] > price_data['upper_band']) &
                          (price_data['close'].shift(1) <= price_data['upper_band']),-1,price_data['signal'])
# creating long and short positions 

price_data['position'] = price_data['signal'].replace(to_replace=0, method='ffill')

# shifting by 1, to account of close price return calculations
price_data['position'] = price_data['position'].shift(1)

# calculating stretegy returns
price_data['strategy_returns'] = price_data['bnh_returns'] * (price_data['position'])

# comparing buy & hold strategy / bollinger bands strategy returns
#print("Buy and hold returns:",price_data['bnh_returns'].cumsum())
#print("Strategy returns:",price_data['strategy_returns'].cumsum())

# plotting strategy historical performance over time
price_data['bnh_returns_cum'] = price_data['bnh_returns'].cumsum()
price_data['strategy_returns_cum'] = price_data['strategy_returns'].cumsum()
price_data[['bnh_returns_cum','strategy_returns_cum']].plot(grid=True, figsize=(12, 8))

expected_return=price_data['strategy_returns'].sum()
vol=price_data['strategy_returns'].std()
sharpe_ratio= price_data['strategy_returns'].sum()/price_data['strategy_returns'].std()
print('Expected return is:', expected_return)
print('Vol is:', vol)
print('Sharpe ratio is:', sharpe_ratio)
print(price_data.tail(5))
