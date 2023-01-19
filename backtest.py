# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyfolio as pf
import datetime as dt
import pandas_datareader.data as web

# print all outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

price_data = pd.read_csv('price_data.csv')

price_data['bnh_returns'] = np.log(price_data['close']/price_data['close'].shift(1))

price_data['ma20']=price_data['close'].rolling(window=20).mean()
price_data['ma50']=price_data['close'].rolling(window=50).mean()
price_data['ma100']=price_data['close'].rolling(window=100).mean()
print(price_data.tail(5))

price_data['std'] = price_data['close'].rolling(window=20).std()
price_data['upper_band'] = price_data['ma20'] + (2 * price_data['std'])
price_data['lower_band'] = price_data['ma20'] - (2 * price_data['std'])
price_data.drop(['Open','High','Low'],axis=1,inplace=True,errors='ignore')

price_data['signal'] = np.where((price_data['close'] < price_data['lower_band']) &
                        (price_data['close'].shift(1) >= price_data['lower_band']),1,0)

# SELL condition
price_data['signal'] = np.where( (price_data['close'] > price_data['upper_band']) &
                          (price_data['close'].shift(1) <= price_data['upper_band']),-1,price_data['signal'])
# creating long and short positions 
price_data['position'] = price_data['signal'].replace(to_replace=0, method='ffill')

# shifting by 1, to account of close price return calculations
price_data['position'] = price_data['position'].shift(1)

# calculating stretegy returns
price_data['strategy_returns'] = price_data['bnh_returns'] * (price_data['position'])


# comparing buy & hold strategy / bollinger bands strategy returns
print("Buy and hold returns:",price_data['bnh_returns'].cumsum()[-1])
print("Strategy returns:",price_data['strategy_returns'].cumsum()[-1])

# plotting strategy historical performance over time
price_data[['bnh_returns','strategy_returns']] = price_data[['bnh_returns','strategy_returns']].cumsum()
price_data[['bnh_returns','strategy_returns']].plot(grid=True, figsize=(12, 8))

pf.create_simple_tear_sheet(price_data['strategy_returns'].diff())

exit()
