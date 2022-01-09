import asyncio
from .token_lookup import TokenMetaData
from .helpers import from_custom
from .router_override import router_override
from . import token_routes

class TokenOverride:

    def __init__(self, session=None):
        self.tokens = {
            'terra1zsaswh926ey8qa5x4vj93kzzlfnef0pstuca0y' : [get_price_from_terraswap, {'query' : token_routes.bPsiDP24m(), 'amount' : '1000000', 'decimal' : 6, 'router' : 'terra19qx5xe6q9ll4w0890ux7lv2p4mf3csd4qvt3ex', 'client' : session}],
}

async def get_price_from_pool(token_in, decimal, client, mongo_db, token_override, luna_price=None):
    
    otkn = token_override
    if token_in in otkn:
        return await otkn[token_in][0](**otkn[token_in][1])


    if not luna_price:
        get_luna =  await client.wasm.contract_query('terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6', {"simulation":{"offer_asset":{"amount":"1000000","info":{"native_token":{"denom":"uluna"}}}}})
        luna_price = from_custom(int(get_luna['return_amount']), 6)

    if token_in in router_override:
        decimal = router_override[token_in]['decimal']
        token_in = router_override[token_in]['token']

    find_pool = await TokenMetaData(mongodb=mongo_db, client=client).find_pool(token_in)

    if token_in == 'uusd':
        return 1
    elif find_pool:
        token_amount = 1 * 10 ** decimal
        token_query = {"native_token":{"denom": token_in}} if len(token_in) < 6 else {"token":{"contract_addr": token_in}}
        price_quote =  await client.wasm.contract_query(find_pool['pool'], {"simulation":{"offer_asset":{"amount": str(token_amount), "info": token_query}}})
        return from_custom(int(price_quote['return_amount']), 6) if find_pool['pair'] != 'uluna' else from_custom(int(price_quote['return_amount']), 6) * luna_price
    else:
        return 0
    
async def get_price_from_terraswap(query, amount, decimal, router, client):

    get_luna =  await client.wasm.contract_query(
        router, 
        {
            "simulate_swap_operations":{
                "offer_amount": amount,
                "operations": query
            }
        }
    )

    return from_custom(int(get_luna['amount']), decimal)

