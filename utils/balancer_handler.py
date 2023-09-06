from utils.starknet_balancer import *
from utils.aptos_balancer import *
from utils.file_handler import *


def get_balance(df: pd.DataFrame, chain: str = "Aptos"):
    items = df.index.values

    result = []

    if chain == "Aptos":
        result = asyncio.run(pool_aptos(addresses=items))
    elif chain == "Starknet":
        result = asyncio.run(pool_starknet(addresses=items))

    for i in result:
        df.at[i[0], 'amount in USDT'] = i[1]
        df.at[i[0], 'txs'] = i[2]

    return df
