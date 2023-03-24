from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import datetime
from datetime import time,date,datetime,timedelta
import pandas as pd


def entrade_login(username,userpassword):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://trading.entrade.com.vn/dang-nhap')
    username_input = driver.find_element(By.XPATH,('//*[@id="username-inp"]'))
    username_input.send_keys(username)

    userpassword_input = driver.find_element(By.XPATH,('//*[@id="password-inp"]'))
    userpassword_input.send_keys(userpassword)

    login_input = driver.find_element(By.XPATH,('//*[@id="login-btn"]'))
    login_input.click()

def selenium_order(username,userpassword,lots,order):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://trading.entrade.com.vn/dang-nhap')
    username_input = driver.find_element(By.XPATH,('//*[@id="username-inp"]'))
    username_input.send_keys(username)

    userpassword_input = driver.find_element(By.XPATH,('//*[@id="password-inp"]'))
    userpassword_input.send_keys(userpassword)

    login_input = driver.find_element(By.XPATH,('//*[@id="login-btn"]'))
    login_input.click()
    import time
    time.sleep(5)
 
    account_mode = driver.find_element(By.XPATH,('//*[@id="paper-trade-btn"]/div/div[1]/div[1]/label')).text
    if account_mode=='Demo':
        pass
    else:
        driver.find_element(By.XPATH,('//*[@id="paper-trade-btn"]/div/div[1]/div[2]/div/label')).click()

    MTL_click = MTL_click = driver.find_element(By.XPATH,('//*[@id="order-type"]/button[2]'))
    MTL_click.click()

    lots_input = driver.find_element(By.XPATH,('//*[@id="order-quantity-inp"]'))
    lots_input.send_keys(lots)

    if order=='long':
        long_click = driver.find_element(By.XPATH,('//*[@id="root"]/main/div/div[1]/div[1]/div/div[3]/form/div/div/div[2]/div[2]/div[1]'))
        long_click.click()
    elif order=='short':
        short_click = driver.find_element(By.XPATH,('//*[@id="root"]/main/div/div[1]/div[1]/div/div[3]/form/div/div/div[2]/div[2]/div[2]'))
        short_click.click()

def selenium_bbstrat_order(username,userpassword,price,lots,order):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://trading.entrade.com.vn/dang-nhap')
    username_input = driver.find_element(By.XPATH,('//*[@id="username-inp"]'))
    username_input.send_keys(username)

    userpassword_input = driver.find_element(By.XPATH,('//*[@id="password-inp"]'))
    userpassword_input.send_keys(userpassword)

    login_input = driver.find_element(By.XPATH,('//*[@id="login-btn"]'))
    login_input.click()
    import time
    time.sleep(5)
    agree_push = driver.find_element(By.XPATH,('//*[@id="agree-btn"]'))
    agree_push.click()

    account_mode = driver.find_element(By.XPATH,('//*[@id="paper-trade-btn"]/div/div[1]/div[1]/label')).text
    if account_mode=='Demo':
        pass
    else:
        driver.find_element(By.XPATH,('//*[@id="paper-trade-btn"]/div/div[1]/div[2]/div/label')).click()

    #MTL_click = driver.find_element(By.XPATH,('//*[@id="order-type"]/button[2]'))
    #MTL_click.click()
    
    #LO_click = driver.find_element(By.XPATH,('//*[@id="order-type"]/button[2]'))
    #LO_click.click()
    
    price_input = driver.find_element(By.XPATH,('//*[@id="order-price-inp"]'))
    price_input.send_keys(price)

    lots_input = driver.find_element(By.XPATH,('//*[@id="order-quantity-inp"]'))
    lots_input.send_keys(lots)
    

    if order=='long':
        #cancel_click = driver.find_element(By.XPATH,('//*[@id="deal-row-0-close-btn"]/span[1]'))
        #cancel_click.click()
        long_click = driver.find_element(By.XPATH,('//*[@id="root"]/main/div/div[1]/div[1]/div/div[3]/form/div/div/div[2]/div[2]/div[1]'))
        long_click.click()
    elif order=='short':
        #cancel_click = driver.find_element(By.XPATH,('//*[@id="deal-row-0-close-btn"]/span[1]'))
        #cancel_click.click()
        short_click = driver.find_element(By.XPATH,('//*[@id="root"]/main/div/div[1]/div[1]/div/div[3]/form/div/div/div[2]/div[2]/div[2]'))
        short_click.click()

def get_file_name(mypath):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def format_date_pd(series):
    #series in the form : pandas date range
    yymmdd = list(map(lambda x: int(x), str(series).split(" ")[0].split("-")))
    return datetime.date(int(yymmdd[0]),int(yymmdd[1]),int(yymmdd[2]))

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

def get_vn30f_df():
    vn30f1m_df = get_data("VN30F1M")
    vn30f2m_df = get_data("VN30F2M")
    vn30f_df = vn30f1m_df.merge(vn30f2m_df, on='Date', how='left')
    cols = ['Close VN30F2M', 'High VN30F2M', 'Low VN30F2M', 'Open VN30F2M']
    for col in cols:
        vn30f_df[col]= vn30f_df[col].ffill()
    vn30f_df['Volume VN30F2M'] = vn30f_df['Volume VN30F2M'].fillna(0)
    return vn30f_df
        
    

    