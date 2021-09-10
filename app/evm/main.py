from .farms import Farms
from . import external_contracts
from . import farm_templates
from . import oracles
from .price_override import tokens as otkn
from .find_token_type import get_token_data, token_list_from_stakes
from .calculator import calculate_prices
from . import routers
import asyncio

INCH_SUPPORTED = ['bsc','matic','eth']

def return_farms_list():
    x = Farms()
    return x.farms

async def get_evm_positions(wallet, farm_id, mongo_db, http_session):
    set_farms = Farms(wallet, farm_id)
    farm_configuraiton = set_farms.farms[farm_id]
    farm_network = farm_configuraiton['network']
    masterchef_pool_list = [farm_id] + farm_configuraiton['add_chefs'] if 'add_chefs' in farm_configuraiton else [farm_id]
    args = {'wallet' : wallet}
    returned_object = ({},{farm_id : {'name' : farm_configuraiton['name'], 'network' : farm_configuraiton['network'], 'wallet' : wallet, 'userData' : {}}})

    if farm_configuraiton['stakedFunction'] is not None:
        masterchef = await farm_templates.get_traditional_masterchef(wallet, masterchef_pool_list, farm_network, set_farms.farms, returned_object[1])
        if masterchef is not None:
            returned_object[0].update(masterchef[0])
            returned_object[1][farm_id]['userData'].update(masterchef[1][farm_id]['userData'])
    if 'extraFunctions' in farm_configuraiton:
        
        if farm_configuraiton['extraFunctions']['vaults'] is not None:
            vaults = await asyncio.gather(*[v(session=http_session, **farm_configuraiton['extraFunctions']['vault_args'][i]) for i, v in enumerate(farm_configuraiton['extraFunctions']['vaults'])])

        farm_infos = await asyncio.gather(*[f(vaults=vaults[i], **{**farm_configuraiton['extraFunctions']['args'][i], **args}) for i, f in enumerate(farm_configuraiton['extraFunctions']['functions'])])

        for farm_info in farm_infos:
            if farm_info is not None:
                returned_object[0].update(farm_info[0])
                returned_object[1][farm_id]['userData'].update(farm_info[1][farm_id]['userData'])

    if len(returned_object[0]) < 1:
        return {}

    build_meta_data = await get_token_data(returned_object, mongo_db, farm_configuraiton['network'])

    token_list = token_list_from_stakes(build_meta_data, farm_configuraiton)

    prices = await oracles.list_router_prices(token_list, farm_network)

    # if farm_configuraiton['network'] in INCH_SUPPORTED:
    #     prices = await oracles.list_router_prices(token_list, farm_network)
    # elif farm_configuraiton['network'] == 'avax':
    #     prices = await oracles.avax_router_prices(token_list, ['PNG', 'JOE', 'SUSHI'])
    # elif farm_configuraiton['network'] == 'ftm':
    #     prices = await oracles.fantom_router_prices(token_list, ['SPOOKY', 'HYPER', 'SPIRIT', 'WAKA', 'PAINT'])
    # elif farm_configuraiton['network'] == 'oke':
    #     prices = await oracles.oke_router_prices(token_list, ['PANDA', 'CHERRY', 'KSWAP'])
    # elif farm_configuraiton['network'] == 'kcc':
    #     prices = await oracles.kcc_router_prices(token_list, ['KUSWAP', 'KOFFEE', 'KANDY', 'BONE'])

    # print(token_list)
    # price_overrides = await asyncio.gather(*[otkn[v['token']][0](**otkn[v['token']][1]) for i, v in enumerate(token_list) if v['token'] in otkn])

    # for each in price_overrides:
    #     prices.update(each)

    response = await calculate_prices(build_meta_data, prices, farm_configuraiton, wallet)

    return response




