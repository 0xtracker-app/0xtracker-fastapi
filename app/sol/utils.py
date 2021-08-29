from base64 import b64decode, b64encode
from base58 import b58decode
from solana.publickey import PublicKey
import json
import asyncio
import aiohttp
import requests
from . import helpers

RPC_CONNECTION = 'https://api.mainnet-beta.solana.com'

def decode_byte_string(byte_string: str, encoding: str = "base64") -> bytes:
    """Decode a encoded string from an RPC Response."""
    b_str = str.encode(byte_string)
    if encoding == "base64":
        return b64decode(b_str)
    if encoding == "base58":
        return b58decode(b_str)

    raise NotImplementedError(f"{encoding} decoding not currently supported.")

def convert_public_key(hash):
    return str(PublicKey(hash))

def generate_farm_dict(token_account):
    with open("./local/raydium_farms.json") as f:
        data = json.load(f)

    return [x for x in data if x['poolLpTokenAccount'] == token_account]

def generate_lp_dict(mint_address):
    with open("./local/raydium_liquidity.json") as f:
        data = json.load(f)
    return [x for x in data if x['lp']['mintAddress'] == mint_address]

def generate_info_account_list():
    with open("./local/solfarm_raydium.json") as f:
        data = json.load(f)
    return [x['oldInfoAccount'] for x in data['vault']['accounts']]

def generate_solfarm_vaults():
    with open("./local/solfarm_raydium.json") as f:
        data = json.load(f)
    return [x['account'] for x in data['vault']['accounts']]

def generate_saber_address():
    with open("./local/saber_farms.json") as f:
        data = json.load(f)
    return [x['address'] for x in data]

def generate_saber_program():
    with open("./local/saber_farms.json") as f:
        data = json.load(f)
    return [x['programId'] for x in data]

def generate_saber_pool_info():
    with open("./local/saber_poolinfo.json") as f:
        data = json.load(f)
    return data['data']

def generate_saber_plot_keys():
    with open("./local/saber_poolinfo.json") as f:
        data = json.load(f)
    return [x['plotKey'] for x in data['data']['pools']]

async def getTokenSupply(publicKey: str):
    ##get_token_supply not in solana.py yet so doing it manually

    headers = {"Content-Type": "application/json"}

    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [publicKey]
    }

    result = await make_request(json.dumps(data), headers)
    return result

async def getMultipleAccounts(accounts: list):
    ##get_multiple_accounts not in solana.py yet so doing it manually

    headers = {"Content-Type": "application/json"}

    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMultipleAccounts",
        "params": [accounts]
    }

    result = await make_request(json.dumps(data), headers)
    return result

async def make_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.text()
            response.raise_for_status()
    
    return json.loads(result)

async def make_request(data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(RPC_CONNECTION, headers=headers, data=data) as response:
            result = await response.text()
            response.raise_for_status()
    
    return json.loads(result)

def get_program_address(vault_account_info,wallet,program):
    return str(PublicKey.find_program_address([helpers.public_key_hex(vault_account_info), helpers.public_key_hex(wallet)], program)[0])

def get_anchor_account(wallet,farm_plot,associated_program):
    return str(PublicKey.find_program_address([memoryview(b'anchor'), helpers.public_key_hex(wallet), helpers.public_key_hex(farm_plot)], associated_program)[0])

async def get_token_metadata():
    token_info = await make_get('https://raw.githubusercontent.com/solana-labs/token-list/main/src/tokens/solana.tokenlist.json')

    return {t['address'] : t for t in token_info['tokens']  }