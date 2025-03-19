import sys
import os

# 상위 디렉토리 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetch_ohlc import fetch_ohlc
from calc_targetprice import calc_targetprice

def optimize_k(market,k_range=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],time_unit=240,debug=False):
    """
    변동성 돌파 전략의 k 값을 최적화하는 함수

    Args:
        market (str): 마켓 코드
        k_range (list, optional): k 값 범위. Defaults to [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0].
        time_unit (int, optional): 캔들 시간 단위(분). Defaults to 60. 1,3,5,15,30,60,240 택1
        debug (bool, optional): 디버그 모드. Defaults to False.

    Returns:
        float: 최적 k 값
    """
    ohlc_data = fetch_ohlc(market,unit=time_unit,count=200)[1:]
    best_k, best_return = 0, 0
    if debug: print(f"최적 K 값 찾기 시작")
    for k in k_range:
        current_return = calc_k(ohlc_data, k, debug)
        if current_return['return_rate'] > best_return:
            best_return = current_return['return_rate']
            best_k = k
    
    if debug:
        print(f"최적 K 값: {best_k}, 수익률: {best_return}")
    return best_k

def calc_k(ohlc_data,k_value,debug=False):
    """
    VB 전략의 수익률을 계산하는 함수
    Args:
        ohlc_data (list): 캔들 데이터 (최신 데이터가 앞에 있는 리스트)
        k_value (float): k 값
        debug (bool): 디버그 모드
    """
    # 과거 데이터부터 처리하기 위해 리스트 순서 반전
    ohlc_data = list(reversed(ohlc_data))
    past_data = None
    return_rate = 1
    trade_count = 0
    for current_data in ohlc_data:
        if not past_data:
            past_data = current_data
            continue
        target_price = calc_targetprice(ohlc=past_data,k=k_value)
        # 타겟 가격보다 가격이 더 올라간 적이 있었으면 타겟 가격에 구매한 것으로 간주
        if current_data['high'] >= target_price :
            # 타겟 가격에 구매하고 청산 시점에 판매
            # debug
            profit_ratio = (current_data['close'] - target_price) / target_price
            return_rate *= (1 + profit_ratio)
            trade_count += 1
        past_data = current_data
    if debug: print(f"VB 수익률 계산 : K = {k_value} / 수익률 : {return_rate} / 매매 횟수 : {trade_count}")
    return {"return_rate":round(return_rate,6),"trade_count":trade_count}
if __name__ == "__main__":
    optimize_k(market="KRW-XRP",k_range = [ i/10 for i in range(40,51)],debug=True)
