import aiohttp
import json
import hjson
from web3 import Web3
import cloudscraper
from .networks import WEB3_NETWORKS_NON_ASYNC

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
    async with session.get(url, **kwargs) as response:
        try:
            result = await response.json()
            return result
        except:
            None

async def cf_make_get_json(session, url, kwargs={}):
    scraper = cloudscraper.create_scraper(sess=session, delay=2)
    return scraper.get(url).json()

async def make_post_json(session, url, kwargs={}):
    async with session.post(url, **kwargs) as response:
        try:
            result = await response.json()
            return result
        except:
            None
    
def set_pool(abi, address, network=None):
    if network == None:
        w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))
    else:
        w3 = WEB3_NETWORKS_NON_ASYNC[network]['connection']
    contract = w3.eth.contract(address=address, abi=abi)
    poolFunctions = contract.functions
    return(poolFunctions)