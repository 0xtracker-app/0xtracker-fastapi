from math import cos
from .networks import CosmosNetwork
from . import queries
from . import oracles
from . import helpers
from .calculator import calculate_prices
from .token_lookup import TokenMetaData
from .farms import Farms
from .networks import CosmosNetwork
import asyncio
import time

def return_farms_list():
    cosmos = Farms()
    return cosmos.farms

async def get_wallet_balances(wallet, session, mongo_client):
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks

    balances = await asyncio.gather(*[queries.get_bank_balances(network, net_config[network], session) for network in net_config])
    traces =  await asyncio.gather(*[queries.get_ibc_tokens(net_config[network['network']], session) for network in balances])
    prices = await oracles.cosmostation_prices(session, mongo_client)
    transform_trace = helpers.transform_trace_routes(traces)

    return_wallets = []
    total_balance = 0
    for i, balance in enumerate(balances):
        token_network = list(net_config.keys())[i]
        if balance['tokens']:
            for token in balance['tokens']:
                token_denom = transform_trace[0][token['denom']] if token['denom'] in transform_trace[0] else token['denom']
                token_metadata = await TokenMetaData(address=token_denom, mongodb=mongo_client, network=net_config[token_network], session=session).lookup()
                if token_metadata:
                    token_decimal = token_metadata['tkn0d']
                else:
                    token_decimal = transform_trace[1][token_denom]['decimal'] if token_denom in transform_trace[1] else 6
                token_price = 0 if token_denom not in prices else prices[token_denom]

                total_balance += token_price * helpers.from_custom(token['amount'], token_decimal)
                return_wallets.append(
                    {
                        "token_address": token['denom'],
                        "symbol": transform_trace[1][token_denom]['display_denom'] if token_denom in transform_trace[1] else token_denom.upper(),
                        "tokenBalance": helpers.from_custom(token['amount'], token_decimal),
                        "tokenPrice": token_price,
                        "wallet" : balance['wallet'],
                        'network' : 'cosmos'
                    }
                    )

    if total_balance > 0:
        mongo_client.xtracker['user_data'].update_one({'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farm_network' : 'cosmos'}, { "$set": {'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farmNetwork' : 'cosmos', 'dollarValue' : total_balance} }, upsert=True)

    return return_wallets

async def get_cosmos_positions(wallet, farm_id, mongo_db, http_session):
    set_farms = Farms(wallet, farm_id)
    farm_configuraiton = set_farms.farms[farm_id]
    
    args = {'wallet' : wallet}
    returned_object = ({},{farm_id : {'name' : farm_configuraiton['name'], 'network' : farm_configuraiton['network'], 'wallet' : wallet, 'userData' : {}}})

    if 'extraFunctions' in farm_configuraiton:
        
        if farm_configuraiton['extraFunctions']['vaults'] is not None:
            vaults = await asyncio.gather(*[v(session=http_session, **farm_configuraiton['extraFunctions']['vault_args'][i]) for i, v in enumerate(farm_configuraiton['extraFunctions']['vaults'])])

        farm_infos = await asyncio.gather(*[f(vaults=vaults[i], session=http_session, mongodb=mongo_db, **{**farm_configuraiton['extraFunctions']['args'][i], **args}) for i, f in enumerate(farm_configuraiton['extraFunctions']['functions'])])

        for farm_info in farm_infos:
            if farm_info is not None:
                returned_object[0].update(farm_info[0])
                returned_object[1][farm_id]['userData'].update(farm_info[1][farm_id]['userData'])

    if len(returned_object[0]) < 1:
        return {}

    prices = await oracles.cosmostation_prices(http_session, mongo_db)

    response = await calculate_prices(returned_object[1], prices, CosmosNetwork(wallet).all_networks['cosmos']['wallet'], mongo_db)

    return response

async def write_tokens(wallet, mongo_db, session):
    # wallet = f'ibc/{wallet}'
    # x = await TokenMetaData(address=wallet, mongodb=mongo_db).lookup()
    # cosmos = CosmosNetwork(wallet)
    # net_config = cosmos.all_networks

    # traces =  await asyncio.gather(*[queries.get_ibc_tokens(net_config[network], session) for network in net_config])
    # # prices = await oracles.cosmostation_prices(session)
    # transform_trace = helpers.transform_trace_routes(traces)

    trace_views = mongo_db.xtracker['cosmos_routes_view']
    denom_database = mongo_db.xtracker['cosmos_tokens']

    # for i, network in enumerate(traces):

    #     if 'ibc_tokens' in network:
    #         for token in network['ibc_tokens']:
    #             token_data = {'hash' : f'ibc/{token["hash"]}', 'base_denom' : token['base_denom'], 'chain_id' : token['counter_party']['chain_id']}
    #             await trace_database.update_one({'hash' : f'ibc/{token["hash"]}', 'base_denom' : token['base_denom'], 'chain_id' : token['counter_party']['chain_id']},{ "$set": token_data }, upsert=True)

    full_dict = trace_views.find({},{'_id': False})        
    for x in await full_dict.to_list(length=None):
        if x['meta_data']:
            record = x['meta_data'][0]
            record['tokenID'] = x['hash']
            del record['_id']      
            await denom_database.update_one({'tokenID' : x['hash']},{ "$set": record }, upsert=True)