from .multicall import Call, Multicall, parsers
from .utils import make_get, make_get_json
from .networks import WEB3_NETWORKS
import json
import os
from dotenv import load_dotenv

load_dotenv()

COVALENT_KEY = os.getenv("COVALENT_API")
NETWORK_MAP = {x : str(WEB3_NETWORKS[x]['id']) for x in WEB3_NETWORKS if WEB3_NETWORKS[x]['covalent']}
async def get_tx_to_contract(network, wallet, token, contract, session):
    query = json.dumps({"$or": [{"from_address": contract},{"to_address": contract}]})
    sorting = json.dumps({'block_height': 1})
    
    response = {
        'totalDeposits' : 0,
        'totalWithdrawls' : 0,
        'estStake' : 0,
        'gasUsed' : 0,
        'deposits' : [],
        'withdrawls' : []
    }
    
    if network not in NETWORK_MAP.keys():
        return response
    
    network = NETWORK_MAP[network]
        
    url = f'https://api.covalenthq.com/v1/{network}/address/{wallet}/transfers_v2/?contract-address={token}&match={query}&sort={sorting}&page-size=2100000000&key={COVALENT_KEY}'

    x = await make_get_json(session, url)

    for block in x['data']['items']:
        response['gasUsed'] += block['gas_quote'] if 'gas_quote' in block else 0
        for tx in block['transfers']:
            token_amount = parsers.from_custom(int(tx['delta']), int(tx['contract_decimals']))
            if token_amount > 0:
                if tx['transfer_type'] == 'IN':
                    response['totalWithdrawls'] += token_amount
                    response['estStake'] -= token_amount
                    response['withdrawls'].append({
                        'block_height' : block['block_height'],
                        'block_signed_at' : tx['block_signed_at'],
                        'token_transfer_amount' : token_amount
                        })
                    if response['estStake'] < 0:
                        response['estStake'] = 0
                else:
                    response['totalDeposits'] += token_amount
                    response['estStake'] += token_amount
                    response['deposits'].append({
                        'block_height' : block['block_height'],
                        'block_signed_at' : tx['block_signed_at'],
                        'token_transfer_amount' : token_amount
                        })

    return response

async def get_router_details(network, contract, session):
    query = json.dumps({"$or": [{"from_address": contract},{"to_address": contract}]})
    sorting = json.dumps({'block_height': 1})
    network = NETWORK_MAP[network]

    primer = json.dumps([
    {
        "$match": {
            "log_events": {
                "$elemmatch": {
                    "decoded.name": "Transfer"
                }
            }
        }
    },
    {
        "$group": {
            "_id": {
                "month": {
                    "$month": "block_signed_at"
                },
                "day": {
                    "$dayOfMonth": "block_signed_at"
                },
                "year": {
                    "$year": "block_signed_at"
                },
                "hour": {
                    "$hourOfDay": "block_signed_at"
                }
            },
            "transfer_count": {
                "$sum": 1
            }
        }
    }
])

    url = f'https://api.covalenthq.com/v1/{network}/address/{contract}/transactions_v2/?page-size=10000&primer={primer}&key={COVALENT_KEY}'
    x = await make_get_json(session, url)

    return x