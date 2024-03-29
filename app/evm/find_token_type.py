from .networks import WEB3_NETWORKS
from .multicall import Multicall, Call, parsers
from . import token_types

async def token_router(wanted_token, farm_address, farm_network):
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
                                            try:
                                                return {**await token_types.get_beethoven_token(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'balancer'}}
                                            except:
                                                try:
                                                    return {**await token_types.get_bancor_token(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'bancor'}}
                                                except:
                                                    try:
                                                        return {**await token_types.get_nft(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'nft'}}
                                                    except:
                                                        try:
                                                            return {**await token_types.get_stargate(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'stargate'}}
                                                        except:
                                                            try:
                                                                return {**await token_types.get_single(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'single'}}
                                                            except:
                                                                return {**await token_types.catch_all(wanted_token, farm_network), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'unknown'}}

async def get_token_data(data,mongo_client, farm_network):

    calls = []
    network = ''
    collection = mongo_client['full_tokens']

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
    
            network = farm_network
            
            found_token = await collection.find_one({'tokenID' : wanted, 'network' : farm_network}, {'_id': False})
            
            if found_token is not None:
                data[1][farm_address]['userData'][pool_id].update(found_token)
                if 'lpToken' in found_token:
                    if found_token['lpToken'].lower() in ['0xf64e1c5b6e17031f5504481ac8145f4c3eab4917'.lower()]:
                        calls.append(Call(found_token['lpToken'], 'totalSupply()(uint256)', [[f'{each}_totalSupply', parsers.from_custom, 9]]))
                    else:
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
                    if 'balancerVault' in found_token:
                        calls.append(Call(found_token['balancerVault'], ['getPoolTokens(bytes32)(address[],uint256[],uint256)', bytes.fromhex(found_token['balancerPoolID'])], [[f'{each}_balancerTokens', None],[f'{each}_balancerBalances', None]]))
                    else:
                        calls.append(Call('0xBA12222222228d8Ba445958a75a0704d566BF2C8', ['getPoolTokens(bytes32)(address[],uint256[],uint256)', bytes.fromhex(found_token['balancerPoolID'])], [[f'{each}_balancerTokens', None],[f'{each}_balancerBalances', None]]))                        
                if 'curve_minter' in found_token:
                    calls.append(Call(found_token['curve_minter'], 'get_virtual_price()(uint256)', [[f'{each}_virtualPrice', parsers.from_wei]]))
                if 'getRatio' in found_token:
                    calls.append(Call(found_token['tokenID'], 'getRatio()(uint256)', [[f'{each}_getRatio', parsers.from_wei]]))
                if 'bancorOwner' in found_token:
                    calls.append(Call(found_token['tokenID'], [f'totalSupply()(uint256)'], [[f'{each}_totalSupply', parsers.from_wei]]))
                    for i,address in enumerate(found_token['bancorTokens']):
                        calls.append(Call(found_token['bancorOwner'], [f'getConnectorBalance(address)(uint256)', address], [[f'{each}_bancor{i}', None]]))
                if 'totalLiquidity' in found_token:
                    calls.append(Call(found_token['tokenID'], 'totalLiquidity()(uint256)', [[f'{each}_totalLiquidity', None]]))
                    calls.append(Call(found_token['tokenID'], 'totalSupply()(uint256)', [[f'{each}_totalSupply', None]]))                 
            else:
                token_data = await token_router(wanted, farm_address, farm_network)
                data[1][farm_address]['userData'][pool_id].update(token_data) 
                collection.update_one({'tokenID' : wanted, 'network' : farm_network}, { "$set": token_data }, upsert=True)

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
        
        if variable == 'bancor0':
            bancor_balances = []
            for i,each in enumerate(data[1][farm_address]['userData'][pool_id]['bancorTokens']):
                balances = (breakdown[0], breakdown[1], breakdown[2], f'bancor{i}')
                balances_key = '_'.join(balances)
                bancor_balances.append(str(token_calls[balances_key]))

            data[1][farm_address]['userData'][pool_id]['bancorBalances'] = bancor_balances
    
    return data[1]

def token_list_from_stakes(data, farm_info):
    tokens = [{'token' : farm_info['rewardToken'].lower(), 'decimal' : farm_info['decimal'], 'network' : farm_info['network']}]
    for d in data:
        tokens += [{'token' : x['token0'].lower(), 'decimal' : x['tkn0d'], 'network' : farm_info['network']} for x in data[d]['userData'].values() if 'token0' in x]
        
        for x in data[d]['userData'].values():
            if 'gambitRewards' in x:
                for rewards in x['gambitRewards']:
                    decimal = rewards['decimal'] if 'decimal' in rewards else 18
                    tokens += [{'token' : rewards['token'].lower(), 'decimal' : decimal, 'network' : farm_info['network']}]
            elif 'rewardDecimal' in x and 'rewardToken' in x:
                tokens += [{'token' : x['rewardToken'].lower(), 'decimal' : x['rewardDecimal'], 'network' : farm_info['network']}]
            elif 'rewardToken' in x:
                tokens += [{'token' : x['rewardToken'].lower(), 'decimal' : 18, 'network' : farm_info['network']}]
            if 'slot0' in x:
                tokens += [{'token' : x['token1'].lower(), 'decimal' : x['tkn1d'], 'network' : farm_info['network']}]

            if 'balancerTokens' in x:
                for i,balancer in enumerate(x['balancerTokens']):
                    tokens += [{'token' : balancer.lower(), 'decimal' : x['balancerDecimals'][i], 'network' : farm_info['network']}]

            if 'bancorTokens' in x:
                for i,balancer in enumerate(x['bancorTokens']):
                    tokens += [{'token' : balancer.lower(), 'decimal' : x['bancorDecimals'][i], 'network' : farm_info['network']}]
    
    return [i for n, i in enumerate(tokens) if i not in tokens[n + 1:]]