async def dummy_vault(session):
    return ['0xDummy']

async def make_get_json(session, url, kwargs={}):
    async with session.get(url, **kwargs) as response:
        try:
            result = await response.json()
            return result
        except:
            None

async def spectrum_farm_contract(session):
    r = await make_get_json(session,'https://api.spec.finance/api/data?type=lpVault')

    farming_contracts = []

    if 'poolInfos' in r:
        for x in r['poolInfos']:
            if r['poolInfos'][x]['farmContract'] not in farming_contracts:
                farming_contracts.append(r['poolInfos'][x]['farmContract'])
                
    return farming_contracts

async def spectrum_staking_contract(session):
    return ['terra1dpe4fmcz2jqk6t50plw0gqa2q3he2tj6wex5cl']

async def loopr_staking_contract(session):
    return ['terra1nd3x2cqaqffp9xfa8epp5lw4cyc48rr4qz4v9d', 'terra1gaawzzmma5s465w4suzlmmpspef89tp4dysl2f', 'terra1th3s05dh6qjk5nngthxsl4d8sv7k05svpjlr87']