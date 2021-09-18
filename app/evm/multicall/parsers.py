def parse_slot_0(data):
    d = {
        'sqrtPriceX96' : data[0],
        'tick' : data[1],
        'observationIndex' : data[2],
        'observationCardinality' : data[3],
        'observationCardinalityNext' : data[4],
        'feeProtocol' : data[5],
        'unlocked' : data[6]
    }

    return d

def parse_uniswap_positions(data):
    d = {
        'nonce' : data[0],
        'operator' : data[1],
        'token0' : data[2],
        'token1' : data[3],
        'fee' : data[4],
        'tickLower' : data[5],
        'tickUpper' : data[6],
        'liquidity' : data[7],
        'feeGrowth0' : data[8],
        'feeGrowth1' : data[9],
        'tokensOwed0' : data[10],
        'tokensOwed1' : data[11],
    }

    return d

def parse_ticks(data):
    d = {
        'liquidityGross' : data[0],
        'liquidityNet' : data[1],
        'feeGrowthOutside0X128' : data[2],
        'feeGrowthOutside1X128' : data[3],
        'tickCumulativeOutside' : data[4],
        'secondsPerLiquidityOutsideX128' : data[5],
        'secondsOutside' : data[6],
        'initialized' : data[7],
    }

    return d

def from_wei(value):
    return value / 1e18

def from_ele(value):
    return '0xAcD7B3D9c10e97d0efA418903C0c7669E702E4C0'

def parseReserves(value):
    return [ str(value[0]), str(value[1])]

def parseWanted(value):
    return value[0]

def parse_wanted_slot_two(value):
    return value[1]

def from_custom(value, decimal):
    return value / (10**decimal)

def parseBunny(data):
    response = { 'userInfo' : {
        'staked': from_wei(data[2]),
        'ppShare' : from_wei(data[9]),
        'pending' : from_wei(data[7]),
        'pendingBunny' : from_wei(data[8])
    } }

    return response

def from_tao(value):
    return value / 1e9

def parseAccountSnapshot(data):
    staked = from_wei(int(data[1]))
    borrow = from_wei(int(data[2]))
    rate = from_wei(int(data[3]))
    return staked * rate

def parseMerlin(data):
    response = { 'userInfo' : {
        'staked': from_wei(data[1]),
        'ppShare' : data[9],
        'pending' : from_wei(data[7]),
        'pendingMerlin' : from_wei(data[8])
    } }

    return response

def from_six(value):
    return value / 1e6

def parse_pancake_bunny_info(data):
    r = {
        'poolID' : data[0],
        'balance' : from_wei(data[1]),
        'principal' : from_wei(data[2]),
        'available' : from_wei(data[3]),
        'pending_base' : from_wei(data[7]),
        'pending_native' : from_wei(data[8])
    }
    return r

def parse_profit_of_pool(data):
    r = [from_wei(data[0]), from_wei(data[1])]
    return r

def parse_value_of_asset(data):
    return from_wei(data[1])

def parse_spacepool(data,offset):
    return data[offset]

def parse_pool_weights(data):
    r = []
    for each in data:
        r.append(from_wei(each))
    return r

def parse_zombie_pool(data):
    d = {
         'lp_token' : data[0],
         'is_grave' : data[5],
         'requires_rug' : data[6]
     }
       
    return d

def parse_router(data, native=None):
    if native is None:
        return from_wei(data[1])
    else:
        return from_wei(data[1]) * native

def parse_router_native(data, native=None):
    if native is None:
        return from_wei(data[1])
    else:
        return from_custom(data[1], native)

def parse_wanted_offset(value, offset):
    return value[offset]