from utils.starknet_balancer import *
from utils.aptos_balancer import *
from utils.file_handler import *


def get_balance(df: pd.DataFrame, chain: str = "Aptos"):
    items = df['address']

    result = []

    if chain == "Aptos":
        result = asyncio.run(pool_aptos(addresses=items))
    elif chain == "Starknet":
        result = asyncio.run(pool_starknet(addresses=items))

    for i in result:
        df.at[result.index(i), 'amount in USDT'] = i[1]
        df.at[result.index(i), 'txs'] = i[2]

    return df
