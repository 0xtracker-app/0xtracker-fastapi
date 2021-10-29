from .utils import make_get_json
from .helpers import from_custom

async def find_native_denom(token, session):
    r = await make_get_json(session, f'https://lcd.terra.dev/cosmos/bank/v1beta1/denoms_metadata/{token}')
    if 'metadata' in r:
        return r['metadata']
    else:
        return None