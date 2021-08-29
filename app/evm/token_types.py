from .networks import WEB3_NETWORKS
from .multicall import Multicall, Call, parsers
from .w3_contract import set_pool
from .abi.balancer_vault import balancer_vault_abi

async def get_lp(token, farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    try:
        return await get_swap(token, farm_id)
    except:
        try:
            return await get_curve_token(token,farm_id)
        except:
            multi_lp = Multicall([
                Call(token, 'symbol()(string)', [['symbol', None]]),
                Call(token, 'token0()(address)', [['token0', None]]),
                Call(token, 'token1()(address)', [['token1', None]]),
                Call(token, 'totalSupply()(uint256)', [['totalSupply', parsers.from_wei]]),
                Call(token, 'getReserves()((uint112,uint112))', [['reserves', parsers.parseReserves]])
            ], network_chain)

            lp_pool = await multi_lp()


            lp_tokens = Multicall([
                Call(lp_pool['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
                Call(lp_pool['token1'], 'decimals()(uint8)', [['tkn1d', None]]),
                Call(lp_pool['token0'], 'symbol()(string)', [['tkn0s', None]]),
                Call(lp_pool['token1'], 'symbol()(string)', [['tkn1s', None]])
            ], network_chain)

            return {**multi_lp, **await lp_tokens(),  **{'lpToken' : token}}

async def get_uniswap_pool(token, farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    multi_lp = Multicall([
        Call(token, 'tickSpacing()(int24)', [['tickSpacing', None]]),
        Call(token, 'token0()(address)', [['token0', None]]),
        Call(token, 'token1()(address)', [['token1', None]]),
    ], network_chain)

    lp_pool = await multi_lp()


    lp_tokens = Multicall([
        Call(lp_pool['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
        Call(lp_pool['token1'], 'decimals()(uint8)', [['tkn1d', None]]),
        Call(lp_pool['token0'], 'symbol()(string)', [['tkn0s', None]]),
        Call(lp_pool['token1'], 'symbol()(string)', [['tkn1s', None]])
    ], network_chain)

    return {**lp_pool, **await lp_tokens(),  **{'uniswapPool' : token}}

async def get_single(token, farm_id):

        network_chain = WEB3_NETWORKS[farm_id]
                
        try:
            token = await Call(token, 'loanTokenAddress()(address)', [['loan', None]], network_chain)()['loan']
        except:
            token = token
        
        single = Multicall([
                        Call(token, 'symbol()(string)', [['tkn0s', None]]),
                        Call(token, 'decimals()(uint8)', [['tkn0d', None]]),
                    ], network_chain)

        add = {'token0' : token}

        return {**add, **await single()}

async def get_curve_token(token, farm_id):
    
    network_chain = WEB3_NETWORKS[farm_id]
    
    swap = Multicall([
            Call(token, 'minter()(address)', [['curve_minter', None]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
        ], network_chain)

    swap=await swap()

    if token in ['0x55088b82748ac28e31e0677241dbbe0a663d7e40', '0xe7419b94082a87c04ffb298805ec07f745d9d216']:
        tokenIndex = 1
    else:
        tokenIndex = 0


    if token.lower() in ['0x5b5cfe992adac0c9d48e05854b2d91c73a003858'.lower(),'0x8096ac61db23291252574D49f036f0f9ed8ab390'.lower(), '0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171'.lower()]:
        token_0 = 'coins'
    else:
        token_0 = 'underlying_coins'

    try:
        swap_token = await Call(swap['curve_minter'], [f'coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()
    except:
        swap_token = await Call(swap['curve_minter'], [f'underlying_coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()

    swapToken = await Multicall([
            Call(swap['curve_minter'], 'get_virtual_price()(uint256)', [['virtualPrice', parsers.from_wei]]),
        ], network_chain)
    
    swapCalls = await swapToken()

    singleSwap = await get_single(swap_token['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap, **swap_token, **{'curve_pool_token': token}}

    final.update(swap)
    final['tkn0s'] = swap['tkn0s']

    return final

async def get_curve_token_two(token, farm_id):
    
    network_chain = WEB3_NETWORKS[farm_id]
    
    swap = Multicall([
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
        ], network_chain)

    swap=await swap()

    if token in ['0x55088b82748ac28e31e0677241dbbe0a663d7e40', '0xe7419b94082a87c04ffb298805ec07f745d9d216']:
        tokenIndex = 1
    else:
        tokenIndex = 0


    if token.lower() in ['0x8096ac61db23291252574D49f036f0f9ed8ab390'.lower(), '0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171'.lower(), '0x92D5ebF3593a92888C25C0AbEF126583d4b5312E'.lower(), '0x27e611fd27b276acbd5ffd632e5eaebec9761e40'.lower(), '0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890'.lower()]:
        token_0 = 'coins'
    else:
        token_0 = 'underlying_coins'

    try:
        swap_token = await Call(token, [f'coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()
    except:
        swap_token = await Call(token, [f'underlying_coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()

    swapToken = await Multicall([
            Call(token, 'get_virtual_price()(uint256)', [['virtualPrice', parsers.from_wei]])
        ], network_chain)
    
    swapCalls = await swapToken()

    singleSwap = await get_single(swap_token['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap, **swap_token, **{'curve_pool_token': token}}

    final.update(swap)
    final['tkn0s'] = swap['tkn0s']

    return final

async def get_swap(token, farm_id):
    
    network_chain = WEB3_NETWORKS[farm_id]
    
    swap = Multicall([
            Call(token, 'swap()(address)', [['swap', None]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
        ], network_chain)

    swap=await swap()

    if token in ['0x55088b82748ac28e31e0677241dbbe0a663d7e40', '0xe7419b94082a87c04ffb298805ec07f745d9d216','0x3d479ce22d8f091df67f8fb8f579251d1b1b3152']:
        tokenIndex = 1
    else:
        tokenIndex = 0

    swapToken = Multicall([
            Call(swap['swap'], 'getVirtualPrice()(uint256)', [['virtualPrice', parsers.from_wei]]),
            Call(swap['swap'], ['getToken(uint8)(address)', tokenIndex], [['swapToken', None]]),
        ], network_chain)
    
    swapCalls = await swapToken()

    singleSwap = await get_single(swapCalls['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap}

    final.update(swap)

    return final

async def get_belt_token(token, farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    try:
        belt = Multicall([
                Call(token, 'getPricePerFullShare()(uint256)', [['getPricePerFullShare', parsers.from_wei]]),
                Call(token, 'symbol()(string)', [['tkn0s', None]]),
                Call(token, 'token()(address)', [['token0', None]])
            ], network_chain)

        belt=await belt()
    except:
        try:
            belt = Multicall([
                    Call(token, 'getPricePerFullShare()(uint256)', [['getPricePerFullShare', parsers.from_wei]]),
                    Call(token, 'symbol()(string)', [['tkn0s', None]]),
                    Call(token, 'want()(address)', [['token0', None]])
                ], network_chain)

            belt=await belt()
        except:
            belt = Multicall([
                    Call(token, 'getPricePerFullShare()(uint256)', [['getPricePerFullShare', parsers.from_wei]]),
                    Call(token, 'symbol()(string)', [['tkn0s', None]]),
                    Call(token, 'wmatic()(address)', [['token0', None]])
                ], network_chain)

            belt=await belt()      

    try:
        wrappedCalls = await get_lp(belt['token0'], farm_id)
        return {**wrappedCalls, **{'getPricePerFullShare': belt['getPricePerFullShare']}}
    except:
        wrappedToken = Multicall([
                Call(belt['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
            ], network_chain)
        
        wrappedCalls = await wrappedToken()

        return {**wrappedCalls, **belt}

async def get_grow_tokens(token, farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    grow = Multicall([
            Call(token, 'reserveToken()(address)', [['reserveToken', None]]),
            Call(token, 'totalReserve()(uint256)', [['growTotalReserve', parsers.from_wei]]),
            Call(token, 'totalSupply()(uint256)', [['growTotalSupply', parsers.from_wei]])
        ], network_chain)

    grow=await grow()

    try:
        wrappedCalls = await get_lp(grow['reserveToken'], farm_id)
        return {**wrappedCalls, **grow}
    except:
        wrappedCalls = await get_single(grow['reserveToken'], farm_id)
        return {**wrappedCalls, **grow}

async def kashi_token(token,farm_id):

    network_chain = WEB3_NETWORKS[farm_id]
    token_decimal = await Call(token, 'decimals()(uint256)', None, network_chain)()

    call = Multicall([
            Call(token, 'asset()(address)', [['kashiAsset', None]]),
            Call(token, 'totalAsset()(uint256)', [['kashiTotalAsset', parsers.from_custom, token_decimal]]),
            Call(token, 'totalBorrow()(uint256)', [['kashiTotalBorrow', parsers.from_custom, token_decimal]]),
            Call(token, 'totalSupply()(uint256)', [['kashiTotalSupply', parsers.from_custom, token_decimal]]),

        ], network_chain)

    calls=await call()

    wrappedCalls = await get_single(calls['kashiAsset'], farm_id)
    
    return {**wrappedCalls, **calls}

async def get_picklejars(token, farm_id):

    network_chain = WEB3_NETWORKS[farm_id]


    call = Multicall([
            Call(token, 'getRatio()(uint256)', [['getRatio', parsers.from_wei]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
            Call(token, 'token()(address)', [['token0', None]])
        ], network_chain)

    calls=await call()      

    try:
        wrappedCalls = await get_lp(calls['token0'], farm_id)
        return {**wrappedCalls, **{'getRatio': calls['getRatio']}}
    except:
        wrappedToken = Multicall([
                Call(calls['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
            ], network_chain)
        
        wrappedCalls = await wrappedToken()

        return {**wrappedCalls, **calls}

async def get_balancer_token(pool_token,farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    vault = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'


    try:
        calls = []
        calls.append(Call(pool_token, [f'getPoolId()(bytes32)'], [[f'pool_id', None]]))
        calls.append(Call(pool_token, [f'totalSupply()(uint256)'], [[f'totalSupply', parsers.from_wei]]))
        calls.append(Call(pool_token, [f'getNormalizedWeights()(uint256[])'], [[f'pool_weights', parsers.parse_pool_weights]]))

        pool_info = await Multicall(calls,network_chain)()
    except:
        calls = []
        calls.append(Call(pool_token, [f'getPoolId()(bytes32)'], [[f'pool_id', None]]))
        calls.append(Call(pool_token, [f'totalSupply()(uint256)'], [[f'totalSupply', parsers.from_wei]]))

        pool_info = await Multicall(calls,network_chain)()

    balancer_vault = set_pool(balancer_vault_abi,vault,farm_id)
    
    vault_info = balancer_vault.getPoolTokens(pool_info['pool_id']).call()

    calls = []

    for token in vault_info[0]:
        calls.append(Call(token, [f'symbol()(string)'], [[f'{token}_symbol', None]]))
        calls.append(Call(token, [f'decimals()(uint256)'], [[f'{token}_decimal', None]]))

    tokens_info = await Multicall(calls,WEB3_NETWORKS[farm_id])()

    token_symbols = []
    token_decimals = []
    for each in tokens_info:
        if 'symbol' in each:
            token_symbols.append(tokens_info[each])
        elif 'decimal' in each:
            token_decimals.append(tokens_info[each])

    if 'pool_weights' not in pool_info:
        pool_weights = []
        pool_lengths = len(vault_info[0])
        for each in vault_info[0]:
            pool_weights.append(1/pool_lengths)
    else:
        pool_weights = pool_info['pool_weights']

    token_data = { 
    "balancerPoolID" : pool_info['pool_id'].hex(),
    "balancerBalances" :  [str(x) for x in vault_info[1]],
    "balancerWeights" : pool_weights,
    "balancerSymbols" : token_symbols,
    "balancerDecimals" : token_decimals,
    'balancerTokens' : vault_info[0],
    "tkn0d" : token_decimals[0], 
    "tkn0s" : '/'.join(token_symbols), 
    "token0" : vault_info[0][0], 
    "totalSupply" : pool_info['totalSupply']
    }

    return token_data

async def get_balancer_ratio(token_data,quote_price):

    userPct = token_data['staked'] / token_data['totalSupply']

    lp_multiplier = 1 / token_data['balancerWeights'][0]

    lp_values = []
    
    for i, each in enumerate(token_data['balancerBalances']):
        lpvalue = (userPct * int(each)) / (10**token_data['balancerDecimals'][i])
        lp_values.append(lpvalue)
    
    lp_price = 0

    for i,lp_balance in enumerate(lp_values):
        token_address = token_data['balancerTokens'][i]
        token_price = quote_price[token_address]
        lp_price += lp_balance * token_price

    return {'lpTotal': '/'.join([str(round(x,2)) for x in lp_values]), 'lpPrice' : lp_price}
