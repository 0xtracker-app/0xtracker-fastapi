from multicall import Call, Multicall
import multicall.parsers as parsers
from networks import WEB3_NETWORKS
import template_helpers

def get_multireward_masterchef(wallet,farm_id,network_id,farm_data):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        if 'poolFunction' not in farm_data:
            pool_function = 'poolLength'
        else:
            pool_function = farm_data['poolFunction']
        
        pool_length = Call(farm_data['masterChef'], [f'{pool_function}()(uint256)'],None,network)() 
        staked_function = farm_data['stakedFunction']
        if 'wantFunction' not in farm_data:
            want_function = 'poolInfo'
        else:
            want_function = farm_data['wantFunction']

        for pid in range(0,pool_length):
            calls.append(Call(farm_data['masterChef'], [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', None]]))
            calls.append(Call(farm_data['masterChef'], [f'{want_function}(uint256)(address)', pid], [[f'{pid}ext_want', None]]))
            for i,each in enumerate(farm_data['rewards']):
                reward_decimal = each['rewardDecimal'] in each if 'rewardDecimal' in each else 18
                pending_function = each['function']
                calls.append(Call(farm_data['masterChef'], [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_pending{i}', parsers.from_custom, reward_decimal]]))

        stakes=Multicall(calls, network, _strict=False)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_decimals = template_helpers.get_token_list_decimals(stakes,network_id,True)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : parsers.from_custom(staked,wanted_decimal), 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    for i, reward_token in enumerate(farm_data['rewards']):
                        if f'{breakdown[0]}_pending{i}' in stakes:
                            pending_reward = stakes[f'{breakdown[0]}_pending{i}']
                            if pending_reward > 0:
                                reward_token_0 = {'pending': pending_reward, 'symbol' : reward_token['rewardSymbol'], 'token' : reward_token['rewardToken']}
                                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_convex(wallet,farm_id,network_id,booster):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        
        pool_length = Call(booster, [f'poolLength()(uint256)'],None,network)() 

        for pid in range(0,pool_length):
            calls.append(Call(booster, [f'poolInfo(uint256)((address,address,address,address,address,bool))', pid], [[f'{pid}', None]]))


        pool_info=Multicall(calls, network)()

        token_list = [pool_info[each][3] for each in pool_info]

        calls = []

        for i,contract in enumerate(token_list):
            calls.append(Call(contract, [f'balanceOf(address)(uint256)', wallet], [[f'{i}_staked', parsers.from_wei]]))
            calls.append(Call(contract, [f'earned(address)(uint256)', wallet], [[f'{i}_earned', parsers.from_wei]]))
            calls.append(Call(contract, [f'rewards(address)(uint256)', wallet], [[f'{i}_rewards', parsers.from_wei]]))


        stakes = Multicall(calls, network)()      

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        cvx_total_supply = parsers.from_wei(Call('0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', f'totalSupply()(uint256)', _w3=network)()) 

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    key = int(breakdown[0])
                    staked = stakes[each]
                    want_token = pool_info[breakdown[0]][0]
                    pending_earned = stakes[f'{breakdown[0]}_earned']
                    pending_rewards = stakes[f'{breakdown[0]}_rewards']
                    pending_cvx = template_helpers.get_cvx_minted(pending_earned,cvx_total_supply)

                    poolNest[poolKey]['userData'][key] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    reward_token_0 = {'pending': pending_earned, 'symbol' : 'CRV', 'token' : '0xD533a949740bb3306d119CC777fa900bA034cd52'}
                    reward_token_1 = {'pending': pending_cvx, 'symbol' : 'CVX', 'token' : '0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B'}
                    #reward_token_0 = {'pending': pending_rewards, 'symbol' : reward_token['rewardSymbol'], 'token' : reward_token['rewardToken']}

                    poolNest[poolKey]['userData'][key]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][key]['gambitRewards'].append(reward_token_1)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_moonpot_contracts(wallet,farm_id,network_id,contracts):
        poolKey = farm_id

        network = WEB3_NETWORKS[network_id]

        reward_calls = []
        for each in contracts:
            reward_calls.append(Call(each['contract'], [f'rewardTokenLength()(uint256)'], [[each['contract'], None]]))

        reward_lengths = Multicall(reward_calls, network)()

        calls = []
        for each in contracts:
            pot_contract = each['contract']
            token_function = each['token_function']
            reward_length = reward_lengths[pot_contract]
            calls.append(Call(pot_contract, [f'userTotalBalance(address)(uint256)',wallet], [[f'{pot_contract}_staked', parsers.from_wei]]))
            calls.append(Call(pot_contract, [f'{token_function}()(address)'], [[f'{pot_contract}_want', None]]))
            for i in range(0,reward_length):
                calls.append(Call(pot_contract, [f'earned(address,uint256)(uint256)', wallet, i], [[f'{pot_contract}pending{i}', None]]))
                calls.append(Call(pot_contract, [f'rewardInfo(uint256)(address)', i], [[f'{pot_contract}rewardaddress{i}', None]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        reward_symbols_decimals = template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'rewardaddress' in x],network_id)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18
                    pot_contract = breakdown[0]
                    reward_length = reward_lengths[pot_contract]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    for i in range(0,reward_length):
                        if f'{pot_contract}pending{i}' in stakes:
                            pending_reward = stakes[f'{breakdown[0]}pending{i}']
                            pending_reward_contract = stakes[f'{breakdown[0]}rewardaddress{i}']
                            pending_reward_symbol = reward_symbols_decimals[f'{pending_reward_contract}_symbol']
                            pending_reward_decimal = reward_symbols_decimals[f'{pending_reward_contract}_decimals']
                            if pending_reward > 0:
                                reward_token_0 = {'pending': parsers.from_custom(pending_reward, pending_reward_decimal), 'symbol' : pending_reward_symbol, 'token' : pending_reward_contract}
                                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_traderjoe_masterchef(wallet,farm_id,network_id,masterchef):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        pool_length = Call(masterchef, [f'poolLength()(uint256)'],None,network)() 

        for pid in range(0,pool_length):
            calls.append(Call(masterchef, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', None]]))
            calls.append(Call(masterchef, [f'poolInfo(uint256)(address)', pid], [[f'{pid}ext_want', None]]))
            calls.append(Call(masterchef, [f'poolInfo(uint256)((address,uint256,uint256,uint256,address))', pid], [[f'{pid}ext_rewarder', None]]))
            calls.append(Call(masterchef, [f'pendingTokens(uint256,address)((uint256,address,uint256,uint256))', pid, wallet], [[f'{pid}ext_pending', None]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_decimals = template_helpers.get_token_list_decimals(stakes,network_id,True)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    rewarder = stakes[f'{breakdown[0]}_rewarder'][4]

                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : parsers.from_custom(staked,wanted_decimal), 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    pending_joe = stakes[f'{breakdown[0]}_pending'][0]
                    pending_address = stakes[f'{breakdown[0]}_pending'][1]
                    pending_reward = stakes[f'{breakdown[0]}_pending'][3]

                    if pending_joe > 0:
                        reward_token_0 = {'pending': parsers.from_custom(pending_joe, 18), 'symbol' : 'JOE', 'token' : '0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd'}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

                    if pending_reward > 0:
                        rti = Multicall(
                            [Call(pending_address, 'decimals()(uint8)', [['decimal', None]]),
                            Call(pending_address, 'symbol()(string)', [['symbol', None]])], _w3=network
                        )()
                        reward_token_0 = {'pending': parsers.from_custom(pending_reward, rti['decimal']), 'symbol' : rti['symbol'], 'token' : pending_address}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_vault_style_custom_pps(wallet, vaults, farm_id, network_id):

    poolKey = farm_id
    calls = []

    network=WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        calls.append(Call(vault, [f'depositToken()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'totalDeposits()(uint256)'], [[f'{vault}_totaldeposits', None]]))
        calls.append(Call(vault, [f'totalSupply()(uint256)'], [[f'{vault}_totalsupply', None]]))
    

    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = template_helpers.get_token_list_decimals(vaults,network_id,False)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                token_decimal = 18 if breakdown[0] not in token_decimals else token_decimals[breakdown[0]]
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']
                total_deposits = stakes[f'{breakdown[0]}_totaldeposits']
                total_supply = stakes[f'{breakdown[0]}_totalsupply']
                compounded_price = staked * total_deposits / total_supply
                real_staked = parsers.from_custom(compounded_price, token_decimal)


                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : real_staked,'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None