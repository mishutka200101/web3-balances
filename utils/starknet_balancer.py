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

    for i in range(0, 5):
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
        'query': 'query ContractPageQuery(\n  $input: ContractInput!\n) {\n  contract(input: $input) {\n    contract_address\n    is_starknet_class_code_verified\n    implementation_type\n    ...ContractPageContainerFragment_contract\n    ...ContractPageOverviewTabFragment_contract\n    ...ContractPageClassCodeHistoryTabFragment_contract\n    ...ContractFunctionReadWriteTabFragment_contract\n    id\n  }\n}\n\nfragment ContractFunctionReadCallsFragment_starknetClass on StarknetClass {\n  is_code_verified\n  abi_final\n}\n\nfragment ContractFunctionReadWriteTabFragment_contract on Contract {\n  contract_address\n  starknet_class {\n    ...ContractFunctionReadCallsFragment_starknetClass\n    ...ContractFunctionWriteCallsFragment_starknetClass\n    id\n  }\n}\n\nfragment ContractFunctionWriteCallsFragment_starknetClass on StarknetClass {\n  is_code_verified\n  abi_final\n}\n\nfragment ContractPageClassCodeHistoryTabFragment_contract on Contract {\n  contract_address\n  starknet_class {\n    is_code_verified\n    id\n  }\n  ...ContractPageCodeSubTabFragment_contract\n}\n\nfragment ContractPageCodeSubTabFragment_contract on Contract {\n  starknet_class {\n    class_hash\n    ...StarknetClassCodeTabFragment_starknetClass\n    id\n  }\n}\n\nfragment ContractPageContainerFragment_contract on Contract {\n  contract_address\n  implementation_type\n  is_starknet_class_code_verified\n  contract_stats {\n    number_of_transactions\n    number_of_account_calls\n    number_of_events\n  }\n  starknet_id {\n    domain\n  }\n}\n\nfragment ContractPageOverviewTabClassHashPlacedAtItemFragment_contract on Contract {\n  deployed_at_transaction_hash\n  class_hash_placed_at_transaction_hash\n  class_hash_placed_at_timestamp\n}\n\nfragment ContractPageOverviewTabEthBalanceItemFragment_contract on Contract {\n  eth_balance {\n    balance_display\n    id\n  }\n}\n\nfragment ContractPageOverviewTabFragment_contract on Contract {\n  contract_address\n  class_hash\n  name_tag\n  is_social_verified\n  deployed_by_contract_address\n  deployed_by_contract_identifier\n  deployed_at_transaction_hash\n  deployed_at_timestamp\n  ...ContractPageOverviewTabEthBalanceItemFragment_contract\n  ...ContractPageOverviewTabTypeItemFragment_contract\n  ...ContractPageOverviewTabStarknetIDItemFragment_contract\n  starknet_class {\n    ...StarknetClassVersionItemFragment_starknetClass\n    id\n  }\n  ...ContractPageOverviewTabClassHashPlacedAtItemFragment_contract\n}\n\nfragment ContractPageOverviewTabStarknetIDItemFragment_contract on Contract {\n  starknet_id {\n    domain\n  }\n}\n\nfragment ContractPageOverviewTabTypeItemFragment_contract on Contract {\n  implementation_type\n  starknet_class {\n    type\n    id\n  }\n}\n\nfragment StarknetClassCodeTabFragment_starknetClass on StarknetClass {\n  ...StarknetClassCodeTabVerifiedItemFragment_starknetClass\n  ...StarknetClassCodeTabSourceCodeItemFragment_starknetClass\n  ...StarknetClassCodeTabOnChainCodeItemFragment_starknetClass\n}\n\nfragment StarknetClassCodeTabOnChainCodeItemFragment_starknetClass on StarknetClass {\n  is_code_verified\n  abi_final\n  bytecode\n  sierra_program\n  entry_points_by_type\n}\n\nfragment StarknetClassCodeTabSourceCodeItemFragment_starknetClass on StarknetClass {\n  class_hash\n  verified {\n    source_code\n  }\n}\n\nfragment StarknetClassCodeTabVerifiedItemFragment_starknetClass on StarknetClass {\n  is_code_verified\n  verified {\n    name\n    source_code\n    verified_at_timestamp\n  }\n}\n\nfragment StarknetClassVersionItemFragment_starknetClass on StarknetClass {\n  is_cairo_one\n}\n',
        'variables': {
            'input': {
                'contract_address': address,
            },
        },
    }

    for _ in range(0, 5):
        try:
            async with session.post('https://graphql.starkscancdn.com', json=json_data) as res:
                res_json = await res.json()

                return int(res_json['data']['contract']['contract_stats']['number_of_transactions'])
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
