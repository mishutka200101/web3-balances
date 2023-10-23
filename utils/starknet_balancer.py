from utils.priceChecker import *


async def get_starknet_balance(session: ClientSession, address: str) -> float | int:
    try:
        async with session.get(f"https://voyager.online/api/contract/{address}/balances") as res:
            r = await res.json()
            balance = 0

            for i in r:
                balance += float(i["usdFormattedBalance"][1:])
            
            return balance
    except Exception:
        return 0


async def get_starknet_transactions(session, address: str) -> int:
        try:
            async with session.get(f"https://voyager.online/api/contract/{address}") as res:
                r = await res.json()

                return int(r["nonce"], 16)
        except Exception:
            return 0


async def mega_starknet(session, address: str) -> list:
    balance = await get_starknet_balance(session, address)
    txs = await get_starknet_transactions(session, address)

    return address, balance, txs


async def pool_starknet(addresses: list):
    async with ClientSession() as session:
        tasks = []

        for address in addresses:
            task = asyncio.ensure_future(mega_starknet(session, address))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses
