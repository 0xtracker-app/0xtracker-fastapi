import asyncio
from aiohttp import helpers
from solana._layouts.shared import PUBLIC_KEY_LAYOUT
from solana.rpc.types import TokenAccountOpts, MemcmpOpts
from solana.publickey import PublicKey
import spl.token._layouts as layouts
from . import stake_layout
from . import utils
from . import slicers
from .helpers import from_custom, get_pending_rewards, saber_farmer_wrapper
from .constants import PROGRAMS

RPC_CONNECTION = 'https://api.mainnet-beta.solana.com'

async def local_balances(wallet, mongodb, session, client):
    public_key = PublicKey(wallet)

    parsed_account_data = []
    token_metadata = x = await utils.get_token_metadata()
    balance = await client.get_token_accounts_by_owner(public_key, TokenAccountOpts(program_id='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'))
    for each in balance['result']['value']:
        account_data = layouts.ACCOUNT_LAYOUT.parse(utils.decode_byte_string(each['account']['data'][0]))
        mint_address = utils.convert_public_key(account_data.mint)
        meta_data = token_metadata[mint_address] if mint_address in token_metadata else None
        if account_data.amount > 0 :
            parsed_account_data.append({
                'token_address' : utils.convert_public_key(account_data.mint),
                'tokenBalance' : account_data.amount,
                'tokenPrice' : ''
            })

    return parsed_account_data

async def get_reserves_and_total_supply(lp_data, client, balance):

    user_balance = from_custom(balance, lp_data['lp']['decimals'])
    amm_address = lp_data['ammOpenOrders']
    coin_account = lp_data['poolCoinTokenAccount']
    pc_account = lp_data['poolPcTokenAccount']
    lp_account = lp_data['lp']['mintAddress']
    coin_decimals = lp_data['coin']['decimals']
    pc_decimals = lp_data['pc']['decimals']

    coin_amount_data = await client.get_token_account_balance(coin_account)
    pc_amount_data = await client.get_token_account_balance(pc_account)
    lp_supply_data = await utils.getTokenSupply(lp_account)
    open_order_data = await client.get_account_info(amm_address)

    coin_decimals = lp_data['coin']['decimals']
    pc_decimals = lp_data['pc']['decimals']

    coin_amount = coin_amount_data['result']['value']['uiAmount']
    pc_amount = pc_amount_data['result']['value']['uiAmount']
    lp_supply = lp_supply_data['result']['value']['uiAmount']
    open_order_data_decode = stake_layout.OPEN_ORDERS_LAYOUT.parse(utils.decode_byte_string(open_order_data['result']['value']['data'][0]))
    open_order_coin = open_order_data_decode.base_token_total / (10 ** coin_decimals)
    open_order_pc = open_order_data_decode.quote_token_total / (10 ** pc_decimals)

    total_coin = coin_amount + open_order_coin
    total_pc = pc_amount + open_order_pc

    user_pct = user_balance / lp_supply
    coin_value = user_pct * total_coin
    pc_value = user_pct * total_pc

    return {'lpTotal' : [coin_value,pc_value]}

async def get_farming_from_program(wallet, program, offset):
    public_key = PublicKey(wallet)
    client = AsyncClient(RPC_CONNECTION)

    #Get Staking Positions filtered by Wallet Address
    staking_program = await client.get_program_accounts(program, encoding='base64', memcmp_opts=slicers.memcmp_owner(public_key, offset))
    user_stakes = {}

    #Loop over each position
    for each in staking_program['result']:

        account_data = stake_layout.USER_STAKE_INFO_ACCOUNT_LAYOUT.parse(
            utils.decode_byte_string(each['account']['data'][0]))
        pool_id = utils.convert_public_key(account_data.poolId)

        user_stakes[pool_id] = {
            'poolID': pool_id, 'depositBalance': account_data.depositBalance, 'rewardDebt': account_data.rewardDebt, 'rewards' : []}

        #Get Pool Info
        pool_info = await client.get_account_info(pool_id)

        stake_info = stake_layout.STAKE_INFO_LAYOUT.parse(
            utils.decode_byte_string(pool_info['result']['value']['data'][0]))

        #Get Token Metadata
        token_info = utils.generate_farm_dict(utils.convert_public_key(stake_info.poolLpTokenAccount))
        l_ti = len(token_info)
        if l_ti > 0:
            user_stakes[pool_id]['tokenInfo'] = token_info[0]

        #Check if is LP and return data needed to get LP Balances
        if l_ti > 0:
            lp_info = utils.generate_lp_dict(token_info[0]['lp']['mintAddress'])

        #If LP then get reserves/total supply
        if len(lp_info) > 0:
            lp_balances = await get_reserves_and_total_supply(lp_info[0], client, account_data.depositBalance)
            user_stakes[pool_id].update(lp_balances)


        user_stakes[pool_id].update({'poolInfo': {'poolLpTokenAccount': utils.convert_public_key(stake_info.poolLpTokenAccount), 'poolRewardTokenAccount': utils.convert_public_key(
            stake_info.poolRewardTokenAccount), 'totalReward': stake_info.totalReward, 'rewardPerShareNet': stake_info.rewardPerShareNet}})



        user_stakes[pool_id]['rewards'].append({'balance' : get_pending_rewards(account_data.depositBalance, stake_info.rewardPerShareNet, 1e9, account_data.rewardDebt, 6)})


    await client.close()

async def get_farming_from_vault_info(wallet, account_info, vault_accounts, program, user_parser, vault_parser):

    client = AsyncClient(RPC_CONNECTION)

    ##Generate list of user accounts
    account_infos = []
    for each in account_info:
        account_infos.append(utils.get_program_address(each,wallet,program))

    ##Get User Positions
    user_positions = await utils.getMultipleAccounts(account_infos)

    ##Get Vault Info
    vault_info = await utils.getMultipleAccounts(vault_accounts)


    user_stakes = {}

    for i,each in enumerate(user_positions['result']['value']):

        if each is not None:
            pool_id = account_infos[i]
            decode_user_balance_info = user_parser.parse(utils.decode_byte_string(each['data'][0]))
            decode_vault_account_info = vault_parser.parse(utils.decode_byte_string(vault_info['result']['value'][i]['data'][0]))

            user_vlp_shares = decode_user_balance_info.amount
            user_lp_tokens = int((user_vlp_shares * decode_vault_account_info.total_vault_balance) / decode_vault_account_info.total_vlp_shares)

            user_stakes[pool_id] = {'poolID': pool_id, 'depositBalance': user_lp_tokens, 'rewards' : []}

            lp_info = utils.generate_lp_dict(utils.convert_public_key(decode_vault_account_info.lp_token_mint))

            if len(lp_info) > 0:
                #Get reserves/total supply
                lp_balances = await get_reserves_and_total_supply(lp_info[0], client, user_lp_tokens)

                ## Set Pool in Dict
                user_stakes[pool_id].update(lp_balances)
                user_stakes[pool_id]['tokenInfo'] = lp_info
            

    await client.close()   




#asyncio.run(get_farming_from_program('8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT', PROGRAMS.SABER_PROGRAM, 8))

#asyncio.run(get_farming_from_vault_info('8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT', utils.generate_info_account_list(), utils.generate_solfarm_vaults()))


#asyncio.run(get_farming_from_vault_info('8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT', ['8MTn6axPimLvgz4VXejZE527NJCePg3SuaHFrFR9CTH4'], ['8MTn6axPimLvgz4VXejZE527NJCePg3SuaHFrFR9CTH4'], PROGRAMS.SABER_PROGRAM, stake_layout.SOLFARM_SABER_USER_BALANCE_LAYOUT, stake_layout.SOLFARM_SABER_VAULT_LAYOUT ))
#asyncio.run(local_balances('8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT'))


# async def get_ma():
#     x = await utils.getMultipleAccounts([
#   "8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT",
#   "EK8iAS8QPTo8VK62m48YtzVij48sCHWbRUTDBYJXQHwx",
#   "2m3HFTZSVJdAVj8uUTc81SynbausmoFVDk5yYNQt49yu",
#   "HKrLLaDhc9X8i1zLcLQYKXLzsEuEAHLRneLtvJDe7VvS",
#   "HuSVastp2sYxXVsrdTWwpgm5kmybSQRuE4T3Kj6kFGv6",
#   "Hx8zvsrFDRevUFbJQ34SFbRzUkSLLbvcrQdhT1758AZF",
#   "8MTn6axPimLvgz4VXejZE527NJCePg3SuaHFrFR9CTH4",
#   "7R9murcoNC4B7BCDGpZrph9vQWTr6FjiuBGE7JMkLs4p"
# ]
# )

#     for each in x['result']['value']:
#         print(each)
#         # y = stake_layout.SOLFARM_SABER_USER_BALANCE_LAYOUT.parse(utils.decode_byte_string(each['data'][0]))
#         # print(y)


# #asyncio.run(get_ma())

# # for each in utils.generate_saber_pool_info()['pools']:
# #     x = utils.get_program_address(each['plotKey'],'8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT',PROGRAMS.SABER_PROGRAM)
# #     print(x)


# # for each in utils.generate_saber_pool_info()['pools']:
# #     print(each['plotKey'])
    
# # x = utils.get_program_address('8MTn6axPimLvgz4VXejZE527NJCePg3SuaHFrFR9CTH4','8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT',PublicKey('SSwpkEEcbUqx4vtoEByFjSkhKdCT862DNVb52nZg1UZ'))
# # print(x)
# # x = utils.get_program_address('EZEBiZieuKrMGyCd72696Vm8HuiimfQGjVrejmp7Abjd','8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT',PublicKey('SSwpkEEcbUqx4vtoEByFjSkhKdCT862DNVb52nZg1UZ'))
# # print(x)
# # x = utils.get_program_address('7R9murcoNC4B7BCDGpZrph9vQWTr6FjiuBGE7JMkLs4p','8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT',PublicKey('SSwpkEEcbUqx4vtoEByFjSkhKdCT862DNVb52nZg1UZ'))
# # print(x)
# # x = utils.get_program_address('HuSVastp2sYxXVsrdTWwpgm5kmybSQRuE4T3Kj6kFGv6','8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT',PublicKey('SSwpkEEcbUqx4vtoEByFjSkhKdCT862DNVb52nZg1UZ'))
# # print(x)
# # x = utils.get_program_address('B38L5x5EszUK4iqcNMAZRyaJx8ie8cgGvxxbYmkWkjZe','8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT',PublicKey('SSwpkEEcbUqx4vtoEByFjSkhKdCT862DNVb52nZg1UZ'))
# # print(x)


# x = utils.get_anchor_account('8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT', '3LGuvwvwLJdzsVJ324u4KSEBsJjNV3Xpu7DziXmwfqqu', PROGRAMS.SABER_PROGRAM)
# conn = Client(RPC_CONNECTION)
# account = conn.get_account_info(x)
# balance = conn.get_token_accounts_by_owner('8MTn6axPimLvgz4VXejZE527NJCePg3SuaHFrFR9CTH4', TokenAccountOpts(program_id='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'))
# for each in balance['result']['value']:
#     account_data = layouts.ACCOUNT_LAYOUT.parse(utils.decode_byte_string(each['account']['data'][0]))

# account_info = saber_farmer_wrapper(stake_layout.SABER_FARMER.parse(utils.decode_byte_string(account['result']['value']['data'][0])))

# user_plots = []
# for each in utils.generate_saber_plot_keys():
#     x = utils.get_anchor_account('8eiVXn3LN5jEXimmxmvFspU654Z7PSK8q31W4Bo8STNT', each, PROGRAMS.SABER_PROGRAM)
#     y = conn.get_account_info(x)
#     if y['result']['value'] is not None:
#         account_info = saber_farmer_wrapper(stake_layout.SABER_FARMER.parse(utils.decode_byte_string(y['result']['value']['data'][0])))
#         print(account_info)

# print(user_plots)