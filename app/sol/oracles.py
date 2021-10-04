from .utils import make_get_json

async def get_sonar_pricing(session):
    token_info = await make_get_json(session, 'https://price-api.sonar.watch/prices')

    return {t['mint'] : t['price'] for t in token_info}