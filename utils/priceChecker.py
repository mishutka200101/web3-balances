import requests as r


def ninjasPrice(token: str, value: float):
    API_KEY = 'eVy9YM5Efe3E//g6qeEtyA==viTgktpo6UQbWRqS'

    symbol = token + 'USDT'
    url = 'https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(symbol)
    res = r.get(url=url, headers={'X-Api-Key': API_KEY})

    if res.status_code == r.codes.ok:
        price = float(res.json()['price'])
        return price * value
    else:
        return 0
