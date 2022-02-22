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

async def get_spectrum_farms(wallet, lcd_client, vaults, farm_id, mongodb, network, session):
    poolKey = farm_id

    tasks = []
    response_key = []
    for contract in vaults:
        tasks.append(lcd_client.wasm.contract_query(contract, { "reward_info": { "staker_addr": wallet }}))
        response_key.append(f'{contract}_userinfo')
        tasks.append(lcd_client.wasm.contract_query(contract, { "pools": {}}))
        response_key.append(f'{contract}_pools')     

    stakes = dict(zip(response_key, await asyncio.gather(*tasks)))

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'userinfo' in each:

            if stakes[each]['reward_infos']:
                breakdown = each.split('_')
                want_token = stakes[f'{breakdown[0]}_pools']['pools'][0]['staking_token'] if 'staking_token' in stakes[f'{breakdown[0]}_pools']['pools'][0] else stakes[f'{breakdown[0]}_pools']['pools'][0]['asset_token']
                want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
                staked = from_custom(stakes[each]['reward_infos'][0]['bond_amount'], want_token_meta['token_decimal'])
                pending = from_custom(stakes[each]['reward_infos'][0]['pending_spec_reward'], 6)
                reward_token = 'terra1s5eczhe0h0jutf46re52x5z4r03c8hupacxmdr'
                reward_symbol = 'SPEC'

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolNest[poolKey]['userData'][breakdown[0]].update(want_token_meta)
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
            
                reward_token_0 = {'pending': pending, 'symbol' : reward_symbol, 'token' : reward_token}
                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_spectrum_staking(wallet, lcd_client, vaults, farm_id, mongodb, network, session, want_token):
    poolKey = farm_id

    tasks = []
    response_key = []
    for contract in vaults:
        tasks.append(lcd_client.wasm.contract_query(contract, { "balance": { "address": wallet }}))
        response_key.append(f'{contract}_userinfo')
 
    stakes = dict(zip(response_key, await asyncio.gather(*tasks)))

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'userinfo' in each:
            for i, pool in enumerate(stakes[each]['pools']):
                if int(pool['balance']) > 0:
                    breakdown = each.split('_')
                    want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
                    staked = from_custom(int(pool['balance']), want_token_meta['token_decimal'])
                    pending = from_custom(int(pool['pending_aust']), 6)
                    reward_token = 'terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu'
                    reward_symbol = 'aUST'

                    poolNest[poolKey]['userData'][f'{breakdown[0]}{i}'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolNest[poolKey]['userData'][f'{breakdown[0]}{i}'].update(want_token_meta)
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
                    reward_token_0 = {'pending': pending, 'symbol' : reward_symbol, 'token' : reward_token}
                    poolNest[poolKey]['userData'][f'{breakdown[0]}{i}']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_loop_farming(wallet, lcd_client, vaults, farm_id, mongodb, network, session, query_contract):
    poolKey = farm_id

    tasks = []
    response_key = []

    vaults = await lcd_client.wasm.contract_query(query_contract, { "query_list_of_stakeable_tokens": {}})

    for contract in vaults:
        tasks.append(lcd_client.wasm.contract_query(query_contract, { "query_staked_by_user": { "wallet": wallet, "staked_token" : contract['token']['token']['contract_addr'] }}))
        response_key.append(f'{contract["token"]["token"]["contract_addr"]}_userinfo')

        tasks.append(lcd_client.wasm.contract_query(query_contract, { "query_user_reward_in_pool": { "wallet": wallet, "pool" : { "token" : { "contract_addr" : contract['token']['token']['contract_addr'] }}}}))
        response_key.append(f'{contract["token"]["token"]["contract_addr"]}_pending')
 
    stakes = dict(zip(response_key, await asyncio.gather(*tasks)))

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'userinfo' in each:
            if int(stakes[each]) > 0:
                breakdown = each.split('_')
                want_token = breakdown[0]
                want_token_meta = await TokenMetaData(breakdown[0], mongodb, lcd_client, session).lookup()
                staked = from_custom(int(stakes[each]), want_token_meta['token_decimal'])

                poolNest[poolKey]['userData'][f'{breakdown[0]}'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolNest[poolKey]['userData'][f'{breakdown[0]}'].update(want_token_meta)
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i,reward in enumerate(stakes[f'{want_token}_pending'][0]['rewards_info']):
                        pending_token = stakes[f'{want_token}_pending'][0]['rewards_info'][i]['info']['token']['contract_addr']
                        reward_token_meta = await TokenMetaData(pending_token, mongodb, lcd_client, session).lookup()
                        reward_token_0 = {'pending': from_custom(stakes[f'{want_token}_pending'][0]['rewards_info'][i]['amount'], reward_token_meta['token_decimal']), 'symbol' : reward_token_meta['tkn0s'], 'token' : pending_token}
                        poolNest[poolKey]['userData'][f'{breakdown[0]}']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_loop_staking(wallet, lcd_client, vaults, farm_id, staking_token, mongodb, network, session):
    poolKey = farm_id

    tasks = []
    response_key = []

    for contract in vaults:
        tasks.append(lcd_client.wasm.contract_query(contract, { "query_staked_by_user": { "wallet": wallet }}))
        response_key.append(f'{contract}_userinfo')

        tasks.append(lcd_client.wasm.contract_query(contract, { "query_user_reward": { "wallet": wallet }}))
        response_key.append(f'{contract}_pending')
 
    stakes = dict(zip(response_key, await asyncio.gather(*tasks)))

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'userinfo' in each:
            if int(stakes[each]) > 0:
                breakdown = each.split('_')
                want_token = staking_token
                want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
                staked = from_custom(int(stakes[each]), want_token_meta['token_decimal'])

                poolNest[poolKey]['userData'][f'{breakdown[0]}'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolNest[poolKey]['userData'][f'{breakdown[0]}'].update(want_token_meta)
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                reward_token_0 = {'pending': from_custom(stakes[f'{breakdown[0]}_pending'], want_token_meta['token_decimal']), 'symbol' : want_token_meta['tkn0s'], 'token' : want_token}
                poolNest[poolKey]['userData'][f'{breakdown[0]}']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_mirror_farming(wallet, lcd_client, vaults, farm_id, mongodb, network, session, query_contract, reward_token):
    poolKey = farm_id

    tasks = []
    response_key = []


    tasks.append(lcd_client.wasm.contract_query(query_contract, {"reward_info":{"staker_addr": wallet}}))

 
    stakes = await asyncio.gather(*tasks)
    reward_token_meta = await TokenMetaData(reward_token, mongodb, lcd_client, session).lookup()
    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes[0]['reward_infos']:

        if each['is_short']:
            want_token = each['asset_token']
            position_type = 'short'
        else:
            pool_info = await lcd_client.wasm.contract_query(query_contract, { "pool_info": { "asset_token":  each['asset_token']}})
            want_token = pool_info['staking_token']
            position_type = 'long'

        
        want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        staked = from_custom(int(each['bond_amount']), want_token_meta['token_decimal'])

        poolNest[poolKey]['userData'][f'{want_token}{position_type}'] = {'want': want_token, 'staked' : staked, 'mirror_position' : position_type, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][f'{want_token}{position_type}'].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, f'{want_token}{position_type}')] = want_token

                
        reward_token_0 = {'pending': from_custom(each['pending_reward'], reward_token_meta['token_decimal']), 'symbol' : reward_token_meta['tkn0s'], 'token' : reward_token}
        poolNest[poolKey]['userData'][f'{want_token}{position_type}']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_mirror_lending(wallet, lcd_client, vaults, farm_id, mongodb, network, session, query_contract):

    poolKey = farm_id
    tasks = []

    tasks.append(lcd_client.wasm.contract_query(query_contract, {"positions":{"owner_addr": wallet}}))

    stakes = await asyncio.gather(*tasks)

    poolNest = {poolKey: 
    { 'userData': { }
     } }

    poolIDs = {}

    for stake in stakes[0]['positions']:

        collat_address = stake['collateral']['info']['native_token']['denom'] if 'native_token' in stake['collateral']['info'] else stake['collateral']['info']['token']['contract_addr']
        borrow_address = stake['asset']['info']['native_token']['denom'] if 'native_token' in stake['asset']['info'] else stake['asset']['info']['token']['contract_addr']

        want_token_meta = await TokenMetaData(collat_address, mongodb, lcd_client, session).lookup()
        collat = from_custom(int(stake['collateral']['amount']), want_token_meta['token_decimal'])
        borrow_rate = await lcd_client.wasm.contract_query(query_contract, { "asset_config" : { "asset_token": borrow_address}})

        if collat_address in poolNest[poolKey]['userData']:
            poolNest[poolKey]['userData'][collat_address]['rate'] = float(borrow_rate['min_collateral_ratio'])
            poolNest[poolKey]['userData'][collat_address]['staked'] += collat
        else:
            poolNest[poolKey]['userData'][collat_address] = {'staked' : collat, 'want': collat_address, 'borrowed' : 0, 'rate' : float(borrow_rate['min_collateral_ratio']), 'gambitRewards' : []}
            poolNest[poolKey]['userData'][collat_address].update(want_token_meta)
            poolIDs['%s_%s_want' % (poolKey, collat_address)] = collat_address
        


        borrow_token_meta = await TokenMetaData(borrow_address, mongodb, lcd_client, session).lookup()
        borrowed = from_custom(int(stake['asset']['amount']), borrow_token_meta['token_decimal'])


        if borrow_address in poolNest[poolKey]['userData']:
            poolNest[poolKey]['userData'][borrow_address]['borrowed'] += borrowed
            poolNest[poolKey]['userData'][borrow_address]['rate'] = float(borrow_rate['min_collateral_ratio'])
        else:
            poolNest[poolKey]['userData'][borrow_address] = {'staked' : 0, 'want': borrow_address, 'borrowed' : borrowed, 'rate' : float(borrow_rate['min_collateral_ratio']), 'gambitRewards' : []}
            poolNest[poolKey]['userData'][borrow_address].update(borrow_token_meta)
            poolIDs['%s_%s_want' % (poolKey, borrow_address)] = borrow_address

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_astroport_locks(wallet, lcd_client, vaults, farm_id, mongodb, network, session):
    poolKey = farm_id

    stakes = await lcd_client.wasm.contract_query('terra1627ldjvxatt54ydd3ns6xaxtd68a2vtyu7kakj', { "user_info": { "address" : wallet }})

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    if 'lockup_infos' in stakes:
        for i, each in enumerate(stakes['lockup_infos']):
            if int(each['lp_units_locked']) > 0:
                want_token = each['terraswap_lp_token']
                want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
                staked = from_custom(int(each['lp_units_locked']), want_token_meta['token_decimal'])

                poolNest[poolKey]['userData'][f'{want_token}{i}'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolNest[poolKey]['userData'][f'{want_token}{i}'].update(want_token_meta)
                poolIDs['%s_%s_want' % (poolKey, f'{want_token}{i}')] = want_token


                pending_token = 'terra1xj49zyqrwpv5k928jwfpfy2ha668nwdgkwlrg3'
                reward_token_meta = await TokenMetaData(pending_token, mongodb, lcd_client, session).lookup()
                reward_token_0 = {'pending': from_custom(each['claimable_generator_astro_debt'], reward_token_meta['tkn0d']), 'symbol' : reward_token_meta['tkn0s'], 'token' : pending_token}
                poolNest[poolKey]['userData'][f'{want_token}{i}']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_anchor_lending(wallet, lcd_client, vaults, farm_id, mongodb, network, session):

    poolKey = farm_id
    tasks = []
    response_key = []


    tasks.append(lcd_client.wasm.contract_query('terra1tmnqgvg567ypvsvk6rwsga3srp7e3lg6u0elp8', { "collaterals": { "borrower": wallet }}))
    response_key.append(f'collateral')

    tasks.append(lcd_client.wasm.contract_query('terra1sepfj7s0aeg5967uxnfk4thzlerrsktkpelm5s', { "borrower_info": { "borrower": wallet }}))
    response_key.append(f'borrowed')

    stakes = dict(zip(response_key, await asyncio.gather(*tasks)))

    poolNest = {poolKey: 
    { 'userData': { }
     } }

    poolIDs = {}

    for each in stakes['collateral']['collaterals']:
        collat_address = each[0]
        want_token_meta = await TokenMetaData(each[0], mongodb, lcd_client, session).lookup()
        collat = from_custom(int(each[1]), want_token_meta['token_decimal'])
        borrow_rate = .6
        
        poolNest[poolKey]['userData'][collat_address] = {'staked' : collat, 'want': collat_address, 'borrowed' : 0, 'rate' : borrow_rate, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][collat_address].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, collat_address)] = collat_address
        

    if int(stakes['borrowed']['loan_amount']) > 0:
        borrow_address = 'uusd'
        borrow_token_meta = await TokenMetaData('uusd', mongodb, lcd_client, session).lookup()
        borrowed = from_custom(int(stakes['borrowed']['loan_amount']), borrow_token_meta['token_decimal'])


        poolNest[poolKey]['userData'][borrow_address] = {'staked' : 0, 'want': borrow_address, 'borrowed' : borrowed, 'rate' : 0, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][borrow_address].update(borrow_token_meta)
        poolIDs['%s_%s_want' % (poolKey, borrow_address)] = borrow_address

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_anchor_staking(wallet, lcd_client, vaults, farm_id, mongodb, network, session):
    poolKey = farm_id
    pending_token = 'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76'
    tasks = []
    response_key = []

    #Staked UST
    tasks.append(lcd_client.wasm.contract_query('terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu', { "balance": { "address": wallet }}))
    response_key.append(f'stakedust')
    #LP Staking
    tasks.append(lcd_client.wasm.contract_query('terra1897an2xux840p9lrh6py3ryankc6mspw49xse3', { "staker_info": { "staker": wallet }}))
    response_key.append(f'lpstaking')
    #Staked ANC
    tasks.append(lcd_client.wasm.contract_query('terra1f32xyep306hhcxxxf7mlyh0ucggc00rm2s9da5', { "staker": { "address": wallet }}))
    response_key.append(f'ancstaking')
    #bLUNA Rewards
    tasks.append(lcd_client.wasm.contract_query('terra17yap3mhph35pcwvhza38c2lkj7gzywzy05h7l0', { "accrued_rewards": { "address": wallet }}))
    response_key.append(f'blunarewards')
    #bETH Rewards
    tasks.append(lcd_client.wasm.contract_query('terra1939tzfn4hn960ychpcsjshu8jds3zdwlp8jed9', { "accrued_rewards": { "address": wallet }}))
    response_key.append(f'bethrewards')
    #Unbonded LUNA
    tasks.append(lcd_client.wasm.contract_query('terra1mtwph2juhj0rvjz7dy92gvl6xvukaxu8rfv8ts', { "withdrawable_unbonded": { "address": wallet }}))
    response_key.append(f'unlocked')
    #Unbonded LUNA
    tasks.append(lcd_client.wasm.contract_query('terra1mtwph2juhj0rvjz7dy92gvl6xvukaxu8rfv8ts', { "unbond_requests": { "address": wallet }}))
    response_key.append(f'requests')
    #Collateral Rewards
    tasks.append(lcd_client.wasm.contract_query('terra1sepfj7s0aeg5967uxnfk4thzlerrsktkpelm5s', { "borrower_info": { "borrower": wallet }}))
    response_key.append(f'collateral')

    stakes = dict(zip(response_key, await asyncio.gather(*tasks)))

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    total_pending_rewards = int(stakes['blunarewards']['rewards']) + int(stakes['bethrewards']['rewards'])
    total_unbonded_luna = sum([int(x[1]) for x in stakes['requests']['requests']])

    if int(stakes['stakedust']['balance']) > 0:
        want_token = 'terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu'
        want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        staked = from_custom(int(stakes['stakedust']['balance']), want_token_meta['token_decimal'])

        poolNest[poolKey]['userData'][f'stakedusd'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][f'stakedusd'].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, 'stakedusd')] = want_token

    if int(stakes['lpstaking']['bond_amount']) > 0:
        want_token = 'terra1gecs98vcuktyfkrve9czrpgtg0m3aq586x6gzm'
        want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        staked = from_custom(int(stakes['lpstaking']['bond_amount']), want_token_meta['token_decimal'])

        poolNest[poolKey]['userData'][f'lpstaking'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][f'lpstaking'].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, 'lpstaking')] = want_token

        reward_token_meta = await TokenMetaData(pending_token, mongodb, lcd_client, session).lookup()
        reward_token_0 = {'pending': from_custom(int(stakes['lpstaking']['pending_reward']), reward_token_meta['token_decimal']), 'symbol' : reward_token_meta['tkn0s'], 'token' : pending_token}
        poolNest[poolKey]['userData'][f'lpstaking']['gambitRewards'].append(reward_token_0)

    if int(stakes['ancstaking']['balance']) > 0:
        want_token = pending_token
        want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        staked = from_custom(int(stakes['ancstaking']['balance']), want_token_meta['token_decimal'])

        poolNest[poolKey]['userData'][f'ancstaking'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][f'ancstaking'].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, 'ancstaking')] = want_token

    if total_pending_rewards > 0:
        want_token = 'uusd'
        want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        staked = 0

        poolNest[poolKey]['userData'][f'total_pending_rewards'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][f'total_pending_rewards'].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, 'total_pending_rewards')] = want_token

        reward_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        reward_token_0 = {'pending': from_custom(total_pending_rewards, reward_token_meta['token_decimal']), 'symbol' : reward_token_meta['tkn0s'], 'token' : want_token}
        poolNest[poolKey]['userData'][f'total_pending_rewards']['gambitRewards'].append(reward_token_0)

    if int(float(stakes['collateral']['pending_rewards'])) > 0:
        want_token = pending_token
        want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        staked = 0

        poolNest[poolKey]['userData'][f'total_collateral_rewards'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][f'total_collateral_rewards'].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, 'total_collateral_rewards')] = want_token

        reward_token_meta = await TokenMetaData(pending_token, mongodb, lcd_client, session).lookup()
        reward_token_0 = {'pending': from_custom(int(float(stakes['collateral']['pending_rewards'])), reward_token_meta['token_decimal']), 'symbol' : reward_token_meta['tkn0s'], 'token' : pending_token}
        poolNest[poolKey]['userData'][f'total_collateral_rewards']['gambitRewards'].append(reward_token_0)
            
    if total_unbonded_luna > 0:
        want_token = 'terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp'
        want_token_meta = await TokenMetaData(want_token, mongodb, lcd_client, session).lookup()
        staked = from_custom(int(total_unbonded_luna), want_token_meta['token_decimal'])

        poolNest[poolKey]['userData'][f'total_unbonded_luna'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData'][f'total_unbonded_luna'].update(want_token_meta)
        poolIDs['%s_%s_want' % (poolKey, 'total_unbonded_luna')] = want_token

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_kujira_staking(wallet, lcd_client, vaults, farm_id, mongodb, network, session):
    poolKey = farm_id

    tasks = []
    tasks.append(lcd_client.wasm.contract_query('terra1w7gtx76rs7x0e27l7x2e88vcr52tp9d8g4umjz', {"staked":{"address": wallet}}))
    tasks.append(lcd_client.wasm.contract_query('terra1cf9q9lq7tdfju95sdw78y9e34a6qrq3rrc6dre', {"staker_info":{"staker": wallet}}))
    tasks.append(lcd_client.wasm.contract_query('terra1w7gtx76rs7x0e27l7x2e88vcr52tp9d8g4umjz', {"claims":{"address": wallet}}))

    user_balances = await asyncio.gather(*tasks)

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    pending_kuji = sum([int(x['amount']) for x in user_balances[2]['claims']])

    if int(user_balances[0]['stake']) > 0 or pending_kuji > 0:
        want_token = 'terra1xfsdgcemqwxp4hhnyk4rle6wr22sseq7j07dnn'
        staked = from_custom(user_balances[0]['stake'], 6)

        poolNest[poolKey]['userData']['terra1w7gtx76rs7x0e27l7x2e88vcr52tp9d8g4umjz'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData']['terra1w7gtx76rs7x0e27l7x2e88vcr52tp9d8g4umjz'].update(await TokenMetaData(want_token, mongodb, lcd_client, session).lookup())
        poolIDs['%s_%s_want' % (poolKey, 'terra1w7gtx76rs7x0e27l7x2e88vcr52tp9d8g4umjz')] = want_token
        
        pending_total = from_custom(pending_kuji, 6)

        reward_token_0 = {'pending': pending_total, 'symbol' : 'KUJI', 'token' : want_token, 'decimal' : 6}
        poolNest[poolKey]['userData']['terra1w7gtx76rs7x0e27l7x2e88vcr52tp9d8g4umjz']['gambitRewards'].append(reward_token_0)
    
    if int(user_balances[1]['bond_amount']) > 0:
        want_token = 'terra1cmqv3sjew8kcm3j907x2026e4n0ejl2jackxlx'
        staked = from_custom(user_balances[1]['bond_amount'], 6)

        poolNest[poolKey]['userData']['terra1cf9q9lq7tdfju95sdw78y9e34a6qrq3rrc6dre'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolNest[poolKey]['userData']['terra1cf9q9lq7tdfju95sdw78y9e34a6qrq3rrc6dre'].update(await TokenMetaData(want_token, mongodb, lcd_client, session).lookup())
        poolIDs['%s_%s_want' % (poolKey, 'terra1cf9q9lq7tdfju95sdw78y9e34a6qrq3rrc6dre')] = want_token
        
        reward_token_0 = {'pending': from_custom(user_balances[1]['pending_reward'], 6), 'symbol' : 'KUJI', 'token' : 'terra1xfsdgcemqwxp4hhnyk4rle6wr22sseq7j07dnn', 'decimal' : 6}
        poolNest[poolKey]['userData']['terra1cf9q9lq7tdfju95sdw78y9e34a6qrq3rrc6dre']['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None