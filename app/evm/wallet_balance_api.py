from multicall import Call, Multicall
import requests
import json
import time
from web3 import Web3
from oracles import coingecko_by_address_network
from networks import WEB3_NETWORKS, SCAN_APIS

def from_wei(value):
    return value / 1e18

def from_ele(value):
    return '0xAcD7B3D9c10e97d0efA418903C0c7669E702E4C0'

def parseReserves(value):
    return [value[0], value[1]]

def parseWanted(value):
    return value[0]

def from_custom(value, decimal):
    return value / (10**decimal)

def convert_timestamp(epoch):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(epoch))

def get_native_balance(wallet,network):
    w3 = WEB3_NETWORKS[network]['connection']
    wallet = Web3.toChecksumAddress(wallet)
    return w3.eth.getBalance(wallet)

def get_balance_of(token_list, wallet, network, native_token):

    calls = []
    for token in token_list:
        token_contract = token['contractAddress']
        token_decimal = token['tokenDecimal']
        token_symbol = token['symbol']
        calls.append(Call(token_contract, ['balanceOf(address)(uint256)', wallet], [[f'{token_contract}_{token_symbol}_{token_decimal}', None]]))
    
    multi_return = Multicall(calls, WEB3_NETWORKS[network])()

    #multi_return['0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c_BNB_18'] = get_native_balance(wallet, 'bsc')
    multi_return = { **{native_token : get_native_balance(wallet, network) }, **multi_return}

    user_holdings = {x : from_custom(multi_return[x], int(x.split('_')[2])) for x in multi_return if multi_return[x] > 0}
    token_ids = [x.split('_')[0] for x in multi_return if multi_return[x] > 0]

    return user_holdings, ','.join(token_ids)

def get_wallet_balance(wallet, network):
    network_data = SCAN_APIS[network]
    apikey = network_data['api_key']
    latest_block = WEB3_NETWORKS[network]['connection'].eth.block_number
    scan_url = network_data['address']
    url = f'https://api.{scan_url}/api?module=account&action=tokentx&address={wallet}&to=startblock=0&endblock={latest_block}&sort=asc&apikey={apikey}'

    r = requests.get(url)
    data = json.loads(r.text)['result']
    filtered_to =[{'symbol': x['tokenSymbol'].replace(' ', '').replace('_', ''), 'tokenDecimal' : x['tokenDecimal'], 'contractAddress' : x['contractAddress']} for x in data if x['to'].lower() == wallet.lower() and int(x['value']) > 0]
    unique_list =[i for n, i in enumerate(filtered_to) if i not in filtered_to[n + 1:]]
    
    wallet_data = get_balance_of(unique_list, wallet, network, network_data['native_token'])
    prices = coingecko_by_address_network(wallet_data[1], network_data['cg_name'])
    payload = []

    for token in wallet_data[0]:
        breakdown = token.split('_')
        address = breakdown[0]
        symbol = breakdown[1]
        try:
            price = prices[address]['usd'] if address in prices else 0
        except:
            price = 0

        data = {
            'token_address' : address,
            'symbol' : symbol,
            'tokenBalance' : wallet_data[0][token],
            'tokenPrice' : price
        }

        payload.append(data)


    return payload