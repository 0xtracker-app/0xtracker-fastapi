from . import queries
class TokenMetaData:

    def __init__(self, address=None, mongodb=None, network=None, session=None):
        self.tokenID = address
        self.cosmos_tokens = mongodb.xtracker['cosmos_tokens']
        self.cosmos_routes = mongodb.xtracker['cosmos_routes']
        self.ibc = True if 'ibc/' in address else False
        self.denom = None if 'ibc/' in address else address
        self.token_metadata = None
        self.session = session
        self.network = network
    
    async def lookup(self):
        if self.ibc:
            found_trace = await self.cosmos_routes.find_one({'hash' : self.tokenID}, {'_id': False})
            if found_trace:
                self.denom = found_trace['base_denom']
                found_token = await self.cosmos_tokens.find_one({'tokenID' : self.denom}, {'_id': False})
                if found_token:
                    self.token_metadata = found_token
            else:
                base_denom = await queries.find_trace_route(self.tokenID, self.network, self.session)
                if base_denom:
                    await self.cosmos_routes.update_one({'hash' : self.tokenID},{ "$set": base_denom}, upsert=True)
                    self.denom = base_denom['base_denom']
                    found_token = await self.cosmos_tokens.find_one({'tokenID' : self.denom}, {'_id': False})
                    if found_token:
                        self.token_metadata = found_token
        elif 'gamm/pool' in self.tokenID:
            found_token = await self.cosmos_tokens.find_one({'tokenID' : self.denom}, {'_id': False})
            if found_token:
                self.token_metadata = found_token
            else:
                get_pool = await queries.get_gamm_pool(self.tokenID, self.network, self.session)
                found_token0 = await self.cosmos_tokens.find_one({'tokenID': get_pool['token0']}, {'_id': False})
                found_token1 = await self.cosmos_tokens.find_one({'tokenID': get_pool['token1']}, {'_id': False})
                get_pool.update({
                    'tokenID': get_pool['base_denom'],
                    'tkn0s': found_token0['tkn0s'],
                    'tkn0d': found_token0['tkn0d'],
                    'tkn1s': found_token1['tkn0s'],
                    'tkn0d': found_token1['tkn0d'],
                    'token0' : found_token0['token0'],
                    'token1' : found_token1['token0'],
                    'token_decimals': [found_token0['tkn0d'],found_token1['tkn0d']],
                    'all_tokens': [found_token0['token0'], found_token1['token0']]})
                await self.cosmos_tokens.update_one({'tokenID': get_pool['base_denom']}, {"$set": get_pool}, upsert=True)
                self.token_metadata = get_pool
        else:
            found_token = await self.cosmos_tokens.find_one({'tokenID' : self.denom}, {'_id': False})
            if found_token:
                self.token_metadata = found_token

        return self.token_metadata   