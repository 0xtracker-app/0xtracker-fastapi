

from .networks import SolanaNetwork
from . import oracles
from solana.rpc.types import TokenAccountOpts, MemcmpOpts
from . import utils
import spl.token._layouts as layouts
from .token_lookup import TokenMetaData
from .helpers import from_custom
from .farms import Farms
import asyncio
from .calculator import calculate_prices

def return_farms_list():
    solana = Farms()
    return solana.farms

async def get_wallet_balances(wallet, mongodb, session, client):
    solana = SolanaNetwork(wallet)

    balances = await client.get_token_accounts_by_owner(solana.public_key, TokenAccountOpts(program_id='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'))
    native = await client.get_balance(solana.public_key)
    prices = await oracles.get_sonar_pricing(session) 

    return_wallets = []
    native_meta = await TokenMetaData(address='11111111111111111111111111111111', mongodb=mongodb, network='solana', session=session, client=client).lookup()
    return_wallets.append({
        "token_address": '11111111111111111111111111111111',
        "symbol": native_meta['tkn0s'],
        "tokenBalance": native['result']['value'] / 1e9,
        "tokenPrice": prices['11111111111111111111111111111111'],
        "wallet": solana.wallet,
    })
    
    for each in balances['result']['value']:
        account_data = layouts.ACCOUNT_LAYOUT.parse(utils.decode_byte_string(each['account']['data'][0]))
        mint_address = utils.convert_public_key(account_data.mint)
        token_price = prices[mint_address] if mint_address in prices else 0

        if account_data.amount > 0 :
            meta_data = await TokenMetaData(address=mint_address, mongodb=mongodb, network='solana', session=session, client=client).lookup()

            return_wallets.append(
            {
                "token_address": mint_address,
                "symbol": f"{meta_data['tkn0s']}-{meta_data['tkn1s']}" if 'tkn1s' in meta_data else meta_data['tkn0s'],
                "tokenBalance": from_custom(account_data.amount, meta_data['token_decimal']),
                "tokenPrice": token_price,
                "wallet" : solana.wallet,
            }
            )


    return return_wallets

async def get_solana_positions(wallet, farm_id, mongo_db, http_session, client):
    set_farms = Farms(wallet, farm_id)
    solana = SolanaNetwork(wallet)
    farm_configuraiton = set_farms.farms[farm_id]
    
    args = {'wallet' : solana}
    returned_object = ({},{farm_id : {'name' : farm_configuraiton['name'], 'network' : farm_configuraiton['network'], 'wallet' : solana.wallet, 'userData' : {}}})

    if 'extraFunctions' in farm_configuraiton:
        
        if farm_configuraiton['extraFunctions']['vaults'] is not None:
            vaults = await asyncio.gather(*[v(session=http_session, **farm_configuraiton['extraFunctions']['vault_args'][i]) for i, v in enumerate(farm_configuraiton['extraFunctions']['vaults'])])

        farm_infos = await asyncio.gather(*[f(vaults=vaults[i], session=http_session, mongodb=mongo_db, client=client, **{**farm_configuraiton['extraFunctions']['args'][i], **args}) for i, f in enumerate(farm_configuraiton['extraFunctions']['functions'])])

        for farm_info in farm_infos:
            if farm_info is not None:
                returned_object[0].update(farm_info[0])
                returned_object[1][farm_id]['userData'].update(farm_info[1][farm_id]['userData'])

    if len(returned_object[0]) < 1:
        return {}

    prices = await oracles.get_sonar_pricing(http_session)

    response = await calculate_prices(returned_object[1], prices)

    return response