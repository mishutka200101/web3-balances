from utils.priceChecker import *


def get_aptos_ballance(session, address: str):
    headers = {
        'authority': 'api.aptscan.ai',
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'origin': 'https://aptscan.ai',
        'referer': 'https://aptscan.ai/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'page': '1',
        'cluster': 'mainnet',
    }

    Tether = ['USDC', 'USDT', 'DAI']
    total_balance = 0

    for i in range(0, 5):
        try:
            res = r.get(
                f"https://api.aptscan.ai/v1/accounts/{address}/coins",
                params=params,
                headers=headers,
            )
            res_json = res.json()
            coins = res_json['data']

            for coin in coins:
                symbol = coin['coin_symbol']
                decimals = coin['coin_decimals']
                value = int(coin['amount']) / 10**int(decimals)

                if symbol not in Tether:
                    usdt_value = ninjasPrice(token=symbol, value=value)
                    total_balance += usdt_value
                else:
                    total_balance += value

            return [address, round(total_balance, 2)]
        except Exception:
            pass
    return 0
