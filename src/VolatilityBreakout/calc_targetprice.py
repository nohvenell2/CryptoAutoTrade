import sys
import os

# 상위 디렉토리 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetch_ohlc import fetch_ohlc

def calc_targetprice(k,ohlc,debug=False):
    opening_price = ohlc['open']
    high_price = ohlc['high']
    low_price = ohlc['low']
    close_price = ohlc['close']
    k_price = (high_price - low_price) * k
    target_price = close_price + k_price
    #debugPrint
    if debug:
        print(f"VB 타겟 가격 계산")
        print(f"High: {high_price}, Low: {low_price}, Close: {close_price}, K: {k}, K_price: {k_price}, Target: {target_price}")
    return target_price
def calc_targetprice_latest(k,debug=False):
    ohlc = fetch_ohlc(count=2)[1]
    target_price = calc_targetprice(k,ohlc,debug)
    return target_price

if __name__ == "__main__":
    calc_targetprice_latest(0.15,debug=True)