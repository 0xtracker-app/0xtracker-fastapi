from .utils import make_get_json
from .token_lookup import TokenMetaData
import time
from . import queries
from .helpers import from_custom

class TokenOverride:

    def __init__(self, session=None):
        self.tokens = {
            'juno168ctmpyppk90d34p3jjy658zf5a5l3w8wk35wht6ccqj4mr0yv8s4j5awr' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno168ctmpyppk90d34p3jjy658zf5a5l3w8wk35wht6ccqj4mr0yv8s4j5awr', 'swap_address' : 'juno1e8n6ch7msks487ecznyeagmzd5ml2pq9tgedqt2u63vra0q0r9mqrjy6ys', 'session' : session}],
            'juno1vn38rzq0wc7zczp4dhy0h5y5kxh2jjzeahwe30c9cc6dw3lkyk5qn5rmfa' : [get_price_from_junoswap, { 'decimal' : 3, 'token_in' : 'juno1vn38rzq0wc7zczp4dhy0h5y5kxh2jjzeahwe30c9cc6dw3lkyk5qn5rmfa', 'swap_address' : 'juno1acs6q36t6qje5k82h5g74plr258y2q90cjf9z4wnktt7caln0mhsx8mt7z', 'session' : session}],
            'juno1wurfx334prlceydmda3aecldn2xh4axhqtly05n8gptgl69ee7msrewg6y' : [get_price_from_junoswap, { 'decimal' : 3, 'token_in' : 'juno1wurfx334prlceydmda3aecldn2xh4axhqtly05n8gptgl69ee7msrewg6y', 'swap_address' : 'juno133xa84qnue3uy0mj9emvauddxzw554rfl9rr6eadhfau50ws7gvs4ynm79', 'session' : session}],
            'juno1pshrvuw5ng2q4nwcsuceypjkp48d95gmcgjdxlus2ytm4k5kvz2s7t9ldx' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno1pshrvuw5ng2q4nwcsuceypjkp48d95gmcgjdxlus2ytm4k5kvz2s7t9ldx', 'swap_address' : 'juno16zn96yf3vnxengke3vcf6mg9x7qyppgsdh3dnnmvdd8hvtpw58wsrjuu56', 'session' : session}],
            'juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa', 'swap_address' : 'juno1m08vn7klzxh9tmqwajuux202xms2qz3uckle7zvtturcq7vk2yaqpcwxlz', 'session' : session}],
            'juno1g2g7ucurum66d42g8k5twk34yegdq8c82858gz0tq2fc75zy7khssgnhjl' : [get_price_from_junoswap, { 'decimal' : 3, 'token_in' : 'juno1g2g7ucurum66d42g8k5twk34yegdq8c82858gz0tq2fc75zy7khssgnhjl', 'swap_address' : 'juno1cvjuc66rdg34guugmxpz6w59rw6ghrun5m33z3hpvx6q60f40knqglhzzx', 'session' : session}],
            'juno1re3x67ppxap48ygndmrc7har2cnc7tcxtm9nplcas4v0gc3wnmvs3s807z' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno1re3x67ppxap48ygndmrc7har2cnc7tcxtm9nplcas4v0gc3wnmvs3s807z', 'swap_address' : 'juno18nflutunkth2smnh257sxtxn9p5tq6632kqgsw6h0c02wzpnq9rq927heu', 'session' : session}],
}

async def get_price_from_junoswap(token_in, session, swap_address, decimal, native=True):
    if native:
        juno_price = await queries.query_contract_state(session, 'https://rpc-juno.itastakers.com', 'juno1hue3dnrtgf9ly2frnnvf8z5u7e224ctc4hk7wks2xumeu3arj6rs9vgzec', {"token1_for_token2_price":{"token1_amount":"1000000"}})
    else:
        juno_price = {'token2_amount': '1000000'}

    token_price = await queries.query_contract_state(session, 'https://rpc-juno.itastakers.com', swap_address, {"token2_for_token1_price":{"token2_amount":str(1 * 10 ** decimal)}})

    return {token_in : from_custom(int(juno_price['token2_amount']), 6) * from_custom(int(token_price['token1_amount']), 6)}

async def cosmostation_prices(session, mongo_db, network_data):
    r = await make_get_json(session, 'https://serverlessrepo-downloader-bucket-1qsab6s7fy5e1.s3.amazonaws.com/cosmos/prices.json')
    
    if 'message' not in r:
        dict_of_prices = {x['denom'] : x['prices'][0]['current_price'] for x in r if x['prices'][0]['currency'] == 'usd'}
    else:
        dict_of_prices = {}

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