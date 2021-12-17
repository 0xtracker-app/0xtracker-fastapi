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

async def get_coinhall_pairs(session):
    r = await make_get_json(session, 'https://api.coinhall.org/api/v1/charts/terra/pairs')
    
    return [x for x in r]

async def get_luna_price(client):
    get_luna =  await client.wasm.contract_query('terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6', {"simulation":{"offer_asset":{"amount":"1000000","info":{"native_token":{"denom":"uluna"}}}}})
    luna_price = from_custom(int(get_luna['return_amount']), 6)
    return luna_price


async def get_network_staking(wallet, session):
    endpoint = 'https://lcd.terra.dev'
    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegations/{wallet}')
    return r

async def get_network_staking_unbonded(wallet, session):
    endpoint = 'https://lcd.terra.dev'
    r = await make_get_json(session, f'{endpoint}/cosmos/staking/v1beta1/delegators/{wallet}/unbonding_delegations')

    return r

async def get_network_staking_rewards(wallet, session):
    endpoint = 'https://lcd.terra.dev'
    r = await make_get_json(session, f'{endpoint}/cosmos/distribution/v1beta1/delegators/{wallet}/rewards')

    return r