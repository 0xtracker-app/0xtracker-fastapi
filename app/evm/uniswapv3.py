import decimal
import math
from .networks import WEB3_NETWORKS
from .multicall import Call, Multicall, parsers
from web3 import Web3

#Constants
x96 = pow(2, 96)
x128 = pow(2, 128)
max_amount = pow(2,128)-1

async def get_uniswap_v3_positions(wallet,network,uniswap_nft,uniswap_factory,farm_id,vaults):

    chain = WEB3_NETWORKS[network]
    poolKey = farm_id
    
    nft_balance = await Call(uniswap_nft,['balanceOf(address)(uint256)',wallet], None, chain)()

    v3_index_calls = []

    for token_index in range(0,nft_balance):
        v3_index_calls.append(Call(uniswap_nft,['tokenOfOwnerByIndex(address,uint256)(uint256)',wallet,token_index], [[str(token_index), None]]))

    v3_token_ids = await Multicall(v3_index_calls,chain)()

    v3_position_calls = []
    position_types = '(uint96,address,address,address,uint24,int24,int24,uint128,uint256,uint256,uint128,uint128)'
    for each in v3_token_ids:
        token_id = v3_token_ids[each]
        v3_position_calls.append(Call(uniswap_nft,[f'positions(uint256)({position_types})',token_id], [[token_id, parsers.parse_uniswap_positions]]))

    
    v3_positions = await Multicall(v3_position_calls, chain)()

    stakes = await get_uniswap_token_data(v3_positions,'eth',uniswap_factory,uniswap_nft,Web3.toChecksumAddress(wallet))

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if stakes[each]['liquidity'] > 0:
            stakes[each]['staked'] = parsers.from_wei(stakes[each]['liquidity'])
            poolNest[poolKey]['userData'][each] = stakes[each]
            poolIDs['%s_%s_want' % (poolKey, each)] = stakes[each]['pooladdress']
            stakes[each]['pendingfees'] = await Call(uniswap_nft,['collect((uint256,address,uint128,uint128))(uint256,uint256)',(each,wallet,max_amount,max_amount)],None,WEB3_NETWORKS[network])()

                
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_uniswap_token_data(v3_positions, network, uniswap_factory,uniswap_nft,wallet):

    chain = WEB3_NETWORKS[network]

    pool_calls =[]

    #Get Pool Address and Token Data
    for each in v3_positions:
        pool_calls.append(Call(uniswap_factory,[f'getPool(address,address,uint24)(address)',v3_positions[each]['token0'],v3_positions[each]['token1'],v3_positions[each]['fee']], [[f'{each}_pooladdress', None]]))
        pool_calls.append(Call(v3_positions[each]['token0'], [f'decimals()(uint256)'], [[f'{each}_tkn0d', None]]))
        pool_calls.append(Call(v3_positions[each]['token1'], [f'decimals()(uint256)'], [[f'{each}_tkn1d', None]]))
        pool_calls.append(Call(v3_positions[each]['token0'], [f'symbol()(string)'], [[f'{each}_tkn0s', None]]))
        pool_calls.append(Call(v3_positions[each]['token1'], [f'symbol()(string)'], [[f'{each}_tkn1s', None]]))
    pool_address = await Multicall(pool_calls,chain,_strict=False)()

    slot_calls = []
    for each in pool_address:
        breakdown = each.split('_')
        nft_id = int(breakdown[0])
        v3_positions[nft_id][breakdown[1]] = pool_address[each]
        if breakdown[1] == 'pooladdress':
            slot_calls.append(Call(pool_address[each], 'slot0()((uint160,int24,uint16,uint16,uint16,uint8,bool))', [[f'{breakdown[0]}_slot0',parsers.parse_slot_0]]))
            slot_calls.append(Call(pool_address[each], ['ticks(int24)((uint128,int128,uint256,uint256,int56,uint160,uint32,bool))', v3_positions[nft_id]['tickLower']],[[f'{breakdown[0]}_ticksLower',parsers.parse_ticks]]))
            slot_calls.append(Call(pool_address[each], ['ticks(int24)((uint128,int128,uint256,uint256,int56,uint160,uint32,bool))', v3_positions[nft_id]['tickUpper']],[[f'{breakdown[0]}_ticksUpper',parsers.parse_ticks]]))
            slot_calls.append(Call(pool_address[each], 'feeGrowthGlobal0X128()(uint256)',[[f'{breakdown[0]}_feeGrowthGlobal0X128',None]]))
            slot_calls.append(Call(pool_address[each], 'feeGrowthGlobal1X128()(uint256)',[[f'{breakdown[0]}_feeGrowthGlobal1X128',None]]))
            slot_calls.append(Call(pool_address[each], 'liquidity()(uint128)',[[f'{breakdown[0]}_poolliquidity',None]]))

    slot_call_result = await Multicall(slot_calls,chain)()

    for each in slot_call_result:
        breakdown = each.split('_')
        nft_id = int(breakdown[0])
        v3_positions[nft_id][breakdown[1]] = slot_call_result[each]

    return v3_positions

def get_uniswap_v3_balance(token_data,network,prices):

    token0 = token_data['token0']
    token1 = token_data['token1']
    ints0 = token_data['tkn0d']
    ints1 = token_data['tkn1d']
    symbol0 = token_data['tkn0s']
    symbol1 = token_data['tkn1s']   

    positionLiquidity = token_data['liquidity']
    int_difference = ints1 - ints0

    price_current = sqrtPriceToPrice(token_data['slot0']['sqrtPriceX96'])
    price_upper = pow(1.0001, token_data['tickUpper'])
    price_lower = pow(1.0001, token_data['tickLower'])

    price_current_sqrt = token_data['slot0']['sqrtPriceX96'] / pow(2,96)
    price_upper_sqrt = math.sqrt(price_upper)
    price_lower_sqrt = math.sqrt(price_lower)

    price_current_adjusted = sqrtPriceToPriceAdjusted(token_data['slot0']['sqrtPriceX96'],int_difference)
    price_upper_adjusted = price_upper / pow(10,int_difference)
    price_lower_adjusted = price_lower / pow(10,int_difference)

    price_current_adjusted_reversed = 1 / price_current_adjusted
    price_lower_adjusted_reversed = 1 / price_upper_adjusted
    price_upper_adjusted_reversed = 1 / price_lower_adjusted

    if price_current <= price_lower:
        amount_0 = positionLiquidity * (1/price_current_sqrt - 1 / price_upper_sqrt)
        amount_1 = 0
    elif price_current < price_upper:
        amount_0 = positionLiquidity * (1/price_current_sqrt - 1 / price_upper_sqrt)
        amount_1 = positionLiquidity * (price_current_sqrt - price_lower_sqrt)
    else:
        amount_1 = positionLiquidity * (price_upper_sqrt - price_lower_sqrt)
        amount_0 = 0

    amount_0_adjusted = amount_0 / pow(10,ints0)
    amount_1_adjusted = amount_1 / pow(10,ints1)

    return {'lpTotal': '%s/%s' % (round(amount_0_adjusted, 2),round(amount_1_adjusted, 2)),
    'lpPrice' : (amount_0_adjusted * prices[token0]) + (amount_1_adjusted * prices[token1]),
    'uniswapFee' : get_uniswap_fees(token_data),
    'uniswapData': {
    'priceCurrent': price_current_adjusted,
    'priceUpper' : price_upper_adjusted,
    'priceLower' : price_lower_adjusted,
    'priceCurrentR' : price_current_adjusted_reversed,
    'priceUpperR' : price_upper_adjusted_reversed,
    'priceLowerR' : price_lower_adjusted_reversed, 
    }} 
    
def get_uniswap_fees(swap_data):

    uncollectedFeesAdjusted_0 = (swap_data['pendingfees'][0] / pow(10, swap_data['tkn0d']))
    uncollectedFeesAdjusted_1 = (swap_data['pendingfees'][1] / pow(10, swap_data['tkn1d']))

    return [{'pending': uncollectedFeesAdjusted_0, 'symbol' : swap_data['tkn0s'], 'token' : swap_data['token0'], 'decimal' : swap_data['tkn0d']},{'pending': uncollectedFeesAdjusted_1, 'symbol' : swap_data['tkn1s'], 'token' : swap_data['token1'], 'decimal' : swap_data['tkn1d']}]


#Helpers
def sqrtPriceToPriceAdjusted(sqrtPriceX96Prop, intDifference):
    sqrtPrice = sqrtPriceX96Prop / x96
    divideBy = pow(10, intDifference)
    price = pow(sqrtPrice, 2) / divideBy
    
    return price

def sqrtPriceToPrice(sqrtPriceX96Prop):
    sqrtPrice = sqrtPriceX96Prop / x96
    price = pow(sqrtPrice, 2)
    return price



