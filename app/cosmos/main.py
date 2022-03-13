from math import cos

from ..redis.cache import cache_function
from .networks import CosmosNetwork
from . import queries
from . import oracles
from . import helpers
from .calculator import calculate_prices
from .token_lookup import TokenMetaData
from .farms import Farms
from .networks import CosmosNetwork
from .oracles import TokenOverride
from .helpers import token_list_from_stakes
import asyncio
import time
import os
from ..db.schemas import UserRecord
from ..db.crud import create_user_history
from datetime import datetime, timezone

def return_farms_list():
    cosmos = Farms()
    return cosmos.farms

def return_network_list():
    return CosmosNetwork('cosmos14m46c90sz30m7y6fnl4ftaraaj8h4uu5p0v7uc').supported_networks

@cache_function(keyparams=1)
async def get_wallet_balances(wallet, session, mongo_client, pdb):
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks
    token_overrides = TokenOverride(session).tokens
    cw20_tokens = ['juno168ctmpyppk90d34p3jjy658zf5a5l3w8wk35wht6ccqj4mr0yv8s4j5awr']
    balances = await asyncio.gather(*[queries.get_bank_balances(network, net_config[network], session) for network in net_config])
    traces =  await asyncio.gather(*[queries.get_ibc_tokens(net_config[network['network']], session) for network in balances])
    prices = await oracles.cosmostation_prices(session, mongo_client, net_config)
    transform_trace = helpers.transform_trace_routes(traces)
    cw20_balances = await asyncio.gather(*[queries.query_contract_state(session, net_config['juno']['rpc'], x, { "balance" : { "address": net_config['juno']['wallet']}}) for x in cw20_tokens])
    print(prices)
    return_wallets = []
    total_balance = 0
    for i, balance in enumerate(balances):
        token_network = list(net_config.keys())[i]
        if balance['tokens']:

            if token_network == 'juno':
                for i, cw in enumerate(cw20_balances):
                    balance['tokens'].append({'denom' : cw20_tokens[i], 'amount' : cw['balance']})

            for token in balance['tokens']:
                token_denom = transform_trace[0][token['denom']] if token['denom'] in transform_trace[0] else token['denom']
                token_metadata = await TokenMetaData(address=token_denom, mongodb=mongo_client, network=net_config[token_network], session=session).lookup()

                if token_metadata:
                    token_decimal = token_metadata['tkn0d']
                    token_symbol = f"{token_metadata['tkn0s']}-{token_metadata['tkn1s']}" if 'tkn1s' in token_metadata else token_metadata['tkn0s']
                else:
                    token_decimal = transform_trace[1][token_denom]['decimal'] if token_denom in transform_trace[1] else 6
                    token_symbol = transform_trace[1][token_denom]['display_denom'] if token_denom in transform_trace[1] else token_denom.upper()
                if token_denom in token_overrides:
                    fetch_price = await token_overrides[token_denom][0](**token_overrides[token_denom][1])
                    token_price = fetch_price[token_denom]
                else:
                    token_price = 0 if token_denom not in prices else prices[token_denom]

                total_balance += token_price * helpers.from_custom(token['amount'], token_decimal)
                return_wallets.append(
                    {
                        "token_address": token['denom'],
                        "symbol": token_symbol,
                        "tokenBalance": helpers.from_custom(token['amount'], token_decimal),
                        "tokenPrice": token_price,
                        "wallet" : balance['wallet'],
                        'network' : 'cosmos'
                    }
                    )

    if total_balance > 0 and os.getenv('USER_WRITE', 'True') == 'True':
        create_user_history(pdb, UserRecord(timestamp=datetime.fromtimestamp(int(time.time()), tz=timezone.utc), farm='wallet', farm_network='cosmos', wallet=wallet.lower(), dollarvalue=total_balance, farmnetwork='cosmos' ))
        #mongo_client.xtracker['user_data'].update_one({'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farm_network' : 'cosmos'}, { "$set": {'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farmNetwork' : 'cosmos', 'dollarValue' : total_balance} }, upsert=True)

    return return_wallets

@cache_function(keyparams=2)
async def get_cosmos_positions(wallet, farm_id, mongo_db, http_session, client, pdb):
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


    token_list = token_list_from_stakes(returned_object[1], farm_configuraiton)
    prices = await oracles.cosmostation_prices(http_session, mongo_db, CosmosNetwork(wallet).all_networks)
    otkn = TokenOverride(http_session).tokens
    
    price_overrides = await asyncio.gather(*[otkn[v['token']][0](**otkn[v['token']][1]) for i, v in enumerate(token_list) if v['token'] in otkn])

    for each in price_overrides:
        prices.update(each)

    response = await calculate_prices(returned_object[1], prices, wallet, mongo_db, pdb)

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