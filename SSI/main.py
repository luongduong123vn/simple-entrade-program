import json
import pandas as pd
import random
import datetime

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

database_df,instruments=gu.load_file(r"C:/Users/luong/Desktop/SSI_API/SSI/Data/vn30_div_adj.obj")
#run simulation for 5 years
VOL_TARGET = 0.30
print(database_df.index[-1]) #date today: 2023-02-08
sim_start = database_df.index[-1] - relativedelta(years=5)
print(sim_start) #start trading backtest from 018-02-08
strat = Lbmom(instruments_config="C:/Users/luong/Desktop/SSI_API/SSI/subsystems/LBMOM/vn30.json", historical_df=database_df, simulation_start=sim_start, vol_target=VOL_TARGET)
strat.get_subsys_pos()

exit()
#to save the sp500 data as an obj file
df, instruments = du.get_sp500_df()
df=du.extend_dataframe(traded=instruments, df=df)
gu.save_file(r"C:/Users/luong/Desktop/Hanguk_course/1/Data/data.obj",(df,instruments))

# dump to json
with open(r"C:/Users/luong/Desktop/Hanguk_course/1/subsystems/LBMOM/config.json",'w') as f:
    json.dump({'instruments': instruments}, f, indent=4)

# get pairs for trade
pairs = []
while len(pairs) <= 20:
    pair = random.sample(list(range(16,300)),2)
    if pair[0] == pair[1]: 
        continue
    pairs.append((min(pair[0],pair[1]), max(pair[0], pair[1])))
print(pairs)


#get access token
token= trade_client.access_token()
auth_config['access_jwt'] = token['data']['accessToken']
with open("C:/Users/luong/Desktop/SSI_API/SSI/config/ssi_auth_config.json", "w") as f: 
    f.write(json.dumps(auth_config))

#get vn30 list
vn_30=trade_client.index_components('vn30',1,50)
with open(r"C:/Users/luong/Desktop/SSI_API/SSI/Data/vn30.json",'w') as f:
    json.dump({'instruments': vn_30['data']['IndexComponent']}, f, indent=4)

#loop for ssi data 
with open("C:/Users/luong/Desktop/SSI_API/SSI/config/ssi_date_config.json", "r") as f:
    date_list = json.load(f)
date_list=date_list["5 years"]
poll_df = pd.DataFrame()
for date_item in date_list:
    df, instruments = trade_client.get_vn30_df(date_item[0], date_item[1])
    print(df)

    if len(poll_df) == 0:
        poll_df = df
    else:
        poll_df = poll_df.combine_first(df)
database_df = database_df.loc[:poll_df.index[0]][:-1] #this means take original database up to the starting point of the new database, and drop the overlapping data entry point
database_df = database_df.append(poll_df)