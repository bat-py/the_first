import requests

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'accept': '*/*',
}


# currency: btc or ltc
def get_cource(currency: str, product_price: int):
    cource = requests.get(f'https://apirone.com/api/v2/ticker?currency={currency}', headers=HEADERS).json()['rub']
    price_in_crypto = int(product_price) / cource

    return int(cource), round(price_in_crypto, 8)
