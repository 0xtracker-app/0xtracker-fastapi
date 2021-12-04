from .utils import make_get_json, decode_byte_string
from . helpers import from_custom
from . import stake_layout

async def get_raydium_tokens(session):
    r = await make_get_json(session, f'https://api.raydium.io/cache/solana-token-list')

    return { x['address'] : x for x in r['tokens'] }

async def get_raydium_pairs(session):
    r = await make_get_json(session, f'https://api.raydium.io/pairs')

    return { x['lp_mint'] : {**x, **{'coin_mint_address' : x['pair_id'].split('-')[0], 'pc_mint_address' : x['pair_id'].split('-')[1]}} for x in r }

async def get_solana_tokenlist(session):
    r = await make_get_json(session, f'https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json')

    return { x['address'] : x for x in r['tokens'] }

async def ts_reserves(token, client):
    if 'lp_data' in token:
        if 'ammOpenOrders' in token['lp_data']:
            lp_data = token['lp_data']
            amm_address = lp_data['ammOpenOrders']
            coin_account = lp_data['poolCoinTokenAccount']
            pc_account = lp_data['poolPcTokenAccount']
            lp_account = lp_data['lpMintAddress']

            coin_amount_data = await client.get_token_account_balance(coin_account)
            pc_amount_data = await client.get_token_account_balance(pc_account)
            lp_supply_data = await client.get_token_supply(lp_account)
            open_order_data = await client.get_account_info(amm_address)

            coin_amount = int(coin_amount_data['result']['value']['amount'])
            pc_amount = int(pc_amount_data['result']['value']['amount'])
            lp_supply = int(lp_supply_data['result']['value']['amount'])
            
            open_order_data_decode = stake_layout.OPEN_ORDERS_LAYOUT.parse(decode_byte_string(open_order_data['result']['value']['data'][0]))
            open_order_coin = open_order_data_decode.base_token_total
            open_order_pc = open_order_data_decode.quote_token_total       

            total_coin = coin_amount + open_order_coin
            total_pc = pc_amount + open_order_pc

            token.update({'total_shares' : from_custom(lp_supply, token['token_decimal']), 'reserves' : [total_coin, total_pc]})

            return token
    else:
        return token