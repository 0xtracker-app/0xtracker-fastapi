from .utils import make_get_json
from .networks import CosmosNetwork
from . import queries
from . import helpers
from .token_lookup import TokenMetaData
import asyncio

async def get_delegations(wallet, session, vaults, farm_id, mongodb):
    poolKey = farm_id
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks

    staking = await asyncio.gather(*[queries.get_network_staking(network, net_config[network], session) for network in net_config], return_exceptions=True)
    unbonded = await asyncio.gather(*[queries.get_network_staking_unbonded(network, net_config[network], session) for network in net_config], return_exceptions=True)
    rewards = await asyncio.gather(*[queries.get_network_staking_rewards(network, net_config[network], session) for network in net_config], return_exceptions=True)

    poolNest = {
        poolKey: {
            'userData': {},
            }
        }

    poolIDs = {}

    for i,each in enumerate(staking):

        if 'result' in each:
            if len(each['result']) > 0:
                staked_position = {'staked' : 0, 'gambitRewards' : [], 'validators' : [], 'network' : 'cosmos'}
                reward_token = {'pending': 0}
                want_token = each['result'][0]['balance']['denom']

                staked_position.update(await TokenMetaData(address=want_token, mongodb=mongodb, session=session).lookup())

                for position in each['result']:
                    staked_position['validators'].append(position['delegation']['validator_address'])
                    staked_position['staked'] += float(position['balance']['amount'])
                    staked_position['want'] = position['balance']['denom']

                if 'result' in unbonded[i]:
                    if len(unbonded[i]['result']) > 0:
                        for entry in unbonded[i]['result']:
                            for pending in entry['entries']:
                                staked_position['staked'] += float(pending['balance'])

                if 'result' in rewards[i]:
                    if len(rewards[i]['result']) > 0:
                        for reward_position in rewards[i]['result']['total']:
                            reward_token['pending'] += float(reward_position['amount'])
                            reward_token['token'] = reward_position['denom']

                staked_position['staked'] = helpers.from_custom(staked_position['staked'], staked_position['tkn0d'])
                poolNest[poolKey]['userData'][want_token] = staked_position
                poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

                reward_token['pending'] = helpers.from_custom(reward_token['pending'], staked_position['tkn0d'])
                reward_token['symbol'] = staked_position['tkn0s']
                if 'token' not in reward_token:
                    reward_token['pending'] = want_token
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

    for i,each in enumerate(staking[0]['coins']):

            staked_position = {'staked' : 0, 'gambitRewards' : [], 'network' : 'cosmos'}
            want_token = each['denom']
            staked_position.update(await TokenMetaData(address=want_token, mongodb=mongodb, network=net_config, session=session).lookup())
            staked_position['want'] = want_token
            staked_position['staked'] = helpers.from_custom(each['amount'], 18)
        
            poolNest[poolKey]['userData'][want_token] = staked_position
            poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

    if 'coins' in staking[1]:
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

async def get_sifchain_assets(wallet, session, vaults, farm_id, mongodb, network):
    poolKey = farm_id
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks[network]

    staking = await make_get_json(session, f'https://api.sifchain.finance/clp/getAssets?lpAddress={net_config["wallet"]}')
    
    poolNest = {
        poolKey: {
            'userData': {},
            }
        }

    poolIDs = {}
    if staking['result']:
        staking_lp_data = await asyncio.gather(*[queries.get_sif_pool(x['symbol'], net_config, session) for x in staking['result']])
        staking_user_data = await asyncio.gather(*[queries.get_user_sif_pool(x['symbol'], net_config['wallet'], session) for x in staking['result']])
        
        for i,each in enumerate(staking['result']):

                staked_position = {'staked' : staking_user_data[i]['staked'], 'gambitRewards' : [], 'network' : 'cosmos'}
                want_token = f'sifchain-lp-{i}'
                token_0 = await TokenMetaData(address=each['symbol'], mongodb=mongodb, network=net_config, session=session).lookup()
                staked_position.update(staking_lp_data[i])
                staked_position.update({
                    'tokenID': want_token,
                    'tkn0s': token_0['tkn0s'],
                    'tkn0d': token_0['tkn0d'],
                    'tkn1s': 'ROWAN',
                    'tkn1d': 18,
                    'token0' : token_0['token0'],
                    'token1' : 'rowan',
                    'token_decimals': [token_0['tkn0d'],18],
                    'all_tokens': [token_0['token0'], 'rowan']})
                poolNest[poolKey]['userData'][want_token] = staked_position
                poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None