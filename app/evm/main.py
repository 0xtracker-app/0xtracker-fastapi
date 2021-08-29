from .farms import farms
from . import external_contracts
from . import farm_templates
from .oracles import get_one_inch_quote
from .find_token_type import get_token_data, token_list_from_stakes
from .calculator import calculate_prices
import asyncio

def return_farms_list():
    return farms

async def get_evm_positions(wallet, farm_id, mongo_db, http_session):
    farm_configuraiton = farms[farm_id]
    farm_network = farm_configuraiton['network']
    masterchef_pool_list = [farm_id]
    args = {'wallet' : wallet}
    returned_object = ({},{farm_id : {'name' : farm_configuraiton['name'], 'network' : farm_configuraiton['network'], 'wallet' : wallet, 'userData' : {}}})

    if farm_configuraiton['stakedFunction'] is not None:
        masterchef = await farm_templates.get_traditional_masterchef(wallet, masterchef_pool_list, farm_network, farm_configuraiton, returned_object[1])
        if masterchef is not None:
            returned_object[0].update(masterchef[0])
            returned_object[1][farm_id]['userData'].update(masterchef[1][farm_id]['userData'])
    if 'extraFunctions' in farm_configuraiton:

        if farm_configuraiton['extraFunctions']['vaults'] is not None:
            vaults = await asyncio.gather(*[v(session=http_session) for v in farm_configuraiton['extraFunctions']['vaults']])
        
        # if farm_configuraiton['extraFunctions']['args'] is not None:
        #     args.update(farm_configuraiton['extraFunctions']['args'])
        
        farm_infos = await asyncio.gather(*[f(vaults=vaults[i], **{**farm_configuraiton['extraFunctions']['args'][i], **args}) for i, f in enumerate(farm_configuraiton['extraFunctions']['functions'])])
 
        for farm_info in farm_infos:
            if farm_info is not None:
                returned_object[0].update(farm_info[0])
                returned_object[1][farm_id]['userData'].update(farm_info[1][farm_id]['userData'])

    if len(returned_object[0]) < 1:
        return {}

    build_meta_data = await get_token_data(returned_object, mongo_db)

    prices = await get_one_inch_quote(token_list_from_stakes(build_meta_data), http_session)

    response = await calculate_prices(build_meta_data, prices, farm_configuraiton, wallet)

    return response



