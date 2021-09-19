from .networks import CosmosNetwork
from . import queries
from . import oracles
from . import helpers
import asyncio


async def get_wallet_balances(wallet, session):
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks

    balances = await asyncio.gather(*[queries.get_bank_balances(network, net_config[network], session) for network in net_config])
    traces =  await asyncio.gather(*[queries.get_ibc_tokens(net_config[network['network']], session) for network in balances])
    prices = await oracles.cosmostation_prices(session)
    transform_trace = helpers.transform_trace_routes(traces)

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

