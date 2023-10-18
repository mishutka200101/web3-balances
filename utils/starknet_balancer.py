from utils.priceChecker import *


def create_session_starknet():
    headers = {
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Referer': 'https://starkscan.co/',
        'sec-ch-ua-platform': '"Windows"',
    }

    return ClientSession(headers=headers)


async def get_starknet_balance(session: ClientSession, address: str) -> float | int:
    json_data = {
        'query': 'query ERC20BalancesByOwnerAddressTableQuery(\n  $input: ERC20BalancesByOwnerAddressInput!\n) {\n  erc20BalancesByOwnerAddress(input: $input) {\n    id\n    ...ERC20BalancesByOwnerAddressTableRowFragment_erc20Balance\n  }\n}\n\nfragment ERC20BalancesByOwnerAddressTableRowFragment_erc20Balance on ERC20Balance {\n  id\n  contract_address\n  contract_erc20_identifier\n  contract_erc20_contract {\n    symbol\n    is_social_verified\n    icon_url\n    id\n  }\n  balance_display\n}\n',
        'variables': {
            'input': {
                'owner_address': address,
            },
        },
    }

    for _ in range(0, 5):
        try:
            async with session.post('https://graphql.starkscancdn.com', json=json_data) as res:
                res_json = await res.json()

                all_tokens = res_json['data']['erc20BalancesByOwnerAddress']

                total_balance = 0
                Tethers = ['USDT', 'USDC', 'DAI']

                for token in all_tokens:
                    token_name = token['contract_erc20_contract']['symbol']
                    balance = float(token['balance_display'])

                    if token_name not in Tethers:
                        total_balance += await ninjasPrice(token=token_name, value=balance)
                    else:
                        total_balance += balance

                return round(total_balance, 2)
        except Exception:
            pass
    return 0


async def get_starknet_transactions(session, address: str) -> int:
    json_data = {
        'query': 'query TransactionsTableQuery(\n  $first: Int!\n  $after: String\n  $input: TransactionsInput!\n) {\n  ...TransactionsTablePaginationFragment_transactions_2DAjA4\n}\n\nfragment TransactionsTableExpandedItemFragment_transaction on Transaction {\n  entry_point_selector_name\n  calldata_decoded\n  entry_point_selector\n  calldata\n  initiator_address\n  initiator_identifier\n  main_calls {\n    selector\n    selector_name\n    calldata_decoded\n    selector_identifier\n    calldata\n    contract_address\n    contract_identifier\n    id\n  }\n}\n\nfragment TransactionsTablePaginationFragment_transactions_2DAjA4 on Query {\n  transactions(first: $first, after: $after, input: $input) {\n    edges {\n      node {\n        id\n        ...TransactionsTableRowFragment_transaction\n        __typename\n      }\n      cursor\n    }\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n  }\n}\n\nfragment TransactionsTableRowFragment_transaction on Transaction {\n  id\n  transaction_hash\n  block_number\n  transaction_status\n  transaction_type\n  timestamp\n  initiator_address\n  initiator_identifier\n  initiator {\n    is_social_verified\n    id\n  }\n  main_calls {\n    selector_identifier\n    id\n  }\n  ...TransactionsTableExpandedItemFragment_transaction\n}\n',
        'variables': {
            'first': 10,
            'after': None,
            'input': {
                'initiator_address': address,
                'transaction_types': None,
                'sort_by': 'timestamp',
                'order_by': 'desc',
                'min_block_number': None,
                'max_block_number': None,
                'min_timestamp': None,
                'max_timestamp': None,
            },
        },
    }

    for _ in range(0, 5):
        try:
            async with session.post('https://graphql.starkscancdn.com', json=json_data) as res:
                res_json = await res.json()

                return len(res_json["data"]["transactions"]["edges"])
        except Exception:
            pass
    return 0


async def mega_starknet(session, address: str) -> list:
    balance = await get_starknet_balance(session, address)
    txs = await get_starknet_transactions(session, address)

    return address, balance, txs


async def pool_starknet(addresses: list):
    session = create_session_starknet()

    tasks = []

    for address in addresses:
        task = asyncio.ensure_future(mega_starknet(session, address))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    await session.close()
    return responses
