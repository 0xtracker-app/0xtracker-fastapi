from terra_sdk.client.lcd import LCDClient, wallet
import requests
import json

from terra_sdk.core.coin import Coin
from thegraph import call_graph

terra = LCDClient(chain_id="columbus-4", url="https://lcd.terra.dev")
address='terra1vlm42u2z5kkhkkujpd0l2840aysjmxf0y3dufa'

x = terra.bank.balance('terra1vlm42u2z5kkhkkujpd0l2840aysjmxf0y3dufa').to_data()

print(x)


##URLS
aamc = Coin('terra1qelfthdanju7wavc5tq0k5r0rhsyzyyrsn09qy', 1000000)
terra.market.swap_rate(aamc, 'uusd')

router_query = {"simulation":{"offer_asset":{"amount":"1000000","info":{"token":{"contract_addr":"terra1227ppwxxj3jxz8cfgq00jgnxqcny7ryenvkwj6"}}}}}
#x = terra.wasm.contract_query('terra1uenpalqlmfaf4efgtqsvzpa3gh898d9h2a232g', router_query)

terra_swap_router=f'https://fcd.terra.dev/wasm/contracts/terra1uenpalqlmfaf4efgtqsvzpa3gh898d9h2a232g/store?query_msg={json.dumps(router_query)}'
terra_wallet_balance=f'https://fcd.terra.dev/bank/balances/{address}'
terra_token_info = f'https://fcd.terra.dev/wasm/contracts/terra1qelfthdanju7wavc5tq0k5r0rhsyzyyrsn09qy/store?query_msg='


x = call_graph('https://mantle.terra.dev/?BankBalancesAddress',{"query":"\n  query BankBalancesAddress($address: String) {\n    BankBalancesAddress(Address: $address) {\n      Result {\n        Amount\n        Denom\n      }\n    }\n  }\n","variables":{"address":"terra1vlm42u2z5kkhkkujpd0l2840aysjmxf0y3dufa"}})

print(x)