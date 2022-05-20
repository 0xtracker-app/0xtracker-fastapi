import re
import requests
import json
from functools import reduce
import math
import numpy as np
from .multicall import Call, Multicall, parsers
from .routers import BSCRouter, FTMRouter, KCCRouter, OKERouter, ONERouter, AVAXRouter, ArbRouter
from .networks import WEB3_NETWORKS
from . import native_tokens
from .utils import make_get, make_get_json
import asyncio
from aiohttp import ClientSession, ClientTimeout
from .native_tokens import LiqCheck, NetworkRoutes
from .router_override import router_override, stable_override
from .uniswapv3 import uniSqrtPrice
from .template_helpers import round_to_hour
import time

APPROVED_TOKENS = ['0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3', '0xc168e40227e4ebd8c1cae80f7a55a4f0e6d66c97']
INCH_QUOTE_TOKENS = {
    'bsc' : {'token' : '0xe9e7cea3dedca5984780bafc599bd69add087d56', 'decimals' : 18},
    'matic' : {'token' : '0x2791bca1f2de4661ed88a30c99a7a9449aa84174', 'decimals' : 6},
    'eth' : {'token' : '0x2791bca1f2de4661ed88a30c99a7a9449aa84174', 'decimals' : 6}}

async def coingecko_by_address_network(address,network,session):
    url = f'https://api.coingecko.com/api/v3/simple/token_price/{network}?contract_addresses={address}&vs_currencies=usd'

    return await make_get_json(session, url)

async def coingecko_by_address_network_single(address,network,session):
    url = f'https://api.coingecko.com/api/v3/simple/token_price/{network}?contract_addresses={address}&vs_currencies=usd'
    response = await make_get_json(session, url)

    return {address.lower() : response[address]['usd']}

async def get_price_from_firebird(token_in, token_out, amount, out_d, session):
    url = f'https://router.firebird.finance/polygon/route?tokenIn={token_in}&tokenOut={token_out}&amountIn={amount}&saveGas=0'
    r = await make_get_json(session, url)
    return {token_in.lower() : parsers.from_custom(int(r['outputAmount']), out_d)}

async def get_tranchess_price(helper,tranch,address,session):
    response = await Call(helper, ['estimateNavs(uint256)((uint256,uint256,uint256))', round_to_hour()], [[f'estimateNavs',parsers.parse_tranchess]], _w3=WEB3_NETWORKS['bsc'])()

    return {address.lower() : response['estimateNavs'][tranch] / 1e18}

async def fantom_router_prices(tokens_in, router):
    calls= []
    out_token = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
    fantom_price = await Call(FTMRouter.SPOOKY, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E']], [[f'fantom_price', parsers.parse_router]], WEB3_NETWORKS['ftm'])()
    
    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(FTMRouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parsers.parse_router, fantom_price['fantom_price']]]))
    
    multi=await Multicall(calls,WEB3_NETWORKS['ftm'], _strict=False)()

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

    return {**prices, **{'0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83' : fantom_price['fantom_price']}}

async def get_price_from_router(token_in, network, router, native=False, decimal=18, bypass_token=None, token_out=None, return_token=None, bypass_router=None):
    chain_w3 = WEB3_NETWORKS[network]
    chain = network.upper()

    if token_out is None:
        token_out = getattr(native_tokens.StableToken, chain)
    else:
        token_out = token_out

    if return_token is None:
        return_token = token_in
    else:
        return_token = return_token

    if bypass_token is None:
        native_token = getattr(native_tokens.NativeToken, chain)
    else:
        native_token = bypass_token

    if bypass_router:
        default_router = bypass_router
    else:
        default_router = getattr(native_tokens.DefaultRouter, chain)

    if native is True:
        stable_decimal = getattr(native_tokens.StableDecimal, chain)
        native_price = await Call(default_router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [native_token, token_out]], [[f'token_in', parsers.parse_router_native, stable_decimal]], chain_w3)()
        token_price = await Call(router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** decimal, [token_in, native_token]], [[f'token_in', parsers.parse_router, native_price['token_in']]],chain_w3)()
        return {return_token.lower() : token_price['token_in']}
    else:
        token_price = await Call(router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** decimal, [token_in, token_out]], [[f'token_in', parsers.parse_router]],chain_w3)()
        return {return_token.lower() : token_price['token_in']}

async def kcc_router_prices(tokens_in, router):
    calls= []
    out_token = '0x4446fc4eb47f2f6586f9faab68b3498f86c07521'
    kcc_price = await Call(KCCRouter.KUSWAP, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0x0039f574ee5cc39bdd162e9a88e3eb1f111baf48']], [[f'price', parsers.parse_router]], WEB3_NETWORKS['kcc'])()

    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(KCCRouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parsers.parse_router, kcc_price['price']]]))
    
    multi=await Multicall(calls,WEB3_NETWORKS['kcc'], _strict=False)()

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

    return {**prices, **{'0x4446fc4eb47f2f6586f9faab68b3498f86c07521' : kcc_price['price']}}

async def oke_router_prices(tokens_in, router):
    calls= []
    out_token = '0x8f8526dbfd6e38e3d8307702ca8469bae6c56c15'
    oke_price = await Call(OKERouter.PANDA, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0x382bb369d343125bfb2117af9c149795c6c65c50']], [[f'oke_price', parsers.parse_router]], WEB3_NETWORKS['oke'])()

    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(OKERouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parsers.parse_router, oke_price['oke_price']]]))
    
    multi=await Multicall(calls,WEB3_NETWORKS['oke'], _strict=False)()

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

    return {**prices, **{'0x8f8526dbfd6e38e3d8307702ca8469bae6c56c15' : oke_price['oke_price']}}

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

async def list_router_prices(tokens_in, network, check_liq=False):

    network_route = NetworkRoutes(network)
    calls= []
    liq_calls = []
    out_token = network_route.native
    network_conn = network_route.network_conn

    if network == 'rsk':
        return await get_bancor_prices(tokens_in, network)

    if network == 'songbird':
        return await get_songbird_prices(tokens_in, network)

    if network in ['dfk','evmos']:
        check_liq = False

    if network_route.default_router == '0xAA30eF758139ae4a7f798112902Bf6d65612045f':
        native_price = await Call(network_route.default_router, ['getAmountsOut(uint256,address[],uint256)(uint[])', 1 * 10 ** network_route.dnative, [out_token, network_route.stable], 0], [[f'native_price', parsers.parse_router_native, network_route.dstable]], network_conn)()
    else:
        native_price = await Call(network_route.default_router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** network_route.dnative, [out_token, network_route.stable]], [[f'native_price', parsers.parse_router_native, network_route.dstable]], network_conn)()

    for token in tokens_in:
        for contract in network_route.lrouters:
             
            token_address = token['token']
            token_in_address = router_override[token_address]['token'] if token_address in router_override else token_address
            token_dec = router_override[token_address]['decimal'] if token_address in router_override else token['decimal']
            if contract == 'SOLAR':
                if token_address.lower() in stable_override:
                    override_out = stable_override[token_address]['token']
                    override_decimal = stable_override[token_address]['decimal']
                    liq_calls.append(Call(network_route.liqcheck, ['check_liquidity(address,address,address)((uint256,uint256))', getattr(network_route.router, contract), token_in_address, override_out], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : override_decimal, 'price' : 1}]]))
                    calls.append(Call(getattr(network_route.router, contract), ['getAmountsOut(uint256,address[],uint256)(uint[])', 1 * 10 ** token_dec, [token_in_address, override_out], 25], [[f'{contract}_{token_address}', parsers.parse_router_native, override_decimal]]))
                else:
                    liq_calls.append(Call(network_route.liqcheck, ['check_liquidity(address,address,address)((uint256,uint256))', getattr(network_route.router, contract), token_in_address, out_token], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : network_route.dnative, 'price' : native_price['native_price']}]]))
                    calls.append(Call(getattr(network_route.router, contract), ['getAmountsOut(uint256,address[],uint256)(uint[])', 1 * 10 ** token_dec, [token_in_address, out_token], 25], [[f'{contract}_{token_address}', parsers.parse_router, native_price['native_price']]]))
            elif contract == 'VALLEY':
                if token_address.lower() in stable_override:
                    override_out = stable_override[token_address]['token']
                    override_decimal = stable_override[token_address]['decimal']
                    liq_calls.append(Call(network_route.liqcheck, ['check_liquidity(address,address,address)((uint256,uint256))', getattr(network_route.router, contract), token_in_address, override_out], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : override_decimal, 'price' : 1}]]))
                    calls.append(Call(getattr(network_route.router, contract), ['getAmountsOut(address,uint256,address[])(uint256[])', '0xa25464822b505968eec9a45c43765228c701d35f', 1 * 10 ** token_dec, [token_in_address, override_out]], [[f'{contract}_{token_address}', parsers.parse_router_native, override_decimal]]))
                else:
                    liq_calls.append(Call(network_route.liqcheck, ['check_liquidity(address,address,address)((uint256,uint256))', getattr(network_route.router, contract), token_in_address, out_token], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : network_route.dnative, 'price' : native_price['native_price']}]]))
                    calls.append(Call(getattr(network_route.router, contract), ['getAmountsOut(address,uint256,address[])(uint256[])', '0xa25464822b505968eec9a45c43765228c701d35f', 1 * 10 ** token_dec, [token_in_address, out_token]], [[f'{contract}_{token_address}', parsers.parse_router, native_price['native_price']]]))    
            else:
                if token_address.lower() in stable_override and network != 'harmony' and token_address.lower() != '0x6ab6d61428fde76768d7b45d8bfeec19c6ef91a8':
                    override_out = stable_override[token_address]['token']
                    override_decimal = stable_override[token_address]['decimal']
                    liq_calls.append(Call(network_route.liqcheck, ['check_liquidity(address,address,address)((uint256,uint256))', getattr(network_route.router, contract), token_in_address, override_out], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : override_decimal, 'price' : 1}]]))
                    calls.append(Call(getattr(network_route.router, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_in_address, override_out]], [[f'{contract}_{token_address}', parsers.parse_router_native, override_decimal]]))
                else:
                    out_token = '0x75cb093E4D61d2A2e65D8e0BBb01DE8d89b53481' if contract in ['STANDARD'] and network in ['metis'] else out_token
                    liq_calls.append(Call(network_route.liqcheck, ['check_liquidity(address,address,address)((uint256,uint256))', getattr(network_route.router, contract), token_in_address, out_token], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : network_route.dnative, 'price' : native_price['native_price']}]]))
                    calls.append(Call(getattr(network_route.router, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_in_address, out_token]], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : network_route.dnative, 'price' : native_price['native_price']}]]))
                    out_token = network_route.native

    # if len(calls) > 1000:
    #     chunks = len(calls) / 1000
    #     x = np.array_split(calls, math.ceil(chunks))
    #     all_calls=await asyncio.gather(*[Multicall(call,network_conn, _strict=False)() for call in x])
    #     multi = reduce(lambda a, b: dict(a, **b), all_calls)
    # else:
    multi=await Multicall(calls,network_conn, _strict=False)()
                                                         
    # if check_liq:
    #     if len(liq_calls) > 2100:
    #         chunks = len(liq_calls) / 2000
    #         x = np.array_split(liq_calls, math.ceil(chunks))
    #         all_calls=await asyncio.gather(*[Multicall(call,network_conn, _strict=False)() for call in x])
    #         liq_check = reduce(lambda a, b: dict(a, **b), all_calls)
    #     else:
    if check_liq:
        liq_check = await Multicall(liq_calls, network_conn, _strict=False)()
    else:
        liq_check = {}

    prices = {}


    for each in multi:
        token = each.split('_')[1]

        if check_liq:
            if token in APPROVED_TOKENS:
                liq = network_route.minliq + 1
            else:
                liq = liq_check[each] if each in liq_check else 0
        else:
            if token.lower() == '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82'.lower() and each.split('_')[0] == 'BURGER':
                liq = 0
            elif token.lower() == '0x2d03bece6747adc00e1a131bba1469c15fd11e03'.lower() and each.split('_')[0] != 'VVS':
                liq = 0
            else:
                liq = network_route.minliq + 1
        looped_value = multi[each] if liq > network_route.minliq else 0

        if token in prices:
            current_value = prices[token]
            if looped_value > current_value:
                prices[token] = looped_value
        else:
            prices[token] = looped_value

    for token in tokens_in:
        if token['token'] not in prices:
            prices[token['token']] = 0

    prices[out_token.lower()] = native_price['native_price']

    if out_token == '0x98878B06940aE243284CA214f92Bb71a2b032B8A':
        prices['0xf50225a84382c74CbdeA10b0c176f71fc3DE0C4d'.lower()] = native_price['native_price']
    
    if out_token == '0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000':
        prices['0x75cb093e4d61d2a2e65d8e0bbb01de8d89b53481'.lower()] = native_price['native_price']

    ##Set Dead Tokens To Zero
    prices['0x0184316f58b9a44acdd3e683257259dc0cf2202a'.lower()] = 0
    prices['0x714a84632ed7edbbbfeb62dacf02db4beb4c69d9'.lower()] = 0
    prices['0xd5e3bf9045cfb1e6ded4b35d1b9c34be16d6eec3'.lower()] = 0
    prices['0x854086dc841e1bfae50cb615bf41f55bf432a90b'.lower()] = 0
    prices['0x04645027122c9f152011f128c7085449b27cb6D7'.lower()] = 0
    prices['0xef27b9cb67aa93ec3494a60f1ea9380e86175b26'.lower()] = 0
    prices['0x27b880865395da6cda9c407e5edfcc32184cf429'.lower()] = 0
    prices['0x0d05a204e27e4815f1f5afdb9d82aa221aa0bdfa'.lower()] = 0
    prices['0x27b880865395da6cda9c407e5edfcc32184cf429'.lower()] = 0
    prices['0x491b25000d386cd31307580171a510d32d7e64ee'.lower()] = 0
    prices['0x556798DD55Db12562A6950EA8339a273539B0495'.lower()] = 0
    prices['0x5ccce837b41dbd2ad74882889749517935741390'.lower()] = 0
    prices['0x893c25c46bfaa9b66cd557837d32af3fe264a07b'.lower()] = 0
    prices['0xd7f1d4f5a1b44d827a7c3cc5dd46a80fade55558'.lower()] = 0
    prices['0xa85f8a198d59f0fda82333be9aeeb50f24dd59ff'.lower()] = 0
    prices['0x2744861accb5bd435017c1cfee789b6ebab42082'.lower()] = 0
    prices['0x265befe2b1a0f4f646dea96ba09c1656b74bda91'.lower()] = 0
    prices['0x2ba6204c23fbd5698ed90abc911de263e5f41266'.lower()] = 0
    prices['0xd35f9ab96d04adb02fd549ef6a576ce4e2c1d935'.lower()] = 0
    prices['0x8bd0e87273364ebbe3482efc166f7e0d34d82c25'.lower()] = 0
    prices['0x0b91b07beb67333225a5ba0259d55aee10e3a578'.lower()] = 0
    prices['0x3bab61ad5d103bb5b203c9092eb3a5e11677a5d0'.lower()] = 0

    return prices

async def avax_router_prices(tokens_in, router):
    calls= []
    out_token = '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7'
    native_price = await Call(AVAXRouter.PNG, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [out_token, '0xd586E7F844cEa2F87f50152665BCbc2C279D8d70']], [[f'native_price', parsers.parse_router]], WEB3_NETWORKS['avax'])()

    for token in tokens_in:
        for contract in router:
            token_dec = token['decimal']
            token_address = token['token']
            calls.append(Call(getattr(AVAXRouter, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_address, out_token]], [[f'{contract}_{token_address}', parsers.parse_router, native_price['native_price']]]))
    
    multi=await Multicall(calls,WEB3_NETWORKS['avax'], _strict=False)()

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
    
    for token in tokens_in:
        if token['token'] not in prices:
            prices[token['token']] = .01

    return {**prices, **{'0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7' : native_price['native_price']}, ** {'0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7' : native_price['native_price']}}

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

async def get_price_from_synpool(token_in,swap_address, token_out_index, decimal, network):

        one_token = 1 * 10 ** decimal
        
        price = await Call(swap_address, ['calculateRemoveLiquidityOneToken(uint256,uint8)(uint256)', one_token, token_out_index], [['price', parsers.from_wei]], _w3=WEB3_NETWORKS[network])()

        return {token_in.lower() : price['price']}

async def get_price_from_platypus(token_in,swap_address, token_out_index, decimal, network):

        one_token = 1 * 10 ** decimal
        
        price = await Call(swap_address, ['quotePotentialWithdraw(address,uint256)(uint256)', token_out_index, one_token], None, _w3=WEB3_NETWORKS[network])()

        return {token_in.lower() : parsers.from_custom(price, decimal)}


async def get_gnana_price():

        banana_price = await Call('0xcF0feBd3f17CEf5b47b0cD257aCf6025c5BFf3b7', ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, ['0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95', '0xe9e7cea3dedca5984780bafc599bd69add087d56']], None, WEB3_NETWORKS['bsc'])()

        return {'0xddb3bd8645775f59496c821e4f55a7ea6a6dc299'.lower() : parsers.from_custom(banana_price[1], 18) * 1.389}

async def get_xjoe_price():
        calls = []

        joe = '0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd'
        xjoe = '0x57319d41F71E81F3c65F2a47CA4e001EbAFd4F33'
        
        calls.append(Call(joe, [f'balanceOf(address)(uint256)', xjoe], [[f'ext_xjoe', parsers.from_wei]]))
        calls.append(Call(xjoe, [f'totalSupply()(uint256)'], [[f'ext_xjoets', parsers.from_wei]]))
        calls.append(Call('0x60aE616a2155Ee3d9A68541Ba4544862310933d4', ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, ['0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd', '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7']], [[f'joe_price', parsers.parse_router]]))
        calls.append(Call('0x60aE616a2155Ee3d9A68541Ba4544862310933d4', ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, ['0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7', '0xd586E7F844cEa2F87f50152665BCbc2C279D8d70']], [[f'avax_price', parsers.parse_router]]))

        multi_call = await Multicall(calls, WEB3_NETWORKS['avax'])()

        joe_ratio = multi_call[f'ext_xjoe'] / multi_call[f'ext_xjoets']
        joe_price_usd = multi_call['avax_price'] * multi_call['joe_price']

        return {'0x57319d41f71e81f3c65f2a47ca4e001ebafd4f33'.lower() : joe_ratio * joe_price_usd}

async def get_xtoken_price(native, xnative, decimal, network, router_address):
        calls = []

        joe = native
        xjoe = xnative
        network_route = NetworkRoutes(network)

        calls.append(Call(joe, [f'balanceOf(address)(uint256)', xjoe], [[f'ext_xjoe', parsers.from_custom, decimal]]))
        calls.append(Call(xjoe, [f'totalSupply()(uint256)'], [[f'ext_xjoets', parsers.from_custom, decimal]]))
        calls.append(Call(router_address, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** decimal, [joe, network_route.native]], [[f'joe_price', parsers.parse_router_custom, network_route.dnative]]))
        calls.append(Call(network_route.default_router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** network_route.dnative, [network_route.native, network_route.stable]], [[f'native_price', parsers.parse_router_native, network_route.dstable]]))

        multi_call = await Multicall(calls, WEB3_NETWORKS[network])()

        joe_ratio = multi_call[f'ext_xjoe'] / multi_call[f'ext_xjoets']
        joe_price_usd = multi_call['native_price'] * multi_call['joe_price']

        return {xjoe.lower() : joe_ratio * joe_price_usd}

async def get_xboo_price():
        calls = []

        boo = '0x841fad6eae12c286d1fd18d1d525dffa75c7effe'
        xboo = '0xa48d959AE2E88f1dAA7D5F611E01908106dE7598'
        
        calls.append(Call(boo, [f'balanceOf(address)(uint256)', xboo], [[f'ext_xboo', parsers.from_wei]]))
        calls.append(Call(xboo, [f'totalSupply()(uint256)'], [[f'ext_xboots', parsers.from_wei]]))
        calls.append(Call('0xF491e7B69E4244ad4002BC14e878a34207E38c29', ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, ['0x841fad6eae12c286d1fd18d1d525dffa75c7effe', '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83']], [[f'boo_price', parsers.parse_router]]))
        calls.append(Call('0xF491e7B69E4244ad4002BC14e878a34207E38c29', ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, ['0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83', '0x04068da6c83afcfa0e13ba15a6696662335d5b75']], [[f'ftm_price', parsers.parse_router_native, 6]]))
        multi_call = await Multicall(calls, WEB3_NETWORKS['ftm'])()

        boo_ratio = multi_call[f'ext_xboo'] / multi_call[f'ext_xboots']
        boo_price_usd = multi_call['ftm_price'] * multi_call['boo_price']

        return {xboo.lower() : boo_ratio * boo_price_usd}

async def get_blackswan_lp():
    x = [] 
    x.append(Call('0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46', [f'getReserves()((uint112,uint112))'], [[f'reserves', None]]))
    x.append(Call('0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46','totalSupply()(uint256)', [['totalSupply', parsers.from_wei]]))

    multi = await Multicall(x,WEB3_NETWORKS['matic'])()
    userPct = 1 / multi['totalSupply']
    lpval = (userPct * multi['reserves'][0] / (10**6))

    return {'0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'.lower() : lpval}

async def return_stable(token_in):
    return {token_in.lower() : 1}

async def get_goldbar_price():

    nugget = await get_price_from_router(token_in='0xE0B58022487131eC9913C1F3AcFD8F74FC6A6C7E',network='bsc',router=BSCRouter.APESWAP, native=True)
    return {'0x24f6ECAF0B9E99D42413F518812d2c4f3EeFEB12'.lower() : nugget['0xE0B58022487131eC9913C1F3AcFD8F74FC6A6C7E'.lower()] * 213.33}

async def get_glp_price():

    x = [] 
    x.append(Call('0x321F653eED006AD1C29D174e17d96351BDe22649', [f'getAumInUsdg(bool)(uint256)', True], [[f'getAum', parsers.from_wei]]))
    x.append(Call('0x4277f8F2c384827B5273592FF7CeBd9f2C1ac258','totalSupply()(uint256)', [['totalSupply', parsers.from_wei]]))

    multi = await Multicall(x,WEB3_NETWORKS['arb'])()
    glp_price = multi['getAum'] / multi['totalSupply']

    return {'0x4277f8F2c384827B5273592FF7CeBd9f2C1ac258'.lower() : glp_price}

async def get_glp_price_avax():

    x = [] 
    x.append(Call('0xe1ae4d4b06A5Fe1fc288f6B4CD72f9F8323B107F', [f'getAumInUsdg(bool)(uint256)', True], [[f'getAum', parsers.from_wei]]))
    x.append(Call('0x01234181085565ed162a948b6a5e88758CD7c7b8','totalSupply()(uint256)', [['totalSupply', parsers.from_wei]]))

    multi = await Multicall(x,WEB3_NETWORKS['avax'])()
    glp_price = multi['getAum'] / multi['totalSupply']

    return {'0x01234181085565ed162a948b6a5e88758CD7c7b8'.lower() : glp_price}

async def get_gmx_price(return_token):

    ETH = await get_price_from_router(token_in='0x82af49447d8a07e3bd95bd0d56f35241523fbab1',network='arb',router=ArbRouter.SUSHI)
    ether_price = (ETH['0x82af49447d8a07e3bd95bd0d56f35241523fbab1'] * 1e18) / 1e6

    x = await Call('0x80A9ae39310abf666A87C743d6ebBD0E8C42158E', 'slot0()((uint160,int24,uint16,uint16,uint16,uint8,bool))', [[f'slot0',parsers.parse_slot_0]], _w3=WEB3_NETWORKS['arb'])()

    return {return_token.lower() : uniSqrtPrice([18,18], x['slot0']['sqrtPriceX96']) * ether_price}

async def get_ygg_price():

    ETH = await get_price_from_router(token_in='0x6983d1e6def3690c4d616b13597a09e6193ea013',network='harmony', native=True, router=ONERouter.SUSHI)
    
    x = await get_price_from_router(token_in='0x63cf309500d8be0b9fdb8f1fb66c821236c0438c', token_out= '0x6983d1e6def3690c4d616b13597a09e6193ea013',network='harmony',router=ONERouter.SUSHI)

    return {'0x63cf309500d8be0b9fdb8f1fb66c821236c0438c'.lower() : ETH['0x6983d1e6def3690c4d616b13597a09e6193ea013'] * x['0x63cf309500d8be0b9fdb8f1fb66c821236c0438c']}

async def get_price_from_uni3(return_token, pool, network, token_decimals, native=False):
    x = await Call(pool, 'slot0()((uint160,int24,uint16,uint16,uint16,uint8,bool))', [[f'slot0',parsers.parse_slot_0]], _w3=WEB3_NETWORKS[network])()

    if native:
        network_route = NetworkRoutes(network)
        native_price = await Call(network_route.default_router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** network_route.dnative, [network_route.native, network_route.stable]], [[f'native_price', parsers.parse_router_native, network_route.dstable]], WEB3_NETWORKS[network])()

        return {return_token.lower() : native_price['native_price'] / uniSqrtPrice(token_decimals, x['slot0']['sqrtPriceX96'])}
    else:
        return {return_token.lower() : uniSqrtPrice(token_decimals, x['slot0']['sqrtPriceX96'])}

async def get_synth_price(address,aggregator,network):

    price = await Call(aggregator, [f'latestAnswer()(uint256)'], _w3=WEB3_NETWORKS[network])()

    return {address.lower() : parsers.from_custom(price, 8)}

async def get_gohm_price(token_in, network, router, native=False, decimal=18, bypass_token=None, token_out=None, return_token=None, gohm_token=None):
    chain_w3 = WEB3_NETWORKS[network]
    chain = network.upper()

    if token_out is None:
        token_out = getattr(native_tokens.StableToken, chain)
    else:
        token_out = token_out

    if return_token is None:
        return_token = token_in
    else:
        return_token = return_token

    if bypass_token is None:
        native_token = getattr(native_tokens.NativeToken, chain)
    else:
        native_token = bypass_token
    default_router = getattr(native_tokens.DefaultRouter, chain)
        
    if native is True:
        stable_decimal = getattr(native_tokens.StableDecimal, chain)
        native_price = await Call(default_router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, [native_token, token_out]], [[f'token_in', parsers.parse_router_native, stable_decimal]], chain_w3)()
        token_price = await Call(router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** decimal, [token_in, native_token]], [[f'token_in', parsers.parse_router, native_price['token_in']]],chain_w3)()
    else:
        token_price = await Call(router, ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** decimal, [token_in, token_out]], [[f'token_in', parsers.parse_router]],chain_w3)()

    gohm_index = await Call(return_token, ['index()(uint256)'], None, _w3=chain_w3)()

    return {return_token.lower() : token_price['token_in'] * parsers.from_custom(gohm_index, 9)}

async def get_bancor_prices(tokens_in, network):

    network_route = NetworkRoutes(network)
    route_calls= []
    price_calls = []
    out_token = network_route.native
    network_conn = network_route.network_conn

    native_price = await Call('0x98ace08d2b759a265ae326f010496bcd63c15afc', ['rateByPath(address[],uint256)(uint256)',('0x542fda317318ebf1d3deaf76e0b632741a7e677d', '0x6f96096687952349dd5944e0eb1be327dcdeb705', '0xb5999795be0ebb5bab23144aa5fd6a02d080299f'), 1 * 10 ** 18], [['native_price', parsers.from_wei]], network_conn)()


    for token in tokens_in:

        token_address = token['token']
        route_calls.append(Call('0x98ace08d2b759a265ae326f010496bcd63c15afc', ['conversionPath(address,address)(address[])', token_address, out_token], [[token_address, None]]))

    token_routes = await Multicall(route_calls, network_conn)()

    for token in tokens_in:
        if token_routes.get(token['token']):
            swap_route = token_routes.get(token['token'])
            price_calls.append(Call('0x98ace08d2b759a265ae326f010496bcd63c15afc', ['rateByPath(address[],uint256)(uint256)',swap_route, 1 * 10 ** token['decimal']], [[ token['token'], parsers.parse_bancor, {'decimal' : network_route.dnative, 'price' : native_price['native_price']} ]]))
        
        price_calls.append(Call('0x102692AbBAB9a1AA75AA78Fff6E23f6ea7b84f61', ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token['decimal'], [token['token'], out_token]], [[token['token'], parsers.parse_liq, {'decimal' : network_route.dnative, 'price' : native_price['native_price']}]]))

    multi = await Multicall(price_calls, network_conn, _strict=False)()

    prices = {}
    for each in multi:
        prices[each] = multi[each]
    
    for token in tokens_in:
        if token['token'] not in prices:
            prices[token['token']] = 0

    prices[out_token.lower()] = native_price['native_price']
    
    return prices

async def get_songbird_prices(tokens_in, network):

    network_route = NetworkRoutes(network)
    calls= []
    out_token = network_route.native
    network_conn = network_route.network_conn

    songbird_price = parsers.from_custom(await Call('0x69F068C83e07634bCa3aa56F0FB8345552F40A16', ['fetchPrice()(uint256)'], None, network_conn)(), 18)
    cand_price = await Call('0x40fe25Fc866794d468685Bb8AD2E61757400338f', ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** 18, ['0x70Ad7172EF0b131A1428D0c1F66457EB041f2176', '0x02f0826ef6aD107Cfc861152B32B52fD11BaB9ED']], None, network_conn)()
    native_price = songbird_price * parsers.from_custom(cand_price[1], 18)

    for token in tokens_in:
        for contract in network_route.lrouters:

            token_address = token['token']
            token_in_address = router_override[token_address]['token'] if token_address in router_override else token_address
            token_dec = router_override[token_address]['decimal'] if token_address in router_override else token['decimal']

            calls.append(Call(getattr(network_route.router, contract), ['getAmountsOut(uint256,address[])(uint[])', 1 * 10 ** token_dec, [token_in_address, '0x70Ad7172EF0b131A1428D0c1F66457EB041f2176']], [[f'{contract}_{token_address}', parsers.parse_liq, {'decimal' : network_route.dnative, 'price' : native_price}]]))

    multi = await Multicall(calls, network_conn, _strict=False)()

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
    
    for token in tokens_in:
        if token['token'] not in prices:
            prices[token['token']] = 0

    prices[out_token.lower()] = songbird_price
    
    return prices

