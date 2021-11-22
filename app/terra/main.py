# from math import cos
# from .networks import CosmosNetwork
# from . import queries
# from . import oracles
# from . import helpers
# from .calculator import calculate_prices
# from .token_lookup import TokenMetaData
# from .farms import Farms
# from .networks import CosmosNetwork
import asyncio
import time
from . import utils
from .helpers import from_custom
from .token_lookup import TokenMetaData
# def return_farms_list():
#     cosmos = Farms()
#     return cosmos.farms

async def get_wallet_balances(wallet, mongo_client, session, client):
    user_balance = await client.bank.balance(wallet)
    cw_tokens = await utils.make_get_json(session, 'https://api.terraswap.io/tokens')
    cw_token_balances =  await asyncio.gather(*[client.wasm.contract_query(token['contract_addr'], {"balance":{"address": wallet}}) for token in cw_tokens])

    # prices = await oracles.cosmostation_prices(session)

    return_wallets = []
    total_balance = 0
    
    for i,balance in enumerate(cw_token_balances):       
        if int(balance['balance']) > 0:
            token_metadata = await TokenMetaData(cw_tokens[i]['contract_addr'], mongo_client, client, session).lookup()
 
            #total_balance += prices[token_denom] * helpers.from_custom(token['amount'], token_decimal)

            return_wallets.append(
                {
                    "token_address": token_metadata['token0'],
                    "symbol": token_metadata['tkn0s'],
                    "tokenBalance": from_custom(int(balance['balance']), token_metadata['tkn0d']),
                    # "tokenPrice": prices[token_denom],
                    "wallet" : wallet,
                    'network' : 'terra'
                }
                )

    for balance in user_balance.to_list():
        if balance.amount > 0:
            token_metadata = await TokenMetaData(balance.denom, mongo_client, client, session).lookup()
     
            #total_balance += prices[token_denom] * helpers.from_custom(token['amount'], token_decimal)

            return_wallets.append(
                {
                    "token_address": token_metadata['token0'],
                    "symbol": token_metadata['tkn0s'],
                    "tokenBalance": from_custom(balance.amount, token_metadata['tkn0d']),
                    # "tokenPrice": prices[token_denom],
                    "wallet" : wallet,
                    'network' : 'terra'
                }
                )

    # if total_balance > 0:
    #     mongo_client.xtracker['user_data'].update_one({'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farm_network' : 'cosmos'}, { "$set": {'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farmNetwork' : 'cosmos', 'dollarValue' : total_balance} }, upsert=True)

    return return_wallets

# async def get_terra_positions(wallet, farm_id, mongo_db, http_session):
#     set_farms = Farms(wallet, farm_id)
#     farm_configuraiton = set_farms.farms[farm_id]
    
#     args = {'wallet' : wallet}
#     returned_object = ({},{farm_id : {'name' : farm_configuraiton['name'], 'network' : farm_configuraiton['network'], 'wallet' : wallet, 'userData' : {}}})

#     if 'extraFunctions' in farm_configuraiton:
        
#         if farm_configuraiton['extraFunctions']['vaults'] is not None:
#             vaults = await asyncio.gather(*[v(session=http_session, **farm_configuraiton['extraFunctions']['vault_args'][i]) for i, v in enumerate(farm_configuraiton['extraFunctions']['vaults'])])

#         farm_infos = await asyncio.gather(*[f(vaults=vaults[i], session=http_session, mongodb=mongo_db, **{**farm_configuraiton['extraFunctions']['args'][i], **args}) for i, f in enumerate(farm_configuraiton['extraFunctions']['functions'])])

#         for farm_info in farm_infos:
#             if farm_info is not None:
#                 returned_object[0].update(farm_info[0])
#                 returned_object[1][farm_id]['userData'].update(farm_info[1][farm_id]['userData'])

#     if len(returned_object[0]) < 1:
#         return {}

#     prices = await oracles.cosmostation_prices(http_session)

#     response = await calculate_prices(returned_object[1], prices, CosmosNetwork(wallet).all_networks['cosmos']['wallet'], mongo_db)

#     return response