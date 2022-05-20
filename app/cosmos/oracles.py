import os
from ..redis.cache import cache_function
from .utils import make_get_json
from .token_lookup import TokenMetaData
import time
from . import queries
from .helpers import from_custom

CONTRACTS_TTL = os.getenv("CACHE_TTL_CONTRACTS", 86400)

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
            'juno1cl2ewl842wcnagz5psd68z4dpp4gfxrrm9atm807uvyyg235h85stg7awy' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno1cl2ewl842wcnagz5psd68z4dpp4gfxrrm9atm807uvyyg235h85stg7awy', 'swap_address' : 'juno14nak8v6xeawstrq7r7qmpa67qqfc9xzzymfdfpnp0luycv8knyuq5a6w2m', 'session' : session}],
            'juno1t8dnpktypue65q0hjz7tr3cvqypgj5vkxhd2twvng4a2ywa3j25spjuk6z' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno1t8dnpktypue65q0hjz7tr3cvqypgj5vkxhd2twvng4a2ywa3j25spjuk6z', 'swap_address' : 'juno1enl842z00cklnathpv8f3t3w2u70dkrq22crz3gxg38we7xjfq5s8lktmg', 'session' : session}],
            'juno1p32te9zfhd99ehpxfd06hka6hc9p7tv5kyl5909mzedg5klze09qrg08ry' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno1p32te9zfhd99ehpxfd06hka6hc9p7tv5kyl5909mzedg5klze09qrg08ry', 'swap_address' : 'juno14p3wvpeezqueenfu9jy29s96xuk0hp38k5d5k4ysyzk789v032sqp8uvh3', 'session' : session}],
            'juno1gzys54drag6753qq75mkt3yhjwyv4rp698kfvesh0wcy5737z4tsn0chtm' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno1gzys54drag6753qq75mkt3yhjwyv4rp698kfvesh0wcy5737z4tsn0chtm', 'swap_address' : 'juno1fzl79pekf8wtd0y37q92dmz5h9dxtfpl97w3kguyc59m7ufnlzvsf46vf8', 'session' : session}],
            'juno1vaeuky9hqacenay9nmuualugvv54tdhyt2wsvhnjasx9s946hhmqaq3kh7' : [get_price_from_junoswap, { 'decimal' : 10, 'token_in' : 'juno1vaeuky9hqacenay9nmuualugvv54tdhyt2wsvhnjasx9s946hhmqaq3kh7', 'swap_address' : 'juno19859m5x8kgepwafc3h0n36kz545ngc2vlqnqxx7gx3t2kguv6fws93cu25', 'session' : session}],
            'juno15u3dt79t6sxxa3x3kpkhzsy56edaa5a66wvt3kxmukqjz2sx0hes5sn38g' : [get_price_from_junoswap, { 'decimal' : 6, 'token_in' : 'juno15u3dt79t6sxxa3x3kpkhzsy56edaa5a66wvt3kxmukqjz2sx0hes5sn38g', 'swap_address' : 'juno124d0zymrkdxv72ccyuqrquur8dkesmxmx2unfn7dej95yqx5yn8s70x3yj', 'session' : session}],
            'ubcre' : [get_crescent_pricing, {'session' : session, 'denom' : 'ubcre'}],
            'ucre' : [get_crescent_pricing, {'session' : session, 'denom' : 'ucre'}],
}

@cache_function(ttl=10800, keyparams=[])
async def juno_usd_cg(session):
    return await make_get_json(session, 'https://api.coingecko.com/api/v3/simple/price?ids=juno-network&vs_currencies=usd')

async def get_price_from_junoswap(token_in, session, swap_address, decimal, native=True):
    if native:
        juno_price = await juno_usd_cg(session)
    else:
        juno_price =  {"juno-network":{"usd": 1}}

    token_price = await queries.query_contract_state(session, 'https://rpc-juno.itastakers.com', swap_address, {"token2_for_token1_price":{"token2_amount":str(1 * 10 ** decimal)}})

    return {token_in : juno_price['juno-network']['usd'] * from_custom(int(token_price['token1_amount']), 6)}

async def get_price_from_crescent(token_in, session, token_out, native=True):
    if native:
        native_price = await make_get_json(session, f'https://crescent-api.polkachu.com/crescent/liquidity/v1beta1/pairs?denoms=ubcre&denoms=ibc%2F6F4968A73F90CF7DE6394BF937D6DF7C7D162D74D839C13F53B41157D315E05F')
    else:
        native_price = {'pairs' : [{'last_price': '1.0'}]}

    token_price = await make_get_json(session, f'https://crescent-api.polkachu.com/crescent/liquidity/v1beta1/pairs?denoms={token_in}&denoms={token_out}')

    return {token_in : float(native_price['pairs'][0]['last_price']) * float(token_price['pairs'][0]['last_price'])}

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

@cache_function(ttl=CONTRACTS_TTL, keyparams=[])
async def check_osmosis_pricing(session, mongo_db, network_data):
    r = await make_get_json(session, 'https://api-osmosis.imperator.co/tokens/v2/all')
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

@cache_function(ttl=CONTRACTS_TTL, keyparams=[])
async def check_sif_pricing(session, network_data):
    r = await make_get_json(session, 'https://data.sifchain.finance/beta/asset/tokenStats')
    sif_prices = {}

    if 'body' in r:
        for each in r['body']['pools']:
            sif_prices[f'c{each["symbol"]}'] = each["priceToken"]

    return sif_prices

async def get_crescent_pricing(session, denom):
    r = await make_get_json(session, 'https://apigw.crescent.network/asset/live')

    if 'data' in r:
        for each in r['data']:
            if each['denom'] == denom:
                token_price = each['priceOracle']

    return { denom : token_price }