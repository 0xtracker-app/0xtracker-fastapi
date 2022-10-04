from eth_typing import encoding
from . import queries
from . import slicers
from . import utils
from . import stake_layout

def parse_ray_ammv4(container):
    data = {
        'poolCoinTokenAccount': container.poolCoinTokenAccount,
        'poolPcTokenAccount': container.poolPcTokenAccount,
        'coinMintAddress': container.coinMintAddress,
        'pcMintAddress': container.pcMintAddress,
        'lpMintAddress': container.lpMintAddress,
        'ammOpenOrders': container.ammOpenOrders,
        'serumMarket': container.serumMarket,
        'serumProgramId': container.serumProgramId,
        'ammTargetOrders': container.ammTargetOrders,
        'poolWithdrawQueue': container.poolWithdrawQueue,
        'poolTempLpTokenAccount': container.poolTempLpTokenAccount,
        'ammOwner': container.ammOwner,
        'pnlOwner': container.pnlOwner,
    }
    return data

def parse_ray_ammv3(container):
    data = {
        'poolCoinTokenAccount': container.poolCoinTokenAccount,
        'poolPcTokenAccount': container.poolPcTokenAccount,
        'coinMintAddress': container.coinMintAddress,
        'pcMintAddress': container.pcMintAddress,
        'lpMintAddress': container.lpMintAddress,
        'ammOpenOrders': container.ammOpenOrders,
        'serumMarket': container.serumMarket,
        'serumProgramId': container.serumProgramId,
        'ammTargetOrders': container.ammTargetOrders,
        'ammQuantities': container.ammQuantities,
        'poolWithdrawQueue': container.poolWithdrawQueue,
        'poolTempLpTokenAccount': container.poolTempLpTokenAccount,
        'ammOwner': container.ammOwner,
        'pnlOwner': container.pnlOwner,
        'srmTokenAccount': container.srmTokenAccount,
    }
    return data

def parse_ray_amm(container):
    data = {
        'poolCoinTokenAccount': container.poolCoinTokenAccount,
        'poolPcTokenAccount': container.poolPcTokenAccount,
        'coinMintAddress': container.coinMintAddress,
        'pcMintAddress': container.pcMintAddress,
        'lpMintAddress': container.lpMintAddress,
        'ammOpenOrders': container.ammOpenOrders,
        'serumMarket': container.serumMarket,
        'serumProgramId': container.serumProgramId,
        'ammTargetOrders': container.ammTargetOrders,
        'ammQuantities': container.ammQuantities,
        'poolWithdrawQueue': container.poolWithdrawQueue,
        'poolTempLpTokenAccount': container.poolTempLpTokenAccount,
        'ammOwner': container.ammOwner,
        'pnlOwner': container.pnlOwner,
    }
    return data

async def check_raydium_lp(client, token, session):
    token_lookup = await queries.get_solana_tokenlist(session)

    lp_token = {
        'tokenID': token,
        "network" : "solana",
        "type": "lp",
    }

    rayv4 = await client.get_program_accounts('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8', data_size=752, encoding='base64', memcmp_opts=slicers.memcmp_owner(token, 464))
    
    if rayv4['result']:
        account_data = stake_layout.RAYDIUM_AMM_V4.parse(utils.decode_byte_string(rayv4['result'][0]['account']['data'][0]))
        token_0 = token_lookup[account_data.coinMintAddress]
        token_1 = token_lookup[account_data.pcMintAddress]
        
        lp_token['token_decimal'] = 6
        lp_token['symbol'] = f"{token_0['symbol']}-{token_1['symbol']}"
        lp_token['tkn0s'] = token_0['symbol']
        lp_token['tkn0d'] = account_data.coinDecimals
        lp_token['tkn1s'] = token_1['symbol']
        lp_token['tkn1d'] = account_data.pcDecimals
        lp_token['token0'] = account_data.coinMintAddress
        lp_token['token1'] = account_data.pcMintAddress
        lp_token['token_decimals'] = [account_data.coinDecimals, account_data.pcDecimals]
        lp_token['all_tokens'] = [account_data.coinMintAddress, account_data.pcMintAddress]
        lp_token['lp_data'] = parse_ray_ammv4(account_data)
        lp_token['type'] = "ray-v4-lp"

        return lp_token
    else:
        rayv3 = await client.get_program_accounts('27haf8L6oxUeXrHrgEgsexjSY5hbVUWEmvv9Nyxg8vQv', data_size=680, encoding='base64', memcmp_opts=slicers.memcmp_owner(token, 328))

        if rayv3['result']:
            account_data = stake_layout.RAYDIUM_AMM_V3.parse(utils.decode_byte_string(rayv4['result'][0]['account']['data'][0]))

            # lp_token['lp_data'] = parse_ray_ammv3(account_data)
            # lp_token['type'] = "ray-v3-lp"
        else:
            ray = await client.get_program_accounts('RVKd61ztZW9GUwhRbbLoYVRE5Xf1B2tVscKqwZqXgEr', data_size=624, encoding='base64', memcmp_opts=slicers.memcmp_owner(token, 304))

            if ray['result']:
                account_data = stake_layout.RAYDIUM_AMM.parse(utils.decode_byte_string(rayv4['result'][0]['account']['data'][0]))

                # lp_token['lp_data'] = parse_ray_amm(account_data)
                # lp_token['type'] = "ray-lp"
                
    return None

class TokenMetaData:

    def __init__(self, address=None, mongodb=None, network=None, session=None, client=None):
        self.tokenID = address
        self.solana_tokens = mongodb['solana_tokens']
        self.solana_accounts = mongodb['solana_accounts']
        self.token_metadata = None
        self.session = session
        self.network = network
        self.client = client

    async def lookup(self):
        found_token = await self.solana_tokens.find_one({'tokenID': self.tokenID}, {'_id': False})

        if found_token:
            return found_token
        else:
            pair_lookup = await queries.get_raydium_pairs(self.session)
            token_lookup = await queries.get_raydium_tokens(self.session)

            if self.tokenID in pair_lookup:
                token_metadata = pair_lookup[self.tokenID]
                if token_metadata['coin_mint_address']:
                    found_token0 = token_lookup[token_metadata['coin_mint_address']]
                    found_token1 = token_lookup[token_metadata['pc_mint_address']]
                    lp_decimal = await self.client.get_account_info(self.tokenID, encoding='jsonParsed')

                    lp_token = {
                        'tokenID': self.tokenID,
                        'token_decimal': lp_decimal['result']['value']['data']['parsed']['info']['decimals'],
                        "network" : "solana",
                        "type": "lp",
                        "symbol": token_metadata['name'],
                        'tkn0s': found_token0['symbol'],
                        'tkn0d': found_token0['decimals'],
                        'tkn1s': found_token1['symbol'],
                        'tkn0d': found_token1['decimals'],
                        'token0': found_token0['address'],
                        'token1': found_token1['address'],
                        'token_decimals': [found_token0['decimals'], found_token1['decimals']],
                        'all_tokens': [found_token0['address'], found_token1['address']]}

                    rayv4 = await self.client.get_program_accounts('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8', data_size=752, encoding='base64', memcmp_opts=slicers.memcmp_owner(self.tokenID, 464))
                    
                    if rayv4['result']:
                        account_data = stake_layout.RAYDIUM_AMM_V4.parse(utils.decode_byte_string(rayv4['result'][0]['account']['data'][0]))
                        lp_token['lp_data'] = parse_ray_ammv4(account_data)
                        lp_token['type'] = "ray-v4-lp"
                    else:
                        rayv3 = await self.client.get_program_accounts('27haf8L6oxUeXrHrgEgsexjSY5hbVUWEmvv9Nyxg8vQv', data_size=680, encoding='base64', memcmp_opts=slicers.memcmp_owner(self.tokenID, 328))

                        if rayv3['result']:
                            account_data = stake_layout.RAYDIUM_AMM_V3.parse(utils.decode_byte_string(rayv4['result'][0]['account']['data'][0]))
                            lp_token['lp_data'] = parse_ray_ammv3(account_data)
                            lp_token['type'] = "ray-v3-lp"
                        else:
                            ray = await self.client.get_program_accounts('RVKd61ztZW9GUwhRbbLoYVRE5Xf1B2tVscKqwZqXgEr', data_size=624, encoding='base64', memcmp_opts=slicers.memcmp_owner(self.tokenID, 304))

                            if ray['result']:
                                account_data = stake_layout.RAYDIUM_AMM.parse(utils.decode_byte_string(rayv4['result'][0]['account']['data'][0]))
                                lp_token['lp_data'] = parse_ray_amm(account_data)
                                lp_token['type'] = "ray-lp"
                    
                    await self.solana_tokens.update_one({'tokenID': self.tokenID}, {"$set": lp_token}, upsert=True)
                    self.token_metadata = lp_token
                else:
                    single_token = {
                        "network": "solana",
                        "tokenID": self.tokenID,
                        'token_decimal': token_metadata['decimals'],
                        "tkn0d": token_metadata['decimals'],
                        "tkn0s": token_metadata['symbol'],
                        "token0": token_metadata['mint_address'],
                        "type": "single"
                    }
                    await self.solana_tokens.update_one({'tokenID': self.tokenID}, {"$set": single_token}, upsert=True)
                    self.token_metadata = single_token
            else:
                ray_lp = await check_raydium_lp(self.client, self.tokenID, self.session)

                if ray_lp:
                    await self.solana_tokens.update_one({'tokenID': self.tokenID}, {"$set": ray_lp}, upsert=True)
                    self.token_metadata = ray_lp
                else: 
                    single_token_data = token_lookup.get(self.tokenID)

                    if single_token_data:
                        self.token_metadata = {
                            "network": "solana",
                            "tokenID": self.tokenID,
                            'token_decimal': single_token_data['decimals'],
                            "tkn0d": single_token_data['decimals'],
                            "tkn0s": single_token_data['symbol'],
                            "token0": self.tokenID,
                            "type": "single"
                        }
                        await self.solana_tokens.update_one({'tokenID': self.tokenID}, {"$set": self.token_metadata}, upsert=True)
                    else:
                        self.token_metadata = {
                            "network": "solana",
                            "tokenID": self.tokenID,
                            'token_decimal': 6,
                            "tkn0d": 6,
                            "tkn0s": 'unknown',
                            "token0": self.tokenID,
                            "type": "single"
                        }

        return self.token_metadata

    async def account_to_mint(self):
        found_token = await self.solana_accounts.find_one({'public_account': self.tokenID}, {'_id': False})

        if found_token:
            self.tokenID = found_token['mint_address']
            return await self.lookup()
        else:
            account_to_mint = await self.client.get_account_info(self.tokenID, encoding="jsonParsed")
            mint_address = account_to_mint['result']['value']['data']['parsed']['info']['mint']
            await self.solana_accounts.update_one({'public_account': self.tokenID}, {"$set": {'public_account' : self.tokenID, 'mint_address' : mint_address}}, upsert=True)
            self.tokenID = mint_address
            return await self.lookup()