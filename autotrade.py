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
    print("today open:", today_open, "yesterday high:", yesterday_high, "yesterday_low:", yesterday_low)
    print(target)
    return target


def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['bids'][0]['price']
    unit = krw/float(sell_price)*0.75
    desc = bithumb.buy_market_order(ticker, unit)
    print("buy", desc)


def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    desc = bithumb.sell_market_order(ticker, unit)
    print("sell", desc)


def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]


now = datetime.datetime.now() + datetime.timedelta(hours=9)
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)
ma5 = get_yesterday_ma5("BTC")
target_price = get_target_price("BTC")

while True:
    try:
        now = datetime.datetime.now() + datetime.timedelta(hours=9)
        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price("BTC")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.datetime(days=1)
            ma5 = get_yesterday_ma5("BTC")
            sell_crypto_currency("BTC")

        current_price = pybithumb.get_current_price("BTC")
        if current_price > target_price and current_price > ma5:
            if bithumb.get_balance("BTC")[2] > 5000:
                buy_crypto_currency("BTC")
            
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(1)
