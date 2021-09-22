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