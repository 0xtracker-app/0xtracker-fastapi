def from_wei(value):
    return value / 1e18

def from_ele(value):
    return '0xAcD7B3D9c10e97d0efA418903C0c7669E702E4C0'

def parseReserves(value):
    return [ str(value[0]), str(value[1])]

def parseWanted(value):
    return value[0]

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

def parse_router(data, native=None):
    if native is None:
        return from_wei(data[1])
    else:
        return from_wei(data[1]) * native