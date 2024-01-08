from pybithumb import Bithumb
import time
import datetime

bithumb = Bithumb("06b42812e4aaec48580d555510727836", "a67680d16e15140a872911b6728e0be9")

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

coin = 'BTC'

total = 0
buy_price = Bithumb.get_orderbook(coin)['bids'][0]['price']

# 자동 거래 시작
while True:
    try:
        now = datetime.datetime.now()

        # 자정이면 total 초기화
        if mid < now < mid + datetime.timedelta(seconds=10):
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.datetime(1)
            total = 0

        # 15억 이상이면 스탑
        if total > 1500000000:
            continue

        # 코인의 현재 잔고 조회
        balance = bithumb.get_balance(coin) # 비트코인의 총 잔고, 거래 중인 비트코인의 수량, 보유 중인 총원화, 주문에 사용된 원화

        # 매도
        if balance[0] > 0.0001:
            time.sleep(2)
            ask_price = Bithumb.get_orderbook(coin)['asks'][0]['price'] # 제 1 매도호가
            sell_price = max(ask_price, buy_price)

            desc = bithumb.sell_limit_order(coin, sell_price, balance[0])
            start_time = time.time()

            # 20초 이내에 팔리지 않으면 매도 취소
            while time.time() - start_time < 20:
                quanity = bithumb.get_outstanding_order(desc)
                balance = bithumb.get_balance(coin)
                
                if not balance[1]: # 매도 완료
                    total += sell_price * balance[0]
                    print("sell successfully")
                    print("total", total)
                    break
            
            if balance[1]: # 매도 실패
                status = bithumb.cancel_order(desc)
                buy_price = ask_price
                print('cancel sell', status)

        # 매수
        if balance[0] <= 0.0001:
            time.sleep(2)
            bid_price = Bithumb.get_orderbook(coin)['bids'][0]['price'] # 제 1 매수호가

            if balance[2] < 970000: # 손실이 많이 일어났으면 Stop
                total = 1600000000

            desc = bithumb.buy_limit_order(coin, bid_price, balance[2] / bid_price * 0.99)
            start_time = time.time()

            # 10초 이내에 팔리지 않으면 매수 취소:
            while time.time() - start_time < 10:
                quanity = bithumb.get_outstanding_order(desc)

                if not quanity: # 매수 완료
                    total += balance[2] * 0.99
                    buy_price = bid_price
                    print("buy successfully")
                    print("total", total)
                    break
            
            if quanity: # 매수 실패
                status = bithumb.cancel_order(desc)
                print('cancel buy', status)

    except Exception as e:
        print(f"An error occurred: {e}")