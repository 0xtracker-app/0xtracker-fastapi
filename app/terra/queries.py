from .utils import make_get_json
from .helpers import from_custom

async def find_native_denom(token, session):
    r = await make_get_json(session, f'https://lcd.terra.dev/cosmos/bank/v1beta1/denoms_metadata/{token}')
    if 'metadata' in r:
        return r['metadata']
    else:
        return None

async def get_cw_tokens(session):
    r = await make_get_json(session, 'https://api.terraswap.io/tokens')
    return_list = []

    for each in r:
        if len(each['contract_addr']) > 5 and 'ibc' not in each['contract_addr']:
            return_list.append(each)

    return return_list