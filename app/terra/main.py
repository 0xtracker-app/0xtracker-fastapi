from redis.cache import cache_function
from .farms import Farms
import asyncio
import time
from . import utils
from .helpers import from_custom, token_list_from_stakes
from .token_lookup import TokenMetaData
from .queries import get_luna_price
from .oracles import get_price_from_pool, TokenOverride
from .calculator import calculate_prices
import os
from ..db.schemas import UserRecord
from ..db.crud import create_user_history
from datetime import datetime, timezone

def return_farms_list():
    terra = Farms()
    return terra.farms

@cache_function(keyparams=2)
async def get_wallet_balances(wallet, mongo_client, session, client, pdb):
    user_balance = await client.bank.balance(wallet)
    cw_tokens = await mongo_client.xtracker['terra_tokens'].find({"type" : "single", "$expr": { "$gt": [ { "$strLenCP": "$token0" }, 6 ] }}, {'_id': False}).to_list(length=None)
    cw_token_balances =  await asyncio.gather(*[client.wasm.contract_query(token['tokenID'], {"balance":{"address": wallet}}) for token in cw_tokens])
    luna_price = await get_luna_price(client)
    skip_tokens = ['terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu']

    return_wallets = []
    total_balance = 0
    
    for i,balance in enumerate(cw_token_balances):
        if int(balance['balance']) > 0 and cw_tokens[i]['tokenID'] not in skip_tokens:
            token_metadata = await TokenMetaData(cw_tokens[i]['tokenID'], mongo_client, client, session).lookup()
            token_price = await get_price_from_pool(token_metadata['token0'], token_metadata['tkn0d'], client, mongo_client, {}, luna_price)
            total_balance += token_price * from_custom(int(balance['balance']), token_metadata['tkn0d'])

            return_wallets.append(
                {
                    "token_address": token_metadata['token0'],
                    "symbol": token_metadata['tkn0s'],
                    "tokenBalance": from_custom(int(balance['balance']), token_metadata['tkn0d']),
                    "tokenPrice": token_price,
                    "wallet" : wallet,
                    'network' : 'terra'
                }
                )

    for balance in user_balance.to_list():
        if balance.amount > 0:
            token_metadata = await TokenMetaData(balance.denom, mongo_client, client, session).lookup()
            token_price = await get_price_from_pool(token_metadata['token0'], token_metadata['tkn0d'], client, mongo_client, {}, luna_price)
            total_balance += token_price * from_custom(balance.amount, token_metadata['tkn0d'])

            return_wallets.append(
                {
                    "token_address": token_metadata['token0'],
                    "symbol": token_metadata['tkn0s'],
                    "tokenBalance": from_custom(balance.amount, token_metadata['tkn0d']),
                    "tokenPrice": token_price,
                    "wallet" : wallet,
                    'network' : 'terra'
                }
                )

    if total_balance > 0 and os.getenv('USER_WRITE', 'True') == 'True':
        #mongo_client.xtracker['user_data'].update_one({'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farm_network' : 'terra'}, { "$set": {'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : 'wallet', 'farmNetwork' : 'terra', 'dollarValue' : total_balance} }, upsert=True)
        create_user_history(pdb, UserRecord(timestamp=datetime.fromtimestamp(int(time.time()), tz=timezone.utc), farm='wallet', farm_network='terra', wallet=wallet.lower(), dollarvalue=total_balance, farmnetwork='terra' ))

    return return_wallets

@cache_function(keyparams=2)
async def get_terra_positions(wallet, farm_id, mongo_db, http_session, lcd_client, pdb):
    set_farms = Farms(wallet, farm_id)
    farm_configuraiton = set_farms.farms[farm_id]
    
    args = {'wallet' : wallet}
    returned_object = ({},{farm_id : {'name' : farm_configuraiton['name'], 'network' : farm_configuraiton['network'], 'wallet' : wallet, 'userData' : {}}})

    if 'extraFunctions' in farm_configuraiton:
        
        if farm_configuraiton['extraFunctions']['vaults'] is not None:
            vaults = await asyncio.gather(*[v(session=http_session, **farm_configuraiton['extraFunctions']['vault_args'][i]) for i, v in enumerate(farm_configuraiton['extraFunctions']['vaults'])])

        farm_infos = await asyncio.gather(*[f(vaults=vaults[i], session=http_session, mongodb=mongo_db, lcd_client=lcd_client, **{**farm_configuraiton['extraFunctions']['args'][i], **args}) for i, f in enumerate(farm_configuraiton['extraFunctions']['functions'])])

        for farm_info in farm_infos:
            if farm_info is not None:
                returned_object[0].update(farm_info[0])
                returned_object[1][farm_id]['userData'].update(farm_info[1][farm_id]['userData'])

    if len(returned_object[0]) < 1:
        return {}

    luna_price = await get_luna_price(lcd_client)
    token_list = token_list_from_stakes(returned_object[1], farm_configuraiton)
    token_over = TokenOverride(lcd_client).tokens
    
    prices = dict(zip([x['token'] for x in token_list], await asyncio.gather(*[get_price_from_pool(x['token'], x['decimal'], lcd_client, mongo_db, token_over, luna_price) for x in token_list])))

    response = await calculate_prices(returned_object[1], prices, wallet, mongo_db, farm_configuraiton, pdb)

    return response