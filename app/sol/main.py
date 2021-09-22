

from .networks import SolanaNetwork
from . import oracles
from solana.rpc.types import TokenAccountOpts, MemcmpOpts

async def get_wallet_balances(wallet, mongodb, session, client):
    solana = SolanaNetwork(wallet)

    balances = await client.get_token_accounts_by_owner(solana.public_key, TokenAccountOpts(program_id='TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'))
    prices = await oracles.get_sonar_pricing(session) 
    print(prices)
    return_wallets = []
    for balance in balances:

        if balance['tokens']:
            for token in balance['tokens']:

                token_denom = transform_trace[0][token['denom']] if token['denom'] in transform_trace[0] else token['denom']
                token_decimal = transform_trace[1][token_denom]['decimal'] if token_denom in transform_trace[1] else 6
            return_wallets.append(
                {
                    "token_address": token['denom'],
                    "symbol": transform_trace[1][token_denom]['display_denom'] if token_denom in transform_trace[1] else token_denom.upper(),
                    "tokenBalance": helpers.from_custom(token['amount'], token_decimal),
                    "tokenPrice": prices[token_denom],
                    "wallet" : balance['wallet'],
                }
                )

    return return_wallets