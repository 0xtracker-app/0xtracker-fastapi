from . import queries
from . import slicers
from . import stake_layout
from . import utils
from . import helpers
from .token_lookup import TokenMetaData
from solana.rpc.types import TokenAccountOpts, MemcmpOpts
from solana.publickey import PublicKey
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

async def get_solend_positions(farm_id, wallet, program, offset, client, vaults, session, mongodb):
    solana = wallet
    poolKey = farm_id
    from_seed = PublicKey.create_with_seed(solana.public_key,'4UpD2fh7xH3VP9QQaXtsS1YY3bxzWhtfpks7FatyKvdY'[0:32], PublicKey(program))

    lm_info = await client.get_account_info(from_seed)
    lm_check = stake_layout.SOLEND_OBLIGATION.parse(utils.decode_byte_string(lm_info['result']['value']['data'][0]))

    deposits_reserves = await asyncio.gather(*[client.get_account_info(PublicKey(d['depositReserveKey'])) for d in lm_check.deposits])
    deposits_reserves_parsed = [stake_layout.RESERVE_SCHEMA.parse(utils.decode_byte_string(r['result']['value']['data'][0])) for r in deposits_reserves]

    borrows_reserves = await asyncio.gather(*[client.get_account_info(PublicKey(b['borrowReserveKey'])) for b in lm_check.borrows])
    borrows_reserves_parsed = [stake_layout.RESERVE_SCHEMA.parse(utils.decode_byte_string(r['result']['value']['data'][0])) for r in borrows_reserves]

    # token_accounts = [t.liquidityMintPubkeyKey for t in deposits_reserves_parsed] + [t.liquidityMintPubkeyKey for t in borrows_reserves_parsed]
    # token_metadata = await asyncio.gather(*[TokenMetaData(address=mint, mongodb=mongodb, network='solana', session=session, client=client).lookup() for mint in token_accounts])

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for i, d in enumerate(lm_check['deposits']): 

        want_token = deposits_reserves_parsed[i].liquidityMintPubkeyKey
        exchange_rate = helpers.solend_collateral_exchange_rate(deposits_reserves_parsed[i])
        token_metadata = await TokenMetaData(address=want_token, mongodb=mongodb, network='solana', session=session, client=client).lookup()
        loan_to_value = deposits_reserves_parsed[i].loanToValueRatio / 100
        deposited_amount = helpers.from_custom(d.depositedAmount, token_metadata['token_decimal']) * exchange_rate

        poolNest[poolKey]['userData'][want_token] = {'staked' : deposited_amount, 'want': want_token, 'borrowed' : 0, 'rate' : loan_to_value, 'gambitRewards' : [{'pending': 0, 'symbol' : 'SLND', 'token' : 'SLNDpmoWTVADgEdndyvWzroNL7zSi1dF9PC3xHGtPwp'}]}
        poolNest[poolKey]['userData'][want_token].update(token_metadata)
        poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

    for i, d in enumerate(lm_check['borrows']): 

        want_token = borrows_reserves_parsed[i].liquidityMintPubkeyKey
        exchange_rate = helpers.solend_collateral_exchange_rate(borrows_reserves_parsed[i])
        token_metadata = await TokenMetaData(address=want_token, mongodb=mongodb, network='solana', session=session, client=client).lookup()
        loan_to_value = borrows_reserves_parsed[i].loanToValueRatio / 100
        raw_borrow = d.borrowAmountWads * borrows_reserves_parsed[i].cumulativeBorrowRateWads / d.cumulativeBorrowRateWads / 1000000000000000000
        borrowed_amount = helpers.from_custom(raw_borrow, token_metadata['token_decimal'])

        poolNest[poolKey]['userData'][want_token] = {'staked' : 0, 'want': want_token, 'borrowed' : borrowed_amount, 'rate' : loan_to_value, 'gambitRewards' : [{'pending': 0, 'symbol' : 'SLND', 'token' : 'SLNDpmoWTVADgEdndyvWzroNL7zSi1dF9PC3xHGtPwp'}]}
        poolNest[poolKey]['userData'][want_token].update(token_metadata)
        poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token


    # user_stakes = []
    # pool_infos = []
    # lp_infos = []
    # reward_infos = []

    # for each in staking_program['result']:

    #     account_data = stake_layout.USER_STAKE_INFO_ACCOUNT_LAYOUT.parse(utils.decode_byte_string(each['account']['data'][0]))
    #     pool_id = utils.convert_public_key(account_data.poolId)
    #     user_stakes.append({'poolID': pool_id, 'depositBalance': account_data.depositBalance, 'rewardDebt': account_data.rewardDebt, 'rewards' : []})
    #     pool_infos.append(client.get_account_info(pool_id))

    # pool_data = await asyncio.gather(*pool_infos)

    # for each in pool_data:
    #     stake_info = stake_layout.STAKE_INFO_LAYOUT.parse(utils.decode_byte_string(each['result']['value']['data'][0]))
    #     lp_infos.append(TokenMetaData(address=utils.convert_public_key(stake_info.poolLpTokenAccount), mongodb=mongodb, network='solana', session=session, client=client))
    #     reward_infos.append(TokenMetaData(address=utils.convert_public_key(stake_info.poolRewardTokenAccount), mongodb=mongodb, network='solana', session=session, client=client))

    # all_token_metadata = await asyncio.gather(*[x.account_to_mint() for x in lp_infos])
    # reward_data = await asyncio.gather(*[x.account_to_mint() for x in reward_infos])
    # update_reserves = await asyncio.gather(*[queries.ts_reserves(x, client) for x in all_token_metadata])

    # poolNest = {poolKey: 
    # { 'userData': { } } }

    # poolIDs = {}

    # for idx, each in enumerate(pool_data):
    #     stake_info = stake_layout.STAKE_INFO_LAYOUT.parse(utils.decode_byte_string(each['result']['value']['data'][0]))

    #     if user_stakes[idx]['depositBalance'] > 0:
    #         staked = helpers.from_custom(user_stakes[idx]['depositBalance'], update_reserves[idx]['token_decimal'])
    #         want_token = update_reserves[idx]['tokenID']

    #         poolNest[poolKey]['userData'][user_stakes[idx]['poolID']] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
    #         poolNest[poolKey]['userData'][user_stakes[idx]['poolID']].update(update_reserves[idx])
    #         poolIDs['%s_%s_want' % (poolKey, user_stakes[idx]['poolID'])] = want_token
            
    #         pending_rewards = user_stakes[idx]['depositBalance'] * stake_info.rewardPerShareNet / 1e9 - user_stakes[idx]['rewardDebt']
    #         reward_token_0 = {'pending': helpers.from_custom(pending_rewards, reward_data[idx]['token_decimal']), 'symbol' : reward_data[idx]['tkn0s'], 'token' : reward_data[idx]['tokenID']}
    #         poolNest[poolKey]['userData'][user_stakes[idx]['poolID']]['gambitRewards'].append(reward_token_0)
            

    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None