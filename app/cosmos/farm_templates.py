from .networks import CosmosNetwork
from . import queries
from . import helpers
import asyncio

async def get_delegations(wallet, session, vaults, farm_id):
    poolKey = farm_id
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks

    staking = await asyncio.gather(*[queries.get_network_staking(network, net_config[network], session) for network in net_config])
    unbonded = await asyncio.gather(*[queries.get_network_staking_unbonded(network, net_config[network], session) for network in net_config])
    rewards = await asyncio.gather(*[queries.get_network_staking_rewards(network, net_config[network], session) for network in net_config])

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for i,each in enumerate(staking):
        if 'delegation_responses' in each:

            staked_position = {'staked' : 0, 'gambitRewards' : [], 'validators' : []}
            reward_token = {'pending': 0}
            want_token = each['delegation_responses'][0]['balance']['denom']

            for position in each['delegation_responses']:
                staked_position['validators'].append(position['delegation']['validator_address'])
                staked_position['staked'] += float(position['balance']['amount'])
                staked_position['want'] = position['balance']['denom']
            
            if unbonded[i]['unbonding_responses']:
                for entry in unbonded[i]['unbonding_responses']:
                    for pending in entry['entries']:
                        staked_position['staked'] += float(pending['balance'])

            if rewards[i]['total']:
                for reward_position in rewards[i]['total']:
                    reward_token['pending'] += float(reward_position['amount'])
                    reward_token['token'] = reward_position['denom']

            poolNest[poolKey]['userData'][want_token] = staked_position
            poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

            poolNest[poolKey]['userData'][want_token]['gambitRewards'].append(reward_token)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None