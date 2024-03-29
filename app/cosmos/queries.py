from .utils import make_get_json, make_get, make_post_json
from .helpers import from_custom
import base64
from cosmpy.protos.cosmwasm.wasm.v1beta1.query_pb2 import QuerySmartContractStateRequest, QuerySmartContractStateResponse
import js2py
import json


async def get_bank_balances(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/bank/balances/{wallet}', {'timeout' : 8})

    if 'result' in r and r['result']:
        return {'wallet' : wallet, 'network' : network, 'tokens' : r['result']}
    else:
        return {'wallet' : wallet, 'network' : network, 'tokens' : []}

async def get_ibc_tokens(network_data, session):
    network = network_data['chain_id']
    
    r = await make_get(session, f'https://serverlessrepo-downloader-bucket-1qsab6s7fy5e1.s3.amazonaws.com/cosmos/ibc/traces/{network}.json', {'timeout' : 8})

    return json.loads(r)

async def get_network_staking(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
#    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegations/{wallet}', {'timeout' : 5})
    r = await make_get_json(session, f'{endpoint}/staking/delegators/{wallet}/delegations', {'timeout' : 8})
    return r

async def get_network_staking_unbonded(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
#    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegators/{wallet}/unbonding_delegations', {'timeout' : 5})
    r = await make_get_json(session, f'{endpoint}/staking/delegators/{wallet}/unbonding_delegations', {'timeout' : 8})

    return r

async def get_cresent_farming(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
#    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegators/{wallet}/unbonding_delegations', {'timeout' : 5})
    r = await make_get_json(session, f'{endpoint}/crescent/farming/v1beta1/positions/{wallet}')

    return r

async def get_cresent_rewards(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
#    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegators/{wallet}/unbonding_delegations', {'timeout' : 5})
    r = await make_get_json(session, f'{endpoint}/crescent/farming/v1beta1/rewards/{wallet}')

    return r

async def get_cresent_pool_info(pool, network_data, session):
    endpoint = network_data['rest']

    r = await make_get_json(session, f'{endpoint}/crescent/liquidity/v1beta1/pools/{pool.split("pool")[1]}')

    return r

async def get_cresent_farming_v2(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/crescent/farming/v1beta1/positions/{wallet}')

    return r

async def get_cresent_rewards_v2(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    r = await make_get_json(session, f'{endpoint}/crescent/farming/v1beta1/rewards/{wallet}')

    return r

async def get_cresent_pool_info_v2(pool, network_data, session):
    endpoint = network_data['rest']
    r = await make_get_json(session, f'{endpoint}/crescent/liquidity/v1beta1/pools/{pool.split("pool")[1]}')

    return r

async def get_denom_total_supply(network, denom, network_data, session):
    endpoint = network_data['rest']

    r = await make_get_json(session, f'{endpoint}/cosmos/bank/v1beta1/supply/{denom}')

    return r

async def get_network_staking_rewards(network, network_data, session):
    endpoint = network_data['rest']
    wallet = network_data['wallet']
    #r = await make_get_json(session, f'{endpoint}/cosmos/distribution/v1beta1/delegators/{wallet}/rewards', {'timeout' : 5})
    r = await make_get_json(session , f'{endpoint}/distribution/delegators/{wallet}/rewards')

    return r

async def find_trace_route(ibc,network_data, session):
    endpoint = network_data['rest']
    route = ibc.replace('ibc/', '')
    if network_data['chain_id'] in ['osmosis-1', 'juno-1']:
        r = await make_get_json(session, f'{endpoint}/ibc/apps/transfer/v1/denom_traces/{route}')
    else:
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
        if r['pool']['@type'] == '/osmosis.gamm.poolmodels.stableswap.v1beta1.Pool':
            imperator = await make_get_json(session, f'https://api-osmosis.imperator.co/stream/pool/v1/{pool_id}')

            return {
                'base_denom' : r['pool']['total_shares']['denom'],
                'address' : r['pool']['address'],
                'stable_swap' : True,
                'total_shares' : from_custom(int(r['pool']['total_shares']['amount']), 18),
                'reserves' : [x['amount'] for x in r['pool']['pool_liquidity']], 
                'pool_tokens' : [x['denom'] for x in r['pool']['pool_liquidity']],
                'token_weights' : [x['percent'] / 100 for x in imperator['pool_tokens']],
                }
        elif len(r['pool']['pool_assets']) > 2:
            return {
                'base_denom' : r['pool']['total_shares']['denom'],
                'address' :r['pool']['address'],
                'stable_swap' : False,
                'total_shares' : from_custom(int(r['pool']['total_shares']['amount']), 18),
                'reserves' : [x['token']['amount'] for x in r['pool']['pool_assets']], 
                'pool_tokens' : [x['token']['denom'] for x in r['pool']['pool_assets']],
                'token_weights' : [int(x['weight']) / int(r['pool']['total_weight']) for x in r['pool']['pool_assets']],
                }
        else:
            return {
                'base_denom' : r['pool']['total_shares']['denom'],
                'stable_swap' : False,
                'total_shares' : from_custom(int(r['pool']['total_shares']['amount']), 18),
                'reserves' : [r['pool']['pool_assets'][0]['token']['amount'], r['pool']['pool_assets'][1]['token']['amount']], 
                'token0' : r['pool']['pool_assets'][0]['token']['denom'],
                'token1' : r['pool']['pool_assets'][1]['token']['denom'],
                'token_weights' : [int(r['pool']['pool_assets'][0]['weight']) / int(r['pool']['total_weight']), int(r['pool']['pool_assets'][1]['weight'])/int(r['pool']['total_weight'])],
                }
    else:
        return None

async def get_gamm_balances(pool,network_data,session):
    endpoint = network_data['rest']
    pool_id = pool.split('/')[2]
    r = await make_get_json(session, f'{endpoint}/osmosis/gamm/v1beta1/pools/{pool_id}')

    if 'pool' in r:
        if r['pool']['@type'] == '/osmosis.gamm.poolmodels.stableswap.v1beta1.Pool':
            return {
                'total_shares' : from_custom(int(r['pool']['total_shares']['amount']), 18),
                'reserves' : [x['amount'] for x in r['pool']['pool_liquidity']], 
                }
        else:
            return {
                'total_shares' : from_custom(int(r['pool']['total_shares']['amount']), 18),
                'reserves' : [int(x['token']['amount']) for x in r['pool']['pool_assets']], 
                }            
    else:
        return None

async def get_sif_pool(pool,network_data,session):
    endpoint = f'https://api.sifchain.finance/clp/getPool?symbol={pool}'

    r = await make_get_json(session, endpoint)

    if 'result' in r:
        return {
            'total_shares' : from_custom(int(r['result']['pool']['pool_units']), 18),
            'reserves' : [int(r['result']['pool']['external_asset_balance']),int(r['result']['pool']['native_asset_balance'])], 
            'token_weights' : [.5, .5],
            }
    else:
        return None

async def get_user_sif_pool(pool,wallet,session):
    endpoint = f'https://api.sifchain.finance/clp/getLiquidityProvider?symbol={pool}&lpAddress={wallet}'

    r = await make_get_json(session, endpoint)

    if 'result' in r:
        return {
            'staked' : from_custom(r['result']['liquidity_provider']['liquidity_provider_units'], 18)
            }
    else:
        return None

async def get_sif_assets(session):
    endpoint = f'https://raw.githubusercontent.com/Sifchain/sifchain-ui/develop/core/src/config/networks/sifchain/assets.sifchain.mainnet.json'
    r = await make_get_json(session, endpoint)

    # x = r.split('assets: [')[1].split(']')[0]
    # response = list(js2py.eval_js(f'[{x}]'))

    return {x['symbol'] : {
            'denom' : x['symbol'],
            'symbol' : x['displaySymbol'].upper(),
            'decimal' : x['decimals']
        } for x in r["assets"]}


async def get_osmosis_assets(session):
    endpoint = f'https://raw.githubusercontent.com/osmosis-labs/assetlists/main/osmosis-1/osmosis-1.assetlist.json'
    r =  json.loads(await make_get(session, endpoint))

    token_dict = {}

    for x in r['assets']:
        if 'ibc' in x and len(x['denom_units']) == 2:
            token_dict[x['ibc']['source_denom']] = { 'denom' : x['ibc']['source_denom'], 'symbol': x['symbol'], 'decimal' : x['denom_units'][1]['exponent']}

    return token_dict

async def query_contract_state(client, rpc, contract_address, message):

    payload = json.dumps({
                "jsonrpc":"2.0",
                "id":-1,
                "method":"abci_query",
                "params":
                    {
                        "path":"/cosmwasm.wasm.v1.Query/SmartContractState",
                        "data": QuerySmartContractStateRequest(address=contract_address, query_data=json.dumps(message).encode("UTF8")).SerializeToString().hex(),
                        "prove": False
                    }
            })

    r = await make_post_json(client, rpc, {'data' : payload})

    if r:
        offset = base64.b64decode(r['result']["response"]["value"]).find('{'.encode())
        return json.loads(base64.b64decode(r['result']["response"]["value"])[offset:].decode('utf8'))
    else:
        return {}
