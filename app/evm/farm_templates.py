from xmlrpc.client import MultiCall
from .multicall import Call, Multicall, parsers
from .networks import WEB3_NETWORKS
from web3 import Web3
from . import template_helpers
from .thegraph import call_graph
from .utils import set_pool
from .user_config import parse_calls, parse_calls_master
from . import abi
import asyncio
import math
import numpy as np
from functools import reduce

async def get_multireward_masterchef(wallet,farm_id,network_id,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        farm_data = vaults

        if 'poolFunction' not in farm_data:
            pool_function = 'poolLength'
        else:
            pool_function = farm_data['poolFunction']
        
        pool_length = await Call(farm_data['masterChef'], [f'{pool_function}()(uint256)'],None,network)() 
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

        stakes=await Multicall(calls, network, _strict=False)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : parsers.from_custom(staked,wanted_decimal), 'contractAddress' : farm_data['masterChef'], 'gambitRewards' : []}
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

async def get_convex(wallet,farm_id,network_id,booster, vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        
        pool_length = await Call(booster, [f'poolLength()(uint256)'],None,network)() 

        for pid in range(0,pool_length):
            calls.append(Call(booster, [f'poolInfo(uint256)((address,address,address,address,address,bool))', pid], [[f'{pid}', None]]))


        pool_info=await Multicall(calls, network)()

        token_list = [pool_info[each][3] for each in pool_info]

        calls = []

        for i,contract in enumerate(token_list):
            calls.append(Call(contract, [f'balanceOf(address)(uint256)', wallet], [[f'{i}_staked', parsers.from_wei]]))
            calls.append(Call(contract, [f'earned(address)(uint256)', wallet], [[f'{i}_earned', parsers.from_wei]]))
            calls.append(Call(contract, [f'rewards(address)(uint256)', wallet], [[f'{i}_rewards', parsers.from_wei]]))


        stakes = await Multicall(calls, network)()      

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        cvx_total_supply = await Call('0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', f'totalSupply()(uint256)', _w3=network)()

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    key = int(breakdown[0])
                    staked = stakes[each]
                    want_token = pool_info[breakdown[0]][0]
                    pending_earned = stakes[f'{breakdown[0]}_earned']
                    pending_rewards = stakes[f'{breakdown[0]}_rewards']
                    pending_cvx = template_helpers.get_cvx_minted(pending_earned,parsers.from_wei(cvx_total_supply))

                    poolNest[poolKey]['userData'][key] = {'want': want_token, 'staked' : staked, 'contractAddress' : booster, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    reward_token_0 = {'pending': pending_earned, 'symbol' : 'CRV', 'token' : '0xD533a949740bb3306d119CC777fa900bA034cd52'}
                    reward_token_1 = {'pending': pending_cvx, 'symbol' : 'CVX', 'token' : '0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B'}

                    poolNest[poolKey]['userData'][key]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][key]['gambitRewards'].append(reward_token_1)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_moonpot_contracts(wallet,farm_id,network_id,vaults):
        poolKey = farm_id
        contracts = vaults
        network = WEB3_NETWORKS[network_id]

        reward_calls = []
        for each in contracts:
            if 'reward_length' not in each:
                reward_calls.append(Call(each['contract'], [f'rewardTokenLength()(uint256)'], [[each['contract'], None]]))

        reward_lengths = await Multicall(reward_calls, network)()

        calls = []
        for each in contracts:
            pot_contract = each['contract']
            token_function = each['token_function']
            reward_length = reward_lengths[pot_contract] if pot_contract in reward_lengths else 1
            calls.append(Call(pot_contract, [f'userTotalBalance(address)(uint256)',wallet], [[f'{pot_contract}_staked', parsers.from_wei]]))
            calls.append(Call(pot_contract, [f'{token_function}()(address)'], [[f'{pot_contract}_want', None]]))
            
            if 'reward_length' not in each:
                for i in range(0,reward_length):
                    calls.append(Call(pot_contract, [f'earned(address,uint256)(uint256)', wallet, i], [[f'{pot_contract}pending{i}', None]]))
                    calls.append(Call(pot_contract, [f'rewardInfo(uint256)(address)', i], [[f'{pot_contract}rewardaddress{i}', None]]))
            else:
                calls.append(Call(pot_contract, [f'earned(address)(uint256)', wallet], [[f'{pot_contract}pending0', None]]))
                calls.append(Call(pot_contract, [f'rewardToken()(address)'], [[f'{pot_contract}rewardaddress0', None]]))          

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        reward_symbols_decimals = await template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'rewardaddress' in x],network_id)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18
                    pot_contract = breakdown[0]
                    reward_length = reward_lengths[pot_contract] if pot_contract in reward_lengths else 1

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : pot_contract,'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    for i in range(0,reward_length):
                        if f'{pot_contract}pending{i}' in stakes:
                            pending_reward = stakes[f'{breakdown[0]}pending{i}']
                            pending_reward_contract = stakes[f'{breakdown[0]}rewardaddress{i}']
                            pending_reward_symbol = reward_symbols_decimals[f'{pending_reward_contract}_symbol']
                            pending_reward_decimal = reward_symbols_decimals[f'{pending_reward_contract}_decimals']
                            if pending_reward > 0:
                                reward_token_0 = {'pending': parsers.from_custom(pending_reward, pending_reward_decimal), 'symbol' : pending_reward_symbol, 'token' : pending_reward_contract, 'decimal' : pending_reward_decimal}
                                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_traderjoe_masterchef(wallet,farm_id,network_id,masterchef, vaults, user_config=False):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        pool_length = await Call(masterchef, [f'poolLength()(uint256)'],None,network)() 

        for pid in range(0,pool_length):
            calls.append(Call(masterchef, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', None]]))
            calls.append(Call(masterchef, [f'poolInfo(uint256)(address)', pid], [[f'{pid}ext_want', None]]))
            calls.append(Call(masterchef, [f'poolInfo(uint256)((address,uint256,uint256,uint256,address))', pid], [[f'{pid}ext_rewarder', None]]))
            calls.append(Call(masterchef, [f'pendingTokens(uint256,address)((uint256,address,uint256,uint256))', pid, wallet], [[f'{pid}ext_pending', None]]))

        if user_config:
            return await parse_calls(calls)


        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    rewarder = stakes[f'{breakdown[0]}_rewarder'][4]

                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : parsers.from_custom(staked,wanted_decimal), 'contractAddress' : masterchef, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    pending_joe = stakes[f'{breakdown[0]}_pending'][0]
                    pending_address = stakes[f'{breakdown[0]}_pending'][1]
                    pending_reward = stakes[f'{breakdown[0]}_pending'][3]

                    if pending_joe > 0:
                        reward_token_0 = {'pending': parsers.from_custom(pending_joe, 18), 'symbol' : 'JOE', 'token' : '0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd'}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

                    if pending_reward > 0:
                        rti = await Multicall(
                            [Call(pending_address, 'decimals()(uint8)', [['decimal', None]]),
                            Call(pending_address, 'symbol()(string)', [['symbol', None]])], _w3=network
                        )()
                        reward_token_0 = {'pending': parsers.from_custom(pending_reward, rti['decimal']), 'symbol' : rti['symbol'], 'token' : pending_address}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_vault_style_custom_pps(wallet, vaults, farm_id, network_id):

    poolKey = farm_id
    calls = []

    network=WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        calls.append(Call(vault, [f'depositToken()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'totalDeposits()(uint256)'], [[f'{vault}_totaldeposits', None]]))
        calls.append(Call(vault, [f'totalSupply()(uint256)'], [[f'{vault}_totalsupply', None]]))
    

    stakes=await Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = await template_helpers.get_token_list_decimals(vaults,network_id,False)

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


                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : real_staked, 'contractAddress' : breakdown[0], 'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

##No Contract Address
async def get_bingo_board(wallet, vaults, network):

    bingoKey = '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08'
    boardRoom = '0xc9525f505040fecd4b754407De72d7bCf5a8f78F'
    nestName = 'bingoBoard'
    calls = []

    calls.append(Call(boardRoom, ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (nestName), parsers.from_wei]]))
    calls.append(Call(boardRoom, ['earned(address)(uint256)', wallet], [['%s_pending' % (nestName), parsers.from_wei]]))
        
    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

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

##No Contract Address
async def get_iron_finance(wallet, vaults, farm_id, network):
    
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
    
    stakes=await Multicall(calls, network)()

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

##No Contract Address
async def get_diamond_hands(wallet, vaults):

    poolKey = '0xDiamondHands'
    calls = []

    for pool in vaults:
        if pool['contract'] in ['0xe5476aA8f9b0D22580bb7c796c53493BAD942Db4', '0xF26a92c8281e83Ec7E09C64C70e649e74dB22Ad4', '0x22210d79264B77c3545eb3E12415796AE2CA108c']:
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), parsers.from_wei]]))
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % (pool['contract']), parsers.from_wei]])) 
        else:
            calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['stakedFunction']), 0, wallet], [['%s_staked' % (pool['contract']), parsers.from_wei]]))
            calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['rewardFunction']), 0, wallet], [['%s_pending' % (pool['contract']), parsers.from_wei]]))        
    stakes=await Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolCheck = {x['contract'] : x for x in vaults}
    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'rewardToken' : poolCheck[addPool[0]]['rewardToken'], 'rewardSymbol' : poolCheck[addPool[0]]['rewardSymbol'], 'pending' : stakes[f'{addPool[0]}_pending'] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

##No Contract Address
async def get_wault_locked(wallet, network, vaults, farm_id):

    poolKey = farm_id
    network_conn = WEB3_NETWORKS[network]
    calls = []

    for vault in vaults:
        vault_info = vaults[vault]
        for i in range(0,vault_info['pool_length']):
            calls.append(Call(vault, [f'userInfo(uint256,address)(uint256)', i, wallet], [[f'{vault}_{i}_staked', parsers.from_wei]])) 
            calls.append(Call(vault, [f'pendingRewards(uint256,address)(uint256)', i, wallet], [[f'{vault}_{i}_pending', parsers.from_wei]]))


    stakes=await Multicall(calls, network_conn)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                vault_key = f'{breakdown[0]}_{breakdown[1]}'
                staked = stakes[each]
                reward_token = vaults[breakdown[0]]['staking_token']
                reward_symbol = vaults[breakdown[0]]['reward_symbol']
                reward_token_0 = {'pending': stakes[f'{vault_key}_pending'], 'symbol' : reward_symbol, 'token' : reward_token}

                want_token = reward_token

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_gambits(wallet, vaults, network, farm_id):

    poolKey = farm_id
    calls = []
    gambits = vaults

    for pool in gambits:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), parsers.from_wei]]))
        for i, reward in enumerate(pool['rewards']):
            calls.append(Call(reward['yieldTracker'], ['%s(address)(uint256)' % (reward['rewardFunction']), wallet], [['%s_pending_%s_%s' % (pool['contract'], reward['symbol'], reward['rewardToken']), parsers.from_wei]]))

    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    poolCheck = {x['contract'] : x for x in gambits}

    for stake in stakes:
        addPool = stake.split('_')       
        if addPool[0] not in poolNest[poolKey]['userData']:
            poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'contractAddress' : addPool[0], 'gambitRewards' : [] }
            poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
        else:
            if 'pending' in addPool[1]:     
                poolNest[poolKey]['userData'][addPool[0]]['gambitRewards'].append({addPool[1]: stakes[stake], 'symbol' : addPool[2], 'token' : addPool[3]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_taodao(wallet, vaults, network):
    poolKey = '0xTaodao'
    calls = []
    dao = vaults

    for pool in dao:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % pool['stakeToken'], parsers.from_tao if pool['decimal'] == 9 else parsers.from_wei ]]))
        if pool['rewardFunction'] is not None:
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % pool['stakeToken'], parsers.from_tao]]))
    
    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0], 'contractAddress' : addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_pop(wallet, vaults, network):
    poolKey = '0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0'
    epsChef = '0xcce949De564fE60e7f96C85e55177F8B9E4CF61b'
    wantToken = '0x049d68029688eAbF473097a2fC38ef61633A3C7A'
    calls = []

    calls.append(Call(epsChef, ['%s(uint256,address)(uint256)' % ('userInfo'), 2, wallet], [['%s_staked' % (epsChef), parsers.from_wei ]]))
    calls.append(Call(epsChef, ['%s(uint256,address)(uint256)' % ('claimableReward'), 2, wallet], [['%s_pending' % (epsChef), parsers.from_wei]]))
    
    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': wantToken, 'contractAddress' : epsChef }
                poolIDs['%s_%s_want' % (poolKey, epsChef)] = wantToken
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_fortress(wallet, vaults):

    faiVault = '0x066807c7B22c6c0a7fa370A2cA812e5Fc22DBef6'
    poolKey = '0xFortress'
    calls = []
    forts = vaults

    for fort in forts:
        calls.append(Call(fort, ['%s(address)((uint256,uint256,uint256,uint256))' % ('getAccountSnapshot'), wallet], [['%s_staked' % (fort), parsers.parseAccountSnapshot ]]))
        if fort != '0xE24146585E882B6b59ca9bFaaaFfED201E4E5491':
            calls.append(Call(fort, 'underlying()(address)', [['%s_want' % fort, None]]))
    
    calls.append(Call(faiVault, ['%s(address)(uint256)' % ('userInfo'), wallet], [['%s_staked' % (faiVault), parsers.from_wei ]]))
    calls.append(Call(faiVault, ['%s(address)(uint256)' % ('pendingFTS'), wallet], [['%s_pending' % (faiVault), parsers.from_wei ]]))
    
    stakes=await Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

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
                        poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': want, 'pending' : pending, 'contractAddress' : addPool[0] }
                        poolIDs['%s_%s_want' % (poolKey, addPool[0])] = want


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_dyp(wallet, vaults, network_id):

    dypPools = vaults
    poolKey = '0xDYP'
    calls = []

    for pool in dypPools:
        calls.append(Call(pool, ['%s(address)(uint256)' % ('depositedTokens'), wallet], [['%s_staked' % (pool), parsers.from_wei ]]))
        calls.append(Call(pool, ['%s(address)(uint256)' % ('getPendingDivsEth'), wallet], [['%s_pending' % (pool), parsers.from_wei ]]))
        calls.append(Call(pool, 'trustedDepositTokenAddress()(address)', [['%s_want' % pool, None]]))

    
    stakes=await Multicall(calls, WEB3_NETWORKS[network_id])()

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
                        poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': want, 'pending' : pending, 'rewardToken' : rewarded, 'rewardSymbol' : rewardSym, 'contractAddress' : addPool[0] }
                        poolIDs['%s_%s_want' % (poolKey, addPool[0])] = want


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_beefy_style_stakes(wallet,vaults,farm_id,network,user_config=False):

    poolKey = farm_id
    calls = []

    vault_list = []
    want_list = []
    want_lookup = {}

    for vault in vaults:
        vault_address = vault['vault']
        want_address = vault['want']
        calls.append(Call(vault_address, ['balanceOf(address)(uint256)', wallet], [[f'{vault_address}_staked', None]]))
        calls.append(Call(vault_address, [f'getPricePerFullShare()(uint256)'], [[f'{vault_address}_getPricePerFullShare', parsers.from_wei]]))
        vault_list.append(vault_address)
        want_list.append(want_address)
        want_lookup[vault_address] = want_address
    
    if user_config:
        return await parse_calls(calls)


    if len(calls) > 200:
        chunks = len(calls) / 100
        x = np.array_split(calls, math.ceil(chunks))
        all_calls=await asyncio.gather(*[Multicall(call,WEB3_NETWORKS[network], _strict=False)() for call in x])
        stakes = reduce(lambda a, b: dict(a, **b), all_calls)
    else:
        stakes = await Multicall(calls, WEB3_NETWORKS[network], _strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = await template_helpers.get_token_list_decimals(want_list,network,False)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                token_decimal = 18 if want_lookup[breakdown[0]] not in token_decimals else token_decimals[want_lookup[breakdown[0]]]
                staked = parsers.from_custom(stakes[each], token_decimal)
                want_token = want_lookup[breakdown[0]]
                price_per = stakes[f'{breakdown[0]}_getPricePerFullShare'] if f'{breakdown[0]}_getPricePerFullShare' in stakes else 1
                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'getPricePerFullShare' : price_per, 'contractAddress' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_nuts(wallet, network, farm_id, vaults):

    poolKey = farm_id
    nuts = vaults
    calls = []

    for pool in nuts:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), parsers.from_wei]]))
        for i, reward in enumerate(pool['rewards']):
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (reward['rewardFunction']), wallet], [['%s_pending_%s_%s' % (pool['contract'], reward['symbol'], reward['rewardToken']), parsers.from_wei]]))

    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    poolCheck = {x['contract'] : x for x in nuts}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'contractAddress' : addPool[0], 'gambitRewards' : [] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
            else:
                if 'pending' in addPool[1]:     
                    poolNest[poolKey]['userData'][addPool[0]]['gambitRewards'].append({addPool[1]: stakes[stake], 'symbol' : addPool[2], 'token' : addPool[3]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_adamant_funds_dynamic(wallet, vaults, farm_id, calculator, minter, network, reward):
    poolKey = farm_id
    
    addy_mints = await Call(minter, 'addyPerProfitEth()(uint256)', None, WEB3_NETWORKS[network])()
    
    adamant_user_info = []
    strat_vaults = vaults
    for item in strat_vaults:
        strategy = item['strategyAddress']
        vault = item['vaultAddress']

        adamant_user_info.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        adamant_user_info.append(Call(vault, ['getPendingReward(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
        adamant_user_info.append(Call(vault, ['getRewardMultiplier()(uint256)'], [[f'{vault}_multiplier', None]]))
        adamant_user_info.append(Call(strategy, ['want()(address)'], [[f'{vault}_want', None]]))
    
    user_data = await Multicall(adamant_user_info, WEB3_NETWORKS[network])()

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
                reward_token = reward

                extra_data = await Multicall(
                    
                [Call(breakdown[0], ['getRatio()(uint256)'], [['getPricePerFullShare', parsers.from_wei]]),
                Call(calculator,['valueOfAsset(address,uint256)(uint256)', reward_token, pending], [['real_pending', None]])], WEB3_NETWORKS[network])()

                ppfs = extra_data['getPricePerFullShare']
                actual_staked = staked * ppfs
                actual_pending = extra_data['real_pending']
                 

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked, 'pending': (parsers.from_wei((actual_pending * addy_mints)) * reward_multi) / 1000, 'contractAddress' : breakdown[0] }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

    # addy_eth = await get_addy_eth(wallet, addy_mints)
    
    # if addy_eth is not None:
    #     poolIDs.update(addy_eth[0])
    #     poolNest['0xAdamant']['userData'].update(addy_eth[1]['0xAdamant']['userData'])

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_adamant_funds(wallet, vaults):
    poolKey = '0xAdamant'
    calculator = '0x80d8dad3753887731BA8f92AEe84Df371B6A7790'
    minter = '0xAAE758A2dB4204E1334236Acd6E6E73035704921'
    
    addy_mints = await Call(minter, 'addyPerProfitEth()(uint256)', None, WEB3_NETWORKS['matic'])()
    
    adamant_user_info = []
    strat_vaults = vaults
    for item in strat_vaults:
        strategy = item['strategyAddress']
        vault = item['vaultAddress']
        if strategy == "" or vault == "":
            continue
        adamant_user_info.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        adamant_user_info.append(Call(vault, ['getPendingReward(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
        adamant_user_info.append(Call(vault, ['getRewardMultiplier()(uint256)'], [[f'{vault}_multiplier', None]]))
        adamant_user_info.append(Call(strategy, ['want()(address)'], [[f'{vault}_want', None]]))

    user_data = await Multicall(adamant_user_info, WEB3_NETWORKS['matic'], _strict=False)()

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

                extra_data = await Multicall(
                    
                [Call(breakdown[0], ['getRatio()(uint256)'], [['getPricePerFullShare', parsers.from_wei]]),
                Call(calculator,['valueOfAsset(address,uint256)(uint256)', reward_token, pending], [['real_pending', None]])], WEB3_NETWORKS['matic'])()

                ppfs = extra_data['getPricePerFullShare']
                actual_staked = staked * ppfs
                actual_pending = extra_data['real_pending']
                 

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked, 'pending': (parsers.from_wei((actual_pending * addy_mints)) * reward_multi) / 1000, 'contractAddress' : breakdown[0] }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

    addy_eth = await get_addy_eth(wallet, addy_mints)
    
    if addy_eth is not None:
        poolIDs.update(addy_eth[0])
        poolNest['0xAdamant']['userData'].update(addy_eth[1]['0xAdamant']['userData'])

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_addy_eth(wallet, minting_rate=None):

    poolKey = '0xAdamant'
    
    adamant_user_info = []

    vault = '0xF7661EE874Ec599c2B450e0Df5c40CE823FEf9d3'

    adamant_user_info.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
    adamant_user_info.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
    adamant_user_info.append(Call(vault, ['stakingToken()(address)'], [[f'{vault}_want', None]]))
    
    user_data = await Multicall(adamant_user_info, WEB3_NETWORKS['matic'])()

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
                actual_pending = parsers.from_wei(pending * minting_rate)
                 

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending': actual_pending, 'contractAddress' : breakdown[0] }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_quickswap_style(wallet, vaults, farm_id, network, want_function=None):
    network_conn = WEB3_NETWORKS[network]
    if want_function is None:
        want_function = 'stakingToken'
    else:
        want_function = want_function

    poolKey = farm_id
    calls = []

    
    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', parsers.from_wei]]))
        calls.append(Call(vault, [f'{want_function}()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network_conn, _strict=False)()

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

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending': pending, 'contractAddress' : breakdown[0] }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_quickswap_style_multi(wallet, vaults, farm_id, network):
    network_conn = WEB3_NETWORKS[network]
    poolKey = farm_id
    calls = []

    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, ['stakingToken()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, ['bothTokensEarned(address)(address[])', wallet], [[f'{vault}_rewardtokens', None]]))
    
    stakes=await Multicall(calls, network_conn)()

    reward_calls = []

    for each in stakes:
        if 'rewardtokens' in each:
            for i, token in enumerate(stakes[each]):
                vault = each.split('_')[0]
                reward_calls.append(Call(vault, ['earned(address,address)(uint256)', wallet, token], [[f'{vault}_{i}_{token}_pending', parsers.from_wei]]))
                reward_calls.append(Call(token, 'symbol()(string)', [[f'{vault}_{i}_{token}_symbol', None]]))


    rewards=await Multicall(reward_calls, network_conn)()

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

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
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

async def get_vault_style(wallet, vaults, farm_id, network, _pps=None, _stake=None, _strict=None, want_token=None, decimal_from=None, pancake=False):

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

    if decimal_from is None:
        decimal_from = True
    else:
        decimal_from = False

    poolKey = farm_id
    calls = []
    for vault in vaults:

        if vault in ['0x45c54210128a065de780C4B0Df3d16664f7f859e']:
            calls.append(Call(vault, [f'{stake}(address)((uint256,uint256,uint256,uint256,uint256,uint256,uint256,bool,uint256))', wallet], [[f'{vault}_staked', None]]))
        else:
            calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        
        if vault in ['0xa6Fc07819eE785C120aB765981b313D71b4FF406']:
            calls.append(Call(vault, [f'wmatic()(address)'], [[f'{vault}_want', None]]))
        elif vault in ['0x929e9dEfF1070bA346FB45EB841F035dCC29D131','0x5cD44E5Aa00b8D77c8c7102E530d947AB86c9551','0xA0FfC3b52c315B00ea3DaFbC3094059D46aA5Daf','0x2bffD2442C4509c32Cc4bcACC4aC85B89A0076BA','0x6F5be5d7Ecdd948dB34C111C06AEa1E2fE2D2c2F','0xCf2CF4B53B62022F81Ad73cAe04E433936eca6c0']:
            calls.append(Call(vault, [f'want()(address)'], [[f'{vault}_want', None]]))
        elif vault in ['0xb409ffdaa37f8b98766e5b11d183accfc7ca6822', '0x75415bf29f054ab9047d26501ad5ef93b5364eb0']:
            calls.append(Call(vault, [f'pool()(address)'], [[f'{vault}_want', None]]))
        else:
            calls.append(Call(vault, [f'{want_token}()(address)'], [[f'{vault}_want', None]]))
        
        if vault in ['0x45c54210128a065de780C4B0Df3d16664f7f859e']:
            calls.append(Call(vault, [f'{pps}()(uint256)'], [[f'{vault}_getPricePerFullShare', None]]))
        else:
            calls.append(Call(vault, [f'{pps}()(uint256)'], [[f'{vault}_getPricePerFullShare', parsers.from_wei]]))

    if len(calls) > 1000:
        chunks = len(calls) / 500
        x = np.array_split(calls, math.ceil(chunks))
        all_calls=await asyncio.gather(*[Multicall(call,WEB3_NETWORKS[network], _strict=strict)() for call in x])
        stakes = reduce(lambda a, b: dict(a, **b), all_calls)
    else:
        stakes = await Multicall(calls, WEB3_NETWORKS[network], _strict=strict)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    if decimal_from is True:
        token_decimals = await template_helpers.get_token_list_decimals(vaults,network,False)
    else:
        token_decimals = await template_helpers.get_token_list_decimals(stakes,network,True)
    
    for each in stakes:
        if 'staked' in each:
            breakdown = each.split('_')

            if decimal_from is True:
                decimal_lookup = breakdown[0]
            else:
                decimal_lookup = stakes[f'{breakdown[0]}_want']

            token_decimal = 18 if decimal_lookup not in token_decimals else token_decimals[decimal_lookup]

            want_token = stakes[f'{breakdown[0]}_want']

            poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'vault_receipt' : breakdown[0], 'contractAddress' : breakdown[0]}
            
            if breakdown[0] == '0x45c54210128a065de780C4B0Df3d16664f7f859e':
                actual_staked = ((stakes[each][0] * stakes[f'{breakdown[0]}_getPricePerFullShare']) / 1e18) - stakes[each][6]
                poolNest[poolKey]['userData'][breakdown[0]]['staked'] = parsers.from_custom(actual_staked, token_decimal)
            else:
                poolNest[poolKey]['userData'][breakdown[0]]['staked'] = parsers.from_custom(stakes[each], token_decimal)
                poolNest[poolKey]['userData'][breakdown[0]]['getPricePerFullShare'] = stakes[f'{breakdown[0]}_getPricePerFullShare']

            poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_pancake_bunny_clones(wallet, vaults, network_id, dashboard_contract, calculator, farm_id, native_symbol, native_token, _decode=None):
        poolKey = farm_id
        calls = []
        info_calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        if _decode is None:
            decode = 'address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256'
        else:
            decode = 'address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256'

        for vault in vaults:
                calls.append(Call(dashboard_contract, ['profitOfPool(address,address)((uint256,uint256))', vault, wallet], [[f'{vault}_pendings', parsers.parse_profit_of_pool]]))
                info_calls.append(Call(dashboard_contract, [f'infoOfPool(address,address)(({decode}))', vault, wallet], [[f'{vault}_userinfo', parsers.parse_pancake_bunny_info]]))
                calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'rewardsToken()(address)'], [[f'{vault}_rewardtoken', None]]))

        stakes=await Multicall(info_calls, network)()
        ainfo=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'userinfo' in each:
                if stakes[each]['balance'] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]['principal']
                    want_token = ainfo[f'{breakdown[0]}_want']
                    pendings = ainfo[f'{breakdown[0]}_pendings']
                    if ainfo[f'{breakdown[0]}_rewardtoken'] == '0x6b70f0136a7e2bd1fa945566b82b208760632b2e':
                        reward_token = '0xD016cAAe879c42cB0D74BB1A265021bf980A7E96'
                    elif ainfo[f'{breakdown[0]}_rewardtoken'] == '0xf0b5074dbf73c96d766c9a48726cee7a6074d436':
                        reward_token = '0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23'
                    else:
                        reward_token = ainfo[f'{breakdown[0]}_rewardtoken']
                        

                    try:
                        staked_symbol = await Call(reward_token, 'symbol()(string)', None, network)()
                    except:
                        reward_token = await Call(reward_token, [f'rewardsToken()(address)'], None, network)()
                        staked_symbol = await Call(reward_token, 'symbol()(string)', None, network)()

                    staked_single_price = await Call(calculator, ['valueOfAsset(address,uint256)((uint256,uint256))', reward_token, one_token], [[f'prices', parsers.parse_profit_of_pool]], network)()

                    if breakdown[0] in ['0x4Ad69DC9eA7Cc01CE13A37F20817baC4bF0De1ba','0x7a526d4679cDe16641411cA813eAf7B33422501D']:
                        poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : [{'pending': pendings[0], 'symbol' : native_symbol, 'token' : native_token}]}
                    else:
                        poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : [{'pending': pendings[1], 'symbol' : native_symbol, 'token' : native_token}, {'pending': pendings[0], 'symbol' : staked_symbol, 'token' : reward_token, 'valueOfAsset' : staked_single_price['prices'][1]}]}
                        
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_syrup_pools(wallet, vaults, network_id, farm_id, staked=None, reward=None, pending_reward=None, user_info=None, stake_override={}):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        staked = 'stakedToken' if staked is None else staked
        reward = 'rewardToken' if reward is None else reward
        pending_reward = 'pendingReward' if pending_reward is None else pending_reward
        user_info = 'userInfo' if user_info is None else user_info

        for pool in vaults:
            staked_function = stake_override[pool] if pool in stake_override else staked
            calls.append(Call(pool, [f'{user_info}(address)(uint256)', wallet], [[f'{pool}_staked', None]]))
            calls.append(Call(pool, [f'{pending_reward}(address)(uint256)', wallet], [[f'{pool}_pending', None]]))
            calls.append(Call(pool, [f'{staked_function}()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'{reward}()(address)'], [[f'{pool}_rewardtoken', None]]))


        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    token_decimal = 18 if breakdown[0] not in token_decimals else token_decimals[breakdown[0]]
                    pendings = stakes[f'{breakdown[0]}_pending']
                    reward_token = stakes[f'{breakdown[0]}_rewardtoken']

                    reward_calls = []
                    reward_calls.append(Call(reward_token, 'symbol()(string)', [[f'symbol', None]]))
                    reward_calls.append(Call(reward_token, 'decimals()(uint256)', [[f'decimal', None]]))

                    reward_data=await Multicall(reward_calls, network)()

                    reward_symbol = reward_data['symbol']
                    reward_decimal = reward_data['decimal']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'contractAddress' : breakdown[0],'want': want_token, 'staked' : parsers.from_custom(staked, token_decimal), 'pending' : parsers.from_custom(pendings, reward_decimal), 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'rewardDecimal' : reward_decimal, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_adamant_stakes(wallet, farm_id, vaults):
    
    poolKey = farm_id
    staking_contract = '0x920f22E1e5da04504b765F8110ab96A20E6408Bd'
    addy_rewards = set_pool(abi.add_rewards.reward_abi, '0x920f22E1e5da04504b765F8110ab96A20E6408Bd', 'matic')
    wallet = Web3.toChecksumAddress(wallet)

    stakes= await Call(staking_contract, ['totalBalance(address)(uint256)', wallet], [[f'totalBalance', parsers.from_wei]], WEB3_NETWORKS['matic'])()


    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}


    if stakes['totalBalance'] > 0:

        staked = stakes['totalBalance']
        reward_tokens = addy_rewards.claimableRewards(wallet).call()
        want_token = '0xc3FdbadC7c795EF1D6Ba111e06fF8F16A20Ea539'

        poolNest[poolKey]['userData'][staking_contract] = {'want': want_token, 'contractAddress' : staking_contract, 'staked' : staked, 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, staking_contract)] = want_token

        for i, rtoken in enumerate(reward_tokens):
            if rtoken[1] > 0: 
                reward_address = rtoken[0]
                pending_amount = parsers.from_wei(rtoken[1])
                symbol = await Call(reward_address, 'symbol()(string)', _w3=WEB3_NETWORKS['matic'])()
                poolNest[poolKey]['userData'][staking_contract]['gambitRewards'].append({'pending': pending_amount, 'symbol' : symbol, 'token' : reward_address})
                    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_apeswap(wallet, farm_id, network_id, vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        mini_ape = '0x54aff400858Dcac39797a81894D9920f16972D1D'
        mini_complex = '0x1F234B1b83e21Cb5e2b99b4E498fe70Ef2d6e3bf'
        pool_length = await Call(mini_ape, [f'poolLength()(uint256)'],None,network)()
        

        for pid in range(0,pool_length):
            calls.append(Call(mini_ape, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}_staked', parsers.from_wei]]))
            calls.append(Call(mini_ape, [f'pendingBanana(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pending', parsers.from_wei]]))
            calls.append(Call(mini_ape, [f'lpToken(uint256)(address)', pid], [[f'{pid}_want', None]]))
            calls.append(Call(mini_complex, [f'pendingToken(uint256,address)(uint256)', pid, wallet], [[f'{pid}_complexp', parsers.from_wei]]))


        stakes=await Multicall(calls, network)()

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


                    poolNest[poolKey]['userData'][int(breakdown[0])] = {'want': want_token, 'staked' : staked, 'contractAddress' : mini_ape, 'gambitRewards' : [{'pending': pending, 'symbol' : native_symbol, 'token' : reward_token}, {'pending': complex, 'symbol' : staked_symbol, 'token' : complex_token}]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_single_masterchef(wallet,farm_id,network_id,farm_data,vaults,length_override=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        if 'poolFunction' not in farm_data:
            pool_function = 'poolLength'
        else:
            pool_function = farm_data['poolFunction']

        if length_override:
            pool_length = length_override
        else:
            pool_length = await Call(farm_data['masterChef'], [f'{pool_function}()(uint256)'],None,network)() 
        staked_function = farm_data['stakedFunction']
        pending_function = farm_data['pendingFunction']
        reward_token = farm_data['rewardToken']
        reward_symbol = farm_data['rewardSymbol']
        if 'wantFunction' not in farm_data:
            want_function = 'poolInfo'
        else:
            want_function = farm_data['wantFunction']

        for pid in range(0,pool_length):
            calls.append(Call(farm_data['masterChef'], [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_staked', None]]))
            if pending_function:
                calls.append(Call(farm_data['masterChef'], [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_pending', parsers.from_wei]]))
            calls.append(Call(farm_data['masterChef'], [f'{want_function}(uint256)(address)', pid], [[f'{pid}{farm_data["masterChef"]}ext_want', None]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    want_token = stakes[f'{breakdown[0]}_want']
                    try:
                        token_decimal = token_decimals.get(want_token) if token_decimals.get(want_token) else 18
                    except:
                        token_decimal = 18
                    staked = parsers.from_custom(stakes[each], token_decimal)
                    pending = stakes[f'{breakdown[0]}_pending'] if f'{breakdown[0]}_pending' in stakes else 0

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'contractAddress' : farm_data["masterChef"]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_acryptos_style_boosts(wallet, vaults, farm_id, network, caller, pfunc):
    network_conn = WEB3_NETWORKS[network]
    poolKey = farm_id
    calls = []

    for vault in vaults:
        calls.append(Call(caller, [f'userInfo(address,address)(uint256)',vault,wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(caller, [f'{pfunc}(address,address)(uint256)',vault,wallet], [[f'{vault}_pending', parsers.from_wei]]))
    
    stakes=await Multicall(calls, network_conn)()

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
                poolNest[poolKey]['userData'][f'{breakdown[0]}-BOOST'] = {'want': want_token, 'staked' : staked, 'pending'  : pending, 'contractAddress' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, f'{breakdown[0]}-BOOST')] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_pyq_triple_staking(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'stakes(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
                calls.append(Call(vault, [f'lqtyToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'getPendingETHGain(address)(uint256)', wallet], [[f'{vault}_pendingETH', parsers.from_wei]]))
                calls.append(Call(vault, [f'getPendingLQTYGain(address)(uint256)', wallet], [[f'{vault}_pendingLQTY', parsers.from_wei]]))
                calls.append(Call(vault, [f'getPendingLUSDGain(address)(uint256)', wallet], [[f'{vault}_pendingLUSD', parsers.from_wei]]))

        stakes=await Multicall(calls, network)()

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

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_2)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

async def get_pyq_double_staking(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'getCompoundedLUSDDeposit(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
                calls.append(Call(vault, [f'lusdToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'getDepositorETHGain(address)(uint256)', wallet], [[f'{vault}_pendingETH', parsers.from_wei]]))
                calls.append(Call(vault, [f'getDepositorLQTYGain(address)(uint256)', wallet], [[f'{vault}_pendingLQTY', parsers.from_wei]]))


        stakes=await Multicall(calls, network)()

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

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

async def get_pyq_trove(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'getTroveColl(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
                calls.append(Call(vault, [f'getTroveDebt(address)(uint256)', wallet], [[f'{vault}_pending', parsers.from_wei]]))


        stakes=await Multicall(calls, network)()

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

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

#No Contract Address
async def get_mai_cvault(wallet, farm_id, vaults):
        poolKey = farm_id

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        stakes = vaults

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

async def get_wault_pools(wallet, vaults, network_id, farm_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for pool in vaults:
            calls.append(Call(pool, [f'userInfo(address)(uint256)', wallet], [[f'{pool}_staked', parsers.from_wei]]))
            calls.append(Call(pool, [f'pendingRewards(address)(uint256)', wallet], [[f'{pool}_pending', parsers.from_wei]]))
            calls.append(Call(pool, [f'pool()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'rewardToken()(address)'], [[f'{pool}_rewardtoken', None]]))


        stakes=await Multicall(calls, network)()

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
                    reward_symbol = await Call(reward_token, 'symbol()(string)', _w3=network)()

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pendings, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_farmhero_staking(wallet,vaults,network,farm_id):

    calls = []
    poolKey = farm_id

    calls.append(Call(vaults, [f'totalBalance(address)(uint256)', wallet], [[f'{vaults}_staked', parsers.from_wei]]))
    calls.append(Call(vaults, [f'stakingToken()(address)'], [[f'{vaults}_want', None]]))

    stakes = await Multicall(calls,WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']
                w3_instance = set_pool(abi.farmhero.multi_fee_v2,vaults,network)
                reward_tokens = w3_instance.claimableRewards(wallet).call()

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i, rtoken in enumerate(reward_tokens):
                    reward_address = rtoken[0]
                    if rtoken[1] > 1:
                        pending_amount = parsers.from_wei(rtoken[1])
                        symbol = await Call(reward_address, [f'symbol()(string)'], _w3=WEB3_NETWORKS[network])()
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
                    reward_token_want = await Call(reward_token, 'want()(address)', WEB3_NETWORKS[network])()
                    reward_token_pps =  await Call(reward_token, 'getPricePerFullShare()(uint256)', _w3=WEB3_NETWORKS[network])()
                    reward_token_symbol =  await Call(reward_token_want['want'], 'symbol()(string)', _w3=WEB3_NETWORKS[network])()
                    reward_token = reward_token_want
                except:
                    reward_token_symbol = await Call(reward_token, 'symbol()(string)', _w3=WEB3_NETWORKS[network])()
                    reward_token_pps =  1 * 10 ** 18
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'] * parsers.from_wei(reward_token_pps), 'symbol' : reward_token_symbol, 'token' : reward_token}
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

#No Contract Address
async def get_quickswap_lps(farm_id,vaults,wallet):

    poolKey = farm_id

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for lp in vaults['data']['liquidityPositions']:
        if float(lp['liquidityTokenBalance']) > 0:
                staked = float(lp['liquidityTokenBalance'])
                want_token = lp['pair']['id']

                poolNest[poolKey]['userData'][f'QSLP{want_token}'] = {'want': want_token, 'staked' : staked, 'pending' : 0}
                poolIDs['%s_%s_want' % (poolKey, f'QSLP{want_token}')] = want_token
                    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_aperocket_space_pool(wallet,vaults,rewardtoken,network_id,farm_id,profit_offset):
    
    calls = []
    poolKey = farm_id
    
    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, [f'SPACE()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'profitOf(address)((uint256,uint256,uint256))', wallet], [[f'{vault}_pending', parsers.parse_spacepool, profit_offset]]))

    stakes = await Multicall(calls,WEB3_NETWORKS[network_id])()

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
                reward_token_0 = {'pending': parsers.from_custom(stakes[f'{breakdown[0]}_pending'],reward_token_decimal), 'symbol' : reward_token_symbol, 'token' : reward_token}
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_balancer_user_pools(wallet,vaults,network_id,farm_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for pool in vaults:
            calls.append(Call(pool, [f'balanceOf(address)(uint256)', wallet], [[f'{pool}_staked', parsers.from_wei]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = breakdown[0]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'pending' : 0}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_pickle_chef(wallet,farm_id,network_id,chef,rewarder,vaults):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]
    pool_length = await Call(chef, [f'poolLength()(uint256)'],None,network)() 

    for pid in range(0,pool_length):
        calls.append(Call(chef, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}_staked', parsers.from_wei]]))
        calls.append(Call(chef, [f'pendingPickle(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pendingPickle', parsers.from_wei]]))
        calls.append(Call(rewarder, [f'pendingToken(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pendingMatic', parsers.from_wei]]))
        calls.append(Call(chef, [f'lpToken(uint256)(address)', pid], [[f'{pid}_want', None]]))

    stakes=await Multicall(calls, network,_strict=False)()

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

                poolNest[poolKey]['userData'][pid] = {'want': want_token, 'staked' : staked, 'contractAddress' : chef, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][pid]['gambitRewards'].append(reward_token_0)
                poolNest[poolKey]['userData'][pid]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_curve_gauage(wallet,farm_id,network_id,vaults,rewards=None):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    gauages = vaults

    if rewards is None:
        rewards = ['0x172370d5Cd63279eFa6d502DAB29171933a610AF', '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270']

    for guage in gauages:
        calls.append(Call(guage, [f'balanceOf(address)(uint256)', wallet], [[f'{guage}_staked', parsers.from_wei]]))
        for i,each in enumerate(rewards):
            calls.append(Call(guage, [f'claimable_reward_write(address,address)(uint256)', wallet,each], [[f'{guage}_pending{i}', parsers.from_wei]]))
        calls.append(Call(guage, [f'lp_token()(address)'], [[f'{guage}_want', None]]))

    stakes=await Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i,each in enumerate(rewards):
                    symbol = await Call(each, [f'symbol()(string)'], _w3=network)()
                    reward_gambit = {'pending': stakes[f'{breakdown[0]}_pending{i}'], 'symbol' : symbol, 'token' : each}

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_gambit)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_telx_single(wallet,farm_id,network_id,vaults):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, [f'earned(address)(uint256)', wallet], [[f'{vault}_pending', parsers.from_wei]]))
        calls.append(Call(vault, [f'rewardsToken()(address)'], [[f'{vault}_rewardToken', None]]))
        calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_token = stakes[f'{breakdown[0]}_rewardToken']
                reward_symbol = await Call(reward_token, [f'symbol()(string)'], _w3=network)()
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : reward_symbol, 'token' : reward_token}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_telx_double(wallet,farm_id,network_id,vaults):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, [f'earnedA(address)(uint256)', wallet], [[f'{vault}_pendingA', parsers.from_wei]]))
        calls.append(Call(vault, [f'earnedB(address)(uint256)', wallet], [[f'{vault}_pendingB', parsers.from_wei]]))
        calls.append(Call(vault, [f'rewardsTokenA()(address)'], [[f'{vault}_rewardTokenA', None]]))
        calls.append(Call(vault, [f'rewardsTokenB()(address)'], [[f'{vault}_rewardTokenB', None]]))
        calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network,_strict=False)()

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
                reward_symbolA = await Call(reward_tokenA, [f'symbol()(string)'], _w3=network)()
                reward_symbolB = await Call(reward_tokenB, [f'symbol()(string)'], _w3=network)()
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingA'], 'symbol' : reward_symbolA, 'token' : reward_tokenA}
                reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingB'], 'symbol' : reward_symbolB, 'token' : reward_tokenB}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_blackswan_stakes(wallet,vaults):
    
    poolKey = '0xBlackSwan'
    calls = []
    swan_lake = '0xE420CC7F8F0df0f145d146e9FDC8a4237660Eecb'
    distribution_pool = '0xbCf0734600AC0AcC1BaD85f62c0BE82BBC8Ca3B5'

    calls.append(Call(distribution_pool,['balanceOf(address)(uint256)', wallet], [[f'{distribution_pool}_staked', parsers.from_custom, 6]]))
    calls.append(Call(distribution_pool,['takeWithAddress(address)(uint256)', wallet], [[f'{distribution_pool}_pending', parsers.from_wei]]))
    calls.append(Call(distribution_pool,['token()(address)'], [[f'{distribution_pool}_want', None]]))
    calls.append(Call(swan_lake,['balanceOf(address)(uint256)', wallet], [[f'{swan_lake}_staked', parsers.from_wei]]))
    calls.append(Call(swan_lake,['_takeWithAddress(address)((uint256,uint256))', wallet], [[f'{swan_lake}_pending', None]]))
    calls.append(Call(swan_lake,['token()(address)'], [[f'{swan_lake}_want', None]]))

    stakes = await Multicall(calls,WEB3_NETWORKS['matic'])()
    
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
                reward_pendingA = stakes[f'{distribution_pool}_pending'] if breakdown[0] == distribution_pool else parsers.from_wei(stakes[f'{swan_lake}_pending'][1])
                reward_token_0 = {'pending': reward_pendingA , 'symbol' : reward_symbolA, 'token' : reward_tokenA}
                
                if breakdown[0] == swan_lake:
                    reward_tokenB = '0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'
                    reward_symbolB = 'SWAN-LP'
                    reward_pendingB = parsers.from_wei(stakes[f'{swan_lake}_pending'][0])
                    reward_token_1 = {'pending': reward_pendingB, 'symbol' : reward_symbolB, 'token' : reward_tokenB}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                if breakdown[0] == swan_lake:
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_feeder_style(wallet, vaults, network, farm_id):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for vault in vaults:
        calls.append(Call(vault, [f'userInfo(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, [f'token()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'depositedTokenBalance(bool)(uint256)',False], [[f'{vault}_depositedTokenBalance', parsers.from_wei]]))
        calls.append(Call(vault, [f'totalShares()(uint256)'], [[f'{vault}_totalShares', parsers.from_wei]]))

    stakes=await Multicall(calls, network)()

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

async def get_sfeed(wallet,vaults,receipt_token,network,farm_id):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for vault in vaults:
        calls.append(Call(receipt_token, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', receipt_token], [[f'{vault}_totalDepositedFeeds', parsers.from_wei]]))
        calls.append(Call(receipt_token, [f'totalSupply()(uint256)'], [[f'{vault}_totalSFeedTokens', parsers.from_wei]]))

    stakes=await Multicall(calls, network)()

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

async def get_xsnob_lock(wallet,vaults,receipt_token,network,farm_id):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for vault in vaults:
        calls.append(Call(receipt_token, [f'locked(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))

    stakes=await Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = breakdown[0]       

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : receipt_token}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_vault_style_no_want(wallet, vaults, farm_id, network, _pps=None, _stake=None, _strict=None, want_token=None, pps_decimal=None):

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
        calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))        
        calls.append(Call(vault, [f'{pps}()(uint256)'], [[f'{vault}_getPricePerFullShare', parsers.from_custom, pps_decimal]]))
    
    stakes=await Multicall(calls, WEB3_NETWORKS[network], _strict=strict)()

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
                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'getPricePerFullShare' : price_per, 'vault_receipt' : breakdown[0], 'contractAddress' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_lending_protocol(wallet,vaults,farm_id,network):

    lending_vaults = vaults
    poolKey = farm_id
    calls = []

    for vault in lending_vaults:
        vault_address = vault['address']
        calls.append(Call(vault_address, [f'getAccountSnapshot(address)((uint256,uint256,uint256,uint256))', wallet], [[f'{vault_address}_accountSnapshot', None ]]))
        
    stakes=await Multicall(calls, WEB3_NETWORKS[network], _strict=False)()

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
                collat = parsers.from_custom(snapshot[1], underlying_decimal)
                collat_rate = hash_map[addPool[0]]['collat_rate']
                borrow = parsers.from_custom(snapshot[2], underlying_decimal)
                rate = parsers.from_wei(snapshot[3])
                poolNest[poolKey]['userData'][addPool[0]] = {'staked' : collat * rate, 'want': underlying, 'borrowed' : borrow, 'rate' : collat_rate, 'contractAddress' : addPool[0]}
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = underlying


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

#No Contract Address
async def get_aave_protocol(wallet,vaults,farm_id,pool_address,pool_provider,network):

    lending_vaults = vaults
    poolKey = farm_id
    calls = []

    get_reserves = await Call(pool_address, [f'getReservesList()(address[])'], None, WEB3_NETWORKS[network])()

    for r in get_reserves:
        calls.append(Call(pool_provider, [f'getReserveTokensAddresses(address)((address,address,address))', r], [[f'{r}_tokens', None ]]))
        calls.append(Call(pool_provider, [f'getReserveConfigurationData(address)((uint256,uint256))', r], [[f'{r}_ltv', None ]]))

    vault_data = await Multicall(calls, WEB3_NETWORKS[network])()

    calls = []

    for vault in get_reserves:
        a_token = vault_data.get(f'{vault}_tokens')
        ltv = vault_data.get(f'{vault}_ltv')
        calls.append(Call(a_token[0], [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_custom, ltv[0] ]]))
        calls.append(Call(a_token[2], [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_borrowed', parsers.from_custom, ltv[0] ]]))
        
    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { }
     } }

    poolIDs = {}

    for stake in stakes:
        if 'stake' in stake:
            loaned = stakes[stake]
            borrowed = stakes[f'{stake.split("_")[0]}_borrowed']
            if loaned > 0 or borrowed > 0:
                addPool = stake.split('_')
                if addPool[0] not in poolNest[poolKey]['userData']:

                    underlying = addPool[0]       
                    collat = loaned
                    collat_rate = ltv = vault_data.get(f'{underlying}_ltv')[1] / 10000
                    borrow = borrowed
                    #rate = parsers.from_wei(snapshot[3])
                    poolNest[poolKey]['userData'][addPool[0]] = {'staked' : collat, 'want': underlying, 'borrowed' : borrow, 'rate' : collat_rate}
                    poolIDs['%s_%s_want' % (poolKey, addPool[0])] = underlying


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

#No Contract Address
async def get_just_pending(wallet,vaults,network,farm_id,reward_method,reward_token):
    contracts = vaults
    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for contract in contracts:
        calls.append(Call(contract, [f'{reward_method}(address)(uint256)', wallet], [[f'{contract}_pending', parsers.from_wei]]))

    stakes=await Multicall(calls, network, _strict=False)()

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

async def get_moneypot(wallet, rewards, farm_id, network_id, contract, vaults, token_pair=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for i,reward in enumerate(rewards):
            reward_address = reward['address']
            calls.append(Call(contract, [f'pendingTokenRewardsAmount(address,address)(uint256)', reward['address'], wallet], [[f'{reward_address}_{i}', parsers.from_wei]]))
        calls.append(Call(token_pair, [f'balanceOf(address)(uint256)', wallet], [[f'{token_pair}', parsers.from_wei]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        want_token = token_pair

        poolNest[poolKey]['userData'][contract] = {'want': token_pair, 'staked' : stakes[token_pair], 'contractAddress' : contract, 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, contract)] = want_token

        for i in range(0,len(rewards)):
            token = rewards[i]['address']
            token_id = f'{token}_{i}'
            pending = stakes[token_id]

            if pending > 0:
                reward_token_data = {'pending': pending, 'symbol' : rewards[i]['symbol'], 'token' : token}
                poolNest[poolKey]['userData'][contract]['gambitRewards'].append(reward_token_data)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_zombie_masterchef(wallet,farm_id,network_id,chef,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        pool_function = 'poolLength'
        pool_length = await Call(chef, [f'{pool_function}()(uint256)'],None,network)() 
        
        staked_function = 'userInfo'
        pending_function = 'pendingZombie'
        reward_token = '0x50ba8bf9e34f0f83f96a340387d1d3888ba4b3b5'
        reward_symbol = 'ZMBE'
        want_function = 'poolInfo'

        for pid in range(0,pool_length):
            calls.append(Call(chef, [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', parsers.from_wei]]))
            calls.append(Call(chef, [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_pending', parsers.from_wei]]))
            calls.append(Call(chef, [f'{want_function}(uint256)((address,uint256,uint256,uint256,uint256,bool,bool,address,address,uint256,uint256,uint256,uint256))', pid], [[f'{pid}ext_want', parsers.parse_zombie_pool]]))

        stakes=await Multicall(calls, network)()

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
        masterchef = farm_info[pool]['masterChef']
        if 'poolLength' in farm_info[pool]:
            pool_length = farm_info[pool]['poolLength']
        else:
            pool_length = 'poolLength'

        
        if farm_info[pool]['stakedFunction'] is not None and pool.lower() not in [
            '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08'.lower(),
            '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7'.lower(),
            '0xcc0a87F7e7c693042a9Cc703661F5060c80ACb43'.lower(),
            '0x31D3966DA1cAB3dE7E9221ed016484E4Bb03Ba02'.lower(),
            '0xE6DCE53f17FBF673f4FA60A38746F110517457B2'.lower(),
            '0x6Bb9EAb44Dc7f7e0a0454107F9e46Eedf0aA0285'.lower(),
            '0xA51054BDf0910E3cE9B233e6B5BdDc0931b2E2ED'.lower(),
            '0x752feacfda5c3b440fd6d40ecf338a86b568c2d2'.lower(),
            '0x63Df75d039f7d7A8eE4A9276d6A9fE7990D7A6C5'.lower(),
            '0x1da194f8baf85175519d92322a06b46a2638a530'.lower(),
            '0x189F734769cD18099d8a66d1224fef2b1fBf438D'.lower()
            ]:
            calls.append(Call(masterchef, f'{pool_length}()(uint256)', [[pool, None]]))
        elif pool.lower() in ['0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7'.lower()]:
            calls.append(Call(masterchef, 'getRewardsLength()(uint256)', [[pool, None]]))

    if '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' : 5}
        }
    elif '0xcc0a87F7e7c693042a9Cc703661F5060c80ACb43' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0xcc0a87F7e7c693042a9Cc703661F5060c80ACb43' : 2}
        }
    elif '0x31D3966DA1cAB3dE7E9221ed016484E4Bb03Ba02' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0x31D3966DA1cAB3dE7E9221ed016484E4Bb03Ba02' : 6}
        }
    elif '0xE6DCE53f17FBF673f4FA60A38746F110517457B2' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0xE6DCE53f17FBF673f4FA60A38746F110517457B2' : 5}
        }
    elif '0x6Bb9EAb44Dc7f7e0a0454107F9e46Eedf0aA0285' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0x6Bb9EAb44Dc7f7e0a0454107F9e46Eedf0aA0285' : 4}
        }
    elif '0xA51054BDf0910E3cE9B233e6B5BdDc0931b2E2ED' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0xA51054BDf0910E3cE9B233e6B5BdDc0931b2E2ED' : 2}
        }
    elif '0x752feacfda5c3b440fd6d40ecf338a86b568c2d2' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0x752feacfda5c3b440fd6d40ecf338a86b568c2d2' : 2}
        }
    elif '0x63Df75d039f7d7A8eE4A9276d6A9fE7990D7A6C5' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0x63Df75d039f7d7A8eE4A9276d6A9fE7990D7A6C5' : 7}
        }
    elif '0x1da194f8baf85175519d92322a06b46a2638a530' in pools:
        poolLengths = {
        **await Multicall(calls, network_conn)(),
        **{'0x1da194f8baf85175519d92322a06b46a2638a530' : 10}
        }
    elif '0x189F734769cD18099d8a66d1224fef2b1fBf438D' in pools:
        poolLengths = {
            **await Multicall(calls, network_conn)(),
            **{'0x189F734769cD18099d8a66d1224fef2b1fBf438D' : 5}
        }
    else:
        poolLengths = await Multicall(calls, network_conn)()

    return poolLengths

async def get_only_staked(wallet, pools, network, farm_info, user_config=False):
    
    calls = []
    network_conn = WEB3_NETWORKS[network]
    final = pools[1]
    
    
    for pool in pools[0]:
        masterchef = farm_info[pool]['masterChef']    
        stakedFunction = farm_info[pool]['stakedFunction']
        death_index = [] if 'death_index' not in farm_info[pool] else farm_info[pool]['death_index']
        rng = 1 if pool in ['0x0895196562C7868C5Be92459FaE7f877ED450452'] else 0
        end = 3 if pool in [''] else pools[0][pool]
        for i in range(rng, end):
            if i in death_index:
                continue
            # elif pool == '' and i == 0:
            #     continue
            else:
                if pool == '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4': 
                    calls.append(Call(masterchef, ['%s(address,uint256)(uint256)' % (stakedFunction), wallet, i], [['%s_%s' % (pool, i), None]]))
                else:
                    calls.append(Call(masterchef, ['%s(uint256,address)(uint256)' % (stakedFunction), i, wallet], [['%s_%s' % (pool, i), None]]))
    if user_config:
        return await parse_calls_master(calls)

    if len(calls) > 200:
        chunks = len(calls) / 100
        x = np.array_split(calls, math.ceil(chunks))
        all_calls=await asyncio.gather(*[Multicall(call,WEB3_NETWORKS[network])() for call in x])
        stakes = reduce(lambda a, b: dict(a, **b), all_calls)
    else:
        stakes = await Multicall(calls, WEB3_NETWORKS[network])()    

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

async def get_pending_want(wallet, stakes, network, farm_info, user_config=False):

    if user_config:
        final = None
    else:
        final = stakes[1]
    network_conn = WEB3_NETWORKS[network]
    calls = []

    for stake in stakes[0]:
        key = next(iter(stake.keys()))
        address = key.split('_')[0]
        poolID = int(key.split('_')[1])
        network_id = farm_info[address]['network']
        masterchef = farm_info[address]['masterChef']

        if farm_info[address]['pendingFunction'] is not None:
            pendingFunction = farm_info[address]['pendingFunction']
            if address not in ['0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904', '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4', '0xf730af26e87D9F55E46A6C447ED2235C385E55e0']:
                calls.append(Call(masterchef, ['%s(uint256,address)(uint256)' % (pendingFunction), poolID, wallet], [['%s_%s_pending' % (address, poolID), None]]))
            
            if address in ['0x0B29065f0C5B9Db719f180149F0251598Df2F1e4']:
                calls.append(Call(masterchef, [f'{pendingFunction}(address,uint256)(uint256)', wallet, poolID], [['%s_%s_pending' % (address, poolID), None]]))

            if address in ['0xf730af26e87D9F55E46A6C447ED2235C385E55e0']:
                calls.append(Call(masterchef, [f'userInfoMap(uint256,address)((uint256,uint256,uint256))', poolID, wallet], [['%s_%s_pending' % (address, poolID), parsers.parse_wanted_offset, 2]]))


        if farm_info[address]['stakedFunction'] is not None:
            if address in ['0xF1F8E3ff67E386165e05b2B795097E95aaC899F0', '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3', '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d', '0x6685C8618298C04b6E42dDAC06400cc5924e917e']:
                calls.append(Call(masterchef, ['poolInfo(uint256)((uint256,address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parsers.parse_wanted_offset, 1]]))
            elif address == '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7':
                calls.append(Call(masterchef, ['rewardsInfo(uint256)((address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parsers.parse_wanted_offset, 0]]))
            elif address == '0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904':
                calls.append(Call(masterchef, ['poolInfo(uint256)((address,address))', poolID], [['%s_%s_want' % (address, poolID), parsers.parse_wanted_offset, 0]]))
            elif address in [
                '0x6e2ad6527901c9664f016466b8DA1357a004db0f',
                '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F',
                '0x67da5f2ffaddff067ab9d5f025f8810634d84287',
                '0x7875Af1a6878bdA1C129a4e2356A3fD040418Be5',
                '0x8F5BBB2BB8c2Ee94639E55d5F41de9b4839C1280',
                '0x3a01521F8E7F012eB37eAAf1cb9490a5d9e18249',
                '0xd10eF2A513cEE0Db54E959eF16cAc711470B62cF',
                '0xF4d73326C13a4Fc5FD7A064217e12780e9Bd62c3',
                '0x73186f2Cf2493f20836b17b21ae79fc12934E207',
                '0xaeD5b25BE1c3163c907a471082640450F928DDFE',
                '0xd5609cD0e1675331E4Fb1d43207C8d9D83AAb17C',
                '0x13cc0A2644f4f727db23f5B9dB3eBd72134085b7',
                '0x7ecc7163469f37b777d7b8f45a667314030ace24',
                '0x23423292396a37c0c2e4d384dce7ab67738bec28',
                '0x3A3Ef6912d8D5b4E770f80F69635dcc9Ca1d7311',
                '0xC3842B2d35dd249755f170dD8F0f83b8BF967E21',
                '0x182CD0C6F1FaEc0aED2eA83cd0e160c8Bd4cb063',
                '0xSynHarmony',
                '0x067eC87844fBD73eDa4a1059F30039584586e09d',
                '0x02703e13b5d3d3056ac9321983b44a2cc065bb22',
                '0xD7b0B7a86441397097B71d9D009cc41F5C69F259'
                ]:
                calls.append(Call(masterchef, ['lpToken(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))
            elif address in ['0x876F890135091381c23Be437fA1cec2251B7c117', '0xBF65023BcF48Ad0ab5537Ea39C9242de499386c9', '0xd54AA6fEeCc289DeceD6cd0fDC54f78079495E79', '0x4dF0dDc29cE92106eb8C8c17e21083D4e3862533', '0xd3ab90ce1eecf9ab3cbae16a00acfbace30ebd75']:
                calls.append(Call(masterchef, ['poolInfo(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))
            elif address in ['0xEF6d860B22cEFe19Ae124b74eb80F0c0eb8201F4', '0x9c821500eaBa9f9737fDAadF7984Dff03edc74d1']:
                calls.append(Call(masterchef, ['getPoolInfo(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))
            elif address in ['0xf730af26e87D9F55E46A6C447ED2235C385E55e0']:
                calls.append(Call(masterchef, ['poolInfoList(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))
            elif address in ['0xaE0aF27df228ACd8BA91AF0c917a31A9a681A097']:
                calls.append(Call(masterchef, ['poolInfo(uint256)((uint256,address))', poolID], [['%s_%s_want' % (address, poolID), parsers.parse_wanted_offset, 1]]))    
            else:
                calls.append(Call(masterchef, ['poolInfo(uint256)((address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parsers.parse_wanted_offset, 0]]))

        if address == '0x89d065572136814230A55DdEeDDEC9DF34EB0B76':
            calls.append(Call(masterchef, ['poolInfo(uint256)((address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parsers.parse_wanted_offset, 0]]))

    if user_config:
        return await parse_calls(calls)

    stakes = await Multicall(calls, network_conn)()
        

    ##Should pull token decimals here
    if len(stakes) > 0:
        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

    if type(stakes) is dict:
        for stake in stakes:
                addPool = stake.split('_')
                
                if addPool[2] == 'want':
                    
                    value_key = f'{addPool[0]}_{addPool[1]}'

                    wanted = stakes[stake]
                    token_decimal = 18 if wanted not in token_decimals else token_decimals[wanted]
                    reward_decimal = 18 if 'decimal' not in farm_info[addPool[0]] else farm_info[addPool[0]]['decimal']
                    raw_stakes = final[addPool[0]]['userData'][int(addPool[1])]['staked']
                    raw_pending = 0 if f'{value_key}_pending' not in stakes else stakes[f'{value_key}_pending']
                    pool_id = int(addPool[1])

                    final[addPool[0]]['userData'][int(addPool[1])]['want'] = wanted
                    final[addPool[0]]['userData'][int(addPool[1])]['rawStakes'] = raw_stakes
                    final[addPool[0]]['userData'][int(addPool[1])]['rawPending'] = raw_pending
                    final[addPool[0]]['userData'][int(addPool[1])]['poolID'] = pool_id
                    final[addPool[0]]['userData'][int(addPool[1])]['contractAddress'] = addPool[0]
                    final[addPool[0]]['userData'][int(addPool[1])]['staked'] = parsers.from_custom(raw_stakes, token_decimal)
                    final[addPool[0]]['userData'][int(addPool[1])]['pending'] = parsers.from_custom(raw_pending, reward_decimal)

    else:
        stakes = {}
    return stakes, final

async def get_traditional_masterchef(wallet, pools, network, farm_info, return_obj, user_config=False):

    for farm in pools:
        if farm not in return_obj:
            return_obj[farm] = {'name' : farm_info[farm]['name'], 'network' : farm_info[farm]['network'], 'wallet' : wallet, 'userData' : {}}

    if user_config:
        pool_lengths = await get_pool_lengths(wallet, pools, network, farm_info)
        only_staked = await get_only_staked(wallet, (pool_lengths, return_obj), network, farm_info, user_config)
        #pending_wants = await get_pending_want(wallet, only_staked, network, farm_info, user_config)

        return only_staked

    pool_lengths = await get_pool_lengths(wallet, pools, network, farm_info)
    only_staked = await get_only_staked(wallet, (pool_lengths, return_obj), network, farm_info)
    pending_wants = await get_pending_want(wallet, only_staked, network, farm_info)

    return pending_wants

async def get_multireward(wallet,farm_id,network_id,farm_data,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        masterchef = farm_data['masterChef']

        staked_function = farm_data['stakedFunction']
        if 'wantFunction' not in farm_data:
            want_function = 'poolInfo'
        else:
            want_function = farm_data['wantFunction']

        for masterchef in vaults:
            calls.append(Call(masterchef, [f'{staked_function}(address)(uint256)', wallet], [[f'{masterchef}ext_staked', None]]))
            calls.append(Call(masterchef, [f'{want_function}()(address)'], [[f'{masterchef}ext_want', None]]))
            for i,each in enumerate(farm_data['rewards']):
                reward_decimal = each['rewardDecimal'] in each if 'rewardDecimal' in each else 18
                pending_function = each['function']
                calls.append(Call(masterchef, [f'{pending_function}(address)(uint256)', wallet], [[f'{masterchef}ext_pending{i}', parsers.from_custom, reward_decimal]]))

        stakes=await Multicall(calls, network, _strict=False)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : parsers.from_custom(staked,wanted_decimal), 'contractAddress' : breakdown[0][:-3], 'gambitRewards' : []}
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

#No Contract Address
async def get_lending_staked_rewards(wallet,farm_id,network_id,accrued_function,locked_function,accrue_contract,locked_contract,wanted_token,vaults=None):
        poolKey = farm_id

        network = WEB3_NETWORKS[network_id]

        reward_calls = []

        reward_calls.append(Call(locked_contract, [f'{locked_function}(address)(uint256)', wallet], [['staked', parsers.from_wei]]))
        reward_calls.append(Call(accrue_contract, [f'{accrued_function}(address)(uint256)', wallet], [['pending', parsers.from_wei]]))

        stakes=await Multicall(reward_calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = wanted_token
                pending = stakes['pending']

                if staked > 0 or pending > 0:
                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_qubit_lending_protocol(wallet,vaults,farm_id,network,snapshot='getAccountSnapshot'):

    poolKey = farm_id
    calls = []

    lending_vaults = vaults

    for vault in lending_vaults:
        vault_address = vault['address']
        calls.append(Call(vault_address, [f'{snapshot}(address)((uint256,uint256,uint256))', wallet], [[f'{vault_address}_accountSnapshot', None ]]))
        
    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { }
     } }

    poolIDs = {}

    hash_map = {x['address'] : x for x in lending_vaults}

    for stake in stakes:
        if stakes[stake][0] > 0 or stakes[stake][1] > 0:
            addPool = stake.split('_')
            if addPool[0] not in poolNest[poolKey]['userData']:

                snapshot =  stakes[stake]
                underlying = hash_map[addPool[0]]['want']
                underlying_decimal = hash_map[addPool[0]]['decimal']           
                collat = parsers.from_custom(snapshot[0], underlying_decimal)
                collat_rate = hash_map[addPool[0]]['collat_rate']
                borrow = parsers.from_custom(snapshot[1], underlying_decimal)
                rate = parsers.from_wei(snapshot[2])
                poolNest[poolKey]['userData'][addPool[0]] = {'staked' : collat * rate, 'want': underlying, 'borrowed' : borrow, 'rate' : collat_rate, 'contractAddress' : addPool[0]}
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = underlying


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_pancake_hunny_clones(wallet,farm_id,network_id,vaults,hive,hive_rewards,pending_hive,hive_token):
        poolKey = farm_id

        network = WEB3_NETWORKS[network_id]

        calls = []
        reward_tokens = []

        for vault in vaults:
            if vault != hive:
                calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', None]]))

                if vaults[vault]['reward_length'] == 3:
                    calls.append(Call(vault, [f'profitOf(address)((uint256,uint256,uint256))', wallet], [[f'{vault}_pending', None]]))
                elif vaults[vault]['reward_length'] == 2:
                    calls.append(Call(vault, [f'profitOf(address)((uint256,uint256))', wallet], [[f'{vault}_pending', None]]))
                
                if vault in ['0x434Af79fd4E96B5985719e3F5f766619DC185EAe']:
                    calls.append(Call(vault, [f'token()(address)'], [[f'{vault}_want', None]]))
                else:
                    calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))
                
                if 'rewards' in vaults[vault]:
                    reward_tokens += vaults[vault]['rewards']

        ##HIVE
        calls.append(Call(hive, [f'balanceOf(address)(uint256)', wallet], [[f'{hive}_staked', None]]))
        calls.append(Call(hive_rewards, [f'{pending_hive}(address,address)((uint256))', hive, wallet], [[f'{hive}_pending', None]]))
        calls.append(Call(hive_rewards, [f'{hive_token}()(address)'], [[f'{hive}_want', None]]))


        stakes= await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        reward_token_info = await template_helpers.get_token_list_decimals_symbols(reward_tokens, network_id)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    key = breakdown[0]
                    staked = parsers.from_custom(stakes[each], 18)
                    want_token = stakes[f'{key}_want']
                    vault_info = vaults[key]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    for i,each in enumerate(vault_info['rewards']):
                        symbol = reward_token_info[f'{each}_symbol']
                        offset = vault_info['rewards_offset'][i]
                        reward_gambit = {'pending': parsers.from_custom(stakes[f'{breakdown[0]}_pending'][offset], 18), 'symbol' : symbol, 'token' : each}

                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_gambit)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_vault_style_with_rewards(wallet, vaults, network_id, farm_id, staked=None, reward=None, pending_reward=None, user_info=None, pps=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        staked = 'token' if staked is None else staked
        reward = 'rewardsToken' if reward is None else reward
        pps = 'getRatio' if pps is None else pps
        pending_reward = 'getPendingReward' if pending_reward is None else pending_reward
        user_info = 'userInfo' if user_info is None else user_info
        pools = vaults

        for pool in pools:
            calls.append(Call(pool, [f'{user_info}(address)(uint256)', wallet], [[f'{pool}_staked', None]]))
            calls.append(Call(pool, [f'{pending_reward}(address)(uint256)', wallet], [[f'{pool}_pending', None]]))
            calls.append(Call(pool, [f'{staked}()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'{reward}()(address)'], [[f'{pool}_rewardtoken', None]]))
            calls.append(Call(pool, [f'{pps}()(uint256)'], [[f'{pool}_pps', parsers.from_wei]]))


        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    token_decimal = 18 if breakdown[0] not in token_decimals else token_decimals[breakdown[0]]
                    pps_value = stakes[f'{breakdown[0]}_pps']
                    pendings = stakes[f'{breakdown[0]}_pending']
                    reward_token = stakes[f'{breakdown[0]}_rewardtoken']

                    reward_calls = []
                    reward_calls.append(Call(reward_token, 'symbol()(string)', [[f'symbol', None]]))
                    reward_calls.append(Call(reward_token, 'decimals()(uint256)', [[f'decimal', None]]))

                    reward_data=await Multicall(reward_calls, network)()

                    reward_symbol = reward_data['symbol']
                    reward_decimal = reward_data['decimal']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : parsers.from_custom(staked, token_decimal), f'{pps}' : pps_value, 'pending' : parsers.from_custom(pendings, reward_decimal), 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'rewardDecimal' : reward_decimal, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
        
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_wonderland(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        MEMO_ADDRESS = "0x136Acd46C134E8269052c62A67042D6bDeDde3C9"
        TIME_ADDRESS = "0xb54f16fB19478766A268F172C9480f8da1a7c9C3"
        MIM_ADDRESS = "0x130966628846BFd36ff31a822705796e8cb8C18D"

        RESERVES = ['0x130966628846BFd36ff31a822705796e8cb8C18D', '0x113f413371fc4cc4c9d6416cf1de9dfd7bf747df']
        BONDS = ['0x694738E0A438d90487b4a549b201142c1a97B556', '0xA184AE1A71EcAD20E822cB965b99c287590c4FFe', '0xc26850686ce755FFb8690EA156E5A6cf03DcBDE1', '0xE02B1AA2c4BE73093BE79d763fdFFC0E3cf67318']

        for i,vault in enumerate(BONDS):
                calls.append(Call(vault, [f'bondInfo(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_custom, 9]]))
                calls.append(Call(vault, [f'pendingPayoutFor(address)(uint256)', wallet], [[f'{vault}_pending', parsers.from_custom, 9]]))
                calls.append(Call(vault, [f'percentVestedFor(address)(uint256)', wallet], [[f'{vault}_vested', None]]))
                #calls.append(Call(vault, [f'principle()(address)'], [[f'{vault}_want', None]]))

        calls.append(Call(MEMO_ADDRESS, [f'balanceOf(address)(uint256)', wallet], [[f'{MEMO_ADDRESS}_staked', parsers.from_custom, 9]]))
        calls.append(Call('0x4456B87Af11e87E329AB7d7C7A246ed1aC2168B9', [f'Memories()(address)'], [[f'{MEMO_ADDRESS}_want', None]]))


        stakes=await Multicall(calls, network)()

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    percentage = stakes[f'{breakdown[0]}_vested'] / 10000 if f'{breakdown[0]}_vested' in stakes else 1
                    staked = stakes[each]
                    staked_offset = staked * percentage
                    actual_staked = staked if staked == staked_offset else staked - staked_offset
                    want_token = stakes[f'{breakdown[0]}_want'] if f'{breakdown[0]}_want' in stakes else breakdown[0]
                    token_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked if actual_staked > 0 else 0, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    if f'{breakdown[0]}_pending' in stakes:
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : 'TIME', 'token' : TIME_ADDRESS, 'decimal' : 9}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'] = [reward_token_0]

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_gmx(wallet, vaults, farm_id, network_id):
        gmx = vaults
        poolKey = farm_id
        network = WEB3_NETWORKS[network_id]

        calls = []
        for stake in gmx:
            stake_token = stake['stakeToken']
            calls.append(Call(stake['contract'],['getDepositBalances(address,address[],address[])(uint256[])',wallet,[stake_token],[stake['rewardTracker']]], [[f'{stake_token}_staked', parsers.parse_gmx]]))
            for i,reward in enumerate(stake['rewards']):    
                calls.append(Call(reward['yieldTracker'],['claimable(address)(uint256)',wallet],[[f'{stake_token}_pending{i}', None]]))

        stakes = await Multicall(calls, network)() 

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        farm_infos = {x['stakeToken'] : x  for x in gmx}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = parsers.from_wei(stakes[each])
                    want_token = breakdown[0]
                    farm_info = farm_infos[breakdown[0]]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : farm_info['contract'], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    for i,reward in enumerate(farm_info['rewards']):
                        if f'{breakdown[0]}_pending{i}' in stakes:
                            reward_token_0 = {'pending': parsers.from_wei(stakes[f'{breakdown[0]}_pending{i}']), 'symbol' : reward['symbol'], 'token' : reward['rewardToken']}
                            poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest
        else:
            return None

async def get_tranchess(wallet, vaults, farm_id, network_id, tranch=None, helper=None, want_helper=None, fee_distribution=None, balance_call='availableBalanceOf'):
        
        poolKey = farm_id
        network = WEB3_NETWORKS[network_id]
        
        if tranch == None:
            tranch = ['M', 'A', 'B']
        
        if helper == None:
            helper = ['0x1216Be0c4328E75aE9ADF726141C2254c2Dcc1b6', '0xB13a07C57bA5297506c71e9c958210Fea8bbCEF0', '0x42867df3c1ce62613aae3f4238cbcf3d7630880b']
        
        if want_helper == None:
            want_helper = ['0xd6B3B86209eBb3C608f3F42Bf52818169944E402', '0x677b7304cb944b413d3c9aebc4d4b5da1a698a6b', '0x629d4562033e432b390d0808b54a82b0c4a0896b']
        
        if fee_distribution == None:
            fee_distribution = ['0x85ae5e9d510d8723438b0135CBf29d4F2E8BCda8', '0x67EB546A69c7e4d83F3c66018Fa549Dff5FED35b', '0xE06F85862af08c1C5F67F96e41eA663E29639DAe']
        
        # market = ['0x19Ca3baAEAf37b857026dfEd3A0Ba63987A1008D', '0x57C8041C6Aa3440843b5E48B16016A95F822195f', '0x15F2FeFcF313d397F9933C1Cb7590ab925d5cb59']

        calls = []
        reward_calls = []
        for w,help in enumerate(helper):
            for i,stake in enumerate(tranch):
                calls.append(Call(help,[f'{balance_call}(uint256,address)(uint256)',i, wallet], [[f'{stake}{w}{i}_staked', parsers.from_wei]]))
                calls.append(Call(want_helper[w],[f'token{stake}()(address)'], [[f'{stake}{w}{i}_want', None]]))

            reward_calls.append(Call(help,['claimableRewards(address)(uint256)', wallet], [[f'{help}_pending', parsers.from_wei]]))
            reward_calls.append(Call(fee_distribution[w],['claimableRewards(address)(uint256)', wallet], [[f'{fee_distribution[w]}_pending', parsers.from_wei]]))
            reward_calls.append(Call(fee_distribution[w],['rewardToken()(address)'], [[f'{fee_distribution[w]}_want', None]]))

        reward_calls.append(Call(fee_distribution[0],['userLockedBalances(address)(uint256)', wallet], [[f'chess_staked', parsers.from_wei]]))

        stakes = await Multicall(calls, network)() 
        chess_position = await Multicall(reward_calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

        total_pending_chess = sum([chess_position[f'{n}_pending'] for n in helper])

        if chess_position['chess_staked'] > 0 or total_pending_chess > 0:
            poolNest[poolKey]['userData']['chessPosition'] = {'want': '0x20de22029ab63cf9A7Cf5fEB2b737Ca1eE4c82A6', 'staked' : chess_position['chess_staked'], 'pending' : total_pending_chess}
            poolIDs['%s_%s_want' % (poolKey, 'chessPosition')] = '0x20de22029ab63cf9A7Cf5fEB2b737Ca1eE4c82A6'

        reward_tokens = {'0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c' : 'BTCB', '0x2170ed0880ac9a755fd29b2688956bd959f933f8' : 'ETH', '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c' : 'BNB'}

        for fee in fee_distribution:
            if chess_position[f'{fee}_pending'] > 0:
                    poolNest[poolKey]['userData'][chess_position[f'{fee}_want']] = {'want': chess_position[f'{fee}_want'], 'staked' : 0, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, chess_position[f'{fee}_want'])] = chess_position[f'{fee}_want']
                    reward_token_0 = {'pending': chess_position[f'{fee}_pending'], 'symbol' : reward_tokens[chess_position[f'{fee}_want']], 'token' : chess_position[f'{fee}_want']}
                    poolNest[poolKey]['userData'][chess_position[f'{fee}_want']]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest
        else:
            return None

async def get_spooky_stakes(wallet,farm_id,network_id,farm_data,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        if 'poolFunction' not in farm_data:
            pool_function = 'poolLength'
        else:
            pool_function = farm_data['poolFunction']
        
        pool_length = await Call(farm_data['masterChef'], [f'{pool_function}()(uint256)'],None,network)() 
        staked_function = farm_data['stakedFunction']
        pending_function = farm_data['pendingFunction']

        if 'wantFunction' not in farm_data:
            want_function = 'poolInfo'
        else:
            want_function = farm_data['wantFunction']

        for pid in range(0,pool_length):
            calls.append(Call(farm_data['masterChef'], [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_staked', parsers.from_wei]]))
            calls.append(Call(farm_data['masterChef'], [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_pending', None]]))
            calls.append(Call(farm_data['masterChef'], [f'{want_function}(uint256)(address)', pid], [[f'{pid}{farm_data["masterChef"]}ext_reward', None]]))
            calls.append(Call(farm_data['masterChef'], [f'xboo()(address)'],[[f'{pid}{farm_data["masterChef"]}ext_want', None]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}
        reward_metadata = await template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'reward' in x],network_id)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pending = stakes[f'{breakdown[0]}_pending']
                    reward_token = stakes[f'{breakdown[0]}_reward']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : parsers.from_custom(pending, reward_metadata[f'{reward_token}_decimals']), 'rewardToken' : reward_token, 'rewardSymbol' : reward_metadata[f'{reward_token}_symbol'], 'contractAddress' : farm_data['masterChef']}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
        
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_geist_lending_protocol(wallet,vaults,farm_id,network,snapshot='getAccountSnapshot'):

    poolKey = farm_id
    calls = []

    lending_vaults = vaults

    for vault in lending_vaults:
        vault_address = vault['address']
        calls.append(Call(vault_address, [f'{snapshot}(address)((uint256,uint256))', wallet], [[f'{vault_address}_accountSnapshot', None ]]))
        
    stakes=await Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { }
     } }

    poolIDs = {}

    hash_map = {x['address'] : x for x in lending_vaults}

    for stake in stakes:
        if stakes[stake][0] > 0 or stakes[stake][1] > 0:
            addPool = stake.split('_')
            if addPool[0] not in poolNest[poolKey]['userData']:

                snapshot =  stakes[stake]
                underlying = hash_map[addPool[0]]['want']
                underlying_decimal = hash_map[addPool[0]]['decimal']           
                collat = parsers.from_custom(snapshot[0], underlying_decimal)
                collat_rate = hash_map[addPool[0]]['collat_rate']
                borrow = parsers.from_custom(snapshot[1], underlying_decimal)
                poolNest[poolKey]['userData'][addPool[0]] = {'staked' : collat, 'want': underlying, 'borrowed' : borrow, 'rate' : collat_rate, 'contractAddress' : addPool[0]}
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = underlying

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_singular_masterchef(wallet,farm_id,network_id,farm_data,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        pool_length = await Call(farm_data['masterChef'], [f'poolLength()(uint256)'],None,network)()

        for pid in range(0,pool_length):
            if pid not in [14]:
                calls.append(Call(farm_data['masterChef'], [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}s_staked', parsers.from_wei]]))
                calls.append(Call(farm_data['masterChef'], [f'pendingSing(uint256,address)(uint256)', pid, wallet], [[f'{pid}s_pending', parsers.from_wei]]))
                calls.append(Call(farm_data['masterChef'], [f'pendingEarned(uint256,address)(uint256)', pid, wallet], [[f'{pid}s_pending1', parsers.from_wei]]))
                calls.append(Call(farm_data['masterChef'], [f'poolInfo(uint256)(address)', pid], [[f'{pid}s_want', None]]))
                if network_id == 'ftm':
                    calls.append(Call(farm_data['masterChef'], [f'poolInfo(uint256)((address,uint256,uint256,uint256,uint16,uint256,bool,uint256))', pid], [[f'{pid}s_rewardtoken', parsers.parse_singular_reward]]))
                else:
                    calls.append(Call(farm_data['masterChef'], [f'WL_earn()(address)'], [[f'{pid}s_rewardtoken', None]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_symbols = await template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'rewardtoken' in x],network_id)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked,'contractAddress' : farm_data['masterChef'], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
                    if stakes[f'{breakdown[0]}_pending'] > 0:
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : 'SING', 'token' : farm_data['reward']}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

                    if stakes[f'{breakdown[0]}_pending1'] > 0:
                        reward_address = stakes[f'{breakdown[0]}_rewardtoken']
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending1'], 'symbol' : token_symbols[f'{reward_address}_symbol'], 'token' : stakes[f'{breakdown[0]}_rewardtoken']}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)                    


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_voltswap(wallet, farm_id, network_id, vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        for geyser in vaults['geysers']:
            calls.append(Call(geyser['id'], [f'getGeyserData()((uint256,address,address))'], [[f"{geyser['id']}_tokens", None]]))
            for vault in vaults['user_vaults']:
                calls.append(Call(geyser['id'], [f'getVaultData(address)((uint256,uint256))', vault['id']], [[f"{geyser['id']}_{vault['id']}_user", None]]))
                calls.append(Call(geyser['id'], [f'getCurrentVaultReward(address)(uint256)', vault['id']], [[f"{geyser['id']}_{vault['id']}_reward", None]]))

        stakes=await template_helpers.multicall_chunk(calls, network, 15, 10)

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        token_symbols = await template_helpers.get_token_list_decimals_symbols([stakes[x][2] for x in stakes if 'tokens' in x],network_id)
        geysers = {}
        for each in stakes:
            if 'user' in each:
                if stakes[each][1] > 0:
                    breakdown = each.split('_')
                    staked = parsers.from_wei(stakes[each][1])
                    pending = stakes[f'{breakdown[0]}_{breakdown[1]}_reward']
                    want_token = stakes[f'{breakdown[0]}_tokens'][1]
                    reward_token = stakes[f'{breakdown[0]}_tokens'][2]
                    reward_symbol = token_symbols[f'{reward_token}_symbol']
                    reward_decimal = token_symbols[f'{reward_token}_decimals']

                    if want_token in geysers:
                        geyser_key = geysers[want_token]
                        reward_token_0 = {'pending': parsers.from_custom(pending, reward_decimal), 'symbol' : reward_symbol, 'token' : reward_token, 'decimal' : reward_decimal}
                        poolNest[poolKey]['userData'][geyser_key]['gambitRewards'].append(reward_token_0)
                    else:
                        geysers[want_token] = breakdown[0]
                        poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                        poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                    
                        reward_token_0 = {'pending': parsers.from_custom(pending, reward_decimal), 'symbol' : reward_symbol, 'token' : reward_token, 'decimal' : reward_decimal}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
        

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_sushi_masterchef(wallet,farm_id,network_id,farm_data,vaults,pending_function='pendingSushi'):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        pool_length = await Call(farm_data['masterChef'], [f'poolLength()(uint256)'],None,network)() 
        if 'dead_pools' in farm_data:
            dead_pools = farm_data['dead_pools']
        else:
            dead_pools = []

        for pid in range(0,pool_length):
            if pid not in dead_pools:
                calls.append(Call(farm_data['masterChef'], [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_staked', parsers.from_wei]]))
                calls.append(Call(farm_data['masterChef'], [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_pending', parsers.from_wei]]))
                calls.append(Call(farm_data['rewarder'], [f'pendingToken(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_extra', parsers.from_wei]]))
                calls.append(Call(farm_data['masterChef'], [f'lpToken(uint256)(address)', pid], [[f'{pid}{farm_data["masterChef"]}ext_want', None]]))
        
        stakes=await Multicall(calls, network, _strict=False)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : farm_data['masterChef'], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    if stakes[f'{breakdown[0]}_pending'] > 0:
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : farm_data['r0sym'], 'token' : farm_data['r0t']}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

                    if stakes[f'{breakdown[0]}_extra'] > 0:
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_extra'], 'symbol' : farm_data['r1sym'], 'token' : farm_data['r1t']}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_euler_staking(wallet,farm_id,network_id,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for vault in vaults:
            calls.append(Call(vault, [f'getUserInfo(address)((uint256,uint256))', wallet], [[f'{vault}_staked', None]]))        
            calls.append(Call(vault, [f'euler()(address)'], [[f'{vault}_want', None]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each][0] > 0:
                    breakdown = each.split('_')
                    staked = parsers.from_wei(stakes[each][0])
                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    reward_token_0 = {'pending': parsers.from_wei(stakes[each][1]), 'symbol' : 'EULER', 'token' : want_token}
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_balance_earn(wallet, vaults, farm_id, network, reward_info, want_function=None):
    network_conn = WEB3_NETWORKS[network]
    if want_function is None:
        want_function = 'stakingToken'
    else:
        want_function = want_function

    poolKey = farm_id
    calls = []

    
    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_wei]]))
        calls.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
        calls.append(Call(vault, [f'{want_function}()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network_conn, _strict=False)()

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

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append({'pending': parsers.from_custom(pending, reward_info['decimal']), 'symbol' : reward_info['symbol'], 'token' : reward_info['token']})
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_ohm(wallet, vaults, farm_id, network_id, reward_symbol):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        MEMO_ADDRESS = vaults['MEMO_ADDRESS']
        TIME_ADDRESS = vaults['TIME_ADDRESS']

        BONDS = vaults['BONDS']

        for i,vault in enumerate(BONDS):
                calls.append(Call(vault, [f'bondInfo(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_custom, 9]]))
                calls.append(Call(vault, [f'pendingPayoutFor(address)(uint256)', wallet], [[f'{vault}_pending', parsers.from_custom, 9]]))
                calls.append(Call(vault, [f'percentVestedFor(address)(uint256)', wallet], [[f'{vault}_vested', None]]))

        calls.append(Call(MEMO_ADDRESS, [f'balanceOf(address)(uint256)', wallet], [[f'{MEMO_ADDRESS}_staked', parsers.from_custom, 9]]))
        calls.append(Call(vaults['OHM_CONTRACT'], [f"{vaults['OHM_FUNCTION']}()(address)"], [[f'{MEMO_ADDRESS}_want', None]]))

        stakes=await Multicall(calls, network)()

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    percentage = stakes[f'{breakdown[0]}_vested'] / 10000 if f'{breakdown[0]}_vested' in stakes else 1
                    staked = stakes[each]
                    staked_offset = staked * percentage
                    actual_staked = staked if staked == staked_offset else staked - staked_offset
                    want_token = stakes[f'{breakdown[0]}_want'] if f'{breakdown[0]}_want' in stakes else breakdown[0]
                    token_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked if actual_staked > 0 else 0, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    if f'{breakdown[0]}_pending' in stakes:
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : reward_symbol, 'token' : TIME_ADDRESS, 'decimal' : 9}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'] = [reward_token_0]

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_native_ohm(wallet, vaults, farm_id, network_id, reward_symbol):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        OHM_ADDRESS = vaults['OHM_ADDRESS']
        SOHM_ADDRESS = vaults['SOHM_ADDRESS']
        GOHM_ADDRESS = vaults['GOHM_ADDRESS']

        BONDS = vaults['BONDS']

        for i,vault in enumerate(BONDS):
                calls.append(Call(vault, [f'bondInfo(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_custom, 9]]))
                calls.append(Call(vault, [f'pendingPayoutFor(address)(uint256)', wallet], [[f'{vault}_pending', parsers.from_custom, 9]]))
                calls.append(Call(vault, [f'percentVestedFor(address)(uint256)', wallet], [[f'{vault}_vested', None]]))

        calls.append(Call(SOHM_ADDRESS, [f'balanceOf(address)(uint256)', wallet], [[f'{SOHM_ADDRESS}_staked', parsers.from_custom, 9]]))
        calls.append(Call(vaults['OHM_CONTRACT'], [f"{vaults['SOHM_FUNCTION']}()(address)"], [[f'{SOHM_ADDRESS}_want', None]]))

        calls.append(Call(GOHM_ADDRESS, [f'balanceOf(address)(uint256)', wallet], [[f'{GOHM_ADDRESS}_staked', parsers.from_custom, 18]]))
        calls.append(Call(vaults['OHM_CONTRACT'], [f"{vaults['GOHM_FUNCTION']}()(address)"], [[f'{GOHM_ADDRESS}_want', None]]))

        stakes=await Multicall(calls, network)()

        token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    percentage = stakes[f'{breakdown[0]}_vested'] / 10000 if f'{breakdown[0]}_vested' in stakes else 1
                    staked = stakes[each]
                    staked_offset = staked * percentage
                    actual_staked = staked if staked == staked_offset else staked - staked_offset
                    want_token = stakes[f'{breakdown[0]}_want'] if f'{breakdown[0]}_want' in stakes else breakdown[0]
                    token_decimal = 18 if want_token not in token_decimals else token_decimals[want_token]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked if actual_staked > 0 else 0, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    if f'{breakdown[0]}_pending' in stakes:
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : reward_symbol, 'token' : OHM_ADDRESS, 'decimal' : 9}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'] = [reward_token_0]

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_wagmi_bonds(wallet, vaults, farm_id, network_id, reward_symbol):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        BONDS = vaults['BONDS']

        for i,vault in enumerate(BONDS):
                calls.append(Call(vault, [f'userInfo(address)(uint256)', wallet], [[f'{vault}_staked', parsers.from_custom, 18]]))
                calls.append(Call(vault, [f'claimablePayout(address)(uint256)', wallet], [[f'{vault}_pending', parsers.from_custom, 18]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    pending = stakes[f'{breakdown[0]}_pending']
                    actual_staked = staked - pending
                    want_token = stakes[f'{breakdown[0]}_want'] if f'{breakdown[0]}_want' in stakes else breakdown[0]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked if actual_staked > 0 else 0, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    if f'{breakdown[0]}_pending' in stakes:
                        reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : reward_symbol, 'token' : vaults['REWARD'], 'decimal' : 18}
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'] = [reward_token_0]

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_strong_block(wallet,farm_id,network_id, vaults, contract, reward_function):

        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        pool_length = await Call(contract, [f'entityNodeCount(address)(uint128)', wallet],None,network)() 

        for pid in range(0,pool_length+1):
                calls.append(Call(contract, [f'{reward_function}(uint256)', wallet, pid], [[f'{pid}_pending', parsers.from_wei]]))

        stakes=await Multicall(calls, network, _strict=False)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        total_pending = sum([stakes[n] for n in stakes])

        if total_pending > 0:
            want_token = '0x990f341946a3fdb507ae7e52d17851b87168017c'

            poolNest[poolKey]['userData'][contract] = {'want': want_token, 'staked' : 0, 'contractAddress' : contract, 'gambitRewards' : []}
            poolIDs['%s_%s_want' % (poolKey, contract)] = want_token

            reward_token_0 = {'pending': total_pending, 'symbol' : 'STRONG', 'token' : want_token}
            poolNest[poolKey]['userData'][contract]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

#No Contract Address
async def get_node_layout(wallet,farm_id,network_id,vaults):

        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        for i,node in enumerate(vaults['nodes']):
                calls.append(Call(node, [f'_getNodesCreationTime(address)(string)', wallet], [[f"{i}", None]]))

        node_strings = await Multicall(calls, network, _strict=False)()

        pending_calls = []

        for node in node_strings:
            node_id = int(node)
            for i, timestamp in enumerate(node_strings[node].split('#')):

                pending_calls.append(Call(vaults['nodes'][node_id], [f'_getNodeRewardAmountOf(address,uint256)(uint256)', wallet, int(timestamp)], [[f"{node_id}_{i}", parsers.from_wei]]))

        stakes=await Multicall(pending_calls, network, _strict=False)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for pending in node_strings:
            node_id = int(pending)
            want_token = vaults['reward_token']
            node_length = len(node_strings[pending].split('#'))

            total_pending = sum([stakes[f'{node_id}_{n}'] for n in range(0, node_length)])
            
            poolNest[poolKey]['userData'][node_id] = {'want': want_token, 'staked' : 0, 'gambitRewards' : []}
            poolIDs['%s_%s_want' % (poolKey, node_id)] = want_token

            reward_token_0 = {'pending': total_pending, 'symbol' : vaults['reward_symbol'], 'token' : want_token}
            poolNest[poolKey]['userData'][node_id]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_node_layout_2(wallet,farm_id,network_id,node_manager,reward_token,reward_symbol,vaults):

        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        node_info = await Call(node_manager, ['getAllNodes(address)((string,uint256,uint256,uint256,uint256,bool)[])', wallet], None, network)()

        pending_calls = []

        for i, node in enumerate(node_info):
            creation_time = node[1]
            node_id = node[0]
            pending_calls.append(Call(node_manager, [f'getNodeRewards(address,uint256)((uint256,uint256,uint256))', wallet, i], [[f"{node_id}", None]]))

        stakes=await Multicall(pending_calls, network, _strict=False)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for i, pending in enumerate(stakes):
            node_id = node_info[i][0]
            want_token = reward_token
            
            poolNest[poolKey]['userData'][node_id] = {'want': want_token, 'staked' : 0, 'gambitRewards' : []}
            poolIDs['%s_%s_want' % (poolKey, node_id)] = want_token

            reward_token_0 = {'pending': parsers.from_custom(stakes[pending][2], 18), 'symbol' : reward_symbol, 'token' : want_token}
            poolNest[poolKey]['userData'][node_id]['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None


async def get_planets(wallet,farm_id,network_id,contract,reward_symbol,reward_token,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
       
        planet_list = await Call(contract, [f'getPlanetIdsOf(address)(uint256[])', wallet],None, network)()

        for planet in planet_list:
            calls.append(Call(contract, [f'getPlanetsByIds(uint256[])(((uint256,uint256,uint256,uint256),uint256,uint256,uint256,uint256))', [planet]], [[f'planet{planet}', None]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        total_pending = sum([parsers.from_wei(stakes[each][2]) for each in stakes])

        if total_pending > 0:
            staked = 0
            want_token = reward_token
            pending = total_pending

            poolNest[poolKey]['userData']['planetrewards'] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'contractAddress' : contract}
            poolIDs['%s_%s_want' % (poolKey, 'planetrewards')] = want_token
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_voltage_single(wallet,farm_id,network_id,vaults,reward_token):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        calls.append(Call(vault, [f'earned(address,address)(uint256)', wallet, reward_token], [[f'{vault}_pending', parsers.from_wei]]))
        calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)
    reward_symbol = await Call(reward_token, [f'symbol()(string)'], _w3=network)()
    
    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                want_token = stakes[f'{breakdown[0]}_want']
                staked = parsers.from_custom(stakes[each], 18 if want_token not in token_decimals else token_decimals[want_token])

                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : reward_symbol, 'token' : reward_token}

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_sovryn_masterchef(wallet,farm_id,network_id,masterchef,reward_token, reward_symbol, vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        pool_length = await Call(masterchef, [f'getPoolLength()(uint256)'],None,network)() 

        for pid in range(0,pool_length):
            calls.append(Call(masterchef, [f'userInfoMap(uint256,address)(uint256)', pid, wallet], [[f'{pid}{masterchef}ext_staked', parsers.from_wei]]))
            calls.append(Call(masterchef, [f'poolInfoList(uint256)(address)', pid], [[f'{pid}{masterchef}ext_want', None]]))
        
        calls.append(Call(masterchef, ['getUserAccumulatedRewardList(address)(uint256[])', wallet], [[f'{masterchef}ext_rewards', None]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for i, reward in enumerate(list(stakes[f'{masterchef}ext_rewards'])):
            stakes[f'{i}{masterchef}ext_pending'] = parsers.from_custom(reward, 18)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pending = stakes[f'{breakdown[0]}_pending'] if f'{breakdown[0]}_pending' in stakes else 0

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'contractAddress' : masterchef}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_solidly_gauges(wallet,voting,farm_id,network_id,vaults):
        poolKey = farm_id
        pcalls = []
        gcalls = []
        bcalls = []
        rcalls = []
        calls = []

        network = WEB3_NETWORKS[network_id]
        
        pool_length = await Call(voting, ['length()(uint256)'],None,network)() 

        ##Get Pools
        for pid in range(0,pool_length):
            pcalls.append(Call(voting, ['pools(uint256)(address)', pid], None))

        pools=await Multicall(pcalls, network, _list=True)()

        ##Get Gauges
        for pool in pools:
            gcalls.append(Call(voting, ['gauges(address)(address)', pool], None))

        gauges=await Multicall(gcalls, network, _list=True)()

        ##Get Bribes
        for gauge in gauges:
            bcalls.append(Call(voting, ['bribes(address)(address)', gauge], None))

        bribes=await Multicall(bcalls, network, _list=True)()

        ##Get Rewards Length
        for gauge,bribe in zip(gauges,bribes):
            calls.append(Call(gauge, ['balanceOf(address)(uint256)', wallet], [[f'{gauge}_staked', None]]))
            rcalls.append(Call(gauge, ['rewardsListLength()(uint256)'], [[f'{gauge}_glength', None]]))
            rcalls.append(Call(bribe, ['rewardsListLength()(uint256)'], [[f'{gauge}_blength', None]]))

        reward_lengths=await Multicall(rcalls, network)()

        ##Get Rewards Tokens
        rcalls = []
        for gauge,bribe in zip(gauges,bribes):
            glength = reward_lengths.get(f'{gauge}_glength')
            blength = reward_lengths.get(f'{gauge}_blength')
            
            for i in range(0,glength):
                rcalls.append(Call(gauge, ['rewards(uint256)(address)', i], [[f'{gauge}_{i}_gtoken', None]]))

            for i in range(0,blength):
                rcalls.append(Call(bribe, ['rewards(uint256)(address)', i], [[f'{gauge}_{i}_btoken', None]]))

        reward_tokens=await Multicall(rcalls, network)()

        for gauge,bribe in zip(gauges,bribes):
            glength = reward_lengths.get(f'{gauge}_glength')
            blength = reward_lengths.get(f'{gauge}_blength')
            
            for i in range(0,glength):
                calls.append(Call(gauge, ['earned(address,address)(uint256)', reward_tokens.get(f'{gauge}_{i}_gtoken'), wallet], [[f'{gauge}_{i}_greward', None]]))

            for i in range(0,blength):
                btoken = reward_lengths.get(f'{gauge}_{i}_gtoken')
                calls.append(Call(bribe, ['earned(address,uint256)(uint256)', wallet, i], [[f'{gauge}_{i}_breward', None]]))

        stakes=await Multicall(calls, network)()

        lp_token_meta = await template_helpers.get_token_list_decimals(pools,network_id,parse_wanted=False)  
        reward_token_meta = await template_helpers.get_token_list_decimals_symbols([x for x in set(reward_tokens.values())],network_id)    
            
        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for p, gauge in enumerate(gauges):
            want_token = pools[p]
            staked = parsers.from_custom(stakes.get(f'{gauge}_staked'), lp_token_meta.get(want_token))
            if staked > 0:
                poolNest[poolKey]['userData'][gauge] = {'want': want_token, 'staked' : staked, 'contractAddress' : gauge, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, gauge)] = want_token

                glength = reward_lengths.get(f'{gauge}_glength')
                blength = reward_lengths.get(f'{gauge}_blength')

                for i in range(0,glength):
                    reward_token = reward_tokens.get(f'{gauge}_{i}_gtoken')
                    reward_decimal = reward_token_meta.get(f'{reward_token}_decimals')
                    pending_reward = parsers.from_custom(stakes.get(f'{gauge}_{i}_greward'), reward_decimal)
                    if pending_reward > 0:
                        reward_token_0 = {'pending': pending_reward, 'symbol' : reward_token_meta.get(f'{reward_token}_symbol'), 'token' : reward_token}
                        poolNest[poolKey]['userData'][gauge]['gambitRewards'].append(reward_token_0)
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_protofi_gauges(wallet,voting,farm_id,network_id,want,reward,vaults):
        poolKey = farm_id
        gcalls = []
        calls = []

        network = WEB3_NETWORKS[network_id]
        
        pools=await Call(voting, ['tokens()(address[])'], None, network)()

        ##Get Gauges
        for pool in pools:
            gcalls.append(Call(voting, ['gauges(address)(address)', pool], None))

        gauges=await Multicall(gcalls, network, _list=True)()

        ##Get Rewards Length
        for gauge in gauges:
            calls.append(Call(gauge, ['balanceOf(address)(uint256)', wallet], [[f'{gauge}_staked', None]]))
            calls.append(Call(gauge, [f'{want}()(address)'], [[f'{gauge}_want', None]]))
            calls.append(Call(gauge, ['earned(address)(uint256)', wallet], [[f'{gauge}_pending', None]]))
            calls.append(Call(gauge, [f'{reward}()(address)'], [[f'{gauge}_reward', None]]))

        stakes=await Multicall(calls, network)()

        token_decimals= await template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'want' in x or 'reward' in x],network_id)  
            
        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    want_token = stakes[f'{breakdown[0]}_want']
                    reward_token = stakes[f'{breakdown[0]}_reward']
                    staked = parsers.from_custom(stakes[each], token_decimals.get(f'{want_token}_decimals'))
                    pending = parsers.from_custom(stakes[f'{breakdown[0]}_pending'], token_decimals.get(f'{reward_token}_decimals'))
                    reward_symbol = token_decimals.get(f'{reward_token}_symbol')

                    reward_token_0 = {'pending': pending, 'symbol' : reward_symbol, 'token' : reward_token}

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_solidex(wallet,depositor,farm_id,network_id,vaults,reward_meta):
        poolKey = farm_id
        calls = []

        network = WEB3_NETWORKS[network_id]
        
        ##Get Pools
        for i, pool in enumerate(vaults):
            calls.append(Call(depositor, ['userBalances(address,address)(uint256)', wallet, pool], [[f'{pool}_{i}_staked', None]]))
            # calls.append(Call(depositor, ['tokenForPool(address)(address)', pool], [[f'{pool}_want', None]]))
            calls.append(Call(depositor, ['pendingRewards(address,address[])((uint256,uint256,uint256,uint256))', wallet, [pool]], [[f'{pool}_pending', None]]))

        stakes=await Multicall(calls, network)()

        lp_token_meta = await template_helpers.get_token_list_decimals(vaults,network_id,parse_wanted=False)  
            
        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                
                    breakdown = each.split('_')
                    want_token = vaults[int(breakdown[1])]
                    staked = parsers.from_custom(stakes[each], lp_token_meta.get(want_token))
                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : depositor, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    for i in range(0,len(reward_meta)):
                        reward_token = reward_meta[i]['a']
                        reward_decimal = reward_meta[i]['d']
                        pending_reward = parsers.from_custom(stakes.get(f'{breakdown[0]}_pending')[2+i], reward_decimal)
                        if pending_reward > 0:
                            reward_token_0 = {'pending': pending_reward, 'symbol' : reward_meta[i]['s'], 'token' : reward_token}
                            poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_xliquid(wallet,fee_dist,xtoken,reward_length,farm_id,network_id,vaults):
        poolKey = farm_id
        calls = []
        rcalls = []
        network = WEB3_NETWORKS[network_id]
        
        ##Get Pools
        for pid in range(0,reward_length):
            rcalls.append(Call(fee_dist, ['tokens(uint256)(address)', pid], None))

        reward_tokens=await Multicall(rcalls, network, _list=True)()

        calls.append(Call(xtoken, ['locked(address)(int128)', wallet], [[f'staked', None]]))
        calls.append(Call(xtoken, ['token()(address)'], [[f'want', None]]))
        calls.append(Call(fee_dist, ['claim(address)((uint256,uint256,uint256,uint256,uint256,uint256,uint256))', wallet], [[f'reward', None]]))

        stakes=await Multicall(calls, network)()

        reward_token_meta = await template_helpers.get_token_list_decimals_symbols(reward_tokens,network_id)    

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}


        want_token = stakes.get('want')
        staked = parsers.from_custom(stakes.get('staked'), 18)
        if staked > 0:
            poolNest[poolKey]['userData'][xtoken] = {'want': want_token, 'staked' : staked, 'contractAddress' : xtoken, 'gambitRewards' : []}
            poolIDs['%s_%s_want' % (poolKey, xtoken)] = want_token

            for i in range(0,reward_length):
                reward_token = reward_tokens[i]
                reward_decimal = reward_token_meta.get(f'{reward_token}_decimals')
                pending_reward = parsers.from_custom(stakes.get('reward')[i], reward_decimal)
                if pending_reward > 0:
                    reward_token_0 = {'pending': pending_reward, 'symbol' : reward_token_meta.get(f'{reward_token}_symbol'), 'token' : reward_token}
                    poolNest[poolKey]['userData'][xtoken]['gambitRewards'].append(reward_token_0)
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_factory_lps(wallet, farm_id, network_id, factory, vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        
        pool_length = await Call(factory, [f'allPairsLength()(uint256)'],None,network)() 

        for pid in range(0,pool_length):
            calls.append(Call(factory, [f'allPairs(uint256)(address)', pid], None))
        
        all_lps=await Multicall(calls, network, _list=True)()

        calls = []

        for pool in all_lps:
            calls.append(Call(pool, [f'balanceOf(address)(uint256)', wallet], [[f'{pool}_staked', parsers.from_wei]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = breakdown[0]
                    pending = 0

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'contractAddress' : breakdown[0]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_lens(wallet, lens, farm_id, network_id, vaults):
        poolKey = farm_id
        calls = []
        rcalls = []
        network = WEB3_NETWORKS[network_id]
        
        stakes=await Call(
            lens,
            ['stakingPoolsPositions(address)((address,address,address,uint256,(address,uint256,uint256,uint256,uint256)[])[])',
            wallet],
            None,
            network)()

        tokens = []

        for t in stakes:
            if t[2] not in tokens:
                tokens.append(t[2])
            for r in t[4]:
                if r[0] not in tokens:
                    tokens.append(r[0])

        token_meta = await template_helpers.get_token_list_decimals_symbols(tokens,network_id)    

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for position in stakes:
            want_token = position[2]
            staked = parsers.from_custom(position[3], token_meta.get(f'{want_token}_decimals'))
            otoken = position[0]

            poolNest[poolKey]['userData'][otoken] = {'want': want_token, 'staked' : staked, 'contractAddress' : otoken, 'gambitRewards' : []}
            poolIDs['%s_%s_want' % (poolKey, otoken)] = want_token

            for r in position[4]:
                reward_token = r[0]
                reward_decimal = token_meta.get(f'{reward_token}_decimals')
                pending_reward = parsers.from_custom(r[4], reward_decimal)

                reward_token_0 = {'pending': pending_reward, 'symbol' : token_meta.get(f'{reward_token}_symbol'), 'token' : reward_token}
                poolNest[poolKey]['userData'][otoken]['gambitRewards'].append(reward_token_0)
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_spintop_vault(wallet, vaults, farm_id, network_id):

    poolKey = farm_id
    calls = []

    network=WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'getUserStaked(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        calls.append(Call(vault, [f'vaultInfo()((address,address,address))'], [[f'{vault}_want', None]]))    

    stakes=await Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = await template_helpers.get_token_list_decimals(vaults,network_id,False)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                token_decimal = 18 if breakdown[0] not in token_decimals else token_decimals[breakdown[0]]
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want'][2]
                real_staked = parsers.from_custom(staked, token_decimal)

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : real_staked, 'contractAddress' : breakdown[0], 'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None


async def get_no_pending_lock(wallet, vaults, farm_id, network_id, staked_function, staked_return, want_function):

    poolKey = farm_id
    calls = []

    network=WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'{staked_function}(address)({staked_return})', wallet], [[f'{vault}_staked', None]]))
        calls.append(Call(vault, [f'{want_function}()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = await template_helpers.get_token_list_decimals(stakes,network_id,True)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                token_decimal = 18 if breakdown[0] not in token_decimals else token_decimals[breakdown[0]]
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']
                real_staked = parsers.from_custom(staked, token_decimal)

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : real_staked, 'contractAddress' : breakdown[0], 'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_double_syrup(wallet,farm_id,network_id,vaults,staking_token,earned,token_a,token_b):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        calls.append(Call(vault, [f'{earned}(address)((uint256,uint256))', wallet], [[f'{vault}_pending', None]]))
        calls.append(Call(vault, [f'{token_a}()(address)'], [[f'{vault}_rewardTokenA', None]]))
        calls.append(Call(vault, [f'{token_b}()(address)'], [[f'{vault}_rewardTokenB', None]]))
        calls.append(Call(vault, [f'{staking_token}()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_symbols = await template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'rewardTokenA' in x or 'rewardTokenB' in x or 'want' in x],network_id)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                
                want_token = stakes[f'{breakdown[0]}_want']
                reward_tokenA = stakes[f'{breakdown[0]}_rewardTokenA']
                reward_tokenB = stakes[f'{breakdown[0]}_rewardTokenB']
                staked = parsers.from_custom(stakes[each], token_symbols.get(f'{want_token}_decimals'))


                reward_token_0 = {'pending': parsers.from_custom(stakes[f'{breakdown[0]}_pending'][0], token_symbols.get(f'{reward_tokenA}_decimals')), 'symbol' : token_symbols.get(f'{reward_tokenA}_symbol'), 'token' : reward_tokenA}
                reward_token_1 = {'pending': parsers.from_custom(stakes[f'{breakdown[0]}_pending'][1], token_symbols.get(f'{reward_tokenB}_decimals')), 'symbol' : token_symbols.get(f'{reward_tokenB}_symbol'), 'token' : reward_tokenB}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : breakdown[0], 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_kyber_chef(wallet,farm_id,network_id,vaults):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        pool_length_calls = []
        for contract in vaults:        
            pool_length_calls.append(Call(contract, [f'poolLength()(uint256)'], [[f'{contract}_length', None]]))
            pool_length_calls.append(Call(contract, [f'getRewardTokens()(address[])'], [[f'{contract}_rewards', None]]))

        pool_lengths=await Multicall(pool_length_calls, network)()

        for contract in vaults:
            pool_length = pool_lengths.get(f'{contract}_length')
            for pid in range(0,pool_length):
                calls.append(Call(contract, [f'getUserInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}_{contract}_staked', None]]))
                calls.append(Call(contract, [f'pendingRewards(uint256,address)(uint256[])', pid, wallet], [[f'{pid}_{contract}_pending', None]]))
                calls.append(Call(contract, [f'getPoolInfo(uint256)((uint256,address))', pid], [[f'{pid}_{contract}_want', parsers.parse_wanted_offset, 1]]))

        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }
        reward_token_list = [list(pool_lengths[x]) for x in pool_lengths if 'rewards' in x]
        token_decimals = await template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'want' in x] + [a for tup in reward_token_list for a in tup],network_id)

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    position_id = breakdown[0]+breakdown[1]
                    master_contract = breakdown[1]
                    want_token = stakes[f'{breakdown[0]}_{breakdown[1]}_want']
                    reward_tokens = pool_lengths[f'{master_contract}_rewards']
                    try:
                        token_decimal = token_decimals.get(want_token) if token_decimals.get(want_token) else 18
                    except:
                        token_decimal = 18
                    staked = parsers.from_custom(stakes[each], token_decimal)


                    poolNest[poolKey]['userData'][position_id] = {'want': want_token, 'staked' : staked, 'contractAddress' : master_contract, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, position_id)] = want_token

                    for i,token in enumerate(reward_tokens):
                        reward_token_0 = {
                            'pending': parsers.from_custom(stakes[f'{breakdown[0]}_{breakdown[1]}_pending'][i], 18),
                            'symbol' : token_decimals.get(f'{token}_symbol'),
                            'token' : token
                            }
                        poolNest[poolKey]['userData'][position_id]['gambitRewards'].append(reward_token_0)
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def get_simple_balanceof(wallet, vaults, farm_id, network, want_function=None, single_bypass=None, use_vault=False):
    network_conn = WEB3_NETWORKS[network]

    poolKey = farm_id
    calls = []

    
    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        if want_function:
            calls.append(Call(vault, [f'{want_function}()(address)'], [[f'{vault}_want', None]]))

    stakes=await Multicall(calls, network_conn, _strict=False)()

    if single_bypass:
        stakes = {**stakes, **{f'{x}_want' : single_bypass for x in vaults}}

    if use_vault:
        stakes = {**stakes, **{f'{x}_want' : x for x in vaults}}

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = await template_helpers.get_token_list_decimals(stakes,network,True)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                
                want_token = stakes[f'{breakdown[0]}_want']
                staked = parsers.from_custom(stakes[each], token_decimals.get(want_token))

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending': 0, 'contractAddress' : breakdown[0] }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_multi_masterchef(wallet,farm_id,network_id,farm_data,vaults,length_override=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        if 'poolFunction' not in farm_data:
            pool_function = 'poolLength'
        else:
            pool_function = farm_data['poolFunction']

        if length_override:
            pool_length = length_override
        else:
            pool_length = await Call(farm_data['masterChef'], [f'{pool_function}()(uint256)'],None,network)()
        
        reward_length = await Call(farm_data['masterChef'], [f'rewardPoolLength()(uint256)'],None,network)()
        staked_function = farm_data['stakedFunction']
        pending_function = farm_data['pendingFunction']

        if 'wantFunction' not in farm_data:
            want_function = 'poolInfo'
        else:
            want_function = farm_data['wantFunction']

        for pid in range(0,pool_length):
            calls.append(Call(farm_data['masterChef'], [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}{farm_data["masterChef"]}ext_staked', None]]))
            calls.append(Call(farm_data['masterChef'], [f'{want_function}(uint256)(address)', pid], [[f'{pid}{farm_data["masterChef"]}ext_want', None]]))
            for r in range(0, reward_length):
                calls.append(Call(farm_data['masterChef'], [f'{pending_function}(uint256,uint256,address)(uint256)', pid, r, wallet], [[f'{pid}{farm_data["masterChef"]}ext_pending{r}', None]]))
                calls.append(Call(farm_data['masterChef'], [f'rewardPoolInfo(uint256)(address)', r], [[f'{pid}{farm_data["masterChef"]}ext_reward{r}', None]]))


        stakes=await Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }


        token_list = set([stakes[x] for x in stakes if 'want' in x or 'reward' in x])

        token_decimals = await template_helpers.get_token_list_decimals_symbols(list(token_list),network_id)

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    want_token = stakes[f'{breakdown[0]}_want']
                    try:
                        token_decimal = token_decimals.get(want_token) if token_decimals.get(want_token) else 18
                    except:
                        token_decimal = 18
                    staked = parsers.from_custom(stakes[each], token_decimal)
                    

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : farm_data["masterChef"], 'gambitRewards' : []}

                    for rewards in range(0,reward_length):
                        if stakes[f'{breakdown[0]}_pending{rewards}']:
                            reward_token = stakes[f'{breakdown[0]}_reward{rewards}']

                            reward_token_0 = {
                                'pending': parsers.from_custom(stakes[f'{breakdown[0]}_pending{rewards}'], token_decimals.get(f'{reward_token}_decimals')),
                                'symbol' : token_decimals.get(f'{reward_token}_symbol'),
                                'token' : reward_token
                                }
                            
                            poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token



        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

async def kandyland_staking(wallet, vaults, farm_id, network_id, contract):

    poolKey = farm_id
    calls = []

    network=WEB3_NETWORKS[network_id]


    calls.append(Call(contract, [f'lockedBalances(address)(uint256)', wallet], [[f'locked_staked', None]]))
    calls.append(Call(contract, [f'withdrawableBalance(address)((uint256,uint256))', wallet], [[f'unlocked_staked', None]]))
    calls.append(Call(contract, [f'claimableRewards(address)((address,uint256)[])', wallet], [[f'pending', None]]))
    calls.append(Call(contract, [f'stakingToken()(address)'], [[f'want', None]]))

    

    stakes=await Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    reward_tokens = []
    reward_totals = []

    i = 0

    for x in stakes['pending']:

        reward_tokens.append(x[0])
        reward_totals.append(x[1])
        
    total_staked = stakes['locked_staked'] + stakes['unlocked_staked'][0] + stakes['unlocked_staked'][1]

    token_decimals = await template_helpers.get_token_list_decimals_symbols(reward_tokens + [stakes['want']],network_id)

    if total_staked > 0:
        token_decimal = 18 if stakes['want'] not in token_decimals else token_decimals[stakes['want']]
        staked = total_staked
        want_token = stakes['want']
        real_staked = parsers.from_custom(staked, token_decimal)

        poolNest[poolKey]['userData']['totalstaked'] = {'want': want_token, 'staked' : real_staked, 'contractAddress' : contract, 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, 'totalstaked')] = want_token

        for i, token in enumerate(reward_tokens):
            reward_token = token

            reward_token_0 = {
                'pending': parsers.from_custom(reward_totals[i], token_decimals.get(f'{reward_token}_decimals')),
                'symbol' : token_decimals.get(f'{reward_token}_symbol'),
                'token' : reward_token
                }
            
            poolNest[poolKey]['userData']['totalstaked']['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_mai_lending(wallet,vaults,farm_id,network):

    lending_vaults = vaults
    poolKey = farm_id
    calls = []

    token_balances = Multicall([Call(x, ['balanceOf(address)(uint256)', wallet], None) for x in vaults], WEB3_NETWORKS[network], _list=True)()

    for vault in lending_vaults:
        vault_address = vault['address']
        calls.append(Call(vault_address, [f'getAccountSnapshot(address)((uint256,uint256,uint256,uint256))', wallet], [[f'{vault_address}_accountSnapshot', None ]]))
        
    stakes=await Multicall(calls, WEB3_NETWORKS[network], _strict=False)()

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
                collat = parsers.from_custom(snapshot[1], underlying_decimal)
                collat_rate = hash_map[addPool[0]]['collat_rate']
                borrow = parsers.from_custom(snapshot[2], underlying_decimal)
                rate = parsers.from_wei(snapshot[3])
                poolNest[poolKey]['userData'][addPool[0]] = {'staked' : collat * rate, 'want': underlying, 'borrowed' : borrow, 'rate' : collat_rate, 'contractAddress' : addPool[0]}
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = underlying


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

async def get_aalto_bank(wallet, vaults, farm_id, network_id, base_contract, want, decimal):

    poolKey = farm_id

    network=WEB3_NETWORKS[network_id]

    total_bank = await Call(want, ['lockedBalanceOf(address)(uint256)', wallet], None,network)()
    user_rewards = await Call(base_contract, ['getUserPendingRewards(address)((address,uint256)[])', wallet], None,network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = await template_helpers.get_token_list_decimals_symbols([x[0] for x in user_rewards if x != '0x0000000000000000000000000000000000000000'],network_id)


    if total_bank > 0:
        want_token = want
        real_staked = parsers.from_custom(total_bank, decimal)

        poolNest[poolKey]['userData'][base_contract] = {'want': want_token, 'staked' : real_staked, 'contractAddress' : base_contract, 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, base_contract)] = want_token

        for r in user_rewards:

            if r[1] > 0:
                reward_token = r[0]

                reward_token_0 = {
                    'pending': parsers.from_custom(r[1], token_decimals.get(f'{reward_token}_decimals')),
                    'symbol' : token_decimals.get(f'{reward_token}_symbol'),
                    'token' : reward_token
                    }
                
                poolNest[poolKey]['userData'][base_contract]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None