from .multicall import Call, Multicall, parsers
from .networks import WEB3_NETWORKS
from . import template_helpers

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

def getElevenNerve(wallet):
    calls = []
    nrvCheck = {x['id'] : x for x in extNerve}
    for each in extNerve:
        calls.append(Call(each['earnedTokenAddress'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (each['id']), from_wei]]))
        if each['earnedTokenAddress'] == '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f':
            ethNRV = getETHrewards(wallet)
        else:
            calls.append(Call(each['earnedTokenAddress'], ['pendingEleven(address)(uint256)', wallet], [['%s_pending' % (each['id']), from_wei]]))
            calls.append(Call(each['earnedTokenAddress'], ['pendingNerve(address)(uint256)', wallet], [['%s_pendingNerve' % (each['id']), from_wei]]))
        
    stakes = { **Multicall(calls)(), **ethNRV }

    filteredStakes = []
    elevenNest = {'0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A': 
    { 'userData': { } } }

    poolIDs = {}
    
    nerveMultipler = Call('0x54f4D5dd6164B99603E77C8E13FFC3B239F63147', 'getPricePerFullShare()(uint256)', [['nrvPPS', from_wei]])()
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')

            if addPool[0] not in elevenNest['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData']:
                elevenNest['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': nrvCheck[addPool[0]]['earnedTokenAddress'], 'nerveMultipler' : nerveMultipler['nrvPPS'] }
                poolIDs['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A_%s_want' % (addPool[0])] = nrvCheck[addPool[0]]['earnedTokenAddress']
            else:    
                elevenNest['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, elevenNest    
    else:
        return None

def getETHrewards(wallet):
    
    router = setPool(nrvethABI, Web3.toChecksumAddress('0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f'))
    pendingEleven = router.pendingEleven(Web3.toChecksumAddress(wallet)).call({'from' : Web3.toChecksumAddress(wallet)})
    pendingNerve = router.pendingNerve(Web3.toChecksumAddress(wallet)).call({'from' : Web3.toChecksumAddress(wallet)})

    return { 'nerveeth_pending': from_wei(pendingEleven), 'nerveeth_pendingNerve' : from_wei(pendingNerve) }

def getHorizonStakes(wallet):
    
    calls = []
    hznCheck = {x['id'] : x for x in extHorizon}
    for each in extHorizon:
        calls.append(Call(each['stakingContract'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (each['id']), from_wei]]))
        calls.append(Call(each['stakingContract'], ['earned(address)(uint256)', wallet], [['%s_pending' % (each['id']), from_wei]]))
        #calls.append(Call(each['stakingContract'], ['rewardsToken()(address)'], [['%s_rewardToken' % (each['id']), None]]))
    stakes = Multicall(calls)()

    filteredStakes = []
    hznNest = {'0xHorizon': 
    { 'userData': { 
        } 
    }}

    poolIDs = {}
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')
            if addPool[0] not in hznNest['0xHorizon']['userData']:
                hznNest['0xHorizon']['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': hznCheck[addPool[0]]['tokenAddress'] }
                poolIDs['0xHorizon_%s_want' % (addPool[0])] = hznCheck[addPool[0]]['tokenAddress']
            else:
                hznNest['0xHorizon']['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, hznNest     
    else:
        return None

def getBeefyBoosts(wallet):
    
    calls = []
    for each in bBoostsCheck:
        poolID = bBoostsCheck[each]['earnContractAddress']
        calls.append(Call(poolID, ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (each), from_wei]]))
        calls.append(Call(poolID, ['earned(address)(uint256)', wallet], [['%s_pending' % (each), from_wei]]))
    stakes = Multicall(calls)()

    filteredStakes = []
    boostNest = {'0xBeefy': 
    { 'userData': { 
        } 
    }}

    poolIDs = {}
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')
            if addPool[0] not in boostNest['0xBeefy']['userData']:
                boostNest['0xBeefy']['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want' : bBoostsCheck[addPool[0]]['tokenAddress'], 'boostedReward': bBoostsCheck[addPool[0]]['earnedOracleId'], 'rewardSymbol' : bBoostsCheck[addPool[0]]['earnedToken'] }
                poolIDs['0xBeefy_%s_want' % (addPool[0])] = bBoostsCheck[addPool[0]]['tokenAddress']
            else:
                boostNest['0xBeefy']['userData'][addPool[0]].update({addPool[1]: stakes[stake]})


    if len(poolIDs) > 0:
        return poolIDs, boostNest     
    else:
        return None

def getMoneyPot(wallet):
    
    calls = []

    moneyTokens = [{'token' : '0xe9e7cea3dedca5984780bafc599bd69add087d56', 'symbol' : 'BUSD'}, {'token' : '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', 'symbol' : 'WBNB' }]
    potContract = '0x020Fa682C4249eF7d242691d04cf6Ff0A609B941'
    u235 = '0x28d2E3BB1Ec54A6eE8b3Bee612F03A85d3Ec0C0c'
    lenMoney = len(moneyTokens)

    for i, each in enumerate(moneyTokens):
        calls.append(Call(potContract, ['pendingTokenRewardsAmount(address,address)(uint256)', each['token'], wallet], [['%s_pending' % (each['symbol']), from_wei]]))
        if i+1 == lenMoney:
            calls.append(Call(u235, ['balanceOf(address)(uint256)', wallet], [['u235balance', from_wei]]))
    stakes = Multicall(calls)()

    filteredStakes = []
    moneyNest = {'0xF3ca45633B2b2C062282ab38de74EAd2B76E8800': 
    { 'userData': { 
        } 
    }}

    return stakes

def getbingoBoard(wallet):

    bingoKey = '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08'
    boardRoom = '0xc9525f505040fecd4b754407De72d7bCf5a8f78F'
    nestName = 'bingoBoard'
    calls = []

    calls.append(Call(boardRoom, ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (nestName), from_wei]]))
    calls.append(Call(boardRoom, ['earned(address)(uint256)', wallet], [['%s_pending' % (nestName), from_wei]]))
        
    stakes=Multicall(calls)()

    filteredStakes = []
    
    bingoNest = {bingoKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in bingoNest[bingoKey]['userData']:
                bingoNest[bingoKey]['userData'][nestName] = {addPool[1]: stakes[stake], 'want': '0x53F39324Fbb209693332B87aA94D5519A1a49aB0' }
                poolIDs['%s_%s_want' % (bingoKey, nestName)] = '0x53F39324Fbb209693332B87aA94D5519A1a49aB0'
            else:    
                bingoNest[bingoKey]['userData'][nestName].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, bingoNest    
    else:
        return None

def getIronFinance(wallet, vaults, farm_id, network):
    
    poolKey = farm_id
    calls = []

    for vault in vaults:
        breakdown = vault.split('_')
        masterchef = breakdown[0]
        pool_id = int(breakdown[1])

        calls.append(Call(masterchef, ['userInfo(uint256,address)(uint256)', pool_id, wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(masterchef, ['poolInfo(uint256)(address)', pool_id], [[f'{vault}_want', None]]))
        calls.append(Call(masterchef, ['pendingReward(uint256,address)(uint256)', pool_id, wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(masterchef, ['rewardToken()(address)'], [[f'{vault}_rewardToken', None]]))
    
    stakes=Multicall(calls, network)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                pool_key = f'{breakdown[0]}_{breakdown[1]}'
                no_unders = f'{breakdown[0]}-{breakdown[1]}'
                staked = stakes[each]
                want_token = stakes[f'{pool_key}_want']
                pending = stakes[f'{pool_key}_pending']
                reward_token = stakes[f'{pool_key}_rewardToken']
                reward_symbol = vaults[pool_key]['rewardToken'].upper()

                poolNest[poolKey]['userData'][no_unders] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol}
                poolIDs['%s_%s_want' % (poolKey, no_unders)] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getDiamondHands(wallet):

    poolKey = '0xDiamondHands'
    calls = []

    for pool in diamonds:
        if pool['contract'] in ['0xe5476aA8f9b0D22580bb7c796c53493BAD942Db4', '0xF26a92c8281e83Ec7E09C64C70e649e74dB22Ad4', '0x22210d79264B77c3545eb3E12415796AE2CA108c']:
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % (pool['contract']), from_wei]])) 
        else:
            calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['stakedFunction']), 0, wallet], [['%s_staked' % (pool['contract']), from_wei]]))
            calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['rewardFunction']), 0, wallet], [['%s_pending' % (pool['contract']), from_wei]]))        
    stakes=Multicall(calls)()

    filteredStakes = []


    
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolCheck = {x['contract'] : x for x in diamonds}
    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'rewardToken' : poolCheck[addPool[0]]['rewardToken'], 'rewardSymbol' : poolCheck[addPool[0]]['rewardSymbol'] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getApoyield(wallet):

    poolKey = '0xe87DE2d5BbB4aF23c665Cf7331eC744B020883bB'
    calls = []

    for pool in thirdParty:
        # if pool['contract'] == '0x9Ef9a563C5639349e211450Bfcf59E7f7453ab90':
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % (pool['contract']), from_wei]])) 
        # else:
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['stakedFunction']), 0, wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['rewardFunction']), 0, wallet], [['%s_pending' % (pool['contract']), from_wei]]))        
    stakes=Multicall(calls)()

    filteredStakes = []


    
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolCheck = {x['contract'] : x for x in thirdParty}
    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'rewardToken' : poolCheck[addPool[0]]['rewardToken'], 'rewardSymbol' : poolCheck[addPool[0]]['rewardSymbol'] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getFuelVaults(wallet):

    poolKey = '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56'
    calls = []

    for pool in fuelVaults:
        # if pool['contract'] == '0x9Ef9a563C5639349e211450Bfcf59E7f7453ab90':
        calls.append(Call(pool, ['%s(address)(uint256)' % ('balanceOf'), wallet], [['%s_staked' % (pool), from_wei]])) 
        # else:
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['stakedFunction']), 0, wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['rewardFunction']), 0, wallet], [['%s_pending' % (pool['contract']), from_wei]]))        
    stakes=Multicall(calls)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getBunnyPools(wallet):

    poolKey = '0xPancakeBunny'
    bunnyHop = '0xb3c96d3c3d643c2318e4cdd0a9a48af53131f5f4'
    calls = []

    for pool in bunnies:
        contract = pool
        calls.append(Call(bunnyHop, ['infoOfPool(address,address)((address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256))', contract, wallet], [['%s_userInfo' % (contract), parseBunny]]))
        calls.append(Call(contract, ['rewardsToken()(address)'], [['%s_rewardToken' % (contract), None]]))
        calls.append(Call(contract, ['stakingToken()(address)'], [['%s_want' % (contract), None]]))        
    
    stakes=Multicall(calls)()

    filteredStakes = []

    #print(stakes)
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolIDs = {}

    for stake in stakes:
        if 'userInfo' in stake:
            if stakes[stake]['userInfo']['staked'] > 0:
                #print(stake)
                addPool = stake.split('_')
                poolWant = addPool[0] + '_' + 'want'
                poolReward = addPool[0] + '_' + 'rewardToken'
                #print(addPool[0], stakes[poolReward])
                #print(addPool[0],stakes[poolReward])
                try:
                    rewardSy = Call(stakes[poolReward], 'symbol()(string)', [['symbol', None]])()
                except:
                    rewardSy = {'symbol' : '?'}     
                if addPool[0] not in poolNest[poolKey]['userData']:
                    poolNest[poolKey]['userData'][addPool[0]] = stakes[stake]['userInfo']
                    poolIDs['%s_%s_want' % (poolKey, addPool[0])] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['want'] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardToken'] = stakes[poolReward]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardSymbol'] = rewardSy['symbol']
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getWaultLocked(wallet):

    poolKey = '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D'
    locked = '0x52a2b3beafa46ba51a4792793a7447396d09423f'
    lockedx = '0x06747f6501611baE9dD054cCC37ad076e9Ea2465'
    lockedwex = '0xF4E0943C1D55e883E3C6310CD641970A36a7f870'
    lockedEuler = '0x38Ab2128327107D075a13E6Ed66Bd6184E4Cc20c'
    wault = '0x6ff2d9e5891a7a7c554b80e0d1b791483c78bce9'
    waultx = '0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21'
    euler = '0x3920123482070c1a2dff73aad695c60e7c6f6862'
    wex='0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90'
    lockedVaults = 3
    lockedxVaults = 1
    lockedeVaults = 1
    lockedwexVaults = 1
    calls = []

    for i in range(0,lockedVaults):
        calls.append(Call(locked, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['wault%s_staked' % (i), from_wei]])) 
        calls.append(Call(locked, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['wault%s_pending' % (i), from_wei]]))

    for i in range(0,lockedxVaults):
        calls.append(Call(lockedx, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['waultx%s_staked' % (i), from_wei]]))
        calls.append(Call(lockedx, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['waultx%s_pending' % (i), from_wei]]))

    for i in range(0,lockedeVaults):
        calls.append(Call(lockedEuler, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['euler%s_staked' % (i), from_wei]]))
        calls.append(Call(lockedEuler, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['euler%s_pending' % (i), from_wei]]))

    for i in range(0,lockedwexVaults):
        calls.append(Call(lockedwex, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['wex%s_staked' % (i), from_wei]]))
        calls.append(Call(lockedwex, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['wex%s_pending' % (i), from_wei]]))
    


    stakes=Multicall(calls)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        addPool = stake.split('_')
        if 'staked' in addPool[1]:
            if stakes[stake] > 0:
                poolType = addPool[0][:-1]

                if poolType == 'wault':
                    wanted = wault
                    rewarded = wault
                    rewardSym = 'WAULT'
                elif poolType == 'waultx':
                    wanted = waultx
                    rewarded = waultx
                    rewardSym = 'WAULTX'
                elif poolType == 'euler':
                    wanted = euler 
                    rewarded = euler
                    rewardSym = 'EULER'
                elif poolType == 'wex':
                    wanted = wex 
                    rewarded = wex
                    rewardSym = 'WEX'

                if addPool[0] not in poolNest[poolKey]['userData']:
                    poolNest[poolKey]['userData'][addPool[0]] = {'staked': stakes[stake], 'want': wanted, 'rewardToken' : rewarded, 'rewardSymbol' : rewardSym, 'pending' : stakes['%s_pending' % (addPool[0])] }
                    poolIDs['%s_%s_want' % (poolKey, addPool[0])] = wanted

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getValueSafes(wallet):
    poolKey = '0xd56339F80586c08B7a4E3a68678d16D37237Bd96'
    calls = []

    for pool in getvSafes():
        calls.append(Call(pool['id'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % pool['id'], from_wei]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_user_firebird_vaults(wallet):
    poolKey = '0xE9a8b6ea3e7431E6BefCa51258CB472Df2Dd21d4'
    calls = []

    for pool in get_firebird_vaults():
        calls.append(Call(pool['id'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % pool['id'], from_wei]]))
    
    stakes=Multicall(calls, WEB3_NETWORKS['matic'])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getGambits(wallet):

    poolKey = '0xGambit'
    calls = []

    for pool in gambits:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        for i, reward in enumerate(pool['rewards']):
            calls.append(Call(reward['yieldTracker'], ['%s(address)(uint256)' % (reward['rewardFunction']), wallet], [['%s_pending_%s_%s' % (pool['contract'], reward['symbol'], reward['rewardToken']), from_wei]]))

    stakes=Multicall(calls)()

    filteredStakes = []


    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    poolCheck = {x['contract'] : x for x in gambits}

    #print(stakes)
    for stake in stakes:
    # if stakes[stake] > 0:
        addPool = stake.split('_')       
        if addPool[0] not in poolNest[poolKey]['userData']:
            poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'gambitRewards' : [] }
            poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
        else:
            if 'pending' in addPool[1]:     
                poolNest[poolKey]['userData'][addPool[0]]['gambitRewards'].append({addPool[1]: stakes[stake], 'symbol' : addPool[2], 'token' : addPool[3]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getTaoDao(wallet):
    poolKey = '0xTaodao'
    calls = []

    for pool in dao:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % pool['stakeToken'], from_tao if pool['decimal'] == 9 else from_wei ]]))
        if pool['rewardFunction'] is not None:
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % pool['stakeToken'], from_tao]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getPop(wallet):
    poolKey = '0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0'
    epsChef = '0xcce949De564fE60e7f96C85e55177F8B9E4CF61b'
    wantToken = '0x049d68029688eAbF473097a2fC38ef61633A3C7A'
    calls = []

    calls.append(Call(epsChef, ['%s(uint256,address)(uint256)' % ('userInfo'), 2, wallet], [['%s_staked' % (epsChef), from_wei ]]))
    calls.append(Call(epsChef, ['%s(uint256,address)(uint256)' % ('claimableReward'), 2, wallet], [['%s_pending' % (epsChef), from_wei]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': wantToken }
                poolIDs['%s_%s_want' % (poolKey, epsChef)] = wantToken
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getFortress(wallet):

    faiVault = '0x066807c7B22c6c0a7fa370A2cA812e5Fc22DBef6'
    poolKey = '0xFortress'
    calls = []

    for fort in forts:
        calls.append(Call(fort, ['%s(address)((uint256,uint256,uint256,uint256))' % ('getAccountSnapshot'), wallet], [['%s_staked' % (fort), parseAccountSnapshot ]]))
        if fort != '0xE24146585E882B6b59ca9bFaaaFfED201E4E5491':
            calls.append(Call(fort, 'underlying()(address)', [['%s_want' % fort, None]]))
    
    calls.append(Call(faiVault, ['%s(address)(uint256)' % ('userInfo'), wallet], [['%s_staked' % (faiVault), from_wei ]]))
    calls.append(Call(faiVault, ['%s(address)(uint256)' % ('pendingFTS'), wallet], [['%s_pending' % (faiVault), from_wei ]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    #print(stakes)
    for stake in stakes:
        if 'staked' in stake:
                if stakes[stake] > 0:
                    addPool = stake.split('_')
                    if addPool[0] == '0xE24146585E882B6b59ca9bFaaaFfED201E4E5491':
                        want = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
                        pending = 0
                    elif addPool[0] == '0x066807c7B22c6c0a7fa370A2cA812e5Fc22DBef6':
                        want = '0x10a450A21B79c3Af78fb4484FF46D3E647475db4'
                        pending = stakes['%s_pending' % addPool[0]]
                    else:
                        want = stakes['%s_want' % addPool[0]]
                        pending = 0      
                    if addPool[0] not in poolNest[poolKey]['userData']:
                        poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': want, 'pending' : pending }
                        poolIDs['%s_%s_want' % (poolKey, addPool[0])] = want


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getDYP(wallet):

    poolKey = '0xDYP'
    calls = []

    for pool in dypPools:
        calls.append(Call(pool, ['%s(address)(uint256)' % ('depositedTokens'), wallet], [['%s_staked' % (pool), from_wei ]]))
        calls.append(Call(pool, ['%s(address)(uint256)' % ('getPendingDivsEth'), wallet], [['%s_pending' % (pool), from_wei ]]))
        calls.append(Call(pool, 'trustedDepositTokenAddress()(address)', [['%s_want' % pool, None]]))

    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    rewarded = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
    rewardSym = 'WBNB'
    for stake in stakes:
        if 'staked' in stake:
                if stakes[stake] > 0:
                    addPool = stake.split('_')
                    want = stakes['%s_want' % addPool[0]]
                    pending = stakes['%s_pending' % addPool[0]]    
                    
                    if addPool[0] not in poolNest[poolKey]['userData']:
                        poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': want, 'pending' : pending, 'rewardToken' : rewarded, 'rewardSymbol' : rewardSym }
                        poolIDs['%s_%s_want' % (poolKey, addPool[0])] = want


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getMerlinPools(wallet):

    poolKey = '0xMerlin'
    bunnyHop = '0xfF8B299da344AD8Ff399b4CBd3db01c0c7264bdf'
    calls = []

    for pool in magic:
        contract = pool
        calls.append(Call(bunnyHop, ['infoOfPool(address,address)((address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256))', contract, wallet], [['%s_userInfo' % (contract), parseMerlin]]))
        calls.append(Call(contract, ['rewardsToken()(address)'], [['%s_rewardToken' % (contract), None]]))
        calls.append(Call(contract, ['stakingToken()(address)'], [['%s_want' % (contract), None]]))
        #calls.append(Call(contract, ['priceShare()(uint256)'], [['%s_getPricePerFullShare' % (contract), from_wei]]))
                
    
    stakes=Multicall(calls)()

    filteredStakes = []

    #print(stakes)
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolIDs = {}

    for stake in stakes:
        if 'userInfo' in stake:
            if stakes[stake]['userInfo']['staked'] > 0:
                #print(stake)
                addPool = stake.split('_')
                poolWant = addPool[0] + '_' + 'want'
                poolReward = addPool[0] + '_' + 'rewardToken'
                #pricePer = addPool[0] + '_' + 'getPricePerFullShare'
                #print(addPool[0], stakes[poolReward])
                #print(addPool[0],stakes[poolReward])
                try:
                    rewardSy = Call(stakes[poolReward], 'symbol()(string)', [['symbol', None]])()
                except:
                    rewardSy = {'symbol' : '?'}     
                if addPool[0] not in poolNest[poolKey]['userData']:
                    poolNest[poolKey]['userData'][addPool[0]] = stakes[stake]['userInfo']
                    poolIDs['%s_%s_want' % (poolKey, addPool[0])] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['want'] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardToken'] = stakes[poolReward]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardSymbol'] = rewardSy['symbol']
                    #poolNest[poolKey]['userData'][addPool[0]]['getPricePerFullShare'] = stakes[pricePer]
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_eleven_hodls(wallet, eleven_hodls):

    poolKey = '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A'
    calls = []

    for eleven_token in eleven_hodls:
        if '11' in eleven_token['earnedToken'] and eleven_token['network'] == 'bsc' and eleven_token['earnedTokenAddress'] not in ['0x3Ed531BfB3FAD41111f6dab567b33C4db897f991', '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f', '0x0D5BaE8f5232820eF56D98c04B8F531d2742555F', '0xDF098493bB4eeE18BB56BE45DC43BD655a27E1A9', '0x27DD6E51BF715cFc0e2fe96Af26fC9DED89e4BE8', '0x025E2e9113dC1f6549C83E761d70E647c8CDE187']:
            pool_id = eleven_token['earnedTokenAddress']
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', from_wei]]))
    
    stakes=Multicall(calls)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_beefy_matic_stakes(wallet):

    poolKey = '0xBeefyMatic'
    calls = []

    for token in beefy_matic_pools:
        pool_id = token['earnedTokenAddress']
        if pool_id == '0xE71f3C11D4535a7F8c5FB03FDA57899B2C9c721F':
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', from_six]]))
        else:
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', from_wei]]))

    stakes=Multicall(calls, WEB3_NETWORKS['matic'])()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_beefy_style_stakes(wallet,vaults,farm_id,network):

    poolKey = farm_id
    calls = []

    for vault in vaults:
        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))

    stakes= await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_eleven_hodls_polygon(wallet, eleven_hodls):

    poolKey = '0xD109D9d6f258D48899D7D16549B89122B0536729'
    calls = []

    for eleven_token in eleven_hodls:
        if '11' in eleven_token['earnedToken'] and eleven_token['network'] == 'polygon' and eleven_token['earnedTokenAddress'] not in ['0x0FFb84A4c29147Bd745AAe0330f4F6f4Cb716c92','0x3Ed531BfB3FAD41111f6dab567b33C4db897f991', '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f', '0x0D5BaE8f5232820eF56D98c04B8F531d2742555F', '0xDF098493bB4eeE18BB56BE45DC43BD655a27E1A9', '0x27DD6E51BF715cFc0e2fe96Af26fC9DED89e4BE8', '0x025E2e9113dC1f6549C83E761d70E647c8CDE187']:
            pool_id = eleven_token['earnedTokenAddress']
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', None]]))
    
    stakes=Multicall(calls, WEB3_NETWORKS['matic'])()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 1:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                
                wanted_token = addPool[0]
                
                if wanted_token.lower() in ['0x4f22aaf124853fdaed264746e9d7b21b2df86b90'.lower(),'0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'.lower(), '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'.lower(), '0x299FA358763037657Bea14825CD06ff390C2a634'.lower()]:
                    staked_value = from_custom(stakes[stake], 6)
                elif wanted_token.lower() in ['0x62b728ced61313f17c8b784740aa0fc20a8cffe7'.lower(),'0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6'.lower(), '0xF84BD51eab957c2e7B7D646A3427C5A50848281D'.lower(), '0xa599e42a39dea9230a8164dec8316c2522c9ccd7'.lower()]:
                    staked_value = from_custom(stakes[stake], 8)
                elif wanted_token.lower() in ['0x033d942A6b495C4071083f4CDe1f17e986FE856c'.lower()]:
                    staked_value = from_custom(stakes[stake], 4)
                else:
                    staked_value = from_wei(stakes[stake])
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: staked_value, 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_nuts(wallet):

    poolKey = '0xSquirrel'
    calls = []

    for pool in nuts:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        for i, reward in enumerate(pool['rewards']):
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (reward['rewardFunction']), wallet], [['%s_pending_%s_%s' % (pool['contract'], reward['symbol'], reward['rewardToken']), from_wei]]))

    stakes=Multicall(calls)()

    filteredStakes = []


    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    poolCheck = {x['contract'] : x for x in nuts}

    #print(stakes)
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'gambitRewards' : [] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
            else:
                if 'pending' in addPool[1]:     
                    poolNest[poolKey]['userData'][addPool[0]]['gambitRewards'].append({addPool[1]: stakes[stake], 'symbol' : addPool[2], 'token' : addPool[3]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_adamant_funds(wallet):

    poolKey = '0xAdamant'
    calculator = '0x80d8dad3753887731BA8f92AEe84Df371B6A7790'
    minter = '0xAAE758A2dB4204E1334236Acd6E6E73035704921'
    strat_vaults_calls = []
    
    addy_mints = Call(minter, 'addyPerProfitEth()(uint256)', None, WEB3_NETWORKS['matic'])()
    
    # for deployer in adamant_deployers:
    #         contract = deployer['address']
    #         loop_over = deployer['poolLength']
    #         for lp in range(0,loop_over):
    #             strat_vaults_calls.append(Call(contract, ['deployedVaults(uint256)((address,address))', lp], [[f'{contract}_{lp}_addresses', None]]))
    
    # strat_vaults = Multicall(strat_vaults_calls, WEB3_NETWORKS['matic'])()
    # strat_vaults['0x3253e956a0e70a6b65D170511A84e93e16848dae_0_addresses'] = ('0x3253e956a0e70a6b65d170511a84e93e16848dae', '0xdf70e065ec14ea9a85cf99ec776bf83271ad11a9')
    # strat_vaults['0xD06D816DAae530f5Aa94903e89501f20BEBA6fB2_0_addresses'] = ('0x6eaf123d49f4e233f8283a69bd59a2443650f322', '0x9dd816c8966f0cdcf9c05ceed830163ff46080ff')
    # strat_vaults['0xD06D816DAae530f5Aa94903e89501f20BEBA6fB2_1_addresses'] = ('0x92c7277240e9ac0e82df455e0c808622664a79c3', '0xc872df0159b062c05c99ce6d3ef482980fb2a6a4')

    adamant_user_info = []
    strat_vaults = json.loads(requests.get('https://raw.githubusercontent.com/eepdev/vaults/main/current_vaults.json').text)
    for item in strat_vaults:
        strategy = item['strategyAddress']
        vault = item['vaultAddress']

        adamant_user_info.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        adamant_user_info.append(Call(vault, ['getPendingReward(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
        adamant_user_info.append(Call(vault, ['getRewardMultiplier()(uint256)'], [[f'{vault}_multiplier', None]]))
        adamant_user_info.append(Call(strategy, ['want()(address)'], [[f'{vault}_want', None]]))
    



    user_data = Multicall(adamant_user_info, WEB3_NETWORKS['matic'])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    

    for each in user_data:
        if 'staked' in each:
            if user_data[each] > 0:
                breakdown = each.split('_')
                staked = user_data[each]
                pending = user_data[f'{breakdown[0]}_pending']
                want_token = user_data[f'{breakdown[0]}_want']
                reward_multi = user_data[f'{breakdown[0]}_multiplier']
                reward_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

                extra_data = Multicall(
                    
                [Call(breakdown[0], ['getRatio()(uint256)'], [['getPricePerFullShare', from_wei]]),
                Call(calculator,['valueOfAsset(address,uint256)(uint256)', reward_token, pending], [['real_pending', None]])], WEB3_NETWORKS['matic'])()

                ppfs = extra_data['getPricePerFullShare']
                actual_staked = staked * ppfs
                actual_pending = extra_data['real_pending']
                 

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked, 'pending': (from_wei((actual_pending * addy_mints)) * reward_multi) / 1000 }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

    addy_eth = get_addy_eth(wallet, addy_mints)
    if addy_eth is not None:
        poolIDs.update(addy_eth[0])
        poolNest['0xAdamant']['userData'].update(addy_eth[1]['0xAdamant']['userData'])

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_addy_eth(wallet, minting_rate=None):

    poolKey = '0xAdamant'
    
    adamant_user_info = []

    vault = '0xF7661EE874Ec599c2B450e0Df5c40CE823FEf9d3'

    adamant_user_info.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
    adamant_user_info.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
    adamant_user_info.append(Call(vault, ['stakingToken()(address)'], [[f'{vault}_want', None]]))
    
    user_data = Multicall(adamant_user_info, WEB3_NETWORKS['matic'])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    
    for each in user_data:
        if 'staked' in each:
            if user_data[each] > 0:
                breakdown = each.split('_')
                staked = user_data[each]
                pending = user_data[f'{breakdown[0]}_pending']
                want_token = user_data[f'{breakdown[0]}_want']
                actual_pending = from_wei(pending * minting_rate)
                 

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending': actual_pending }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_quickswap_style(wallet, vaults, farm_id, network, want_function=None):
    
    if want_function is None:
        want_function = 'stakingToken'
    else:
        want_function = want_function

    poolKey = farm_id
    calls = []

    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(vault, [f'{want_function}()(address)'], [[f'{vault}_want', None]]))
    
    stakes=Multicall(calls, network)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                pending = stakes[f'{breakdown[0]}_pending']
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending': pending }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_quickswap_style_multi(wallet, vaults, farm_id, network):
    
    poolKey = farm_id
    calls = []

    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        #calls.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(vault, ['stakingToken()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, ['bothTokensEarned(address)(address[])', wallet], [[f'{vault}_rewardtokens', None]]))
    
    stakes=Multicall(calls, network)()

    reward_calls = []

    for each in stakes:
        if 'rewardtokens' in each:
            for i, token in enumerate(stakes[each]):
                vault = each.split('_')[0]
                reward_calls.append(Call(vault, ['earned(address,address)(uint256)', wallet, token], [[f'{vault}_{i}_{token}_pending', from_wei]]))
                reward_calls.append(Call(token, 'symbol()(string)', [[f'{vault}_{i}_{token}_symbol', None]]))


    rewards=Multicall(reward_calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_tokens = stakes[f'{breakdown[0]}_rewardtokens']
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i, rtoken in enumerate(reward_tokens):
                    reward_address = rtoken
                    reward_key = f'{breakdown[0]}_{i}_{rtoken}'
                    pending_amount = rewards[f'{reward_key}_pending']
                    symbol = rewards[f'{reward_key}_symbol']
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append({'pending': pending_amount, 'symbol' : symbol, 'token' : reward_address})
                    
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_vault_style(wallet, vaults, farm_id, network, _pps=None, _stake=None, _strict=None, want_token=None):

    if _pps == None:
        pps = 'getRatio'
    else:
        pps = _pps
    
    if _stake is None:
        stake = 'balanceOf'
    else:
        stake = _stake

    if _strict is None:
        strict = False
    else:
        strict = _strict
    
    if want_token is None:
        want_token = 'token'
    else:
        want_token = want_token

    poolKey = farm_id
    calls = []
    for vault in vaults:
        if vault == '0x992Ae1912CE6b608E0c0d2BF66259ab1aE62A657':
            calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', from_custom, 9]]))
        else:
            calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        
        if vault in ['0xa6Fc07819eE785C120aB765981b313D71b4FF406']:
            calls.append(Call(vault, [f'wmatic()(address)'], [[f'{vault}_want', None]]))
        elif vault in ['0x929e9dEfF1070bA346FB45EB841F035dCC29D131','0x5cD44E5Aa00b8D77c8c7102E530d947AB86c9551','0xA0FfC3b52c315B00ea3DaFbC3094059D46aA5Daf','0x2bffD2442C4509c32Cc4bcACC4aC85B89A0076BA','0x6F5be5d7Ecdd948dB34C111C06AEa1E2fE2D2c2F','0xCf2CF4B53B62022F81Ad73cAe04E433936eca6c0']:
            calls.append(Call(vault, [f'want()(address)'], [[f'{vault}_want', None]]))
        else:
            calls.append(Call(vault, [f'{want_token}()(address)'], [[f'{vault}_want', None]]))
        
        calls.append(Call(vault, [f'{pps}()(uint256)'], [[f'{vault}_getPricePerFullShare', from_wei]]))
    
    stakes=Multicall(calls, network, _strict=strict)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = template_helpers.get_token_list_decimals(vaults,farms[farm_id]['network'],False)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                token_decimal = 18 if breakdown[0] not in token_decimals else token_decimals[breakdown[0]]
                staked = from_custom(stakes[each], token_decimal)
                want_token = stakes[f'{breakdown[0]}_want']
                price_per = stakes[f'{breakdown[0]}_getPricePerFullShare']
                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'getPricePerFullShare' : price_per, 'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_pancake_bunny_clones(wallet, vaults, network_id, dashboard_contract, calculator, farm_id, native_symbol, _decode=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        if _decode is None:
            decode = 'address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256'
        else:
            decode = 'address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256'

        for vault in vaults:
                calls.append(Call(dashboard_contract, ['profitOfPool(address,address)((uint256,uint256))', vault, wallet], [[f'{vault}_pendings', parse_profit_of_pool]]))
                calls.append(Call(dashboard_contract, [f'infoOfPool(address,address)(({decode}))', vault, wallet], [[f'{vault}_userinfo', parse_pancake_bunny_info]]))
                calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'rewardsToken()(address)'], [[f'{vault}_rewardtoken', None]]))


        stakes=Multicall(calls, network)()

        filteredStakes = []

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'userinfo' in each:
                if stakes[each]['balance'] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]['principal']
                    want_token = stakes[f'{breakdown[0]}_want']
                    pendings = stakes[f'{breakdown[0]}_pendings']
                    reward_token = '0xD016cAAe879c42cB0D74BB1A265021bf980A7E96' if stakes[f'{breakdown[0]}_rewardtoken'] == '0x6b70f0136a7e2bd1fa945566b82b208760632b2e' else stakes[f'{breakdown[0]}_rewardtoken']

                    try:
                        staked_symbol = Call(reward_token, 'symbol()(string)', None, network)()
                    except:
                        reward_token = Call(reward_token, [f'rewardsToken()(address)'], [[f'rewardtoken', None]], network)()['rewardtoken']
                        staked_symbol = Call(reward_token, 'symbol()(string)', None, network)()

                    staked_single_price = Call(calculator, ['valueOfAsset(address,uint256)((uint256,uint256))', reward_token, one_token], [[f'prices', parse_profit_of_pool]], network)()

                    if breakdown[0] in ['0x4Ad69DC9eA7Cc01CE13A37F20817baC4bF0De1ba','0x7a526d4679cDe16641411cA813eAf7B33422501D']:
                        poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : [{'pending': pendings[0], 'symbol' : native_symbol, 'token' : farms[poolKey]['rewardToken']}]}
                    else:
                        poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : [{'pending': pendings[1], 'symbol' : native_symbol, 'token' : farms[poolKey]['rewardToken']}, {'pending': pendings[0], 'symbol' : staked_symbol, 'token' : reward_token, 'valueOfAsset' : staked_single_price['prices'][1]}]}
                        
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_syrup_pools(wallet, pools, network_id, farm_id, staked=None, reward=None, pending_reward=None, user_info=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        staked = 'stakedToken' if staked is None else staked
        reward = 'rewardToken' if reward is None else reward
        pending_reward = 'pendingReward' if pending_reward is None else pending_reward
        user_info = 'userInfo' if user_info is None else user_info

        for pool in pools:
            calls.append(Call(pool, [f'{user_info}(address)(uint256)', wallet], [[f'{pool}_staked', from_wei]]))
            calls.append(Call(pool, [f'{pending_reward}(address)(uint256)', wallet], [[f'{pool}_pending', None]]))
            calls.append(Call(pool, [f'{staked}()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'{reward}()(address)'], [[f'{pool}_rewardtoken', None]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pendings = stakes[f'{breakdown[0]}_pending']
                    reward_token = stakes[f'{breakdown[0]}_rewardtoken']

                    reward_calls = []
                    reward_calls.append(Call(reward_token, 'symbol()(string)', [[f'symbol', None]]))
                    reward_calls.append(Call(reward_token, 'decimals()(uint256)', [[f'decimal', None]]))

                    reward_data=Multicall(reward_calls, network)()

                    reward_symbol = reward_data['symbol']
                    reward_decimal = reward_data['decimal']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : from_custom(pendings, reward_decimal), 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'rewardDecimal' : reward_decimal}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_adamant_stakes(wallet, farm_id):
    
    poolKey = farm_id
    staking_contract = '0x920f22E1e5da04504b765F8110ab96A20E6408Bd'
    addy_rewards = setPool(reward_abi, '0x920f22E1e5da04504b765F8110ab96A20E6408Bd', 'matic')
    wallet = Web3.toChecksumAddress(wallet)

    stakes= Call(staking_contract, ['totalBalance(address)(uint256)', wallet], [[f'totalBalance', from_wei]], WEB3_NETWORKS['matic'])()


    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}


    if stakes['totalBalance'] > 0:

        staked = stakes['totalBalance']
        reward_tokens = addy_rewards.claimableRewards(wallet).call()
        want_token = '0xc3FdbadC7c795EF1D6Ba111e06fF8F16A20Ea539'

        poolNest[poolKey]['userData'][staking_contract] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, staking_contract)] = want_token

        for i, rtoken in enumerate(reward_tokens):
            if rtoken[1] > 0: 
                reward_address = rtoken[0]
                pending_amount = from_wei(rtoken[1])
                symbol = Call(reward_address, 'symbol()(string)', [[f'symbol', None]], WEB3_NETWORKS['matic'])()['symbol']
                poolNest[poolKey]['userData'][staking_contract]['gambitRewards'].append({'pending': pending_amount, 'symbol' : symbol, 'token' : reward_address})
                    
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_apeswap(wallet, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        mini_ape = '0x54aff400858Dcac39797a81894D9920f16972D1D'
        mini_complex = '0x1F234B1b83e21Cb5e2b99b4E498fe70Ef2d6e3bf'
        pool_length = Call(mini_ape, [f'poolLength()(uint256)'],None,network)()
        

        for pid in range(0,pool_length):
            calls.append(Call(mini_ape, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}_staked', from_wei]]))
            calls.append(Call(mini_ape, [f'pendingBanana(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pending', from_wei]]))
            calls.append(Call(mini_ape, [f'lpToken(uint256)(address)', pid], [[f'{pid}_want', None]]))
            calls.append(Call(mini_complex, [f'pendingToken(uint256,address)(uint256)', pid, wallet], [[f'{pid}_complexp', from_wei]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pending = stakes[f'{breakdown[0]}_pending']
                    complex = stakes[f'{breakdown[0]}_complexp']
                    reward_token = '0x5d47baba0d66083c52009271faf3f50dcc01023c'
                    native_symbol = 'BANANA'
                    complex_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
                    staked_symbol = 'WMATIC'


                    poolNest[poolKey]['userData'][int(breakdown[0])] = {'want': want_token, 'staked' : staked, 'gambitRewards' : [{'pending': pending, 'symbol' : native_symbol, 'token' : reward_token}, {'pending': complex, 'symbol' : staked_symbol, 'token' : complex_token}]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_single_masterchef(wallet,farm_id,network_id,farm_data):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        if 'poolFunction' not in farm_data:
            pool_function = 'poolLength'
        else:
            pool_function = farm_data['poolFunction']
        
        pool_length = Call(farm_data['masterChef'], [f'{pool_function}()(uint256)'],None,network)() 
        staked_function = farm_data['stakedFunction']
        pending_function = farm_data['pendingFunction']
        reward_token = farm_data['rewardToken']
        reward_symbol = farm_data['rewardSymbol']
        if 'wantFunction' not in farm_data:
            want_function = 'poolInfo'
        else:
            want_function = farm_data['wantFunction']

        for pid in range(0,pool_length):
            calls.append(Call(farm_data['masterChef'], [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', from_wei]]))
            calls.append(Call(farm_data['masterChef'], [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_pending', from_wei]]))
            calls.append(Call(farm_data['masterChef'], [f'{want_function}(uint256)(address)', pid], [[f'{pid}ext_want', None]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pending = stakes[f'{breakdown[0]}_pending']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_acryptos_style_boosts(wallet, vaults, farm_id, network, caller, pfunc):

    poolKey = farm_id
    calls = []

    for vault in vaults:
        calls.append(Call(caller, [f'userInfo(address,address)(uint256)',vault,wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(caller, [f'{pfunc}(address,address)(uint256)',vault,wallet], [[f'{vault}_pending', from_wei]]))
    
    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = breakdown[0]
                pending = stakes[f'{breakdown[0]}_pending']
                poolNest[poolKey]['userData'][f'{breakdown[0]}-BOOST'] = {'want': want_token, 'staked' : staked, 'pending'  : pending}
                poolIDs['%s_%s_want' % (poolKey, f'{breakdown[0]}-BOOST')] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_pyq_triple_staking(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'stakes(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
                calls.append(Call(vault, [f'lqtyToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'getPendingETHGain(address)(uint256)', wallet], [[f'{vault}_pendingETH', from_wei]]))
                calls.append(Call(vault, [f'getPendingLQTYGain(address)(uint256)', wallet], [[f'{vault}_pendingLQTY', from_wei]]))
                calls.append(Call(vault, [f'getPendingLUSDGain(address)(uint256)', wallet], [[f'{vault}_pendingLUSD', from_wei]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]

                    reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingETH'], 'symbol' : 'WMATIC', 'token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'}
                    reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingLUSD'], 'symbol' : 'PUSD', 'token' : '0x9af3b7dc29d3c4b1a5731408b6a9656fa7ac3b72'}
                    reward_token_2 = {'pending': stakes[f'{breakdown[0]}_pendingLQTY'], 'symbol' : 'PYQ', 'token' : '0x5a3064cbdccf428ae907796cf6ad5a664cd7f3d8'}

                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_2)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

def get_pyq_double_staking(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'getCompoundedLUSDDeposit(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
                calls.append(Call(vault, [f'lusdToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'getDepositorETHGain(address)(uint256)', wallet], [[f'{vault}_pendingETH', from_wei]]))
                calls.append(Call(vault, [f'getDepositorLQTYGain(address)(uint256)', wallet], [[f'{vault}_pendingLQTY', from_wei]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]

                    reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingETH'], 'symbol' : 'WMATIC', 'token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'}
                    reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingLQTY'], 'symbol' : 'PYQ', 'token' : '0x5a3064cbdccf428ae907796cf6ad5a664cd7f3d8'}

                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

def get_pyq_trove(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'getTroveColl(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
                calls.append(Call(vault, [f'getTroveDebt(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : 'PUSD', 'token' : '0x9af3b7dc29d3c4b1a5731408b6a9656fa7ac3b72'}
                    want_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

def get_mai_graph(wallet):
    url = 'https://api.thegraph.com/subgraphs/name/gallodasballo/mai-finance-quick'
    obj = """{
    vaults(where: {account: "%s"}) {
    id
    account {
      id
    }
    deposited
    borrowed
        }
    }"""
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    vaults = json.loads(requests.post(url, json={'query': obj % (wallet.lower()), 'variables': None}, headers=headers).text)['data']['vaults']
    
    staked = 0
    pending = 0

    for each in vaults:
        staked += from_wei(int(each['deposited']))
        pending += from_wei(int(each['borrowed']))

    return {'VAULTS_staked' : staked, 'VAULTS_pending' : pending}

def get_mai_cvault(wallet, farm_id):
        poolKey = farm_id

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        stakes = get_mai_graph(wallet)

        if stakes['VAULTS_staked'] > 0:
            staked = stakes['VAULTS_staked']
            reward_token_0 = {'pending': stakes['VAULTS_pending'], 'symbol' : 'miMATIC', 'token' : '0xa3Fa99A148fA48D14Ed51d610c367C61876997F1'.lower()}
            want_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

            poolNest[poolKey]['userData']['VAULTS'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
            poolIDs['%s_%s_want' % (poolKey, 'VAULTS')] = want_token

            poolNest[poolKey]['userData']['VAULTS']['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_wault_pools(wallet, pools, network_id, farm_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for pool in pools:
            calls.append(Call(pool, [f'userInfo(address)(uint256)', wallet], [[f'{pool}_staked', from_wei]]))
            calls.append(Call(pool, [f'pendingRewards(address)(uint256)', wallet], [[f'{pool}_pending', from_wei]]))
            calls.append(Call(pool, [f'pool()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'rewardToken()(address)'], [[f'{pool}_rewardtoken', None]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pendings = stakes[f'{breakdown[0]}_pending']
                    reward_token = stakes[f'{breakdown[0]}_rewardtoken']
                    reward_symbol = Call(reward_token, 'symbol()(string)', [[f'symbol', None]], network)()['symbol']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pendings, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_farmhero_staking(wallet,vault,network,farm_id):

    calls = []
    poolKey = farm_id

    calls.append(Call(vault, [f'totalBalance(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
    calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes = Multicall(calls,WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']
                w3_instance = setPool(multi_fee_v2,vault,network)
                reward_tokens = w3_instance.claimableRewards(wallet).call()

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i, rtoken in enumerate(reward_tokens):
                    reward_address = rtoken[0]
                    if rtoken[1] > 1:
                        pending_amount = from_wei(rtoken[1])
                        symbol = Call(reward_address, [f'symbol()(string)'], [[f'symbol', None]],WEB3_NETWORKS[network])()['symbol']
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append({'pending': pending_amount, 'symbol' : symbol, 'token' : reward_address})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_fh_pools(wallet,vaults,network,farm_id,stake_func=None,reward_func=None):
    
    poolKey = farm_id

    if stake_func is None:
        stake_func = 'stakeToken'
    
    if reward_func is None:
        reward_func = 'rewardToken'

    
    calls = []
    for pool in vaults:
        #Catch BIFI pool
        if pool == '0x453D4Ba9a2D594314DF88564248497F7D74d6b2C':
            calls.append(Call(pool, ['balanceOf(address)(uint256)', wallet], [[f'{pool}_staked', parsers.from_wei]]))
            calls.append(Call(pool, [f'earned(address)(uint256)', wallet], [[f'{pool}_pending', parsers.from_wei]]))
            calls.append(Call(pool, [f'bifi()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'wbnb()(address)'], [[f'{pool}_rewardtoken', None]]))
        else:
            calls.append(Call(pool, ['balanceOf(address)(uint256)', wallet], [[f'{pool}_staked', parsers.from_wei]]))
            calls.append(Call(pool, [f'earned(address)(uint256)', wallet], [[f'{pool}_pending', parsers.from_wei]]))
            calls.append(Call(pool, [f'{stake_func}()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'{reward_func}()(address)'], [[f'{pool}_rewardtoken', None]])) 

    stakes = await Multicall(calls,WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_token = stakes[f'{breakdown[0]}_rewardtoken']
                try:
                    reward_token_want = await Call(reward_token, 'want()(address)', [[f'want', None]], WEB3_NETWORKS[network])()['want']
                    reward_token_pps =  await Call(reward_token, 'getPricePerFullShare()(uint256)', [[f'pps', parsers.from_wei]], WEB3_NETWORKS[network])()['pps']
                    reward_token_symbol =  await Call(reward_token_want, 'symbol()(string)', [[f'symbol', None]], WEB3_NETWORKS[network])()['symbol']
                    reward_token = reward_token_want
                except:
                    reward_token_symbol = await Call(reward_token, 'symbol()(string)', [[f'symbol', None]], WEB3_NETWORKS[network])()['symbol']
                    reward_token_pps =  1
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'] * reward_token_pps, 'symbol' : reward_token_symbol, 'token' : reward_token}
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_quickswap_lps(wallet,farm_id):

    poolKey = farm_id

    liquidityPositions = call_graph('https://api.thegraph.com/subgraphs/name/sameepsi/quickswap03', {'operationName' : 'liquidityPositions', 'query' : quickswap_lps.query, 'variables' : {'user': wallet.lower()}})

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for lp in liquidityPositions['data']['liquidityPositions']:
        if float(lp['liquidityTokenBalance']) > 0:
                staked = float(lp['liquidityTokenBalance'])
                want_token = lp['pair']['id']

                poolNest[poolKey]['userData'][f'QSLP{want_token}'] = {'want': want_token, 'staked' : staked, 'pending' : 0}
                poolIDs['%s_%s_want' % (poolKey, f'QSLP{want_token}')] = want_token
                    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_aperocket_space_pool(wallet,vaults,rewardtoken,network,farm_id,profit_offset):
    
    calls = []
    poolKey = farm_id
    
    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'SPACE()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'profitOf(address)((uint256,uint256,uint256))', wallet], [[f'{vault}_pending', parse_spacepool, profit_offset]]))

    stakes = Multicall(calls,WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_token = rewardtoken['token']
                reward_token_symbol = rewardtoken['symbol']
                reward_token_decimal = rewardtoken['decimal']
                reward_token_0 = {'pending': from_custom(stakes[f'{breakdown[0]}_pending'],reward_token_decimal), 'symbol' : reward_token_symbol, 'token' : reward_token}
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_balancer_user_pools(wallet,pools,network_id,farm_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for pool in pools:
            calls.append(Call(pool, [f'balanceOf(address)(uint256)', wallet], [[f'{pool}_staked', from_wei]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = breakdown[0]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : 0}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_pickle_chef(wallet,farm_id,network_id,chef,rewarder):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]
    pool_length = Call(chef, [f'poolLength()(uint256)'],None,network)() 

    for pid in range(0,pool_length):
        calls.append(Call(chef, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}_staked', from_wei]]))
        calls.append(Call(chef, [f'pendingPickle(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pendingPickle', from_wei]]))
        calls.append(Call(rewarder, [f'pendingToken(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pendingMatic', from_wei]]))
        calls.append(Call(chef, [f'lpToken(uint256)(address)', pid], [[f'{pid}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                pid = int(breakdown[0])
                staked = stakes[each]
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingPickle'], 'symbol' : 'PICKLE', 'token' : '0x2b88ad57897a8b496595925f43048301c37615da'}
                reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingMatic'], 'symbol' : 'WMATIC', 'token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][pid] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][pid]['gambitRewards'].append(reward_token_0)
                poolNest[poolKey]['userData'][pid]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_curve_gauage(wallet,farm_id,network_id,gauages,rewards=None):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    if rewards is None:
        rewards = ['0x172370d5Cd63279eFa6d502DAB29171933a610AF', '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270']

    for guage in gauages:
        calls.append(Call(guage, [f'balanceOf(address)(uint256)', wallet], [[f'{guage}_staked', from_wei]]))
        for i,each in enumerate(rewards):
            calls.append(Call(guage, [f'claimable_reward_write(address,address)(uint256)', wallet,each], [[f'{guage}_pending{i}', from_wei]]))
        calls.append(Call(guage, [f'lp_token()(address)'], [[f'{guage}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()
    print(stakes)
    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i,each in enumerate(rewards):
                    symbol = Call(each, [f'symbol()(string)'], _w3=network)()
                    reward_gambit = {'pending': stakes[f'{breakdown[0]}_pending{i}'], 'symbol' : symbol, 'token' : each}

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_gambit)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_telx_single(wallet,farm_id,network_id,vaults):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'earned(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(vault, [f'rewardsToken()(address)'], [[f'{vault}_rewardToken', None]]))
        calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_token = stakes[f'{breakdown[0]}_rewardToken']
                reward_symbol = Call(reward_token, [f'symbol()(string)'], _w3=network)()
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : reward_symbol, 'token' : reward_token}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_telx_double(wallet,farm_id,network_id,vaults):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'earnedA(address)(uint256)', wallet], [[f'{vault}_pendingA', from_wei]]))
        calls.append(Call(vault, [f'earnedB(address)(uint256)', wallet], [[f'{vault}_pendingB', from_wei]]))
        calls.append(Call(vault, [f'rewardsTokenA()(address)'], [[f'{vault}_rewardTokenA', None]]))
        calls.append(Call(vault, [f'rewardsTokenB()(address)'], [[f'{vault}_rewardTokenB', None]]))
        calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_tokenA = stakes[f'{breakdown[0]}_rewardTokenA']
                reward_tokenB = stakes[f'{breakdown[0]}_rewardTokenB']
                reward_symbolA = Call(reward_tokenA, [f'symbol()(string)'], _w3=network)()
                reward_symbolB = Call(reward_tokenB, [f'symbol()(string)'], _w3=network)()
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingA'], 'symbol' : reward_symbolA, 'token' : reward_tokenA}
                reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingB'], 'symbol' : reward_symbolB, 'token' : reward_tokenB}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_blackswan_stakes(wallet):
    
    poolKey = '0xBlackSwan'
    calls = []
    swan_lake = '0xE420CC7F8F0df0f145d146e9FDC8a4237660Eecb'
    distribution_pool = '0xbCf0734600AC0AcC1BaD85f62c0BE82BBC8Ca3B5'

    calls.append(Call(distribution_pool,['balanceOf(address)(uint256)', wallet], [[f'{distribution_pool}_staked', from_custom, 6]]))
    calls.append(Call(distribution_pool,['takeWithAddress(address)(uint256)', wallet], [[f'{distribution_pool}_pending', from_wei]]))
    calls.append(Call(distribution_pool,['token()(address)'], [[f'{distribution_pool}_want', None]]))
    calls.append(Call(swan_lake,['balanceOf(address)(uint256)', wallet], [[f'{swan_lake}_staked', from_wei]]))
    calls.append(Call(swan_lake,['_takeWithAddress(address)((uint256,uint256))', wallet], [[f'{swan_lake}_pending', None]]))
    calls.append(Call(swan_lake,['token()(address)'], [[f'{swan_lake}_want', None]]))

    stakes = Multicall(calls,WEB3_NETWORKS['matic'])()
    
    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_tokenA = '0xab7589dE4C581Db0fb265e25a8e7809D84cCd7E8'
                reward_symbolA = 'SWAN'
                reward_pendingA = stakes[f'{distribution_pool}_pending'] if breakdown[0] == distribution_pool else from_wei(stakes[f'{swan_lake}_pending'][1])
                reward_token_0 = {'pending': reward_pendingA , 'symbol' : reward_symbolA, 'token' : reward_tokenA}
                
                if breakdown[0] == swan_lake:
                    reward_tokenB = '0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'
                    reward_symbolB = 'SWAN-LP'
                    reward_pendingB = from_wei(stakes[f'{swan_lake}_pending'][0])
                    reward_token_1 = {'pending': reward_pendingB, 'symbol' : reward_symbolB, 'token' : reward_tokenB}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                if breakdown[0] == swan_lake:
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_feeder_style(wallet, vaults, network, farm_id):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for vault in vaults:
        calls.append(Call(vault, [f'userInfo(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'token()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'depositedTokenBalance(bool)(uint256)',False], [[f'{vault}_depositedTokenBalance', from_wei]]))
        calls.append(Call(vault, [f'totalShares()(uint256)'], [[f'{vault}_totalShares', from_wei]]))

    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']
                depositedTokenBalance = stakes[f'{breakdown[0]}_depositedTokenBalance']
                totalShares = stakes[f'{breakdown[0]}_totalShares']

                if want_token == '0x0000000000000000000000000000000000000000':
                    want_token = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked/totalShares * depositedTokenBalance, 'vault_receipt' : breakdown[0], 'contractAddress' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_sfeed(wallet,staking_token,receipt_token,network,farm_id):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for vault in staking_token:
        calls.append(Call(receipt_token, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', receipt_token], [[f'{vault}_totalDepositedFeeds', from_wei]]))
        calls.append(Call(receipt_token, [f'totalSupply()(uint256)'], [[f'{vault}_totalSFeedTokens', from_wei]]))

    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = breakdown[0]
                virtual_price = stakes[f'{breakdown[0]}_totalDepositedFeeds'] / stakes[f'{breakdown[0]}_totalSFeedTokens']           

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : receipt_token, 'getPricePerFullShare' : virtual_price}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

def get_vault_style_no_want(wallet, vaults, farm_id, network, _pps=None, _stake=None, _strict=None, want_token=None, pps_decimal=None):

    if _pps == None:
        pps = 'getRatio'
    else:
        pps = _pps
    
    if _stake is None:
        stake = 'balanceOf'
    else:
        stake = _stake

    if _strict is None:
        strict = False
    else:
        strict = _strict
    
    if want_token is None:
        want_token = 'token'
    else:
        want_token = want_token

    if pps_decimal is None:
        pps_decimal = 18
    else:
        pps_decimal = pps_decimal

    poolKey = farm_id
    calls = []
    for vault in vaults:
        calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))        
        calls.append(Call(vault, [f'{pps}()(uint256)'], [[f'{vault}_getPricePerFullShare', from_custom, pps_decimal]]))
    
    stakes=Multicall(calls, network, _strict=strict)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = want_token
                price_per = stakes[f'{breakdown[0]}_getPricePerFullShare']
                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'getPricePerFullShare' : price_per, 'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_lending_protocol(wallet,lending_vaults,farm_id,network):

    poolKey = farm_id
    calls = []

    for vault in lending_vaults:
        vault_address = vault['address']
        calls.append(Call(vault_address, [f'getAccountSnapshot(address)((uint256,uint256,uint256,uint256))', wallet], [[f'{vault_address}_accountSnapshot', None ]]))
        
    stakes=Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { }
     } }

    poolIDs = {}

    hash_map = {x['address'] : x for x in lending_vaults}

    for stake in stakes:
        if stakes[stake][1] > 0 or stakes[stake][2] > 0:
            addPool = stake.split('_')
            if addPool[0] not in poolNest[poolKey]['userData']:

                snapshot =  stakes[stake]
                underlying = hash_map[addPool[0]]['want']
                underlying_decimal = hash_map[addPool[0]]['decimal']           
                collat = from_custom(snapshot[1], underlying_decimal)
                collat_rate = hash_map[addPool[0]]['collat_rate']
                borrow = from_custom(snapshot[2], underlying_decimal)
                rate = from_wei(snapshot[3])
                poolNest[poolKey]['userData'][addPool[0]] = {'staked' : collat * rate, 'want': underlying, 'borrowed' : borrow, 'rate' : collat_rate}
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = underlying


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_just_pending(wallet,contracts,network,farm_id,reward_method,reward_token):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for contract in contracts:
        calls.append(Call(contract, [f'{reward_method}(address)(uint256)', wallet], [[f'{contract}_pending', from_wei]]))

    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'pending' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                pending = stakes[each]
                want_token = reward_token

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : 0, 'pending' : pending}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

def get_moneypot(wallet, rewards, farm_id, network_id, contract, token_pair=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for i,reward in enumerate(rewards):
            reward_address = reward['address']
            calls.append(Call(contract, [f'pendingTokenRewardsAmount(address,address)(uint256)', reward['address'], wallet], [[f'{reward_address}_{i}', from_wei]]))
        calls.append(Call(token_pair, [f'balanceOf(address)(uint256)', wallet], [[f'{token_pair}', from_wei]]))

        stakes=Multicall(calls, network)()

        print(stakes)

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        want_token = token_pair

        poolNest[poolKey]['userData'][contract] = {'want': token_pair, 'staked' : stakes[token_pair], 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, contract)] = want_token

        for i in range(0,len(rewards)):
            token = rewards[i]['address']
            token_id = f'{token}_{i}'
            pending = stakes[token_id]

            if pending > 0:
                reward_token_data = {'pending': pending, 'symbol' : rewards[i]['symbol'], 'token' : token}
                poolNest[poolKey]['userData'][contract]['gambitRewards'].append(reward_token_data)

        # for i,reward in enumerate(rewards):
        #     token = reward['address']
        #     token_id = f'{token}_{i}'
        #     pending = stakes[token_id]
        #     print(pending)
        #     if pending > 0:
        #         reward_token_data = {'pending': pending, 'symbol' : reward['symbol'], 'token' : reward['address']}
        #         poolNest[poolKey]['userData'][contract]['gambitRewards'].append(reward_token_data)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_zombie_masterchef(wallet,farm_id,network_id,chef):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        pool_function = 'poolLength'
        pool_length = Call(chef, [f'{pool_function}()(uint256)'],None,network)() 
        
        staked_function = 'userInfo'
        pending_function = 'pendingZombie'
        reward_token = '0x50ba8bf9e34f0f83f96a340387d1d3888ba4b3b5'
        reward_symbol = 'ZMBE'
        want_function = 'poolInfo'

        for pid in range(0,pool_length):
            calls.append(Call(chef, [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', from_wei]]))
            calls.append(Call(chef, [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_pending', from_wei]]))
            calls.append(Call(chef, [f'{want_function}(uint256)((address,uint256,uint256,uint256,uint256,bool,bool,address,address,uint256,uint256,uint256,uint256))', pid], [[f'{pid}ext_want', parser.parse_zombie_pool]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']['lp_token']
                    pending = stakes[f'{breakdown[0]}_pending']
                    zombie_override = True if stakes[f'{breakdown[0]}_want']['is_grave'] and stakes[f'{breakdown[0]}_want']['requires_rug'] else False

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'zombieOverride' : zombie_override, 'contractAddress' : chef}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_pool_lengths(wallet, pools, network, farm_info):

    calls = []
    network_conn = WEB3_NETWORKS[network]

    for pool in pools:
        
        if 'poolLength' in farm_info:
            pool_length = farm_info['poolLength']
        else:
            pool_length = 'poolLength'

        
        if farm_info['stakedFunction'] is not None and pool.lower() not in ['0x97bdB4071396B7f60b65E0EB62CE212a699F4B08'.lower(), '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7'.lower()]:
            calls.append(Call(pool, f'{pool_length}()(uint256)', [[pool, None]]))
        elif pool.lower() in ['0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7'.lower()]:
            calls.append(Call(pool, 'getRewardsLength()(uint256)', [[pool, None]]))

    if '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' : 5}
        }
    else:
        poolLengths = await Multicall(calls, network_conn)()

    return poolLengths

async def get_only_staked(wallet, pools, network, farm_info):
    
    calls = []
    network_conn = WEB3_NETWORKS[network]
    final = pools[1]
    
    for pool in pools[0]:    
        stakedFunction = farm_info['stakedFunction']
        rng = 1 if pool in ['0x0895196562C7868C5Be92459FaE7f877ED450452'] else 0
        end = 3 if pool in [''] else pools[0][pool]
        for i in range(rng, end):
            if pool == '0xd1b3d8ef5ac30a14690fbd05cf08905e1bf7d878' and i == 2:
                continue
            elif pool == '0x0895196562C7868C5Be92459FaE7f877ED450452' and i == 331:
                continue
            elif pool == '0x95030532D65C7344347E61Ab96273B6B110385F2' and i == 43:
                continue
            elif pool == '' and i == 0:
                continue
            else:
                if pool == '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4': 
                    calls.append(Call(pool, ['%s(address,uint256)(uint256)' % (stakedFunction), wallet, i], [['%s_%s' % (pool, i), None]]))
                else:
                    calls.append(Call(pool, ['%s(uint256,address)(uint256)' % (stakedFunction), i, wallet], [['%s_%s' % (pool, i), None]]))
    
    stakes = await Multicall(calls, network_conn)()     

    filteredStakes = []
    for stake in stakes:
        if stakes[stake] > 2:
            addPool = stake.split('_')
            if addPool[0] == '0x1FcCEabCd2dDaDEa61Ae30a2f1c2D67A05fDDa29':
                final[addPool[0]]['userData'][int(addPool[1])] = {'staked': 0}
            else:
                final[addPool[0]]['userData'][int(addPool[1])] = {'staked': stakes[stake]}
            filteredStakes.append({stake : stakes[stake]})
    
    return filteredStakes, final

async def get_pending_want(wallet, stakes, network, farm_info):

    final = stakes[1]
    network_conn = WEB3_NETWORKS[network]
    calls = []

    for stake in stakes[0]:
        key = next(iter(stake.keys()))
        address = key.split('_')[0]
        poolID = int(key.split('_')[1])

        if farm_info['pendingFunction'] is not None:
            pendingFunction = farm_info['pendingFunction']
            if address not in ['0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904', '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4']:
                calls.append(Call(address, ['%s(uint256,address)(uint256)' % (pendingFunction), poolID, wallet], [['%s_%s_pending' % (address, poolID), None]]))
            
            if address in ['0x0B29065f0C5B9Db719f180149F0251598Df2F1e4']:
                calls.append(Call(address, [f'{pendingFunction}(address,uint256)(uint256)', wallet, poolID], [['%s_%s_pending' % (address, poolID), None]]))


        if farm_info['stakedFunction'] is not None:
            if address in ['0xF1F8E3ff67E386165e05b2B795097E95aaC899F0', '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3', '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d', '0x6685C8618298C04b6E42dDAC06400cc5924e917e']:
                calls.append(Call(address, ['poolInfo(uint256)((uint256,address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parsers.parse_wanted_slot_two]]))
            elif address == '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7':
                calls.append(Call(address, ['rewardsInfo(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))
            elif address == '0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904':
                calls.append(Call(address, ['poolInfo(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))
            elif address in ['0x0769fd68dFb93167989C6f7254cd0D766Fb2841F','0x67da5f2ffaddff067ab9d5f025f8810634d84287']:
                calls.append(Call(address, ['lpToken(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))         
            else:
                calls.append(Call(address, ['poolInfo(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))

        if address == '0x89d065572136814230A55DdEeDDEC9DF34EB0B76':
            calls.append(Call(address, ['poolInfo(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))


    stakes = await Multicall(calls, network_conn)()
        

    ##Should pull token decimals here
    token_decimals = await template_helpers.get_token_list_decimals(stakes,network,True)

    if type(stakes) is dict:
        for stake in stakes:
                addPool = stake.split('_')
                
                if addPool[2] == 'want':
                    
                    raw_stakes = final[addPool[0]]['userData'][int(addPool[1])]['staked']
                    final[addPool[0]]['userData'][int(addPool[1])]['rawStakes'] = raw_stakes
                    
                    wanted_token = stakes[stake]
                    wanted_decimal = 18 if wanted_token not in token_decimals else token_decimals[wanted_token]
                    # if wanted_token.lower() in ['0x4f22aaf124853fdaed264746e9d7b21b2df86b90'.lower(),'0x5b8d0f56ea36270bb0eaf5fcbd72ea5ab98ba4af'.lower(),'0xe4b3c431e29b15978556f55b2cd046be614f558d'.lower(),'0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'.lower(), '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'.lower(), '0x299FA358763037657Bea14825CD06ff390C2a634'.lower(), '0x2e1a74a16e3a9f8e3d825902ab9fb87c606cb13f'.lower(), '0x18d755c981a550b0b8919f1de2cdf882f489c155'.lower()]:
                    #     final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 6)
                    # elif wanted_token.lower() in ['0x62b728ced61313f17c8b784740aa0fc20a8cffe7'.lower(),'0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6'.lower(), '0xF84BD51eab957c2e7B7D646A3427C5A50848281D'.lower(), '0xa599e42a39dea9230a8164dec8316c2522c9ccd7'.lower(), '0x97ebf27d40d306ad00bb2922e02c58264b295a95'.lower()]:
                    #     final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 8)
                    # elif wanted_token.lower() in ['0x033d942A6b495C4071083f4CDe1f17e986FE856c'.lower()]:
                    #     final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 4)
                    # elif wanted_token.lower() in ['0x13748d548d95d78a3c83fe3f32604b4796cffa23'.lower()]:
                    #     final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 9)
                    # else:
                    final[addPool[0]]['userData'][int(addPool[1])]['staked'] = parsers.from_custom(raw_stakes, wanted_decimal)


                # if addPool[0] in ['0xF1F8E3ff67E386165e05b2B795097E95aaC899F0', '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3', '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d', '0x6685C8618298C04b6E42dDAC06400cc5924e917e'] and addPool[2] == 'want':                   
                #     final[addPool[0]]['userData'][int(addPool[1])][addPool[2]] = stakes[stake][1]
                #     stakes[stake] == stakes[stake][1]
                #     stakes.update({stake: stakes[stake][1]})
                else:
                    final[addPool[0]]['userData'][int(addPool[1])][addPool[2]] = stakes[stake]

    else:
        stakes = {}
    return stakes, final

async def get_traditional_masterchef(wallet, pools, network, farm_info, return_obj):
    pool_lengths = await get_pool_lengths(wallet, pools, network, farm_info)
    only_staked = await get_only_staked(wallet, (pool_lengths, return_obj), network, farm_info)
    pending_wants = await get_pending_want(wallet, only_staked, network, farm_info)

    return pending_wants
