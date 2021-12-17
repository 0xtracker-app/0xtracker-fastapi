import asyncio
from .helpers import from_custom
from .token_lookup import TokenMetaData
from . import queries

async def get_valkyrie_staking(wallet, lcd_client, vaults, farm_id, mongodb, network, session):
    poolKey = farm_id

    tasks = []
    tasks.append(lcd_client.wasm.contract_query('terra1w6xf64nlmy3fevmmypx6w2fa34ue74hlye3chk', {"staker_state":{"address": wallet}}))    
    tasks.append(lcd_client.wasm.contract_query('terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32', {"staker_info":{"staker": wallet}}))

    user_balances = await asyncio.gather(*tasks)

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    if int(user_balances[0]['balance']) > 0:
        want_token = 'terra1dy9kmlm4anr92e42mrkjwzyvfqwz66un00rwr5'
        staked = from_custom(user_balances[0]['balance'], 6)

        poolNest[poolKey]['userData']['terra1w6xf64nlmy3fevmmypx6w2fa34ue74hlye3chk'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData']['terra1w6xf64nlmy3fevmmypx6w2fa34ue74hlye3chk'].update(await TokenMetaData(want_token, mongodb, lcd_client, session).lookup())
        poolIDs['%s_%s_want' % (poolKey, 'terra1w6xf64nlmy3fevmmypx6w2fa34ue74hlye3chk')] = want_token
        
        reward_token_0 = {'pending': 0, 'symbol' : 'VKR', 'token' : want_token, 'decimal' : 6}
        poolNest[poolKey]['userData']['terra1w6xf64nlmy3fevmmypx6w2fa34ue74hlye3chk']['gambitRewards'].append(reward_token_0)
    
    if int(user_balances[1]['bond_amount']) > 0:
        want_token = 'terra17fysmcl52xjrs8ldswhz7n6mt37r9cmpcguack'
        staked = from_custom(user_balances[1]['bond_amount'], 6)

        poolNest[poolKey]['userData']['terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData']['terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32'].update(await TokenMetaData(want_token, mongodb, lcd_client, session).lookup())
        poolIDs['%s_%s_want' % (poolKey, 'terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32')] = want_token
        
        reward_token_0 = {'pending': from_custom(user_balances[1]['pending_reward'], 6), 'symbol' : 'VKR', 'token' : 'terra1dy9kmlm4anr92e42mrkjwzyvfqwz66un00rwr5', 'decimal' : 6}
        poolNest[poolKey]['userData']['terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_luna_staking(wallet, lcd_client, session, vaults, farm_id, mongodb, network):
    poolKey = farm_id

    staking = [await queries.get_network_staking(wallet, session)]
    unbonded = [await queries.get_network_staking_unbonded(wallet, session)]
    rewards = [await queries.get_network_staking_rewards(wallet, session)]

    poolNest = {
        poolKey: {
            'userData': {},
            }
        }

    poolIDs = {}

    for i,each in enumerate(staking):
        if 'delegation_responses' in each:
            if len(each['delegation_responses']) > 0:
                staked_position = {'staked' : 0, 'gambitRewards' : [], 'validators' : [], 'network' : 'terra'}
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

                staked_position['staked'] = from_custom(staked_position['staked'], staked_position['tkn0d'])
                poolNest[poolKey]['userData'][want_token] = staked_position
                poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

                reward_token['pending'] = from_custom(reward_token['pending'], staked_position['tkn0d'])
                reward_token['symbol'] = staked_position['tkn0s']
                poolNest[poolKey]['userData'][want_token]['gambitRewards'].append(reward_token)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None