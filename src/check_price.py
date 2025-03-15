import requests
def check_price(market,debug=False):
    url = f"https://api.upbit.com/v1/ticker"
    params = {
        'markets': market
    }
    response = requests.get(url, params=params)
    data = response.json()
    if debug: print(data)
    if 'error' in data or not data or len(data) == 0:
        raise Exception("No data found")
    return data[0]['trade_price']

if __name__ == "__main__":
    print(check_price('KRW-XRP',debug=True))

