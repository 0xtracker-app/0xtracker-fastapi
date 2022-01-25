from .utils import make_get_json
from .token_lookup import TokenMetaData
import time

async def cosmostation_prices(session, mongo_db, network_data):
    r = await make_get_json(session, 'https://api-utility.cosmostation.io/v1/market/prices')
    dict_of_prices = {x['denom'] : x['prices'][0]['current_price'] for x in r if x['prices'][0]['currency'] == 'usd'}
    osmos_prices = await check_osmosis_pricing(session, mongo_db, network_data)
    sif_prices = await check_sif_pricing(session, network_data)

    for each in osmos_prices:
        if each not in dict_of_prices:
            dict_of_prices[each] = osmos_prices[each]

    for each in sif_prices:
        if each not in dict_of_prices:
            dict_of_prices[each] = sif_prices[each]    

    return dict_of_prices

async def get_juno_price(session):
    current_time = time.time()
    r = await make_get_json(session, f'https://monitor.bronbro.io/api/datasources/proxy/7/api/v1/query_range?query=Juno_PRICE_total%7B%7D&start={current_time}&end={current_time}&step=15')
    current_price = float(r['data']['result'][0]['values'][0][1])
    return current_price

async def check_osmosis_pricing(session, mongo_db, network_data):
    r = await make_get_json(session, 'https://api-osmosis.imperator.co/tokens/v1/all')
    osmo_prices = {}

    for each in r:
        if 'ibc' in each['denom']:
            # if each['denom'] == 'ibc/B9E0A1A524E98BB407D3CED8720EFEFD186002F90C1B1B7964811DD0CCC12228':
            #     denom = 'uhuahua'
            #     osmo_prices[denom] = each['price']
            # else:
                # route = each['denom'].replace('ibc/', '')
                # d = await make_get_json(session, f'https://lcd-osmosis.keplr.app/ibc/applications/transfer/v1beta1/denom_traces/{route}')
                # if 'denom_trace' in d:
                #     denom = d['denom_trace']['base_denom']
                #     osmo_prices[denom] = each['price']
            d = await TokenMetaData(address=each['denom'], mongodb=mongo_db, network=network_data['osmosis'], session=session).lookup()
            if d:
                denom = d['token0']
                osmo_prices[denom] = each['price']
        else:
            osmo_prices[each['denom']] = each['price']

    return osmo_prices


async def check_sif_pricing(session, network_data):
    r = await make_get_json(session, 'https://data.sifchain.finance/beta/asset/tokenStats')
    sif_prices = {}

    if 'body' in r:
        for each in r['body']['pools']:
            sif_prices[f'c{each["symbol"]}'] = each["priceToken"]

    return sif_prices