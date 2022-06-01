from web3 import Web3

async def parse_calls(m):
    calls = []

    for each in m:
        if 'staked' in each.returns[0][0]:
            calls.append({
                'target' : each.target,
                'type' : 'user_balance',
                'function' : each.function,
                'args' : each.args,
                'signature' : {
                    'fourbyte' : None, #Web3.toText(each.signature.fourbyte),
                    'input_types' : each.signature.input_types,
                    'output_types' : each.signature.output_types,
                },
                'raw_call' : None, #Web3.toText(each.data),
            })

        if 'pending' in each.returns[0][0]:
            calls.append({
                'target' : each.target,
                'type' : 'pending_rewards',
                'function' : each.function,
                'args' : each.args,
                'signature' : {
                    'fourbyte' : None, #Web3.toText(each.signature.fourbyte),
                    'input_types' : each.signature.input_types,
                    'output_types' : each.signature.output_types,
                },
                'raw_call' : None, #Web3.toText(each.data),
            })
    
    return calls

async def parse_calls_master(m):
    calls = []

    for each in m:
        calls.append({
            'target' : each.target,
            'type' : 'user_balance',
            'function' : each.function,
            'args' : each.args,
            'signature' : {
                'fourbyte' : None, #Web3.toText(each.signature.fourbyte),
                'input_types' : each.signature.input_types,
                'output_types' : each.signature.output_types,
            },
            'raw_call' : None, #Web3.toText(each.data),
        })
    
    return calls