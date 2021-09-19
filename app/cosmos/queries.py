from .utils import make_get_json

async def get_bank_balances(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/bank/balances/{wallet}')

    if r['result']:
        return {'wallet' : wallet, 'network' : network, 'tokens' : r['result']}
    else:
        return {'wallet' : wallet, 'network' : network, 'tokens' : []}

async def get_ibc_tokens(network_data, session):
    network = network_data['chain_id']
    r = await make_get_json(session, f'https://api-utility.cosmostation.io/v1/ibc/tokens/{network}')

    return r
