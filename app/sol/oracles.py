from .utils import make_get_json

async def get_sonar_pricing(session):
    token_info = await make_get_json(session, 'https://sonar-backend-production-2.herokuapp.com/latest_data')

    return {token_info['prices'][t]['address'] : token_info['prices'][t]['value'] for t in token_info['prices']}