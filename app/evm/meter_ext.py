from .multicall import Call, Multicall, parsers
from .networks import WEB3_NETWORKS
from web3 import Web3
from .thegraph import call_graph
from .utils import make_get
from .bitquery.voltswap import geysers_tvl
from .find_token_type import token_router
from .oracles import list_router_prices
import json

def get_lp_balances(staked, totalSupply, reserves, token0, tkn0d, tkn1d, prices):

    quotePrice = prices[token0.lower()]
    userPct = staked / totalSupply
    lp1val = (userPct * int(reserves[0])) / (10**tkn0d)
    lp2val = (userPct * int(reserves[1])) / (10**tkn1d)

    return (lp1val * quotePrice) * 2


async def get_voltswap_llama(mongodb, session, network):

    graph_urls = {'meter' : 'https://newgraph.voltswap.finance/subgraphs/name/meter/geyser-v2', 'theta' : 'https://geyser-graph-on-theta.voltswap.finance/subgraphs/name/theta/geyser-v2'}

    geyser_data = await call_graph(graph_urls[network], {'operationName' : 'getGeysers', 'query' : geysers_tvl}, session)

    collection = mongodb.xtracker['full_tokens']
    lp_calls = []


    for i,x in enumerate(geyser_data['data']['geysers']):
        found_token = await collection.find_one({'tokenID' : x['stakingToken'], 'network' : network}, {'_id': False})

        if found_token:
            geyser_data['data']['geysers'][i].update(found_token)
        else:
            found_token = await token_router(x['stakingToken'], None, network)
            geyser_data['data']['geysers'][i].update(found_token)
            collection.update_one({'tokenID' : x['stakingToken'], 'network' : network}, { "$set": found_token }, upsert=True)
        
        if 'lpToken' in found_token:
            lp_calls.append(Call(x['stakingToken'], 'totalSupply()(uint256)', [[f'{x["stakingToken"]}_totalSupply', parsers.from_wei]]))
            lp_calls.append(Call(x['stakingToken'], 'getReserves()((uint112,uint112))', [[f'{x["stakingToken"]}_reserves', parsers.parseReserves]]))

    lp_metadata = await Multicall(lp_calls, WEB3_NETWORKS[network])()

    token_prices = await list_router_prices([{'token' : x['token0'], 'decimal' : x['tkn0d']} for x in geyser_data['data']['geysers']], network)

    total_usd = 0

    for i,x in enumerate(geyser_data['data']['geysers']):

        if x['type'] == 'lp':
            geyser_data['data']['geysers'][i]['totalSupply'] = lp_metadata[f'{x["stakingToken"]}_totalSupply']
            geyser_data['data']['geysers'][i]['reserves'] = lp_metadata[f'{x["stakingToken"]}_reserves']

            geyser_data['data']['geysers'][i]['totalUSD'] = get_lp_balances(parsers.from_custom(int(x['totalStake']), 18), x['totalSupply'], x['reserves'], x['token0'], x['tkn0d'], x['tkn1d'], token_prices)
            total_usd += geyser_data['data']['geysers'][i]['totalUSD']
        else:
            geyser_data['data']['geysers'][i]['totalUSD'] = parsers.from_custom(int(x['totalStake']), x['tkn0d']) * token_prices[x["stakingToken"].lower()]
            total_usd += geyser_data['data']['geysers'][i]['totalUSD']
            
    geyser_data['data']['totalUSD'] = total_usd 

    return geyser_data

async def get_passport_llama(mongodb, session):

    NETWORK_DATA = {
        'eth' : {
            'handler' : '0xde4fC7C3C5E7bE3F16506FcC790a8D93f8Ca0b40',
            'token_list' : 'Ethereum',
            'ampl_contract' : ''
        },
        'meter' : {
            'handler' : '0x60f1ABAa3ED8A573c91C65A5b82AeC4BF35b77b8',
            'token_list' : 'Meter',
            'ampl_contract' : ''
        },
        'bsc' : {
            'handler' : '0x5945241BBB68B4454bB67Bd2B069e74C09AC3D51',
            'token_list' : 'BSC',
            'ampl_contract' : ''
        },
        'moon' : {
            'handler' : '0x48A6fd66512D45006FC0426576c264D03Dfda304',
            'token_list' : 'Moonriver',
            'ampl_contract' : ''
        },
        'avax' : {
            'handler' : '0x48A6fd66512D45006FC0426576c264D03Dfda304',
            'token_list' : 'Avalanche',
            'ampl_contract' : ''
        },
        'polis' : {
            'handler' : '0x911F32FD5d347b4EEB61fDb80d9F1063Be1E78E6',
            'token_list' : 'Polis',
            'ampl_contract' : ''
        },
        'theta' : {
            'handler' : '0x48A6fd66512D45006FC0426576c264D03Dfda304',
            'token_list' : 'Theta',
            'ampl_contract' : ''
        },
    }

    passport_tokens = json.loads(await make_get(session, 'https://raw.githubusercontent.com/meterio/token-list/master/generated/passport-tokens.json'))

    calls = []
    r = {}
    grand_total = 0

    for network in NETWORK_DATA:
        network_total = 0
        r[network] = { 'tokens' : [] }
        r[network]['handler'] = NETWORK_DATA[network]['handler']
        for token in passport_tokens[NETWORK_DATA[network]['token_list']]:
            if NETWORK_DATA[network]['handler']:
                calls.append(Call(token['address'], ['balanceOf(address)(uint256)', NETWORK_DATA[network]['handler']], [[f'{token["address"]}_{token["decimals"]}_{token["symbol"]}', parsers.from_custom, token["decimals"]]]))

        token_balances = await Multicall(calls, WEB3_NETWORKS[network])()
        calls = []

        token_prices = await list_router_prices([{'token' : x.split("_")[0].lower(), 'decimal' : int(x.split("_")[1])} for x in token_balances if token_balances[x]], network)

        for x in token_balances:
            if token_balances[x] > 0:
                token_address = x.split("_")[0].lower()
                token_decimal = x.split("_")[1]
                token_symbol = x.split("_")[2]

                network_total += token_balances[x] * token_prices[token_address]
                grand_total += token_balances[x] * token_prices[token_address]
                r[network]['tokens'].append({'token' : token_address, 'balance' : token_balances[x], 'totalUSD' : token_balances[x] * token_prices[token_address], 'symbol' : token_symbol, 'price' : token_prices[token_address]})
        
        r[network]['totalUSD'] = network_total

    
    r['grandTotal'] = grand_total

    return r

    # total_usd = 0

    # for i,x in enumerate(geyser_data['data']['geysers']):

    #     if x['type'] == 'lp':
    #         geyser_data['data']['geysers'][i]['totalSupply'] = lp_metadata[f'{x["stakingToken"]}_totalSupply']
    #         geyser_data['data']['geysers'][i]['reserves'] = lp_metadata[f'{x["stakingToken"]}_reserves']

    #         geyser_data['data']['geysers'][i]['totalUSD'] = get_lp_balances(parsers.from_custom(int(x['totalStake']), 18), x['totalSupply'], x['reserves'], x['token0'], x['tkn0d'], x['tkn1d'], token_prices)
    #         total_usd += geyser_data['data']['geysers'][i]['totalUSD']
    #     else:
    #         geyser_data['data']['geysers'][i]['totalUSD'] = parsers.from_custom(int(x['totalStake']), x['tkn0d']) * token_prices[x["stakingToken"].lower()]
    #         total_usd += geyser_data['data']['geysers'][i]['totalUSD']
            
    # geyser_data['data']['totalUSD'] = total_usd 

    # return geyser_data