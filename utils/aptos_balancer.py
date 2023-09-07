from utils.priceChecker import *


def create_session_aptos():
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

    return aiohttp.ClientSession(headers=headers)


async def get_aptos_ballance(session, address: str) -> float:
    for i in range(0, 5):
        try:
            async with session.get(f"https://api.aptscan.ai/v1/accounts/{address}/coin_value?cluster=mainnet") as res:
                res_json = await res.json()

                return res_json['data']
        except Exception:
            pass
    return 0


async def get_aptos_transactions(session, address: str) -> int:
    for i in range(0, 5):
        try:
            async with session.get(f"https://api.aptscan.ai/v1/accounts/{address}/transactions?page=1&cluster=mainnet&onlyCount=true") as res:
                res_json = await res.json()

                return int(res_json['data']['count'])
        except Exception:
            pass
    return 0


async def mega_aptos(session, address: str) -> list:
    balance = await get_aptos_ballance(session, address)
    txs = await get_aptos_transactions(session, address)

    return [address, balance, txs]


async def pool_aptos(addresses: list):
    session = create_session_aptos()

    tasks = []

    for address in addresses:
        task = asyncio.ensure_future(mega_aptos(session, address))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    await session.close()
    return responses
