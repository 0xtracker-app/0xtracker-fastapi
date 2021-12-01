from . import queries
import bech32


async def single_token_finder(token, session, client):
    single_token = await queries.find_native_denom(token, session)

    if single_token:
        meta_data = {
                        "network": "terra",
                        "tokenID": token,
                        'token_decimal': 6,
                        "tkn0d": 6,
                        "tkn0s": single_token['symbol'],
                        "token0": token,
                        "type": "single"
                    }

        return meta_data

    non_native_single = await client.wasm.contract_info(token)   

    if 'mint' not in non_native_single['init_msg']:
        meta_data = {
                        "network": "terra",
                        "tokenID": token,
                        'token_decimal': non_native_single['init_msg']['decimals'],
                        "tkn0d": non_native_single['init_msg']['decimals'],
                        "tkn0s": non_native_single['init_msg']['symbol'],
                        "token0": token,
                        "type": "single"
                    }

        return meta_data
    
    return None

async def lp_token_finder(token, session, client):

    try:
        minter = await client.wasm.contract_info(token)
        lp_token = await client.wasm.contract_query(minter['init_msg']['mint']['minter'], {"pool": {} })

        token_0 = await single_token_finder(lp_token['assets'][0]['info']['token']['contract_addr'], session, client)
        if 'native_token' in lp_token['assets'][1]['info']:
            token_1 = await single_token_finder(lp_token['assets'][1]['info']['native_token']['denom'], session, client)
        else:
            token_1 = await single_token_finder(lp_token['assets'][1]['info']['token']['contract_addr'], session, client)

        lp_token = {
            'tokenID': token,
            'token_decimal': 6,
            "network" : "terra",
            "type": "lp",
            "symbol": minter['init_msg']['symbol'],
            'tkn0s': token_0['tkn0s'],
            'tkn0d': token_0['tkn0d'],
            'tkn1s': token_1['tkn0s'],
            'tkn0d': token_1['tkn0d'],
            'token0': token_0['tokenID'],
            'token1': token_1['tokenID'],
            'token_decimals': [token_0['tkn0d'], token_1['tkn0d']],
            'all_tokens': [token_0['tokenID'], token_1['tokenID']]}
        return lp_token
    except:
        return None

class TokenMetaData:

    def __init__(self, address=None, mongodb=None, client=None, session=None):
        self.tokenID = address
        self.terra_tokens = mongodb.xtracker['terra_tokens']
        self.token_metadata = None
        self.session = session
        self.client = client
    
    async def lookup(self):
        found_token = await self.terra_tokens.find_one({'tokenID': self.tokenID}, {'_id': False})

        if found_token:
            return found_token
        else:
            denom_lookup = await lp_token_finder(self.tokenID, self.session, self.client)

            if denom_lookup:
                await self.terra_tokens.update_one({'tokenID': self.tokenID}, {"$set": denom_lookup}, upsert=True)
                self.token_metadata = denom_lookup
            else:
                denom_lookup = await single_token_finder(self.tokenID, self.session, self.client)

                if denom_lookup:
                    await self.terra_tokens.update_one({'tokenID': self.tokenID}, {"$set": denom_lookup}, upsert=True)
                    self.token_metadata = denom_lookup
                else:
                    None

        return self.token_metadata
