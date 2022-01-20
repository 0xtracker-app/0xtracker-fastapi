from .queries import make_get_json, make_get
import json

async def dummy_vault(session):
    return ['0xDummy']

async def junoswap_vaults(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/CosmosContracts/junoswap-asset-list/main/token_list.json')
    r = json.loads(r)
    return [x['swap_address'] for x in r['tokens'] if x['swap_address'] != ""]