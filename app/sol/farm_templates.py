from . import queries
from . import slicers
from . import stake_layout
from . import utils
from . import helpers
from .token_lookup import TokenMetaData
from solana.rpc.types import TokenAccountOpts, MemcmpOpts
import asyncio

async def get_reserves_and_total_supply(lp_data, client, balance):

    user_balance = helpers.from_custom(balance, lp_data['lp']['decimals'])

    coin_account = lp_data['poolCoinTokenAccount']
    pc_account = lp_data['poolPcTokenAccount']
    lp_account = lp_data['lp']['mintAddress']

    coin_decimals = lp_data['coin']['decimals']
    pc_decimals = lp_data['pc']['decimals']

    coin_amount_data = await client.get_token_account_balance(coin_account)
    pc_amount_data = await client.get_token_account_balance(pc_account)
    lp_supply_data = await utils.getTokenSupply(lp_account)
    # open_order_data = await client.get_account_info(amm_address)

    coin_decimals = lp_data['coin']['decimals']
    pc_decimals = lp_data['pc']['decimals']

    coin_amount = coin_amount_data['result']['value']['uiAmount']
    pc_amount = pc_amount_data['result']['value']['uiAmount']
    lp_supply = lp_supply_data['result']['value']['uiAmount']
    #open_order_data_decode = stake_layout.OPEN_ORDERS_LAYOUT.parse(utils.decode_byte_string(open_order_data['result']['value']['data'][0]))
    #open_order_coin = open_order_data_decode.base_token_total / (10 ** coin_decimals)
    #open_order_pc = open_order_data_decode.quote_token_total / (10 ** pc_decimals)

    total_coin = coin_amount
    total_pc = pc_amount

    user_pct = user_balance / lp_supply
    coin_value = user_pct * total_coin
    pc_value = user_pct * total_pc

    return {'lpTotal' : [coin_value,pc_value]}

async def get_farming_from_program(farm_id, wallet, program, offset, client, vaults, session, mongodb):
    solana = wallet
    poolKey = farm_id

    staking_program = await client.get_program_accounts(program, encoding='base64', memcmp_opts=slicers.memcmp_owner(solana.public_key, offset))
    user_stakes = []
    pool_infos = []
    lp_infos = []
    reward_infos = []

    for each in staking_program['result']:

        account_data = stake_layout.USER_STAKE_INFO_ACCOUNT_LAYOUT.parse(utils.decode_byte_string(each['account']['data'][0]))
        pool_id = utils.convert_public_key(account_data.poolId)
        user_stakes.append({'poolID': pool_id, 'depositBalance': account_data.depositBalance, 'rewardDebt': account_data.rewardDebt, 'rewards' : []})
        pool_infos.append(client.get_account_info(pool_id))

    pool_data = await asyncio.gather(*pool_infos)

    for each in pool_data:
        stake_info = stake_layout.STAKE_INFO_LAYOUT.parse(utils.decode_byte_string(each['result']['value']['data'][0]))
        lp_infos.append(TokenMetaData(address=utils.convert_public_key(stake_info.poolLpTokenAccount), mongodb=mongodb, network='solana', session=session, client=client))
        reward_infos.append(TokenMetaData(address=utils.convert_public_key(stake_info.poolRewardTokenAccount), mongodb=mongodb, network='solana', session=session, client=client))

    all_token_metadata = await asyncio.gather(*[x.account_to_mint() for x in lp_infos])
    reward_data = await asyncio.gather(*[x.account_to_mint() for x in reward_infos])
    update_reserves = await asyncio.gather(*[queries.ts_reserves(x, client) for x in all_token_metadata])

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for idx, each in enumerate(pool_data):
        stake_info = stake_layout.STAKE_INFO_LAYOUT.parse(utils.decode_byte_string(each['result']['value']['data'][0]))

        if user_stakes[idx]['depositBalance'] > 0:
            staked = helpers.from_custom(user_stakes[idx]['depositBalance'], update_reserves[idx]['token_decimal'])
            want_token = update_reserves[idx]['tokenID']

            poolNest[poolKey]['userData'][user_stakes[idx]['poolID']] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
            poolNest[poolKey]['userData'][user_stakes[idx]['poolID']].update(update_reserves[idx])
            poolIDs['%s_%s_want' % (poolKey, user_stakes[idx]['poolID'])] = want_token
            
            pending_rewards = user_stakes[idx]['depositBalance'] * stake_info.rewardPerShareNet / 1e9 - user_stakes[idx]['rewardDebt']
            reward_token_0 = {'pending': helpers.from_custom(pending_rewards, reward_data[idx]['token_decimal']), 'symbol' : reward_data[idx]['tkn0s'], 'token' : reward_data[idx]['tokenID']}
            poolNest[poolKey]['userData'][user_stakes[idx]['poolID']]['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

async def get_farming_from_program_dual(farm_id, wallet, program, offset, client, vaults, session, mongodb, reward_dec):
    solana = wallet
    poolKey = farm_id

    staking_program = await client.get_program_accounts(program, encoding='base64', memcmp_opts=slicers.memcmp_owner(solana.public_key, offset))
    user_stakes = []
    pool_infos = []
    lp_infos = []
    reward_infos = []
    reward_infosB = []

    for each in staking_program['result']:

        account_data = stake_layout.USER_STAKE_INFO_ACCOUNT_LAYOUT_V4.parse(utils.decode_byte_string(each['account']['data'][0]))
        pool_id = utils.convert_public_key(account_data.poolId)
        user_stakes.append({'poolID': pool_id, 'depositBalance': account_data.depositBalance, 'rewardDebt': account_data.rewardDebt, 'rewardDebtB' : account_data.rewardDebtB})
        pool_infos.append(client.get_account_info(pool_id))

    pool_data = await asyncio.gather(*pool_infos)

    for each in pool_data:
        stake_info = stake_layout.STAKE_INFO_LAYOUT_V4.parse(utils.decode_byte_string(each['result']['value']['data'][0]))
        lp_infos.append(TokenMetaData(address=utils.convert_public_key(stake_info.poolLpTokenAccount), mongodb=mongodb, network='solana', session=session, client=client))
        reward_infos.append(TokenMetaData(address=utils.convert_public_key(stake_info.poolRewardTokenAccount), mongodb=mongodb, network='solana', session=session, client=client))
        reward_infosB.append(TokenMetaData(address=utils.convert_public_key(stake_info.poolRewardTokenAccountB), mongodb=mongodb, network='solana', session=session, client=client))

    all_token_metadata = await asyncio.gather(*[x.account_to_mint() for x in lp_infos])
    reward_data = await asyncio.gather(*[x.account_to_mint() for x in reward_infos])
    reward_dataB = await asyncio.gather(*[x.account_to_mint() for x in reward_infosB])
    update_reserves = await asyncio.gather(*[queries.ts_reserves(x, client) for x in all_token_metadata])

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for idx, each in enumerate(pool_data):
        stake_info = stake_layout.STAKE_INFO_LAYOUT_V4.parse(utils.decode_byte_string(each['result']['value']['data'][0]))

        if user_stakes[idx]['depositBalance'] > 0:
            staked = helpers.from_custom(user_stakes[idx]['depositBalance'], update_reserves[idx]['token_decimal'])
            want_token = update_reserves[idx]['tokenID']

            poolNest[poolKey]['userData'][user_stakes[idx]['poolID']] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
            poolNest[poolKey]['userData'][user_stakes[idx]['poolID']].update(update_reserves[idx])
            poolIDs['%s_%s_want' % (poolKey, user_stakes[idx]['poolID'])] = want_token
            
            pending_rewards = user_stakes[idx]['depositBalance'] * stake_info.perShare / reward_dec - user_stakes[idx]['rewardDebt']
            reward_token_0 = {'pending': helpers.from_custom(pending_rewards, reward_data[idx]['token_decimal']), 'symbol' : reward_data[idx]['tkn0s'], 'token' : reward_data[idx]['tokenID']}
            poolNest[poolKey]['userData'][user_stakes[idx]['poolID']]['gambitRewards'].append(reward_token_0)

            pending_rewards = user_stakes[idx]['depositBalance'] * stake_info.perShareB / reward_dec - user_stakes[idx]['rewardDebtB']
            reward_token_0 = {'pending': helpers.from_custom(pending_rewards, reward_dataB[idx]['token_decimal']), 'symbol' : reward_dataB[idx]['tkn0s'], 'token' : reward_dataB[idx]['tokenID']}
            poolNest[poolKey]['userData'][user_stakes[idx]['poolID']]['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None