import aiohttp
import json

async def make_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
            response.raise_for_status()
    
    return result

async def make_get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
            response.raise_for_status()
    
    return json.loads(result)