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
    r = await make_get_json(session,'https://specapi.azurefd.net/api/data?type=lpVault')
    return [r['poolInfos'][x]['farmContract'] for x in r['poolInfos']]

async def spectrum_staking_contract(session):
    return ['terra1dpe4fmcz2jqk6t50plw0gqa2q3he2tj6wex5cl']