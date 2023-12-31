from pybithumb import Bithumb
import time
import datetime

bithumb = Bithumb("e94e5052bc5971b42f885a175507c5f9", "53582a67fc5d830641e5e8c1edb332b0")


# 코인 리스트 가져오기
# coins = Bithumb.get_tickers()
coins = ['BTC']

# 내 자산현황 가져오기
# for coin in coins:
#     if bithumb.get_balance(coin)[0] > 0.00001:
#         print(coin, bithumb.get_balance(coin))

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
total = 0

# 자동 거래 시작
while total < 1200000000:
    try:
        now = datetime.datetime.now()

        # 자정이면 total 초기화
        if mid < now < mid + datetime.timedelta(seconds=10):
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.datetime(1)
            total = 0

        for coin in coins:
            # 코인의 현재 잔고 조회
            balance = bithumb.get_balance(coin)

            # 매도
            if balance[0] > 0.000001 and balance[1] < 0.000001:
                time.sleep(5)
                ask_price = Bithumb.get_orderbook(coin)['asks'][0]['price'] # 제 1 매도호가
                desc = bithumb.sell_limit_order(coin, ask_price, balance[0])
                total += ask_price * balance[0]
                print(desc)
                print("total", total)

            # 매수
            if balance[0] < 0.000001 and balance[3] < 0.000001:
                time.sleep(5)
                bid_price = Bithumb.get_orderbook(coin)['bids'][0]['price'] # 제 1 매수호가
                if balance[2] < 930000:
                    total = 16000000000

                desc = bithumb.buy_limit_order(coin, bid_price, balance[2] / float(bid_price))
                total += balance[2] * 0.85
                print(desc)
                print("total", total)

    except Exception as e:
        print(f"An error occurred: {e}")



# 시장가 매수
# desc = bithumb.buy_market_order(coin, quantity)
# 지정가 매수
# desc = bithumb.buy_limit_order(coin, price, quantity)