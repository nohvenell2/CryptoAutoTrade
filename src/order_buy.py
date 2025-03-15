import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
import dotenv
from check_order import check_order
from show_order import show_order
import time

dotenv.load_dotenv()

access_key = os.environ['OTPYRC_ACC']
secret_key = os.environ['OTPYRC_CES']
server_url = os.environ['SERVER_URL']

def order_buy(market,price):
    params = {
        'market': market,
        'side': 'bid',
        'ord_type': 'price',
        'price': price,
    }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }

    res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
    return res.json()

def order_buy_wait(market,price,debug=False):
    order_result = order_buy(market,price)
    order_id = order_result['uuid']
    wait_time = 0
    while True:
        order_result = check_order(order_id)
        if order_result['trades_count'] == '0' or order_result['trades_count'] == 0:
            wait_time += 1
            time.sleep(1)
        else:
            if debug: print(f"매수 주문이 처리되었습니다.")
            break
        # todo 주문이 완료 되었음에도 cancel 로 나오는 경우가 있음. 추후 수정 필요
        """ elif order_result['state'] == 'cancel': 
            if debug: print(f"매수 주문이 취소되었습니다.")
            raise Exception("매수 주문이 취소되었습니다.") """
        if wait_time > 60:
            # todo 주문 취소처리 추가
            if debug: print(f"매수 주문이 60초 이상 처리되지 않았습니다.")
            raise Exception("매수 주문이 60초 이상 처리되지 않았습니다.")

    # debugPrint
    if debug: show_order(order_result)
    return order_result

if __name__ == '__main__':
    order_buy_wait('KRW-XRP',10000.0,debug=True)
