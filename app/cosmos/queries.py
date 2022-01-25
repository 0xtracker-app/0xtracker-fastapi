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
    r = await make_get_json(session, f'https://api-utility.cosmostation.io/v1/ibc/tokens/{network}', {'timeout' : 8})

    return r

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

async def get_gamm_balances(pool,network_data,session):
    endpoint = network_data['rest']
    pool_id = pool.split('/')[2]
    r = await make_get_json(session, f'{endpoint}/osmosis/gamm/v1beta1/pools/{pool_id}')

    if 'pool' in r:
        return {
            'total_shares' : from_custom(int(r['pool']['totalShares']['amount']), 18),
            'reserves' : [int(r['pool']['poolAssets'][0]['token']['amount']),int(r['pool']['poolAssets'][1]['token']['amount'])], 
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
    endpoint = f'https://raw.githubusercontent.com/Sifchain/sifchain-ui/develop/ui/core/src/config/networks/sifchain/assets.sifchain.mainnet.ts'
    r = await make_get(session, endpoint)

    x = r.split('assets: [')[1].split(']')[0]
    response = list(js2py.eval_js(f'[{x}]'))

    return {x['symbol'] : {
        'denom' : x['symbol'],
        'symbol' : x['displaySymbol'].upper(),
        'decimal' : x['decimals']
        
        } for x in response}

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
    offset = base64.b64decode(r['result']["response"]["value"]).find('{'.encode())
    return json.loads(base64.b64decode(r['result']["response"]["value"])[offset:].decode('utf8'))
