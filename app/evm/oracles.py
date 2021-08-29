import requests
import json
from .multicall import Call, Multicall, parsers
from .routers import FTMRouter, KCCRouter, OKERouter, ONERouter, AVAXRouter
from .networks import WEB3_NETWORKS
from . import native_tokens
from .utils import make_get_json
import asyncio
from aiohttp import ClientSession, ClientTimeout

INCH_QUOTE_TOKENS = {
    'bsc' : {'token' : '0xe9e7cea3dedca5984780bafc599bd69add087d56', 'decimals' : 18},
    'matic' : {'token' : '0x2791bca1f2de4661ed88a30c99a7a9449aa84174', 'decimals' : 6},
    'eth' : {'token' : '0x2791bca1f2de4661ed88a30c99a7a9449aa84174', 'decimals' : 6}}

def coingecko_by_address_network(address,network):
    url = f'https://api.coingecko.com/api/v3/simple/token_price/{network}?contract_addresses={address}&vs_currencies=usd'
    r = requests.get(url)

    return json.loads(r.text)

def fantom_router_prices(tokens_in, router):
    calls= []
    out_token = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
    fantom_price = Call(FTMRouter.SPOOKY, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E']], [[f'fantom_price', parse_router]], WEB3_NETWORKS['ftm'])()['fantom_price']
    
    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(FTMRouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parse_router, fantom_price]]))
    
    multi=Multicall(calls,WEB3_NETWORKS['ftm'], _strict=False)()

    prices = {}

    for each in multi:
        token = each.split('_')[1]
        looped_value = multi[each]

        if token in prices:
            current_value = prices[token]
            if looped_value > current_value:
                prices[token] = looped_value
        else:
            prices[token] = looped_value

    return {**prices, **{'0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83' : fantom_price}}

def get_price_from_router(token_in, network, router, native=False, decimal=18, bypass_token=None, token_out=None):
    chain_w3 = WEB3_NETWORKS[network]
    chain = network.upper()

    if token_out is None:
        token_out = getattr(native_tokens.StableToken, chain)
    else:
        token_out = token_out

    if bypass_token is None:
        native_token = getattr(native_tokens.NativeToken, chain)
    else:
        native_token = bypass_token
    default_router = getattr(native_tokens.DefaultRouter, chain)
        
    if native is True:
        native_price = Call(default_router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [native_token, token_out]], [[f'token_in', parse_router]], chain_w3)()['token_in']
        token_price = Call(router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** decimal, [token_in, native_token]], [[f'token_in', parse_router, native_price]],chain_w3)()['token_in']
        return token_price
    else:
        token_price = Call(router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** decimal, [token_in, token_out]], [[f'token_in', parse_router]],chain_w3)()['token_in']
        return token_price

def kcc_router_prices(tokens_in, router):
    calls= []
    out_token = '0x4446fc4eb47f2f6586f9faab68b3498f86c07521'
    #fantom_price = Call(FTMRouter.SPOOKY, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E']], [[f'fantom_price', parse_router]], WEB3_NETWORKS['ftm'])()['fantom_price']
    kcc_price = coingecko_by_address_network('0x4446fc4eb47f2f6586f9faab68b3498f86c07521', 'kucoin-community-chain')['0x4446fc4eb47f2f6586f9faab68b3498f86c07521']['usd']

    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(KCCRouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parse_router, kcc_price]]))
    
    multi=Multicall(calls,WEB3_NETWORKS['kcc'], _strict=False)()

    prices = {}

    for each in multi:
        token = each.split('_')[1]
        looped_value = multi[each]

        if token in prices:
            current_value = prices[token]
            if looped_value > current_value:
                prices[token] = looped_value
        else:
            prices[token] = looped_value

    return {**prices, **{'0x4446fc4eb47f2f6586f9faab68b3498f86c07521' : kcc_price}}

def oke_router_prices(tokens_in, router):
    calls= []
    out_token = '0x8f8526dbfd6e38e3d8307702ca8469bae6c56c15'
    oke_price = Call(OKERouter.PANDA, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0x382bb369d343125bfb2117af9c149795c6c65c50']], [[f'oke_price', parse_router]], WEB3_NETWORKS['oke'])()['oke_price']
    #kcc_price = coingecko_by_address_network('0x4446fc4eb47f2f6586f9faab68b3498f86c07521', 'kucoin-community-chain')['0x4446fc4eb47f2f6586f9faab68b3498f86c07521']['usd']

    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(OKERouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parse_router, oke_price]]))
    
    multi=Multicall(calls,WEB3_NETWORKS['oke'], _strict=False)()

    prices = {}

    for each in multi:
        token = each.split('_')[1]
        looped_value = multi[each]

        if token in prices:
            current_value = prices[token]
            if looped_value > current_value:
                prices[token] = looped_value
        else:
            prices[token] = looped_value

    return {**prices, **{'0x8f8526dbfd6e38e3d8307702ca8469bae6c56c15' : oke_price}}

def harmony_router_prices(tokens_in, router):
    calls= []
    out_token = '0xcf664087a5bb0237a0bad6742852ec6c8d69a27a'
    one_price = Call(ONERouter.SUSHI, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0x224e64ec1bdce3870a6a6c777edd450454068fec']], [[f'one_price', parse_router]], WEB3_NETWORKS['harmony'])()['one_price']

    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(ONERouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parse_router, one_price]]))
    
    multi=Multicall(calls,WEB3_NETWORKS['harmony'], _strict=False)()

    prices = {}

    for each in multi:
        token = each.split('_')[1]
        looped_value = multi[each]

        if token in prices:
            current_value = prices[token]
            if looped_value > current_value:
                prices[token] = looped_value
        else:
            prices[token] = looped_value

    return {**prices, **{'0xcf664087a5bb0237a0bad6742852ec6c8d69a27a' : one_price}}

def avax_router_prices(tokens_in, router):
    calls= []
    out_token = '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7'
    native_price = Call(AVAXRouter.PNG, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0xd586E7F844cEa2F87f50152665BCbc2C279D8d70']], [[f'native_price', parse_router]], WEB3_NETWORKS['avax'])()['native_price']

    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(AVAXRouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parse_router, native_price]]))
    
    multi=Multicall(calls,WEB3_NETWORKS['avax'], _strict=False)()

    prices = {}

    for each in multi:
        token = each.split('_')[1]
        looped_value = multi[each]

        if token in prices:
            current_value = prices[token]
            if looped_value > current_value:
                prices[token] = looped_value
        else:
            prices[token] = looped_value

    return {**prices, **{'0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7' : native_price}}

async def get_one_inch_quote(tokens, session):
    tasks = []
    network_ids={'bsc' : '56', 'matic' : '137', 'kcc' : '321', 'eth' : '1'}

    for token in tokens:

        SAFE_QUOTE = 1000
        SAFE_QUOTE_USD = SAFE_QUOTE * 10 ** INCH_QUOTE_TOKENS[token['network']]['decimals']
        network = network_ids[token['network']]
        quote_token = INCH_QUOTE_TOKENS[token['network']]['token']

        url = f'https://api.1inch.exchange/v3.0/{network}/quote'

        payload = {
            'fromTokenAddress' : quote_token,
            'toTokenAddress' : token['token'],
            'amount' : SAFE_QUOTE_USD
        }

        task = asyncio.ensure_future(make_get_json(session, url, {'params' : payload}))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    list_of_prices = { x['token'] : 0.1 for x in tokens}

    for response in responses:
        if 'toTokenAmount' in response:
            to_token_amount = int(response['toTokenAmount'])
            to_token_address = response['toToken']['address']
            to_token_decimal = int(response['toToken']['decimals'])
            usd_value = 1 / (( to_token_amount / 10**to_token_decimal ) / SAFE_QUOTE)
            list_of_prices[to_token_address] = usd_value

    return list_of_prices