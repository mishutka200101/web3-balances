from utils.starknet_balancer import *
from utils.aptos_balancer import *
from utils.file_handler import *
from multiprocessing import Pool


def get_balance(df: pd.DataFrame, chain: str = "Aptos"):
    items = df.index.values

    processes = 40 if len(items) >= 40 else len(items)

    if chain == "Aptos":
        with Pool(processes=processes) as p:
            result = p.map(func=get_aptos_ballance, iterable=items)
    elif chain == "Starknet":
        with Pool(processes=processes) as p:
            result = p.map(func=get_starknet_balance, iterable=items)

    for i in result:
        df.at[i[0], 'amount in USDT'] = i[1]

    return df
