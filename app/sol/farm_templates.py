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

    #Get Staking Positions filtered by Wallet Address
    staking_program = await client.get_program_accounts(program, encoding='base64', memcmp_opts=slicers.memcmp_owner(solana.public_key, offset))
    user_stakes = []
    pool_infos = []
    lp_infos = []
    #Loop over each position
    for each in staking_program['result']:

        account_data = stake_layout.USER_STAKE_INFO_ACCOUNT_LAYOUT.parse(utils.decode_byte_string(each['account']['data'][0]))
        pool_id = utils.convert_public_key(account_data.poolId)
        user_stakes.append({'poolID': pool_id, 'depositBalance': account_data.depositBalance, 'rewardDebt': account_data.rewardDebt, 'rewards' : []})
        pool_infos.append(client.get_account_info(pool_id))

    pool_data = await asyncio.gather(*pool_infos)

    for each in pool_data:
        stake_info = stake_layout.STAKE_INFO_LAYOUT.parse(utils.decode_byte_string(each['result']['value']['data'][0]))
        print(utils.convert_public_key(stake_info.poolLpTokenAccount))
        lp_infos.append(client.get_account_info(utils.convert_public_key(stake_info.poolLpTokenAccount), encoding="jsonParsed"))

    lp_data = await asyncio.gather(*lp_infos)
    print(lp_data)
    tokens_metadata = []
    for each in lp_data:
        print(each['result']['value']['data']['parsed']['info']['mint'])
        tokens_metadata.append(TokenMetaData(address=each['result']['value']['data']['parsed']['info']['mint'], mongodb=mongodb, network='solana', session=session).lookup)

    all_token_metadata = await asyncio.gather(*[x() for x in tokens_metadata])

    coin_amount_data = await client.get_token_account_balance('4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R')
    pc_amount_data = await client.get_token_account_balance('SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt')
    lp_supply_data = await client.get_token_supply('7P5Thr9Egi2rvMmEuQkLn8x8e8Qro7u2U7yLD2tU2Hbe')

    x = await client.get_program_accounts('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8', encoding='base64')

    for each in x['result']:
        print(each)

    #If LP then get reserves/total supply
    # if len(lp_info) > 0:
    #     lp_balances = await get_reserves_and_total_supply(lp_info[0], client, account_data.depositBalance)
    #     user_stakes[pool_id].update(lp_balances)


        # user_stakes[pool_id].update({'poolInfo': {'poolLpTokenAccount': utils.convert_public_key(stake_info.poolLpTokenAccount), 'poolRewardTokenAccount': utils.convert_public_key(
        #     stake_info.poolRewardTokenAccount), 'totalReward': stake_info.totalReward, 'rewardPerShareNet': stake_info.rewardPerShareNet}})



        # user_stakes[pool_id]['rewards'].append({'balance' : helpers.get_pending_rewards(account_data.depositBalance, stake_info.rewardPerShareNet, 1e9, account_data.rewardDebt, 6)})