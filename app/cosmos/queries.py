from .utils import make_get_json
from .helpers import from_custom

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

async def get_network_staking(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegations/{wallet}')
    
    return r

async def get_network_staking_unbonded(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegators/{wallet}/unbonding_delegations')

    return r

async def get_network_staking_rewards(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/cosmos/distribution/v1beta1/delegators/{wallet}/rewards')

    return r

async def find_trace_route(ibc,network_data, session):
    endpoint = network_data['rest']
    route = ibc.replace('ibc/', '')
    r = await make_get_json(session, f'{endpoint}/ibc/applications/transfer/v1beta1/denom_traces/{route}')
    if 'denom_trace' in r:
        return {'base_denom' : r['denom_trace']['base_denom'], 'chain_id' : network_data['chain_id'], 'hash' : ibc}
    else:
        return None

async def get_osmosis_locked_staking(network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/osmosis/lockup/v1beta1/account_locked_coins/{wallet}')

    return r

async def get_osmosis_unlocked_staking(network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/osmosis/lockup/v1beta1/account_unlockable_coins/{wallet}')

    return r

async def get_gamm_pool(pool,network_data,session):
    endpoint = network_data['rest']
    pool_id = pool.split('/')[2]
    r = await make_get_json(session, f'{endpoint}/osmosis/gamm/v1beta1/pools/{pool_id}')

    if 'pool' in r:
        return {
            'base_denom' : r['pool']['totalShares']['denom'],
            'total_shares' : from_custom(int(r['pool']['totalShares']['amount']), 18),
            'reserves' : [int(r['pool']['poolAssets'][0]['token']['amount']),int(r['pool']['poolAssets'][1]['token']['amount'])], 
            'token0' : r['pool']['poolAssets'][0]['token']['denom'],
            'token1' : r['pool']['poolAssets'][1]['token']['denom'],
            'token_weights' : [int(r['pool']['poolAssets'][0]['weight']) / int(r['pool']['totalWeight']), int(r['pool']['poolAssets'][1]['weight'])/int(r['pool']['totalWeight'])],
            }
    else:
        return None
