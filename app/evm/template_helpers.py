from .multicall import Call, Multicall
from .networks import WEB3_NETWORKS
import time
from functools import reduce
import math
import numpy as np
import asyncio

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

def round_to_half_hour():
    current_time = int(time.time())- 1260
    interval = 1800
    offset = current_time % interval
    rounded = current_time - offset

    return rounded

def round_to_hour():
    current_time = int(time.time()) - 1260
    interval = 3600
    offset = current_time % interval
    rounded = current_time - offset

    return rounded

async def multicall_chunk(calls, network_conn, chunk_limit=None, chunk_size=None, strict=False):

    if len(calls) > chunk_limit:
        chunks = len(calls) / chunk_size
        x = np.array_split(calls, math.ceil(chunks))
        all_calls=await asyncio.gather(*[Multicall(call,network_conn, _strict=strict)() for call in x])
        return reduce(lambda a, b: dict(a, **b), all_calls)
    else:
        return await Multicall(calls, network_conn, _strict=strict)()