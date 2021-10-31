from .networks import CosmosNetwork
from . import queries
from . import helpers
from .token_lookup import TokenMetaData
import asyncio

async def get_delegations(wallet, session, vaults, farm_id, mongodb):
    poolKey = farm_id
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks

    staking = await asyncio.gather(*[queries.get_network_staking(network, net_config[network], session) for network in net_config])
    unbonded = await asyncio.gather(*[queries.get_network_staking_unbonded(network, net_config[network], session) for network in net_config])
    rewards = await asyncio.gather(*[queries.get_network_staking_rewards(network, net_config[network], session) for network in net_config])

    poolNest = {
        poolKey: {
            'userData': {},
            }
        }

    poolIDs = {}

    for i,each in enumerate(staking):
        if 'delegation_responses' in each:
            if len(each['delegation_responses']) > 0:
                staked_position = {'staked' : 0, 'gambitRewards' : [], 'validators' : [], 'network' : 'cosmos'}
                reward_token = {'pending': 0}
                want_token = each['delegation_responses'][0]['balance']['denom']
                staked_position.update(await TokenMetaData(address=want_token, mongodb=mongodb).lookup())

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

                staked_position['staked'] = helpers.from_custom(staked_position['staked'], staked_position['tkn0d'])
                poolNest[poolKey]['userData'][want_token] = staked_position
                poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

                reward_token['pending'] = helpers.from_custom(reward_token['pending'], staked_position['tkn0d'])
                reward_token['symbol'] = staked_position['tkn0s']
                poolNest[poolKey]['userData'][want_token]['gambitRewards'].append(reward_token)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_osmosis_staking(wallet, session, vaults, farm_id, mongodb, network):
    poolKey = farm_id
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks[network]

    staking = await asyncio.gather(*[queries.get_osmosis_locked_staking(net_config, session), queries.get_osmosis_unlocked_staking(net_config, session)])

    poolNest = {
        poolKey: {
            'userData': {},
            }
        }

    poolIDs = {}
    print(staking)
    for i,each in enumerate(staking[0]['coins']):

            staked_position = {'staked' : 0, 'gambitRewards' : [], 'network' : 'cosmos'}
            want_token = each['denom']
            staked_position.update(await TokenMetaData(address=want_token, mongodb=mongodb, network=net_config, session=session).lookup())
            staked_position['want'] = want_token
            staked_position['staked'] = helpers.from_custom(each['amount'], 18)
        
            poolNest[poolKey]['userData'][want_token] = staked_position
            poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

    for i,each in enumerate(staking[1]['coins']):

            want_token = each['denom']

            if want_token in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData']['want'] += helpers.from_custom(each['amount'], 18)
            else:
                staked_position = {'staked' : 0, 'gambitRewards' : [], 'network' : 'cosmos'}
                staked_position.update(await TokenMetaData(address=want_token, mongodb=mongodb, network=net_config, session=session).lookup())
                staked_position['want'] = want_token
                staked_position['staked'] = helpers.from_custom(each['amount'], 18)
        
                poolNest[poolKey]['userData'][want_token] = staked_position
                poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None
