from operator import mul
from .multicall import Call, Multicall, parsers
import json
import time
from web3 import Web3
from .oracles import coingecko_by_address_network, list_router_prices
from .networks import WEB3_NETWORKS, SCAN_APIS
from .utils import make_get_json
from .native_tokens import NetworkRoutes

SCAN_SUPPORTED = [x for x in SCAN_APIS]

def convert_timestamp(epoch):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(epoch))

async def get_native_balance(wallet,network):
    w3 = WEB3_NETWORKS[network]['connection']
    wallet = Web3.toChecksumAddress(wallet)
    return await w3.eth.get_balance(wallet)

async def get_balance_of(token_list, wallet, network, network_info):

    calls = []

    for token in token_list:
        if token != '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2':
            calls.append(Call(token, ['balanceOf(address)(uint256)', wallet], [[f'{token}_balance', None]]))
            calls.append(Call(token, ['symbol()(string)'], [[f'{token}_symbol', None]]))
            calls.append(Call(token, ['decimals()(uint8)'], [[f'{token}_decimal', None]]))
   
    multi_return = await Multicall(calls, WEB3_NETWORKS[network], _strict=False)()

    native_balance = await get_native_balance(wallet, network)

    user_holdings = {f'native+{network}' : {'token' : network_info.native.lower(), 'decimal' : network_info.dnative, 'token_symbol' : network_info.snative, 'token_balance' : parsers.from_custom(native_balance, 18), 'network' : network}}
    user_tokens = [network_info.native]

    for x in multi_return:
        if 'balance' in x:
            if multi_return[x] > 0 and x.split('_')[0].lower() not in user_tokens:
                key = x.split('_')[0]
                token_decimal = multi_return[f'{key}_decimal'] if f'{key}_decimal' in multi_return else 18
                token_symbol = multi_return[f'{key}_symbol'] if f'{key}_symbol' in multi_return else 'UNKNOWN'
                token_balance = parsers.from_custom(multi_return[x], token_decimal)

                user_holdings[key] = {'token' : key, 'decimal' : token_decimal, 'token_symbol' : token_symbol, 'token_balance' : token_balance, 'network' : network}
                user_tokens.append(key.lower())

    return user_holdings, ','.join(user_tokens)

async def get_token_list_from_scan(network,session,wallet):

    network_data = SCAN_APIS[network]
    apikey = network_data['api_key']
    latest_block = await WEB3_NETWORKS[network]['connection'].eth.block_number
    scan_url = network_data['address']

    url = f'https://api.{scan_url}/api?module=account&action=tokentx&address={wallet}&to=startblock=0&endblock={latest_block}&sort=asc&apikey={apikey}'
    r = await make_get_json(session, url)

    data = r['result']
    filtered_to =[x['contractAddress'] for x in data if x['to'].lower() == wallet.lower() and int(x['value']) > 0]

    unique_list =[i for n, i in enumerate(filtered_to) if i not in filtered_to[n + 1:]]

    return unique_list

async def get_token_list_from_mongo(network,mongo):
    x = await mongo.xtracker['tokenListByNetwork'].find_one({'name' : network}, {'_id': False})
    return x['tokens'] if x is not None else []

async def get_wallet_balance(wallet, network, mongodb, session):
    
    network_data = NetworkRoutes(network)

    if network in SCAN_SUPPORTED:
        unique_list = await get_token_list_from_scan(network, session, wallet)
    else:
        unique_list = await get_token_list_from_mongo(network, mongodb)
    
    wallet_data = await get_balance_of(unique_list, wallet, network, network_data)
    prices = await coingecko_by_address_network(wallet_data[1], network_data.coingecko, session)
    router_prices = await list_router_prices([wallet_data[0][x] for x in wallet_data[0]], network)
    payload = []

    for token in wallet_data[0]:
        address = wallet_data[0][token]['token']

        if address not in ['0x9e2d266d6c90f6c0d80a88159b15958f7135b8af']:
            symbol = wallet_data[0][token]['token_symbol']

            price = router_prices[address] if address in router_prices else 0

            if price == 0:
                try:
                    price = prices[address]['usd'] if address in prices else 0
                except:
                    price = 0

            data = {
                'token_address' : address.lower(),
                'symbol' : symbol,
                'tokenBalance' : wallet_data[0][token]['token_balance'],
                'tokenPrice' : price,
                'network' : network
            }

            payload.append(data)


    return payload