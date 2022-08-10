from .queries import make_get_json, make_get
import json

async def dummy_vault(session):
    return ['0xDummy']

async def junoswap_vaults(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/CosmosContracts/junoswap-asset-list/main/pools_list.json')
    r = json.loads(r)
    return [x['swap_address'] for x in r['pools'] if x['swap_address'] != ""]

async def junoswap_locks(session):
    staking_contracts = await make_get(session, 'https://raw.githubusercontent.com/CosmosContracts/junoswap-asset-list/main/pools_list.json')
    rewarder_contracts = await make_get(session, 'https://raw.githubusercontent.com/CosmosContracts/junoswap-asset-list/main/rewards_list.json')
    s = json.loads(staking_contracts)
    r = json.loads(rewarder_contracts)

    stake_by_swap = {x['swap_address'] : { 'staking_address' : x['staking_address'], 'rewards' : [] } for x in s['pools'] if x['staking_address'] != "" }

    for x in r['list']:
        for rewards in x['rewards_tokens']:
            stake_by_swap[x['swap_address']]['rewards'].append(rewards['rewards_address'])


    return stake_by_swap