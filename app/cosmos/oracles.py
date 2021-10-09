from .utils import make_get_json
import time

async def cosmostation_prices(session):
    r = await make_get_json(session, 'https://api-utility.cosmostation.io/v1/market/prices')

    dict_of_prices = {x['denom'] : x['prices'][0]['current_price'] for x in r if x['prices'][0]['currency'] == 'usd'}
    juno_price = await get_juno_price(session)
    dict_of_prices['ujuno'] = juno_price
    return dict_of_prices

async def get_juno_price(session):
    current_time = time.time()
    r = await make_get_json(session, f'https://monitor.bronbro.io/api/datasources/proxy/7/api/v1/query_range?query=Juno_PRICE_total%7B%7D&start={current_time}&end={current_time}&step=15')
    current_price = float(r['data']['result'][0]['values'][0][1])
    return current_price