from .networks import WEB3_NETWORKS
from .multicall import Multicall, Call, parsers
from .farms import farms
from . import token_types

async def token_router(wanted_token, farm_address):
    farm_network = farms[farm_address]['network']
    try:
        return {**await token_types.get_lp(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'lp'}}
    except:
        try:
            return {**await token_types.get_uniswap_pool(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'uniswapv3'}}
        except:
            try:
                return {**await token_types.get_swap(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'swap'}}
            except:
                try:
                    return {**await token_types.get_curve_token(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'curve'}}
                except:
                    try:
                        return {**await token_types.get_curve_token_two(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'curve'}}
                    except:
                        try:
                            return {**await token_types.get_belt_token(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'belt'}}
                        except:
                            try:
                                return {**await token_types.get_picklejars(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'pickle'}}
                            except:
                                try:
                                    return {**await token_types.get_grow_tokens(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'grow'}}
                                except:
                                    try:
                                        return {**await token_types.kashi_token(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'kashi'}}
                                    except:
                                        try:
                                            return {**await token_types.get_balancer_token(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'balancer'}}
                                        except:
                                            return {**await token_types.get_single(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'single'}}

async def get_token_data(data,mongo_client):

    calls = []
    network = ''
    collection = mongo_client.xtracker['full_tokens']

    for each in data[0]:

        breakdown = each.split('_')
        farm_address = breakdown[0]

        try:
            pool_id = int(breakdown[1])
        except:
            pool_id = breakdown[1]

        variable = breakdown[2]

        wanted = data[0][each]

        if 'want' in each:    
            #print(wanted)
            farm_network = farms[farm_address]['network']
            network = farm_network
            
            found_token = await collection.find_one({'tokenID' : wanted, 'network' : farm_network}, {'_id': False})
            
            if found_token is not None:
                data[1][farm_address]['userData'][pool_id].update(found_token)
                if 'lpToken' in found_token:
                    calls.append(Call(found_token['lpToken'], 'totalSupply()(uint256)', [[f'{each}_totalSupply', parsers.from_wei]]))
                    calls.append(Call(found_token['lpToken'], 'getReserves()((uint112,uint112))', [[f'{each}_reserves', parsers.parseReserves]]))
                if 'getPricePerFullShare' in found_token:
                    calls.append(Call(found_token['tokenID'], 'getPricePerFullShare()(uint256)', [[f'{each}_getPricePerFullShare', parsers.from_wei]]))
                if 'swap' in found_token:
                    calls.append(Call(found_token['swap'], 'getVirtualPrice()(uint256)', [[f'{each}_virtualPrice', parsers.from_wei]]))
                if 'reserveToken' in found_token:
                    calls.append(Call(found_token['tokenID'], 'totalReserve()(uint256)', [[f'{each}_growTotalReserve', parsers.from_wei]]))
                    calls.append(Call(found_token['tokenID'], 'totalSupply()(uint256)', [[f'{each}_growTotalSupply', parsers.from_wei]]))
                if 'kashiAsset' in found_token:
                    token_decimal = found_token['tkn0d']
                    calls.append(Call(found_token['tokenID'], 'totalAsset()(uint256)', [[f'{each}_kashiTotalAsset', parsers.from_custom, token_decimal]]))
                    calls.append(Call(found_token['tokenID'], 'totalBorrow()(uint256)', [[f'{each}_kashiTotalBorrow', parsers.from_custom, token_decimal]]))
                    calls.append(Call(found_token['tokenID'], 'totalSupply()(uint256)', [[f'{each}_kashiTotalSupply', parsers.from_custom, token_decimal]]))
                if 'balancerBalances' in found_token:
                    calls.append(Call(found_token['tokenID'], [f'totalSupply()(uint256)'], [[f'{each}_totalSupply', parsers.from_wei]]))
                    calls.append(Call('0xBA12222222228d8Ba445958a75a0704d566BF2C8', ['getPoolTokens(bytes32)(address[],uint256[],uint256)', bytes.fromhex(found_token['balancerPoolID'])], [[f'{each}_balancerTokens', None],[f'{each}_balancerBalances', None]]))
                if 'curve_minter' in found_token:
                    calls.append(Call(found_token['curve_minter'], 'get_virtual_price()(uint256)', [[f'{each}_virtualPrice', parsers.from_wei]]))
                if 'getRatio' in found_token:
                    calls.append(Call(found_token['tokenID'], 'getRatio()(uint256)', [[f'{each}_getRatio', parsers.from_wei]]))
            else:
                token_data = await token_router(wanted, farm_address)
                data[1][farm_address]['userData'][pool_id].update(token_data) 
                collection.update_one({'tokenID' : wanted, 'network' : farm_network}, { "$set": token_data }, upsert=True)

        else:
            if variable == 'pending':
                data[1][farm_address]['userData'][pool_id][variable] = parsers.from_wei(wanted)
                data[1][farm_address]['userData'][pool_id]['rawPending'] = wanted
                data[1][farm_address]['userData'][pool_id]['poolID'] = pool_id
                data[1][farm_address]['userData'][pool_id]['contractAddress'] = farm_address

    token_calls = await Multicall(calls, WEB3_NETWORKS[network])()

    for token_data in token_calls:
        breakdown = token_data.split('_')
        farm_address = breakdown[0]
        try:
            pool_id = int(breakdown[1])
        except:
            pool_id = breakdown[1]
        variable = breakdown[3]
        #print(variable,token_calls[token_data])
        data[1][farm_address]['userData'][pool_id][variable] = token_calls[token_data]

        if variable == 'growTotalReserve':
            grow_supply = (breakdown[0], breakdown[1], breakdown[2], 'growTotalSupply')
            grow_key = '_'.join(grow_supply)
            data[1][farm_address]['userData'][pool_id]['getPricePerFullShare'] = ( token_calls[token_data] / token_calls[grow_key])

        if variable == 'kashiTotalAsset':
            total_borrow = (breakdown[0], breakdown[1], breakdown[2], 'kashiTotalBorrow')
            total_supply = (breakdown[0], breakdown[1], breakdown[2], 'kashiTotalSupply')
            borrow_key = '_'.join(total_borrow)
            supply_key = '_'.join(total_supply)
            data[1][farm_address]['userData'][pool_id]['getPricePerFullShare'] = (token_calls[token_data] + token_calls[borrow_key]) / token_calls[supply_key]

        if variable == 'balancerBalances':
            balances = (breakdown[0], breakdown[1], breakdown[2], 'balancerBalances')
            balances_key = '_'.join(balances)
            data[1][farm_address]['userData'][pool_id]['balancerBalances'] = [str(x) for x in token_calls[balances_key]]
    
    return data[1]

def token_list_from_stakes(data):
    tokens = []
    for d in data:
        tokens += [{'token' : x['token0'], 'decimal' : x['tkn0d'], 'network' : farms[d]['network']} for x in data[d]['userData'].values() if 'token0' in x]
        
        for x in data[d]['userData'].values():
            if 'gambitRewards' in x:
                for rewards in x['gambitRewards']:
                    decimal = rewards['decimal'] if 'decimal' in rewards else 18
                    tokens += [{'token' : rewards['token'], 'decimal' : decimal, 'network' : farms[d]['network']}]
            elif 'rewardDecimal' in x and 'rewardToken' in x:
                tokens += [{'token' : x['rewardToken'], 'decimal' : x['rewardDecimal'], 'network' : farms[d]['network']}]
            elif 'rewardToken' in x:
                tokens += [{'token' : x['rewardToken'], 'decimal' : 18, 'network' : farms[d]['network']}]
            if 'slot0' in x:
                tokens += [{'token' : x['token1'], 'decimal' : x['tkn1d'], 'network' : farms[d]['network']}]


            if 'balancerTokens' in x:
                for i,balancer in enumerate(x['balancerTokens']):
                    tokens += [{'token' : balancer, 'decimal' : x['balancerDecimals'][i], 'network' : farms[d]['network']}]
    
    return tokens