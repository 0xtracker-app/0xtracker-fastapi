from .utils import make_get_json

async def get_raydium_tokens(session):
    r = await make_get_json(session, f'https://api.raydium.io/token')

    return { x['mint_address'] : x for x in r }