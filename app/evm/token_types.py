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


            lp_tokens = await Multicall([
                Call(lp_pool['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
                Call(lp_pool['token1'], 'decimals()(uint8)', [['tkn1d', None]]),
                Call(lp_pool['token0'], 'symbol()(string)', [['tkn0s', None]]),
                Call(lp_pool['token1'], 'symbol()(string)', [['tkn1s', None]])
            ], network_chain)()

            return {**lp_pool, **lp_tokens,  **{'lpToken' : token, 'tokenAddresses' : [lp_pool['token0'], lp_pool['token1']], 'tokenSymbols' : [lp_tokens['tkn0s'], lp_tokens['tkn1s']], 'decimals' : [lp_tokens['tkn0d'], lp_tokens['tkn1d']],'weights' : [.5, .5]}}

async def get_stargate(token, farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    token_data = await Multicall([
        Call(token, 'symbol()(string)', [['symbol', None]]),
        Call(token, 'token()(address)', [['token0', None]]),
        Call(token, 'totalLiquidity()(uint256)', [['totalLiquidity', None]]),
        Call(token, 'totalSupply()(uint256)', [['totalSupply', None]]),
        Call(token, 'symbol()(string)', [['tkn0s', None]]),
    ], network_chain)()

    token_decimal = await Call(token_data['token0'], 'decimals()(uint8)', [['tkn0d', None]], network_chain)()

    return {**token_data, **token_decimal, **{'tokenAddresses' : [token_data['token0']], 'tokenSymbols' : [token_data['tkn0s']], 'decimals' : [token_decimal['tkn0d']],'weights' : [1]}}

async def get_uniswap_pool(token, farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    multi_lp = Multicall([
        Call(token, 'tickSpacing()(int24)', [['tickSpacing', None]]),
        Call(token, 'token0()(address)', [['token0', None]]),
        Call(token, 'token1()(address)', [['token1', None]]),
    ], network_chain)

    lp_pool = await multi_lp()


    lp_tokens = await Multicall([
        Call(lp_pool['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
        Call(lp_pool['token1'], 'decimals()(uint8)', [['tkn1d', None]]),
        Call(lp_pool['token0'], 'symbol()(string)', [['tkn0s', None]]),
        Call(lp_pool['token1'], 'symbol()(string)', [['tkn1s', None]])
    ], network_chain)()

    return {**lp_pool, **lp_tokens,  **{'uniswapPool' : token, 'tokenAddresses' : [lp_pool['token0'], lp_pool['token1']], 'tokenSymbols' : [lp_tokens['tkn0s'], lp_tokens['tkn1s']], 'decimals' : [lp_tokens['tkn0d'], lp_tokens['tkn1d']],'weights' : [.5, .5]}}

async def get_single(token, farm_id):

        network_chain = WEB3_NETWORKS[farm_id]
                
        try:
            x = await Call(token, 'loanTokenAddress()(address)', [['loan', None]], network_chain)()
            token = x['loan']
        except:
            token = token
        
        single = await Multicall([
                        Call(token, 'symbol()(string)', [['tkn0s', None]]),
                        Call(token, 'decimals()(uint8)', [['tkn0d', None]]),
                    ], network_chain)()

        add = {'token0' : token}

        return {**add, **single, **{'tokenAddresses' : [add['token0']], 'tokenSymbols' : [single['tkn0s']], 'decimals' : [single['tkn0d']],'weights' : [1]}}

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

    swapToken = Multicall([
            Call(swap['curve_minter'], 'get_virtual_price()(uint256)', [['virtualPrice', parsers.from_wei]]),
        ], network_chain)
    
    swapCalls = await swapToken()

    singleSwap = await get_single(swap_token['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap, **swap_token, **{'curve_pool_token': token, 'tokenAddresses' : [singleSwap['token0']], 'tokenSymbols' : [swap['tkn0s']], 'decimals' : [singleSwap['tkn0d']],'weights' : [1]}}

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

    swapToken = Multicall([
            Call(token, 'get_virtual_price()(uint256)', [['virtualPrice', parsers.from_wei]])
        ], network_chain)
    
    swapCalls = await swapToken()

    singleSwap = await get_single(swap_token['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap, **swap_token, **{'curve_pool_token': token, 'tokenAddresses' : [singleSwap['token0']], 'tokenSymbols' : [swap['tkn0s']], 'decimals' : [singleSwap['tkn0d']],'weights' : [1]}}

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

    final = {**swapCalls, **singleSwap, **{'tokenAddresses' : [singleSwap['token0']], 'tokenSymbols' : [swap['tkn0s']], 'decimals' : [singleSwap['tkn0d']],'weights' : [1]}}

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

        return {**wrappedCalls, **belt, **{'tokenAddresses' : [belt['token0']], 'tokenSymbols' : [belt['tkn0s']], 'decimals' : [wrappedCalls['tkn0d']],'weights' : [1]}}

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

        return {**wrappedCalls, **calls, **{'tokenAddresses' : [calls['token0']], 'tokenSymbols' : [calls['tkn0s']], 'decimals' : [wrappedCalls['tkn0d']],'weights' : [1]}}

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
    "balancerVault" : vault, 
    "balancerPoolID" : pool_info['pool_id'].hex(),
    "balancerBalances" :  [str(x) for x in vault_info[1]],
    "balancerWeights" : pool_weights,
    "balancerSymbols" : token_symbols,
    "balancerDecimals" : token_decimals,
    'balancerTokens' : vault_info[0],
    
    'tokenAddresses' : vault_info[0],
    'decimals' : token_decimals,
    'weights' : pool_weights,
    'tokenSymbols' : token_symbols,

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

async def get_nft(token, farm_id):
        network_chain = WEB3_NETWORKS[farm_id]
                       
        single = Multicall([
                        Call(token, 'symbol()(string)', [['tkn0s', None]]),
                        Call(token, 'baseTokenURI()(string)', [['baseTokenURI', None]]),
                    ], network_chain)

        add = {'token0' : token, 'tkn0d' : 1}

        return {**add, **await single()}

async def get_beethoven_token(pool_token,farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    vault = '0x20dd72Ed959b6147912C2e529F0a0C651c33c9ce'


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
    "balancerVault" : vault, 
    "balancerPoolID" : pool_info['pool_id'].hex(),
    "balancerBalances" :  [str(x) for x in vault_info[1]],
    "balancerWeights" : pool_weights,
    "balancerSymbols" : token_symbols,
    "balancerDecimals" : token_decimals,
    'balancerTokens' : vault_info[0],

    'tokenAddresses' : vault_info[0],
    'decimals' : token_decimals,
    'weights' : pool_weights,
    'tokenSymbols' : token_symbols,

    "tkn0d" : token_decimals[0], 
    "tkn0s" : '/'.join(token_symbols), 
    "token0" : vault_info[0][0], 
    "totalSupply" : pool_info['totalSupply']
    }

    return token_data

async def get_bancor_token(pool_token,farm_id):

    network_chain = WEB3_NETWORKS[farm_id]

    owner = await Call(pool_token, ['owner()(address)'], None, network_chain)()
    pool_length = await Call(owner, ['connectorTokenCount()(uint16)'], None, network_chain)()
    token_calls = []

    for token in range(0,pool_length):
        token_calls.append(Call(owner, ['connectorTokens(uint256)(address)', token], [[f'{token}_address', None]]))

    token_address = await Multicall(token_calls, network_chain)()

    calls = []
    token_addresses = []
    for token in range(0,pool_length):
        address = token_address.get(f'{token}_address')
        token_addresses.append(address)
        calls.append(Call(address, [f'symbol()(string)'], [[f'{token}_symbol', None]]))
        calls.append(Call(address, [f'decimals()(uint256)'], [[f'{token}_decimal', None]]))
        calls.append(Call(owner, [f'getConnectorBalance(address)(uint256)', address], [[f'{token}_reserve', None]]))
        calls.append(Call(owner, [f'reserveWeight(address)(uint256)', address], [[f'{token}_weight', None]]))

    tokens_info = await Multicall(calls,WEB3_NETWORKS[farm_id])()

    token_symbols = []
    token_decimals = []
    token_reserves = []
    token_weights = []

    for each in tokens_info:
        if 'symbol' in each:
            token_symbols.append(tokens_info[each])
        elif 'decimal' in each:
            token_decimals.append(tokens_info[each])
        elif 'reserve' in each:
            token_reserves.append(str(tokens_info[each]))
        elif 'weight' in each:
            token_weights.append(tokens_info[each] / 1000000)

    token_data = {
    "bancorOwner" : owner, 
    "bancorBalances" :  token_reserves,
    "bancorWeights" : token_weights,
    "bancorSymbols" : token_symbols,
    "bancorDecimals" : token_decimals,
    'bancorTokens' : token_addresses,

    'tokenAddresses' : token_addresses,
    'decimals' : token_decimals,
    'weights' : token_weights,
    'tokenSymbols' : token_symbols,


    "tkn0d" : await Call(pool_token, ['decimals()(uint8)'], None, network_chain)(),
    "tkn0s" : '/'.join(token_symbols), 
    "token0" : pool_token, 
    "totalSupply" : await Call(pool_token, ['totalSupply()(uint256)'], None, network_chain)()
    }

    token_data['totalSupply'] = parsers.from_custom(await Call(pool_token, ['totalSupply()(uint256)'], None, network_chain)(), token_data['tkn0d'])

    return token_data

async def catch_all(token, farm_id):

        network_chain = WEB3_NETWORKS[farm_id]
                        
        # single = Multicall([
        #                 Call(token, 'symbol()(string)', [['tkn0s', None]]),
        #             ], network_chain)

        add = {'token0' : token, 'tkn0d' : 1, 'tkn0s' : 'UNKNOWN'}

        return add