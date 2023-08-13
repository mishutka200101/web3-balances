from utils.priceChecker import *


def get_starknet_balance(address: str):
    headers = {
        'authority': 'starkscan.stellate.sh',
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://starkscan.co',
        'referer': 'https://starkscan.co/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

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
            res = r.post('https://starkscan.stellate.sh/', headers=headers, json=json_data)
            res_json = res.json()

            all_tokens = res_json['data']['erc20BalancesByOwnerAddress']

            total_balance = 0
            Tethers = ['USDT', 'USDC']

            for token in all_tokens:
                token_name = token['contract_erc20_contract']['symbol']
                balance = float(token['balance_display'])

                if token_name not in Tethers:
                    total_balance += ninjasPrice(token_name, balance)
                else:
                    total_balance += balance

            return [address, round(total_balance, 2)]
        except Exception:
            pass
    return 0
