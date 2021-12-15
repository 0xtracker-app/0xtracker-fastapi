import asyncio
from .helpers import from_custom
from .token_lookup import TokenMetaData

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
        
        reward_token_0 = {'pending': 0, 'symbol' : 'VKR', 'token' : want_token}
        poolNest[poolKey]['userData']['terra1w6xf64nlmy3fevmmypx6w2fa34ue74hlye3chk']['gambitRewards'].append(reward_token_0)
    
    if int(user_balances[1]['bond_amount']) > 0:
        want_token = 'terra17fysmcl52xjrs8ldswhz7n6mt37r9cmpcguack'
        staked = from_custom(user_balances[1]['bond_amount'], 6)

        poolNest[poolKey]['userData']['terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData']['terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32'].update(await TokenMetaData(want_token, mongodb, lcd_client, session).lookup())
        poolIDs['%s_%s_want' % (poolKey, 'terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32')] = want_token
        
        reward_token_0 = {'pending': from_custom(user_balances[1]['pending_reward'], 6), 'symbol' : 'VKR', 'token' : 'terra1dy9kmlm4anr92e42mrkjwzyvfqwz66un00rwr5'}
        poolNest[poolKey]['userData']['terra1ude6ggsvwrhefw2dqjh4j6r7fdmu9nk6nf2z32']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None