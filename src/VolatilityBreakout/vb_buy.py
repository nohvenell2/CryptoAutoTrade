import sys
import os

# 상위 디렉토리 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calc_targetprice import calc_targetprice_latest
from check_price import check_price
from check_asset import check_asset
from order_buy import order_buy_wait

def vb_buy(asset,market,k,max_price=10000,debug=False):
    # 자산이 보유중이면 이미 매수 포지션이기 때문에 매수를 실행하지 않음
    if check_asset(asset) > 0:
        if debug: print(f"{asset} 자산을 보유하고있어 매수를 실행하지 않습니다.")
        return 
    target_price = calc_targetprice_latest(k,debug=True)
    current_price = check_price('KRW-XRP',debug=False)

    # debugPrint
    if debug:
        print(f"VB 전략 매수 조건 확인")
        print(f"현재 가격: {current_price} {'>=' if current_price >= target_price else '<'} 타겟 가격: {target_price}")
    if current_price >= target_price:
        if debug: print(f"매수 주문 실행")
        vb_bid(market,max_price,debug)
        # debugPrint
        pass
    else:
        # debugPrint
        if debug: print(f"매수 조건 불만족")

def vb_bid(market,max_price=10000,debug=False):
    """
    변동성 돌파 매수 주문

    Args:
        market (str): 마켓 코드
        max_price (int, optional): 매수 금액 제한. Defaults to 10000.
        debug (bool, optional): 디버그 모드. Defaults to False.
    """
    krw_balance = check_asset('KRW')
    if krw_balance < 5000:
        # debugPrint
        if debug: print(f"KRW 잔액이 최소 매수 금액인 5000원 미만입니다.")
        raise Exception("KRW 잔액이 최소 매수 금액인 5000원 미만입니다.")
    # 매수 금액 제한
    price = min(krw_balance,max_price)
    order_result = order_buy_wait(market,price,debug)
    return order_result

if __name__ == "__main__":
    vb_buy('XRP','KRW-XRP', k=0.15, debug=True)
