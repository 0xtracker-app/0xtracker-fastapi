from functools import wraps

import aioredis
import json
import os

CACHE = os.getenv("CACHE", "True") == "True"
CACHE_TTL = os.getenv("CACHE_TTL", 180)


class RedisClient:
    session: aioredis.Redis = aioredis.from_url(url=os.getenv("REDIS_URL", "redis://localhost:6379"))

if CACHE:
    redis = RedisClient() 


def cache_function(keyparams=None):
    def wrap(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__module__}.{func.__name__}{args[:keyparams]}"
            if CACHE:
                val = await redis.session.get(key)
            else: 
                val = None
        
            if val:
                results = json.loads(val)
            else:
                results = await func(*args, **kwargs)
                if CACHE:
                    await redis.session.set(key, json.dumps(results), ex=CACHE_TTL)
            return results
        return wrapper        
    return wrap