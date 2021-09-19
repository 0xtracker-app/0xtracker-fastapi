from .utils import make_get_json

async def cosmostation_prices(session):
    r = await make_get_json(session, 'https://api-utility.cosmostation.io/v1/market/prices')
    return {x['denom'] : x['prices'][0]['current_price'] for x in r if x['prices'][0]['currency'] == 'usd'}