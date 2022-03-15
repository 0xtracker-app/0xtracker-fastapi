from .utils import make_get_json, make_get
import json
from .networks import WEB3_NETWORKS, SCAN_APIS
from web3 import Web3
from .multicall import Call, Multicall, parsers


async def lookup_token_info(token_list, network):

    calls = []
    for token in token_list:
        calls.append(Call(token, [f'symbol()(string)'], [
                     [f'{token}_symbol', None]]))
        calls.append(Call(token, [f'decimals()(uint256)'], [
                     [f'{token}_decimal', None]]))

    missing_tokens_info = await Multicall(calls, WEB3_NETWORKS[network], _strict=False)()

    format_token_data = {}

    for each in token_list:
        if f'{each}_decimal' in missing_tokens_info and f'{each}_symbol' in missing_tokens_info:
            token_decimal = f'{each}_decimal'
            token_symbol = f'{each}_symbol'
            format_token_data[each] = {
                'tkn0d': missing_tokens_info[token_decimal], 'tkn0s': missing_tokens_info[token_symbol]}
        else:
            format_token_data[each] = {'tkn0d': 18, 'tkn0s': 'Unknown'}

    return format_token_data


async def scan_ethlogs_approval(network, address, session, mongodb):

    network_data = SCAN_APIS[network]
    apikey = network_data['api_key']
    # WEB3_NETWORKS[network]['connection'].eth.block_number
    latest_block = 'latest'
    scan_url = network_data['address']
    stripped_address = address[2:]

    topic0 = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'
    topic1 = f'0x000000000000000000000000{stripped_address}'

    url = f'https://api.{scan_url}/api?module=logs&action=getLogs&fromBlock=0&toBlock={latest_block}&topic0={topic0}&topic0_1_opr=and&topic1={topic1}&apikey={apikey}'

    r = await make_get_json(session, url)
    data0 = r['result']

    format_approvals = {}

    if len(data0) == 0:
        return {
            "userInfo": {
                "wallet": address
            },
            "approvals": {}
        }

    response_length = len(data0) - 1
    last_block = data0[response_length]['blockNumber']
    last_query_block = Web3.toInt(hexstr=last_block) + 1

    url = f'https://api.{scan_url}/api?module=logs&action=getLogs&fromBlock={last_query_block}&toBlock={latest_block}&topic0={topic0}&topic0_1_opr=and&topic1={topic1}&apikey={apikey}'

    r = await make_get_json(session, url)
    data1 = r['result']

    data = data0 + data1

    format_approvals = {'userInfo': {'wallet': address}, 'approvals': {}}

    missing_tokens = []

    for each in data:

        token_approved = each['address']
        contract_approved = '0x' + each['topics'][2][26:]
        block_number = Web3.toInt(hexstr=each['blockNumber'])
        amount = 0 if each['data'] == '0x' else Web3.toInt(hexstr=each['data'])

        if each['address'] not in format_approvals['approvals']:
            token_data = await mongodb['full_tokens'].find_one({'tokenID': token_approved, 'network': network}, {'_id': False})

            if token_data is None:
                token_data = {}
                missing_tokens.append(token_approved)
            else:
                token_data = token_data

            format_approvals['approvals'][token_approved] = {'tokenID': token_approved, 'tokenData': token_data, 'network': network, 'contracts': {
                contract_approved: {'tx': [{'contractApproved': contract_approved, 'amount': amount, 'blockNumber': block_number, 'tx': each['transactionHash']}]}}}

        else:
            if contract_approved not in format_approvals['approvals'][token_approved]['contracts']:
                format_approvals['approvals'][token_approved]['contracts'][contract_approved] = {'tx': [
                    {'contractApproved': contract_approved, 'amount': amount, 'block_number': block_number, 'tx': each['transactionHash']}]}
            else:
                format_approvals['approvals'][token_approved]['contracts'][contract_approved]['tx'].append(
                    [{'contractApproved': contract_approved, 'amount': amount, 'block_number': block_number, 'tx': each['transactionHash']}])

    unknown_tokens = await lookup_token_info(missing_tokens, network)
    balance_calls = []

    for each in format_approvals['approvals']:
        if len(format_approvals['approvals'][each]['tokenData']) == 0:
            format_approvals['approvals'][each]['tokenData'].update(
                unknown_tokens[each])
            decimals = unknown_tokens[each]['tkn0d']
            balance_calls.append(Call(each, ['balanceOf(address)(uint256)', address], [
                                 [f'{each}', parsers.from_custom, decimals]]))
        else:
            if 'tkn1d' in format_approvals['approvals'][each]['tokenData']:
                balance_calls.append(Call(each, ['balanceOf(address)(uint256)', address], [
                                     [f'{each}', parsers.from_custom, 18]]))
            else:
                decimals = format_approvals['approvals'][each]['tokenData']['tkn0d']
                balance_calls.append(Call(each, ['balanceOf(address)(uint256)', address], [
                                     [f'{each}', parsers.from_custom, decimals]]))

    token_balances = await Multicall(balance_calls, WEB3_NETWORKS[network])()

    for each in format_approvals['approvals']:
        format_approvals['approvals'][each]['balance'] = token_balances[each]

    return format_approvals
