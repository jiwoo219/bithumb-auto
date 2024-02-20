import time
import pybithumb
import datetime

bithumb = pybithumb.Bithumb("c8047fbde2e9c12fd6406553b136659f", "f61ac1687cb35be63b9ccf07713a7c9e")

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def get_start_time(ticker):
    df = pybithumb.get_ohlcv(ticker)
    start_time = df.index[-1]
    return start_time

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']   
    unit = krw/float(sell_price)*0.8
    bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean().iloc[-1]
    return ma

print("autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("BTC")
            ma5 = get_yesterday_ma5("BTC")
            print("target_price:", target_price, "ma5:", ma5)
            current_price = pybithumb.get_current_price("BTC")
            print("current_price:", current_price)

            if target_price < current_price and current_price > ma5:
                krw = bithumb.get_balance("BTC")[2] > 5000
                if krw > 5000:
                    bithumb.buy_market_order("KRW-BTC")
        else:
            btc = bithumb.get_balance("BTC")[0]
            if btc > 0.0008:
                sell_crypto_currency("BTC")
    
    except Exception as e:
        print(e) 
        time.sleep(1)