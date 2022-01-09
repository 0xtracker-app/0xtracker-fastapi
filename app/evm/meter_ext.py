from .multicall import Call, Multicall, parsers
from .networks import WEB3_NETWORKS
from web3 import Web3
from .thegraph import call_graph
from .bitquery.voltswap import geysers_tvl
from .find_token_type import token_router
from .oracles import list_router_prices

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