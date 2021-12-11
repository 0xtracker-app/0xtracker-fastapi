import asyncio
from .token_lookup import TokenMetaData
from .helpers import from_custom

async def get_price_from_pool(token_in, decimal, client, mongo_db, luna_price=None):

    if not luna_price:
        get_luna =  await client.wasm.contract_query('terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6', {"simulation":{"offer_asset":{"amount":"1000000","info":{"native_token":{"denom":"uluna"}}}}})
        luna_price = from_custom(int(get_luna['return_amount']), 6)

    find_pool = await TokenMetaData(mongodb=mongo_db, client=client).find_pool(token_in)

    if token_in == 'uusd':
        return 1
    elif find_pool:
        token_amount = 1 * 10 ** decimal
        token_query = {"native_token":{"denom": token_in}} if len(token_in) < 6 else {"token":{"contract_addr": token_in}}
        price_quote =  await client.wasm.contract_query(find_pool['pool'], {"simulation":{"offer_asset":{"amount": str(token_amount), "info": token_query}}})
        return from_custom(int(price_quote['return_amount']), decimal) if find_pool['pair'] != 'uluna' else from_custom(int(price_quote['return_amount']), decimal) * luna_price
    else:
        return 0