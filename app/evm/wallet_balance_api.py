import json
import os
import time
from web3 import Web3
from ..redis.cache import cache_function
from .multicall import Call, Multicall, parsers
from .oracles import coingecko_by_address_network, list_router_prices, get_bancor_prices
from .router_override import stable_override, router_override
from .networks import WEB3_NETWORKS, SCAN_APIS
from .utils import make_get_json
from .native_tokens import NetworkRoutes
from .external_contracts import get_venus_vaults
from ..db.schemas import UserRecord
from ..db.crud import create_user_history
from datetime import datetime, timezone

SCAN_SUPPORTED = [x for x in SCAN_APIS]


def convert_timestamp(epoch):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(epoch))


async def get_native_balance(wallet, network):
    w3 = WEB3_NETWORKS[network]['connection']
    wallet = Web3.toChecksumAddress(wallet)

    try:
        balance = await w3.eth.get_balance(wallet)
    except Exception as e:
        print(f'Error getting wallet balance for {wallet} on {network} : {e}')
        balance = 0

    return balance


async def get_balance_of(token_list, wallet, network, network_info):

    calls = []

    for token in token_list:
        if token.lower() not in [
            '0x52903256dd18D85c2Dc4a6C999907c9793eA61E3'.lower(),
            '0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2'.lower(),
            '0xf1df869abfbcc0af1c9dd859e1c264d4d18d9f8e'.lower(),
            '0x87230146E138d3F296a9a77e497A2A83012e9Bc5'.lower(),
            '0x9531c509a24ceec710529645fc347341ff9f15ea'.lower(),
            '0x04906695d6d12cf5459975d7c3c03356e4ccd460'.lower(),
            '0x0ab87046fbb341d058f17cbc4c1133f25a20a52f'.lower(),
            '0x27F8D03b3a2196956ED754baDc28D73be8830A6e'.lower(),
            '0x1a13F4Ca1d028320A707D99520AbFefca3998b7F'.lower(),
            '0x60D55F02A771d515e077c9C2403a1ef324885CeC'.lower(),
            '0x5c2ed810328349100A66B82b78a1791B101C9D61'.lower(),
            '0x28424507fefb6f7f8E9D3860F56504E4e5f5f390'.lower(),
            '0x8dF3aad3a84da6b69A4DA8aeC3eA40d9091B2Ac4'.lower(),
            '0x1d2a0E5EC8E5bBDCA5CB219e649B565d8e5c3360'.lower(),
            '0x912f594fd096e67e0c0a18d496a9f70e3171c330'.lower()
        ] + [x['address'].lower() for x in await get_venus_vaults('session')]:
            calls.append(Call(token, ['balanceOf(address)(uint256)', wallet], [[f'{token}_balance', None]]))

    # if len(calls) > 2100:
    #     chunks = len(calls) / 2000
    #     x = np.array_split(calls, math.ceil(chunks))
    #     all_calls=await asyncio.gather(*[Multicall(call,WEB3_NETWORKS[network], _strict=False)() for call in x])
    #     multi_return = reduce(lambda a, b: dict(a, **b), all_calls)
    # else:
    multi_return = await Multicall(calls, WEB3_NETWORKS[network], _strict=False)()

    native_balance = await get_native_balance(wallet, network)
    if network == "aurora":
        user_holdings = {f'native+{network}' : {'token' : '0xC9BdeEd33CD01541e1eeD10f90519d2C06Fe3feB'.lower(), 'decimal' : 18, 'token_symbol' : network_info.snative, 'token_balance' : parsers.from_custom(native_balance, 18), 'network' : network}}
    else:
        user_holdings = {f'native+{network}' : {'token' : network_info.native.lower(), 'decimal' : network_info.dnative, 'token_symbol' : network_info.snative, 'token_balance' : parsers.from_custom(native_balance, 18), 'network' : network}}

    user_tokens = [network_info.native]

    token_symbol = []
    for x in multi_return:
        if 'balance' in x:
            if multi_return[x] > 0 and x.split('_')[0] not in ['0x48c80f1f4d53d5951e5d5438b54cba84f29f32a5'.lower(), '0x86fa049857e0209aa7d9e616f7eb3b3b78ecfdb0'.lower(), '0x31A240648e2baf4f9F17225987f6f53fceB1699A'.lower(), '0xB31C219959E06f9aFBeB36b388a4BaD13E802725'.lower()]:
                token = x.split('_')[0]
                token_symbol.append(Call(token, ['symbol()(string)'], [[f'{token}_symbol', None]]))
                token_symbol.append(Call(token, ['decimals()(uint256)'], [[f'{token}_decimal', None]]))

    multi_return = {**multi_return, **await Multicall(token_symbol, WEB3_NETWORKS[network], _strict=False)()}

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


async def get_token_list_from_scan(network, session, wallet):

    if network not in SCAN_APIS.keys():
        return []

    network_data = SCAN_APIS[network]
    apikey = network_data['api_key']
    latest_block = await WEB3_NETWORKS[network]['connection'].eth.block_number
    scan_url = network_data['address']

    url = f'https://api.{scan_url}/api?module=account&action=tokentx&address={wallet}&to=startblock=0&endblock={latest_block}&sort=asc&apikey={apikey}'
    r = await make_get_json(session, url)

    data = r['result']
    if not data or type(data) != list:
        print(f'Error: data returned from {url} {data}: request {json.dumps(r)}')
        return []

    filtered_to = [x['contractAddress'] for x in data if x['to'].lower() == wallet.lower() and int(x['value']) > 0]

    if filtered_to is not None:
        unique_list = [i for n, i in enumerate(filtered_to) if i not in filtered_to[n + 1:]]
        return unique_list
    else:
        return []


async def get_token_list_from_mongo(network, mongo):
    x = await mongo['tokenListByNetwork'].find_one({'name' : network}, {'_id': False})
    return x['tokens'] if x is not None else []


@cache_function(keyparams=2)
async def get_wallet_balance(wallet, network, mongodb, session, pdb):
    network_data = NetworkRoutes(network)

    ##Have to revist this, too many dirty tokens in mongo on BSC
    #unique_list = await get_token_list_from_mongo(network, mongodb)

    if network in SCAN_SUPPORTED:
        unique_list = await get_token_list_from_scan(network, session, wallet)
    else:
        unique_list = await get_token_list_from_mongo(network, mongodb)
    
    try:
        wallet_data = await get_balance_of([x for x in unique_list if x not in ["1"]], wallet, network, network_data)
        prices = await coingecko_by_address_network(wallet_data[1], network_data.coingecko, session)
        if network == 'rsk':
            router_prices = await get_bancor_prices([wallet_data[0][x] for x in wallet_data[0]], network)
        else:
            router_prices = await list_router_prices([wallet_data[0][x] for x in wallet_data[0]], network, check_liq=True)
    except Exception as e:
        print(f"Error getting wallet balance for {wallet} on {network} : {e}")
        wallet_data = [[]]

    payload = []
    stored_tokens = []
    total_balance = 0

    for token in wallet_data[0]:
        address = wallet_data[0][token]['token']

        if address not in ['0x9e2d266d6c90f6c0d80a88159b15958f7135b8af', '0x0000000000000000000000000000000000001010', '0x0b91b07beb67333225a5ba0259d55aee10e3a578', '0xae7ab96520de3a18e5e111b5eaab095312d7fe84']:
            symbol = wallet_data[0][token]['token_symbol']

            price = router_prices[address] if address in router_prices else 0

            if price == 0:
                try:
                    price = prices[address]['usd'] if address in prices else 0
                except:
                    price = 0

            if address in router_override or address in stable_override:
                if address not in ['0xe5417af564e4bfda1c483642db72007871397896']:
                    price = 0

            data = {
                'token_address' : address.lower(),
                'symbol' : symbol,
                'tokenBalance' : wallet_data[0][token]['token_balance'],
                'tokenPrice' : price,
                'network' : network
            }
            if address.lower() not in stored_tokens:
                payload.append(data)
                stored_tokens.append(address.lower())
                total_balance += wallet_data[0][token]['token_balance'] * price

    if total_balance > 0 and os.getenv('USER_WRITE', 'True') == 'True':
        await create_user_history(pdb, UserRecord(timestamp=datetime.fromtimestamp(int(time.time()), tz=timezone.utc), farm='wallet', farm_network=network, wallet=wallet.lower(), dollarvalue=total_balance, farmnetwork=network))

        # mongodb['user_data'].update_one({'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farm_network' : network}, { "$set": {'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farmNetwork' : network, 'dollarValue' : total_balance} }, upsert=True)

    return payload
