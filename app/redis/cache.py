from functools import wraps

import aioredis
import json
import os

CACHE = os.getenv("CACHE", "True") == "True"
CACHE_TTL = os.getenv("CACHE_TTL", 180)


class RedisClient:
    session: aioredis.Redis = aioredis.from_url(
        url=os.getenv("REDIS_URL", "redis://localhost:6379"))


if CACHE:
    redis = RedisClient()

async def getvalue(key):
    try: 
        if CACHE:
            val = await redis.session.get(key)
        else:
            val = '[]'

        return json.loads(val)
    except:
        return []
        
def cache_function(keyparams=None, ttl=None):
    def wrap(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if type(keyparams) == int:
                key = f"i8n_{func.__module__}.{func.__name__}{args[:keyparams]}"
            elif type(keyparams) == list:
                params = ""
                if len(keyparams) > 0 and len(args) > 0:
                    params = [args[i] for i in keyparams]
                key = f"i8n_{func.__module__}.{func.__name__}{params}"
                       
            if CACHE:
                val = await redis.session.get(key)
            else:
                val = None

            if val:
                results = json.loads(val)
            else:
                results = await func(*args, **kwargs)
                if CACHE:
                    await redis.session.set(key, json.dumps(results), ex=ttl or CACHE_TTL)
            return results
        return wrapper
    return wrap
