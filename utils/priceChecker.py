import aiohttp
import asyncio


async def ninjasPrice(token: str, value: float):
    API_KEY = 'eVy9YM5Efe3E//g6qeEtyA==viTgktpo6UQbWRqS'

    symbol = token + 'USDT'
    url = 'https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(symbol)
    headers = {'X-Api-Key': API_KEY}

    session = aiohttp.ClientSession(headers=headers)

    async with session.get(url) as r:
        try:
            res_json = await r.json()
            price = float(res_json['price'])

            return price * value
        except Exception:
            return 0
        finally:
            await session.close()
    # if res.status_code == r.codes.ok:
    #     price = float(res.json()['price'])
    #     return price * value
    # else:
    #     return 0
