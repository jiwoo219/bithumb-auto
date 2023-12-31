from pybithumb import Bithumb
import time
import datetime

bithumb = Bithumb("e94e5052bc5971b42f885a175507c5f9", "53582a67fc5d830641e5e8c1edb332b0")

coins = ['BTC']

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
            if balance[0] > 0.000001:
                time.sleep(5)
                ask_price = Bithumb.get_orderbook(coin)['asks'][0]['price'] # 제 1 매도호가
                desc = bithumb.sell_limit_order(coin, ask_price, balance[0])
                start_time = time.time()

                # 30초 이내에 팔리지 않으면 매도 취소
                while time.time() - start_time < 30:
                    quanity = bithumb.get_outstanding_order(desc)
                    
                    if not quanity: # 매도 완료
                        total += ask_price * balance[0]
                        break
                
                if quanity:
                    status = bithumb.cancel_order(desc)
                    print('cancel order', status)

                print("total", total)

            # 매수
            if balance[0] < 0.000001:
                time.sleep(5)
                bid_price = Bithumb.get_orderbook(coin)['bids'][0]['price'] # 제 1 매수호가
                if balance[2] < 930000: # 손실이 많이 일어났으면 Stop
                    total = 16000000000

                desc = bithumb.buy_limit_order(coin, bid_price, balance[2] / bid_price * 0.99)
                start_time = time.time()

                # 30초 이내에 팔리지 않으면 매수 취소:
                while time.time() - start_time < 30:
                    quanity = bithumb.get_outstanding_order(desc)

                    if not quanity: # 매수 완료
                        total += balance[2] * 0.99
                        break
                
                if quanity:
                    status = bithumb.cancel_order(desc)
                    print('cancel order', status)

                print("total", total)

    except Exception as e:
        print(f"An error occurred: {e}")