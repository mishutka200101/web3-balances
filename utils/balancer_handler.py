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

    for i, res in enumerate(result):
        df.at[i, 'amount in USDT'] = res[1]
        df.at[i, 'txs'] = res[2]

    return df
