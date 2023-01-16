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

price_data['ma20']=price_data['close'].rolling(window=20).mean()
price_data['ma50']=price_data['close'].rolling(window=50).mean()
price_data['ma100']=price_data['close'].rolling(window=100).mean()
print(price_data.tail(5))
