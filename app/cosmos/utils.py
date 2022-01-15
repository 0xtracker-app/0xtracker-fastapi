import json
import hjson
import asyncio

async def make_get(session, url, kwargs={}):
    async with session.get(url, **kwargs) as response:
            result = await response.text()
            response.raise_for_status()
    return result

async def make_get_hson(session, url, kwargs={}):
    async with session.get(url, **kwargs) as response:
            result = await response.text()
            result = json.loads(json.dumps(hjson.loads(result)))
            response.raise_for_status()
    return result

async def make_get_json(session, url, kwargs={}):

        try:
            async with session.get(url, **kwargs) as response:
                result = await response.json()
                return result
        except (Exception, asyncio.TimeoutError):
            return {'message': 'json error', 'details' : 'Error In Response'}

async def make_post_json(session, url, kwargs={}):
    async with session.post(url, **kwargs) as response:
        try:
            result = await response.json()
            return result
        except:
            None