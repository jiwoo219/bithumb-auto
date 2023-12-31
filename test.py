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

last_reset_time = datetime.datetime.now()

total = 0

# 자동 거래 시작
while total < 1500000000:
    try:
        for coin in coins:
            # 코인의 현재 잔고 조회
            balance = bithumb.get_balance(coin)

            if balance[0] > 0.000001 and balance[1] < 0.000001:
                # 매도
                ask_price = Bithumb.get_orderbook(coin)['asks'][1]['price'] # 제 2 매도호가
                desc = bithumb.sell_limit_order(coin, ask_price, balance[0])
                total += ask_price * balance[0]
                print(desc)

                time.sleep(10)
                print("total", total)

            if balance[0] < 0.000001 and balance[3] < 0.000001:
                # 매수
                bid_price = Bithumb.get_orderbook(coin)['bids'][1]['price'] # 제 2 매수호가
                if balance[2] < 400000:
                    total = 16000000000

                desc = bithumb.buy_limit_order(coin, bid_price, balance[2] / bid_price * 0.99)
                total += balance[2] * 0.85
                print(desc)

                time.sleep(10)
                print("total", total)

            # 24시간이 경과하면 total을 0으로 초기화
            current_time = datetime.datetime.now()
            if current_time - last_reset_time >= datetime.timedelta(hours=24):
                total = 0
                last_reset_time = current_time

    except Exception as e:
        print(f"An error occurred: {e}")



# 시장가 매수
# desc = bithumb.buy_market_order(coin, quantity)
# 지정가 매수
# desc = bithumb.buy_limit_order(coin, price, quantity)