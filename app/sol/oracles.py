from .utils import make_get_json

async def get_sonar_pricing(session):
    token_info = await make_get_json(session, 'https://api.sonar.watch/latest')

    return {token_info['prices'][t]['address'] : token_info['prices'][t]['value'] for t in token_info['prices']}