import json
import requests
import pandas as pd 
import pytz
import time
from datetime import datetime

#orderChange_API = API(" https://services.entrade.com.vn/papertrade-entrade-api/risk_configs/" + accountID,
#                  {'cutLossRate' : float, 
#                  'investorAccountId': accountID, 
#                  'investorId': investorID, 
#                  'trailingEnabled': bool (True/False)},
#                  {"accept" : "application/json","Authorization": str(tk)})

#orderPlace_API = API(" https://services.entrade.com.vn/papertrade-entrade-api/derivative/orders",
#                  {'bankMarginPortfolioId': bankMarginPortfolioId, 
#                  'investorId': investorID,
#                  'orderType': (LO/MTL/ATO/ATC),
#                  'price': (set price only for LO orders, default = 0),
#                  'quantity': integer,
#                  'side': “NB”/”NS” (long/short) ,
#                  'symbol': derivatives symbol},
#                  {"accept" : "application/json","Authorization": str(tk)})

#accountInfo_API = API(" https://services.entrade.com.vn/papertrade-entrade-api/investors/" + investorID + "/investor_account",
#                  {},
#                  {"accept" : "application/json","Authorization": str(tk)})

now=datetime.now()
current_timestamp=str(int(time.mktime(now.timetuple())))

class entrade_api(object):
    def __init__(
        self, investorID="1000055826", accountID = "1000061964",
        start_timestamp= "1656640720", data=4):
        self.investorID = investorID
        self.accountID = accountID
        self.start_timestamp=start_timestamp
        self.current_timestamp=current_timestamp
        self.url={}
        self.body={}
        self.headers={}
        self.data=data
    
    def login_api(self):
        self.url["login"]="https://services.entrade.com.vn/entrade-api/v2/auth"
        self.body["login"]={"username": "luongduong123vn@gmail.com","password": "Ngungon234@"}
        self.headers["login"]={"accept": "gzip","Content-Type": "gzip"}
        resp_auth = requests.post(self.url['login'], headers = self.headers['login'] ,data=json.dumps(self.body["login"]))
        login_token=json.loads(resp_auth.text)
        if resp_auth.status_code != 200:
            return print('error: ' + str(resp_auth.status_code))
        else:
            return login_token
    
    def get_data (self):
        self.url["get_data"] = " https://services.entrade.com.vn/chart-api/chart?from=" + self.start_timestamp +"&resolution=1&symbol=VN30F1M&to=" + current_timestamp
        self.body["get_data"] = {}
        self.headers["get_data"] = {"accept" : "application/json","Authorization": str(self.login_api)}
        resp_data = requests.get(self.url["get_data"], headers=self.headers["get_data"])
        if resp_data.status_code != 200:
            return print('error: ' + str(resp_data.status_code))
        else:
            return json.loads(resp_data.text)
    
    def load_pandas(self):
        data = pd.DataFrame(self.get_data())
        data.t = pd.to_datetime(data.t, unit='s')
        data.columns = ['datetime', 'open', 'high', 'low','close','volume','nextTime']
        return data
    
    def price_data(self):
        self.login_api()
        self.get_data()
        self.load_pandas()
        data=self.load_pandas()
        return data

#run_api = entrade_api()
#price_data=run_api.price_data()
#print(price_data.tail(5))
#price_data.to_csv('price_data.csv', index=False)
