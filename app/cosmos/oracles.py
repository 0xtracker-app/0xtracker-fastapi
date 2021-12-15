from .utils import make_get_json
import time

async def cosmostation_prices(session):
    r = await make_get_json(session, 'https://api-utility.cosmostation.io/v1/market/prices')
    dict_of_prices = {x['denom'] : x['prices'][0]['current_price'] for x in r if x['prices'][0]['currency'] == 'usd'}
    osmos_prices = await check_osmosis_pricing(session)

    for each in osmos_prices:
        if each not in dict_of_prices:
            dict_of_prices[each] = osmos_prices[each]

    return dict_of_prices

async def get_juno_price(session):
    current_time = time.time()
    r = await make_get_json(session, f'https://monitor.bronbro.io/api/datasources/proxy/7/api/v1/query_range?query=Juno_PRICE_total%7B%7D&start={current_time}&end={current_time}&step=15')
    current_price = float(r['data']['result'][0]['values'][0][1])
    return current_price

async def check_osmosis_pricing(session):
    r = await make_get_json(session, 'https://api-osmosis.imperator.co/tokens/v1/all')
    osmo_prices = {}
    for each in r:
        if 'ibc' in each['denom']:
            route = each['denom'].replace('ibc/', '')
            d = await make_get_json(session, f'https://lcd-osmosis.keplr.app/ibc/applications/transfer/v1beta1/denom_traces/{route}')
            if 'denom_trace' in d:
                denom = d['denom_trace']['base_denom']
                osmo_prices[denom] = each['price']
        else:
            osmo_prices[each['denom']] = each['price']

    return osmo_prices
