from .multicall import Call, Multicall, parsers
from .utils import make_get_json
import json
import os
from dotenv import load_dotenv

load_dotenv()

COVALENT_KEY = os.getenv("COVALENT_API")
NETWORK_MAP = {'eth' : '1', 'bsc' : '56', 'matic' : '137', 'avax' : '43113', 'ftm' : '250', 'arb' : '42161'}

async def get_tx_to_contract(network, wallet, token, contract, session):
    query = json.dumps({"$or": [{"from_address": contract},{"to_address": contract}]})
    sorting = json.dumps({'block_height': 1})
    network = NETWORK_MAP[network]
    url = f'https://api.covalenthq.com/v1/{network}/address/{wallet}/transfers_v2/?contract-address={token}&match={query}&sort={sorting}&page-size=2100000000&key={COVALENT_KEY}'

    x = await make_get_json(session, url)

    response = {
        'totalDeposits' : 0,
        'totalWithdrawls' : 0,
        'estStake' : 0,
        'gasUsed' : 0,
        'deposits' : [],
        'withdrawls' : []
    }

    for block in x['data']['items']:
        response['gasUsed'] += block['gas_quote']
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
