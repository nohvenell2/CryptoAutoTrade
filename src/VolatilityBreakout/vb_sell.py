import sys
import os
import time
# 상위 디렉토리 경로를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from show_order import show_order_simple
from check_asset import check_asset
from order_sell import order_sell_wait
import time

def vb_sell(market, asset_name, debug=False):
    """
    변동성 돌파 자신 전체 매도

    Args:
        market (str): 마켓 코드
            : 리플 - KRW-XRP
        asset_name (str): 자산 이름
            : 원화 - KRW, 리플 - XRP
        debug (bool, optional): 디버그 모드. Defaults to False.

    Returns:
        _type_: _description_
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if debug: print(f"{current_time} VB 전략 매도 실행")    
    asset_balance = check_asset(asset_name)
    if asset_balance <= 0:
        # debugPrint
        if debug: print(f"{asset_name} 자산을 보유하고있지 않아 매도를 실행하지 않습니다.")
        return None
    order_result = order_sell_wait(market,asset_balance,debug)
    return order_result

if __name__ == "__main__":
    ASSET = 'XRP'
    MARKET = 'KRW-XRP'
    # 매도 실행
    result = vb_sell(MARKET,ASSET,debug=False)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if result:
        print(f"### 💵 {current_time} - 매도 실행")
        print(f"{show_order_simple(result)}")
    else:
        # todo 매도 실행 조건 불만족
        pass
