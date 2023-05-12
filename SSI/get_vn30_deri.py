import json
import pandas as pd
import random
import datetime
import numpy as np

from dateutil.relativedelta import relativedelta

import ssi_fc_data.data_utils as du
import ssi_fc_data.general_utils as gu

from subsystems.LBMOM.subsys import Lbmom
from brokerage.ssi import ssi
from brokerage.TradeClient import TradeClient
import ssi_fc_data.md_client_main as md

with open("C:/Users/luong/Desktop/SSI_API/SSI/config/ssi_auth_config.json", "r") as f:
    auth_config = json.load(f)
ssi = ssi(auth_config=auth_config)
trade_client = ssi.get_trade_client()

fpt_df = trade_client.intraday_ohlc("FPT", "01/03/2023", "31/03/2023", 1, 9999, True)

with open("C:/Users/luong/Desktop/SSI_API/SSI/config/ssi_date_config.json", "r") as f:
    date_list = json.load(f)
    date_list=date_list["5 years"]
    poll_df = pd.DataFrame(columns=['open','high','low','close','volume'])
    for date_item in date_list:
        df = trade_client.intraday_ohlc("FPT", date_item[0], date_item[1], 1, 9999, True)
        print(df)
        if len(poll_df)==0 and df is not None:
            poll_df = df
        elif len(poll_df)!=0 and df is not None:
            poll_df = poll_df.combine_first(df)
        else:
            continue
print(poll_df)
poll_df.to_csv(f"C:/Users/luong/Desktop/fpt_5yrs.csv")



