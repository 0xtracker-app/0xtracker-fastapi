def transform_trace_routes(traces):

    trace_routes = {}
    meta_data = {}

    for i, network in enumerate(traces):

        if 'ibc_tokens' in network:
            for token in network['ibc_tokens']:
                token_hash = token['hash']
                token_denom = token['base_denom']

                trace_routes[f'ibc/{token_hash}'] = token_denom
                if 'decimal' in token and 'display_denom' in token:
                    meta_data[token_denom] = {
                        'base_denom' : token_denom,
                        'display_denom' : token['display_denom'].upper(),
                        'decimal' : token['decimal'],
                        'chain_id' : token['counter_party']['chain_id']
                    }

    return [trace_routes, meta_data]

def from_custom(value, decimal):
    return float(value) / (10**int(decimal))

def token_list_from_stakes(data, farm_info):
    tokens = []
    for d in data:
        tokens += [{'token' : x['token0'].lower(), 'decimal' : x['tkn0d'], 'network' : farm_info['network']} for x in data[d]['userData'].values() if 'token0' in x]
        tokens += [{'token' : x['token1'].lower(), 'decimal' : x['tkn1d'], 'network' : farm_info['network']} for x in data[d]['userData'].values() if 'token1' in x]
        
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
    
    return [i for n, i in enumerate(tokens) if i not in tokens[n + 1:]]