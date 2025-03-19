from datetime import datetime
import pytz

def format_datetime(datetime_str):
    """UTC 시간을 한국 시간으로 변환하고 포맷팅"""
    dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    korea_tz = pytz.timezone('Asia/Seoul')
    korea_time = dt.astimezone(korea_tz)
    return korea_time.strftime('%Y-%m-%d %H:%M:%S')

def show_order_simple(order_result):
    """주문 결과를 한 줄로 간단히 출력하는 함수"""
    if not order_result or 'uuid' not in order_result:
        print("유효하지 않은 주문 결과입니다.")
        return

    order_type = "매수" if order_result['side'] == 'bid' else "매도"
    status = {'wait': '대기', 'done': '완료', 'cancel': '취소'}.get(order_result['state'], '알 수 없음')
    
    if order_result['trades'] and len(order_result['trades']) > 0:
        total_volume = sum(float(trade['volume']) for trade in order_result['trades'])
        total_funds = sum(float(trade['funds']) for trade in order_result['trades'])
        avg_price = total_funds / total_volume if total_volume > 0 else 0
        
        print(f"[{format_datetime(order_result['created_at'])}] {order_type} {status}: {order_result['market']} | " 
              f"수량: {total_volume:.8f} | 평균가: {avg_price:,.2f}원 | 총액: {total_funds:,.2f}원")
    else:
        print(f"[{format_datetime(order_result['created_at'])}] {order_type} {status}: {order_result['market']} | 미체결")

def show_order(order_result):
    """주문 결과를 깔끔하게 출력하는 함수"""
    if not order_result or 'uuid' not in order_result:
        print("유효하지 않은 주문 결과입니다.")
        return

    # 주문 타입 한글로 변환
    order_type = "매수" if order_result['side'] == 'bid' else "매도"
    order_status = {
        'wait': '대기',
        'done': '완료',
        'cancel': '취소'
    }.get(order_result['state'], '알 수 없음')

    print("\n" + "="*50)
    print(f"📊 {order_type} 주문 결과")
    print("="*50)
    print(f"🏷️ 주문 ID: {order_result['uuid']}")
    print(f"📈 마켓: {order_result['market']}")
    print(f"⏰ 주문 시각: {format_datetime(order_result['created_at'])}")
    print(f"📋 상태: {order_status}")
    
    # 거래 정보 출력
    if order_result['trades'] and len(order_result['trades']) > 0:
        trades_count = len(order_result['trades'])
        
        # 단일 거래인 경우
        if trades_count == 1:
            trade = order_result['trades'][0]
            print("\n[체결 정보]")
            print(f"💰 체결 가격: {int(trade['price']):,}원")
            print(f"📊 체결 수량: {float(trade['volume']):.8f}")
            print(f"💵 체결 금액: {float(trade['funds']):,.2f}원")
            print(f"⏰ 체결 시각: {format_datetime(trade['created_at'])}")
            print(f"📈 추세: {'상승' if trade['trend'] == 'up' else '하락'}")
        
        # 다중 거래인 경우
        else:
            print(f"\n[체결 정보] - 총 {trades_count}건")
            total_volume = 0
            total_funds = 0
            
            for i, trade in enumerate(order_result['trades'], 1):
                print(f"\n📍 {i}번째 체결:")
                print(f"  💰 체결 가격: {int(trade['price']):,}원")
                print(f"  📊 체결 수량: {float(trade['volume']):.8f}")
                print(f"  💵 체결 금액: {float(trade['funds']):,.2f}원")
                print(f"  ⏰ 체결 시각: {format_datetime(trade['created_at'])}")
                print(f"  📈 추세: {'상승' if trade['trend'] == 'up' else '하락'}")
                
                total_volume += float(trade['volume'])
                total_funds += float(trade['funds'])
            
            # 총 거래 정보 출력
            print("\n[총 체결 정보]")
            print(f"📊 총 체결 수량: {total_volume:.8f}")
            print(f"💵 총 체결 금액: {total_funds:,.2f}원")
            if total_volume > 0:
                avg_price = total_funds / total_volume
                print(f"💹 평균 체결 가격: {avg_price:,.2f}원")
        
    # 수수료 정보
    print("\n[수수료 정보]")
    print(f"💸 지불 수수료: {float(order_result['paid_fee']):,.8f}원")
    
    print("="*50 + "\n")

def example_usage():
    """함수 사용 예제"""
    # 단일 거래 예제 데이터
    single_trade = {
        'uuid': 'ddedecb4-f477-40f2-ab49-5bbec4d9ed8c',
        'side': 'bid',
        'ord_type': 'price',
        'price': '10000',
        'state': 'done',
        'market': 'KRW-XRP',
        'created_at': '2025-03-16T04:14:02+09:00',
        'reserved_fee': '5',
        'remaining_fee': '0.00000000928',
        'paid_fee': '4.99999999072',
        'locked': '0.00001856928',
        'executed_volume': '2.82565696',
        'trades_count': 1,
        'trades': [{
            'market': 'KRW-XRP',
            'uuid': '974e3a92-0c18-4791-a7b3-8901e5afe00d',
            'price': '3539',
            'volume': '2.82565696',
            'funds': '9999.99998144',
            'trend': 'up',
            'created_at': '2025-03-16T04:14:02+09:00',
            'side': 'bid'
        }]
    }
    
    # 다중 거래 예제 데이터
    multiple_trades = {
        'uuid': 'ddedecb4-f477-40f2-ab49-5bbec4d9ed8c',
        'side': 'bid',
        'ord_type': 'price',
        'price': '10000',
        'state': 'done',
        'market': 'KRW-XRP',
        'created_at': '2025-03-16T04:14:02+09:00',
        'reserved_fee': '5',
        'remaining_fee': '0.00000000928',
        'paid_fee': '4.99999999072',
        'locked': '0.00001856928',
        'executed_volume': '2.82565696',
        'trades_count': 2,
        'trades': [
            {
                'market': 'KRW-XRP',
                'uuid': '974e3a92-0c18-4791-a7b3-8901e5afe00d',
                'price': '3539',
                'volume': '1.82565696',
                'funds': '6459.99998144',
                'trend': 'up',
                'created_at': '2025-03-16T04:14:02+09:00',
                'side': 'bid'
            },
            {
                'market': 'KRW-XRP',
                'uuid': '974e3a92-0c18-4791-a7b3-8901e5afe00e',
                'price': '3540',
                'volume': '1.00000000',
                'funds': '3540.00000000',
                'trend': 'down',
                'created_at': '2025-03-16T04:14:03+09:00',
                'side': 'bid'
            }
        ]
    }

    print("\n[간단한 출력 예제]")
    show_order_simple(single_trade)
    show_order_simple(multiple_trades)
    
"""     print("\n[상세 출력 예제]")
    show_order(single_trade)
    show_order(multiple_trades) """

if __name__ == "__main__":
    example_usage()
