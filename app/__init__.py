from dotenv import load_dotenv
from .redis.cache import RedisClient, CACHE, CACHE_TTL, cache_function 

load_dotenv()