from check_accout import check_account

def check_asset(asset_name):
    """
    자산 확인

    Args:
        asset_name (str): 자산 이름
            : 원화 - KRW, 리플 - XRP

    Raises:
        Exception: 자산 이름이 없을 경우 예외 발생

    Returns:
        int: 자산 잔액
    """
    account_data = check_account()
    for data in account_data:
        if data['currency'] == asset_name:
            return float(data['balance'])
    return 0

if __name__ == "__main__":
    print(check_asset('XRP'))