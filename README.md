## 환경설정

패키지 목록 업데이트: sudo apt update

pip3 설치: sudo apt install python3-pip

pip3로 pyupbit 설치: pip3 install pybithumb

백그라운드 실행: nohup python3 bitcoinAutoTrade.py > output.log &

실행되고 있는지 확인: ps ax | grep .py

프로세스 종료(PID는 ps ax | grep .py를 했을때 확인 가능): kill -9 PID
