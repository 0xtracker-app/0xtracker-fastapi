def from_custom(value, decimal):
    return float(value) / (10**int(decimal))

def token_list_from_stakes(data, farm_info):
    tokens = [{'token' : farm_info['rewardToken'].lower(), 'decimal' : farm_info['decimal'], 'network' : farm_info['network']}]
    for d in data:
        tokens += [{'token' : x['token0'].lower(), 'decimal' : x['tkn0d'], 'network' : farm_info['network']} for x in data[d]['userData'].values() if 'token0' in x]
        tokens += [{'token' : x['token1'].lower(), 'decimal' : x['tkn1d'], 'network' : farm_info['network']} for x in data[d]['userData'].values() if 'token1' in x]

        for x in data[d]['userData'].values():
            if 'gambitRewards' in x:
                for rewards in x['gambitRewards']:
                    decimal = rewards['decimal'] if 'decimal' in rewards else 6
                    tokens += [{'token' : rewards['token'].lower(), 'decimal' : decimal, 'network' : farm_info['network']}]
            elif 'rewardDecimal' in x and 'rewardToken' in x:
                tokens += [{'token' : x['rewardToken'].lower(), 'decimal' : x['rewardDecimal'], 'network' : farm_info['network']}]
            elif 'rewardToken' in x:
                tokens += [{'token' : x['rewardToken'].lower(), 'decimal' : 6, 'network' : farm_info['network']}]
            if 'slot0' in x:
                tokens += [{'token' : x['token1'].lower(), 'decimal' : x['tkn1d'], 'network' : farm_info['network']}]

            if 'balancerTokens' in x:
                for i,balancer in enumerate(x['balancerTokens']):
                    tokens += [{'token' : balancer.lower(), 'decimal' : x['balancerDecimals'][i], 'network' : farm_info['network']}]
    
    return [i for n, i in enumerate(tokens) if i not in tokens[n + 1:]]