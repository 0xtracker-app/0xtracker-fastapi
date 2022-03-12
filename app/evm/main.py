from .farms import Farms
from .networks import WEB3_NETWORKS
from . import external_contracts
from . import farm_templates
from . import oracles
import datetime
from .price_override import TokenOverride
from .find_token_type import get_token_data, token_list_from_stakes
from .calculator import calculate_prices
from . import routers
import asyncio
from eth_account.messages import encode_defunct
from web3.auto import w3
from ..db.crud import delete_user_history

INCH_SUPPORTED = ['bsc','matic','eth']

def return_farms_list():
    evm = Farms()
    return evm.farms

def return_apy_list(parser=None):
    evm = Farms()

    if parser == 'master':
        return [{'sendValue' : evm.farms[x]['masterChef'], 'name' : evm.farms[x]['name'], 'network': WEB3_NETWORKS[evm.farms[x]['network']]['id'], 'featured' : evm.farms[x]['featured']} for x in evm.farms if evm.farms[x].get('stakedFunction') not in [None, 'stakedWantTokens']]
    elif parser == None:
        return [{'sendValue' : evm.farms[x]['masterChef'], 'name' : evm.farms[x]['name'], 'network': WEB3_NETWORKS[evm.farms[x]['network']]['id'], 'featured' : evm.farms[x]['featured']} for x in evm.farms]

async def get_evm_positions(wallet, farm_id, mongo_db, http_session, client, pdb):
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

    otkn = TokenOverride(http_session).tokens
    price_overrides = await asyncio.gather(*[otkn[v['token']][0](**otkn[v['token']][1]) for i, v in enumerate(token_list) if v['token'] in otkn])

    for each in price_overrides:
        prices.update(each)

    response = await calculate_prices(build_meta_data, prices, farm_configuraiton, wallet, mongo_db, pdb)

    return response

async def delete_user_records(wallet, signature, timestamps, mongo_db, pdb):
    message = encode_defunct(text='I authorize deletion of these records.')
    recovered_address = w3.eth.account.recover_message(message, signature=signature)

    if recovered_address == wallet:
        for each in timestamps:
            start = datetime.datetime.strptime(each, "%Y-%m-%dT%H:%M:%S")
            end = start + datetime.timedelta(minutes=59, seconds=59)
            print(type(start))
            delete_user_history(pdb, wallet.lower(), start, end)
    #         deletions = await mongo_db.xtracker['user_data'].delete_many({ 
    #     "$and" : [
    #         { 
    #             "wallet" : wallet.lower()
    #         }, 
    #         { 
    #             "timeStamp" : { 
    #                 "$gte" : gte
    #             }
    #         }, 
    #         { 
    #             "timeStamp" : { 
    #                 "$lte" : gte + (60 * 60) - 1
    #             }
    #         }
    #     ]
    # })

        return {'message' : 'Deletion Succesfull'}
    else:
        return {'message' : 'Signature does not match wallet.'}



