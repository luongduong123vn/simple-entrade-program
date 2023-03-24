from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def selenium_order(username,userpassword,price,lots,order):
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

    price_input = driver.find_element(By.XPATH,('//*[@id="order-price-inp"]'))
    price_input.send_keys(price)

    lots_input = driver.find_element(By.XPATH,('//*[@id="order-quantity-inp"]'))
    lots_input.send_keys(lots)

    if order=='long':
        long_click = driver.find_element(By.XPATH,('//*[@id="root"]/main/div/div[1]/div[1]/div/div[3]/form/div/div/div[2]/div[2]/div[1]'))
        long_click.click()
    elif order=='short':
        short_click = driver.find_element(By.XPATH,('//*[@id="root"]/main/div/div[1]/div[1]/div/div[3]/form/div/div/div[2]/div[2]/div[2]'))
        short_click.click()