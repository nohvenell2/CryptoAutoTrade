import requests

# KRW-BTC 마켓에 2024년 10월 1일(UTC) 이전 가장 최근 1분봉 1개를 요청
DEFAULT_MARKET = 'KRW-XRP'
DEFAULT_UNIT = 240
def fetch_ohlc(market = DEFAULT_MARKET, count = 1, time = None, unit = DEFAULT_UNIT,debug=False):
    """
    캔들 데이터를 가져오는 함수

    Args:
        market (str, optional): 마켓 코드. Defaults to DEFAULT_MARKET.
        count (int, optional): 캔들 개수. Defaults to 1. Maximum is 200.
        time (str, optional): 캔들 시간. Defaults to None.
            : 예시 : utc - 2024-10-01 00:00:00 // kst - 2023-01-01T00:00:00+09:00
            : None 일시 가장 최근 캔들 데이터 반환. close 가격이 실시간으로 변경되므로 주의
        unit (int, optional): 캔들 단위. Defaults to DEFAULT_UNIT.
        debug (bool, optional): 디버그 모드. Defaults to False.

    Raises:
        Exception: 데이터를 가져오지 못한 경우

    Returns:
        list: 캔들 데이터
    """
    url = f"https://api.upbit.com/v1/candles/minutes/{unit}"
    if time:
        params = {  
            'market': market,  
            'count': count,
            'to': time
        }  
    else:
        params = {  
            'market': market,  
            'count': count,
        }
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    fetch_result = response.json()
    # debugPrint
    if debug: print(fetch_result)
    if not fetch_result:
        raise Exception("No data found")
    result = []
    for p in fetch_result:
        result.append({
            'time': p['candle_date_time_kst'],
            'open': p['opening_price'],
            'high': p['high_price'],
            'low': p['low_price'],
            'close': p['trade_price'],
        })
    return result

if __name__ == "__main__":
    print(fetch_ohlc(count=5,unit=60,debug=True))
