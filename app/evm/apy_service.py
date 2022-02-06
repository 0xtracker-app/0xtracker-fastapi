from .farms import Farms
from .networks import WEB3_NETWORKS
from .multicall import Call, Multicall, parsers
from .find_token_type import token_router
from hashlib import sha256
from .native_tokens import NetworkRoutes

class Pools:
    def __init__(self, wallet=None, selected_farm=None):
        self.wallet

async def get_protocol_apy(farm_id, mongo_db, http_session):
    farm_info = Farms().farms[farm_id]
    collection = mongo_db.xtracker['full_tokens']
    calls = []
    web_3 = WEB3_NETWORKS[farm_info['network']]
    network_info = NetworkRoutes(farm_info['network'])

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

    stakes=await Multicall(calls, web_3, _strict=False)()

    balance = []
    for x in range(0, pool_length): 
        if stakes.get(f'{x}_want') and str(stakes.get(f'{x}_want') or '') not in [x.lower() for x in network_info.dead]:
            balance.append(Call(stakes[f'{x}_want'], ['balanceOf(address)(uint256)', farm_info['masterChef']], [[f'{x}_balance', None]]))
            balance.append(Call(stakes[f'{x}_want'], ['decimals()(uint8)'], [[f'{x}_decimals', None]]))

    balances = await Multicall(balance, web_3, _strict=False)()

    pools = []

    # print(stakes.get(f"{farm_info['masterChef']}_points"))
    # print(stakes.get(f"{farm_info['masterChef']}_block"))

    if stakes.get(f"{farm_info['masterChef']}_points") is None or stakes.get(f"{farm_info['masterChef']}_block") is None:
        print({'error' : 'Farm failed due to no totalAlloc and rewardPerBlock'})
        return {'error' : 'Farm failed due to no totalAlloc and rewardPerBlock'}

    for pool in range(0,pool_length):
        if f'{pool}_want' in stakes and f'{pool}_balance' in balances:
            want_token = stakes[f'{pool}_want']
            found_token = await collection.find_one({'tokenID' : want_token, 'network' : farm_info['network']}, {'_id': False})

            if not found_token:
                found_token = await token_router(want_token, None, farm_info['network'])
                collection.update_one({'tokenID' : want_token, 'network' : farm_info['network']}, { "$set": found_token }, upsert=True)


            pool_data = {
                'name' : f"{found_token['tkn0s']}-{found_token['tkn1s']}" if 'tkn1s' in found_token else found_token['tkn0s'],
                'address' : want_token,
                'lp_token_address' : want_token,
                'farm' : farm_info['name'],
                'master' : farm_info['masterChef'],
                'pool_id' : pool,
                'rewards' : [farm_info['rewardToken']],
                'staking' : [found_token['token0'], found_token['token1']] if 'tkn1s' in found_token else [found_token['token0']],
                'decimals_staking' : [found_token['tkn0d'], found_token['tkn1d']] if 'tkn1s' in found_token else [found_token['tkn0d']],
                'decimals_rewards' : [farm_info['decimal']],
                'allocation_point' : stakes[f'{pool}_alloc'],
                'rewards_multiplier' : stakes[f'{pool}_alloc'] / stakes[f"{farm_info['masterChef']}_points"],
                'apy' : 0,
                'risk' : 0,
                'stable_only' : False,
                'tvl' : balances[f'{pool}_balance'],
                'ad' : False,
                'chain' : WEB3_NETWORKS[farm_info['network']]['id'],
                'total_yearly_rewards' : [((parsers.from_custom(stakes[f"{farm_info['masterChef']}_block"], farm_info['decimal']) * network_info.bpy) * (stakes[f'{pool}_alloc'] / stakes[f"{farm_info['masterChef']}_points"]))]
            }

            pool_data['hash'] = sha256(f"{pool_data['lp_token_address']},{pool_data['pool_id']},{pool_data['master']},{pool_data['chain']},{pool_data['name']}".lower().encode('utf-8')).hexdigest()
            
            pools.append(pool_data)



    return {
        'farm_id' : '',
        'total_allocation' : stakes[f"{farm_info['masterChef']}_points"],
        'reward_per_block' : parsers.from_custom(stakes[f"{farm_info['masterChef']}_block"], farm_info['decimal']),
        'pools' : pools
    }


async def get_all_protocols(mongo_db, http_session):
    
    for i, farm in enumerate([Farms().farms[farm_id]['masterChef'] for farm_id in Farms().farms if Farms().farms[farm_id]['stakedFunction']]):
        if i >= 1:
            print(f'/////// {i} Running {farm} ............')
            data = await get_protocol_apy(farm, mongo_db, http_session)
