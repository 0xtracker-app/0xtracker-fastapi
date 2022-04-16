from . import queries
import re
from . import helpers

async def get_ibc(token, network, session, cosmos_routes, cosmos_tokens):

    is_found = await cosmos_tokens.find_one({'tokenID': token}, {'_id': False})

    if is_found:
        return is_found
    else:
        base_denom = await queries.find_trace_route(token, network, session)

        if base_denom:
            await cosmos_routes.update_one({'hash' : token},{ "$set": base_denom}, upsert=True)
            
            if 'cw20' in base_denom['base_denom']:
                denom = base_denom['base_denom'].split(':')[1]
            else:
                denom = base_denom['base_denom']

            found_token = await cosmos_tokens.find_one({'tokenID' : re.compile('^' + re.escape(denom) + '$', re.IGNORECASE)}, {'_id': False})        
            
            if found_token:
                single_token = {
                    "tokenID" : token, 
                    "tkn0d" : found_token['tkn0d'], 
                    "tkn0s" : found_token['tkn0s'], 
                    "token0" : found_token['token0']
                }
                await cosmos_tokens.update_one({'tokenID': token}, {"$set": single_token}, upsert=True)

                return single_token
            else:
                single = await get_single(denom, network, session)

                if single:
                    token_metadata = { "tokenID" : single['denom'], "tkn0d" : single['decimal'], "tkn0s" : single['symbol'], "token0" : single['denom']}
                    await cosmos_tokens.update_one({'tokenID': denom}, {"$set": token_metadata}, upsert=True)
                    return token_metadata
                else:
                    return None
                
        else:
            return None

async def get_single(token, network, session):

    osmosis_tokens = await queries.get_osmosis_assets(session)

    if token in osmosis_tokens:
        return osmosis_tokens[token]

    sif_tokens = await queries.get_sif_assets(session)

    if token in sif_tokens:
        return sif_tokens[token]

    return None

async def get_cw20(token, network, session):

    cw20 = await queries.query_contract_state(session, network['rpc'], token, { "token_info": {} })
    
    return { 'denom' : token, 'symbol': cw20['symbol'], 'decimal' : cw20['decimals']}

class TokenMetaData:

    def __init__(self, address=None, mongodb=None, network=None, session=None, cw20=False):
        self.tokenID = address
        self.cosmos_tokens = mongodb['cosmos_tokens']
        self.cosmos_routes = mongodb['cosmos_routes']
        self.ibc = True if 'ibc/' in address else False
        self.denom = None if 'ibc/' in address else address
        self.token_metadata = None
        self.session = session
        self.network = network
        self.cw20 = cw20
    
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
                else:
                    full_traces = await queries.get_ibc_tokens(self.network, self.session)
                    found_trace = list(filter(lambda trace: trace['hash'] == self.tokenID.replace('ibc/', ''), full_traces['ibc_tokens']))
                    if found_trace:
                        base_denom = {'base_denom' : found_trace[0]['base_denom'], 'chain_id' : self.network['chain_id'], 'hash' : self.tokenID}
                        await self.cosmos_routes.update_one({'hash' : self.tokenID},{ "$set": base_denom}, upsert=True)
                        self.denom = base_denom['base_denom']
                        found_token = await self.cosmos_tokens.find_one({'tokenID' : self.denom}, {'_id': False})
                        if found_token:
                            self.token_metadata = found_token

        elif 'gamm/pool' in self.tokenID:
            found_token = await self.cosmos_tokens.find_one({'tokenID' : self.denom}, {'_id': False})

            if found_token:

                if 'tkn1d' not in found_token:
                    found_token['tkn1d'] = found_token['token_decimals'][1]
                    await self.cosmos_tokens.update_one({'tokenID': found_token['tokenID']}, {"$set": found_token}, upsert=True)

                get_pool = await queries.get_gamm_balances(self.tokenID, self.network, self.session)
                if get_pool:
                    found_token.update(get_pool)
                self.token_metadata = found_token
            else:
                get_pool = await queries.get_gamm_pool(self.tokenID, self.network, self.session)
                found_token0 = await get_ibc(get_pool['token0'], self.network, self.session, self.cosmos_routes, self.cosmos_tokens)
                found_token1 = await get_ibc(get_pool['token1'], self.network, self.session, self.cosmos_routes, self.cosmos_tokens)
                # print(get_pool['token0'], get_pool['token1'], self.network)
                get_pool.update({
                    'tokenID': get_pool['base_denom'],
                    'tkn0s': found_token0['tkn0s'],
                    'tkn0d': found_token0['tkn0d'],
                    'tkn1s': found_token1['tkn0s'],
                    'tkn1d': found_token1['tkn0d'],
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
            else:

                if self.cw20:
                    single = await get_cw20(self.denom, self.network, self.session)
                else:
                    single = await get_single(self.denom, self.network, self.session)

                if single:
                    self.token_metadata = { "tokenID" : single['denom'], "tkn0d" : single['decimal'], "tkn0s" : single['symbol'], "token0" : single['denom']}
                    await self.cosmos_tokens.update_one({'tokenID': self.denom}, {"$set": self.token_metadata}, upsert=True)
                else:
                    self.token_metadata = { "tokenID" : self.denom, "tkn0d" : 6, "tkn0s" : self.denom.upper(), "token0" : self.denom}

        return self.token_metadata   
