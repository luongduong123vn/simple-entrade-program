import json
import pandas as pd
import datetime
from ssi_fc_data.fc_md_client import MarketDataClient
from ssi_fc_data.model import constants
from ssi_fc_data.model import model

from collections import defaultdict

class TradeClient():

    def __init__(self, auth_config):
        self.auth_type=auth_config["auth_type"]
        self.consumerID = auth_config["consumerID"]
        self.consumerSecret = auth_config["consumerSecret"]
        self.access_jwt= auth_config['access_jwt']
        self.url = auth_config["url"]
        self.stream_url = auth_config["stream_url"]


        # if _type_jwt == constants.AUTH_TOKEN:
        # 	self._type_jwt = self._config.auth_jwt
        # else:
        # 	self._type_jwt = self._config.access_jwt 

    def access_token(self):

        req = model.accessToken

        req['consumerID'] = self.consumerID
        req['consumerSecret'] = self.consumerSecret

        client = MarketDataClient(self)
        res = client.access_token(req, constants.NONE)
        return res
    
    def index_components(self, indexCode: str, pageIndex: int, pageSize: int):

        req = model.index_components

        req['indexCode'] = indexCode
        req['pageIndex'] = pageIndex
        req['pageSize'] = pageSize

        # client = MarketDataClient(config, constants.OTHER)
        client = MarketDataClient(self)
        res = client.index_components(constants.NONE, req)
        return res
    
    def format_date_ssi(self, series):
            #series in the form : SSI
            ddmmyy = series.split("/")
            return datetime.date(int(ddmmyy[2]), int(ddmmyy[1]), int(ddmmyy[0]))
    
    def format_date_pd(self, series):
            #series in the form : pandas date range
            yymmdd = list(map(lambda x: int(x), str(series).split(" ")[0].split("-")))
            return datetime.date(int(yymmdd[0]),int(yymmdd[1]),int(yymmdd[2]))
        
    def daily_ohlc(self, symbol: str, fromDate: str, toDate: str, pageIndex: int, pageSize: int, ascending: bool):
        req = model.daily_ohlc

        req['symbol'] = symbol
        req['fromDate'] = fromDate
        req['toDate'] = toDate
        req['pageIndex'] = pageIndex
        req['pageSize'] = pageSize
        req['ascending'] = ascending

        # client = MarketDataClient(config, constants.OTHER)	
        client = MarketDataClient(self)
        res = client.daily_ohlc(constants.NONE, req)
        
        if not res["data"]:
            ohlcv_df = pd.DataFrame(columns=["date", "open", "high", "low", "close", "volume"])
            time_range = pd.date_range(start=fromDate,end=toDate,freq='d')
            for i in range(len(time_range)):
                ohlcv_df.loc[i, "date"]=time_range[i].to_pydatetime()
            ohlcv_df.set_index(["date"], inplace=True)
            ohlcv_df = ohlcv_df.apply(pd.to_numeric)
            ohlcv_df.index = pd.Series(ohlcv_df.index).apply(lambda x: self.format_date_pd(x))
            return ohlcv_df
        else:
            
            ohlcv = pd.DataFrame(res)
            ohlcv=ohlcv["data"]
            ohlcv = ohlcv.dropna().apply(pd.Series)
            ohlcv_df=ohlcv.drop(columns=['TradingDate','Symbol','Market','Time','Value'])
            ohlcv_df.index = ohlcv['TradingDate']
            ohlcv_df.index.name = "date"
            ohlcv_df = ohlcv_df.apply(pd.to_numeric)
            ohlcv_df.columns = ["open", "high", "low", "close", "volume"]
            ohlcv_df.index = pd.Series(ohlcv_df.index).apply(lambda x: self.format_date_ssi(x))
            return ohlcv_df
    
    def get_vn30_df(self, start_date, end_date):
        with open(r"C:/Users/luong/Desktop/SSI_API/SSI/config/vn30.json",'r') as d:
            symbols=json.load(d)
        symbols=symbols["symbols"]
        ohlcvs = {}
        for symbol in symbols:
            symbol_df = self.daily_ohlc(symbol, start_date, end_date, 1, 50, True)
            ohlcvs[symbol] = symbol_df
            print(symbol)
            print(ohlcvs[symbol]) 
        
        df = pd.DataFrame(index=ohlcvs["HPG"].index)
        df.index.name = "date"
        instruments = list(ohlcvs.keys())

        for inst in instruments:
            inst_df = ohlcvs[inst]
            columns = list(map(lambda x: "{} {}".format(inst, x), inst_df.columns)) 
            df[columns] = inst_df
            df["{} % ret".format(inst)] = df["{} close".format(inst)] / df["{} close".format(inst)].shift(1) - 1 
        
        return df, instruments

    def market_order(self, inst, order_config={}):
        pass

    def get_account_details(self):
        pass

    def get_account_summary(self):
        pass

    def get_account_instruments(self):
        pass

    def get_account_capital(self):
        pass

    def get_account_positions(self):
        pass

    def get_account_trades(self):
        pass

