from .farms import Farms
from .networks import WEB3_NETWORKS
from .multicall import Call, Multicall, parsers
from .find_token_type import token_router

class Pools:
    def __init__(self, wallet=None, selected_farm=None):
        self.wallet

async def get_protocol_apy(farm_id, mongo_db, http_session):
    farm_info = Farms().farms[farm_id]
    collection = mongo_db.xtracker['full_tokens']
    calls = []
    web_3 = WEB3_NETWORKS[farm_info['network']]
    
    pool_length = await Call(farm_info['masterChef'], [farm_info['pool_length'] if 'pool_length' in farm_info else f'poolLength()(uint256)'],None,web_3)() 

    calls.append(Call(farm_info['masterChef'], [f"{farm_info['total_alloc']}()(uint256)" if 'total_alloc' in farm_info else f'totalAllocPoint()(uint256)'], [[f'{farm_info["masterChef"]}_points', None]]))
    calls.append(Call(farm_info['masterChef'], [f"{farm_info['perBlock']}()(uint256)"], [[f'{farm_info["masterChef"]}_block', None]]))

    death_index = [] if 'death_index' not in farm_info else farm_info['death_index']

    for pid in range(0,pool_length):
        if pid in death_index:
            continue
        else:
            calls.append(Call(farm_info['masterChef'], [f"{farm_info['want']}(uint256)(address)" if 'want' in farm_info else f'poolInfo(uint256)(address)', pid], [[f'{pid}_want', None]]))
            calls.append(Call(farm_info['masterChef'], [f"{farm_info['pool_alloc']}" if 'pool_alloc' in farm_info else f'poolInfo(uint256)((address,uint256,uint256,uint256))', pid], [[f'{pid}_alloc', parsers.parse_wanted_offset, farm_info['alloc_offset'] if 'alloc_offset' in farm_info else 1]]))

    stakes=await Multicall(calls, web_3)()
    balances = await Multicall([Call(stakes[f'{x}_want'], ['balanceOf(address)(uint256)', farm_info['masterChef']], [[f'{x}_balance', None]]) for x in range(0,pool_length) if f'{x}_want' in stakes], web_3)()

    pools = []

    for pool in range(0,pool_length):
        if f'{pool}_want' in stakes:
            want_token = stakes[f'{pool}_want']
            found_token = await collection.find_one({'tokenID' : want_token, 'network' : farm_info['network']}, {'_id': False})

            if not found_token:
                found_token = await token_router(want_token, None, farm_info['network'])
                collection.update_one({'tokenID' : want_token, 'network' : farm_info['network']}, { "$set": found_token }, upsert=True)

            pools.append({
                'hash' : '',
                'name' : f"{found_token['tkn0s']}-{found_token['tkn1s']}" if 'tkn1s' in found_token else found_token['tkn0s'],
                'address' : want_token,
                'lp_token_address' : want_token,
                'farm' : '',
                'master' : farm_info['masterChef'],
                'pool_id' : pool,
                'rewards' : [],
                'staking' : [found_token['token0'], found_token['token1']] if 'tkn1s' in found_token else [found_token['token0']],
                'decimals_staking' : [found_token['tkn0d'], found_token['tkn1d']] if 'tkn1s' in found_token else [found_token['tkn0d']],
                'decimals_rewards' : [],
                'allocation_point' : stakes[f'{pool}_alloc'],
                'rewards_multiplier' : stakes[f'{pool}_alloc'] / stakes[f"{farm_info['masterChef']}_points"],
                'apy' : 0,
                'risk' : 0,
                'stable_only' : False,
                'tvl' : balances[f'{pool}_balance'],
                'ad' : False,
                'chain' : WEB3_NETWORKS[farm_info['network']]['id']
            })


    return {
        'farm_id' : '',
        'total_allocation' : stakes[f"{farm_info['masterChef']}_points"],
        'reward_per_block' : stakes[f"{farm_info['masterChef']}_block"],
        'pools' : pools
    }
