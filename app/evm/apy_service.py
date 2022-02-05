from .farms import Farms
from .networks import WEB3_NETWORKS
from .multicall import Call, Multicall, parsers

class Pools:
    def __init__(self, wallet=None, selected_farm=None):
        self.wallet

async def get_protocol_apy(farm_id, mongo_db, http_session):
    farm_info = Farms().farms[farm_id]
    calls = []
    web_3 = WEB3_NETWORKS[farm_info['network']]
    
    pool_length = await Call(farm_info['masterChef'], [farm_info['pool_length'] if 'pool_length' in farm_info else f'poolLength()(uint256)'],None,web_3)() 

    calls.append(Call(farm_info['masterChef'], [f"{farm_info['total_alloc']}()(uint256)" if 'total_alloc' in farm_info else f'totalAllocPoint()(uint256)'], [[f'{farm_info["masterChef"]}_points', None]]))
    calls.append(Call(farm_info['masterChef'], [f"{farm_info['total_alloc']}()(uint256)"], [[f'{farm_info["masterChef"]}_block', None]]))

    death_index = [] if 'death_index' not in farm_info else farm_info['death_index']

    for pid in range(0,pool_length):
        if pid in death_index:
            continue
        else:
            calls.append(Call(farm_info['masterChef'], [f"{farm_info['total_alloc']}()(uint256)" if 'total_alloc' in farm_info else f'poolInfo(uint256)(address)', pid], [[f'{pid}ext_want', None]]))
            calls.append(Call(farm_info['masterChef'], [f"{farm_info['total_alloc']}()(uint256)" if 'total_alloc' in farm_info else f'poolInfo(uint256)(address,uint256,uint256,uint256)', pid], [[f'{pid}ext_rewarder', None]]))

    stakes=await Multicall(calls, web_3)()

    print(stakes)
