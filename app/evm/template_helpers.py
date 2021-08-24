from .multicall import Call, Multicall
from .networks import WEB3_NETWORKS


async def get_token_list_decimals(tokens,network_id,parse_wanted):
    
    network = WEB3_NETWORKS[network_id]
    
    if parse_wanted is True:
        tokens = parse_out_want_contracts(tokens)

    calls = []

    for each in tokens:
        calls.append(Call(each, 'decimals()(uint8)', [[f'{each}', None]]))

    return await Multicall(calls, network, _strict=False)()


def parse_out_want_contracts(data):

    token_list = []

    for each in data:
        if 'want' in each:
            token_list.append(data[each])

    return token_list


def get_cvx_minted(crv_earned, total_supply):

    cliff_size = 100000
    cliff_count = 1000
    max_supply = 100000000

    current_cliff = total_supply / cliff_size

    if current_cliff < cliff_count:
        remaining = cliff_count - current_cliff
        cvx_earned = crv_earned * remaining / cliff_count
        amount_till_max = max_supply - total_supply

        if (cvx_earned > amount_till_max):
            cvx_earned = amount_till_max

        return cvx_earned
    else:
        return 0

def get_token_list_decimals_symbols(tokens,network_id):
    
    network = WEB3_NETWORKS[network_id]
    
    calls = []

    for each in tokens:
        calls.append(Call(each, 'decimals()(uint8)', [[f'{each}_decimals', None]]))
        calls.append(Call(each, 'symbol()(string)', [[f'{each}_symbol', None]]))

    return Multicall(calls, network)()