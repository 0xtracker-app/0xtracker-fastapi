import aiohttp
import json

async def make_get(session, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
            response.raise_for_status()
    
    return result

async def make_get_json(session, url, kwargs={}):
    async with session.get(url, **kwargs) as response:
        try:
            result = await response.json()
            return result
        except:
            None
    
    