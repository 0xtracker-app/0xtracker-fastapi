from multicall import Call, Multicall
import requests
import json
import time
import pandas as pd
from web3 import Web3
from networks import WEB3_NETWORKS, SCAN_APIS
import multicall.parsers as parser

def round_unix(time):
    ts = pd.to_datetime(time,unit='s')
    return int(ts.round(freq = 'D').timestamp())

def get_historical_transfer(wallet, token, filtered_farm,network):
    apikey = SCAN_APIS[network]['api_key']
    scan_url = SCAN_APIS[network]['address']
    url = f'https://api.{scan_url}/api?module=account&action=tokentx&contractaddress={token}&address={wallet}&to=startblock=0&endblock=9605337&sort=asc&apikey={apikey}'
    r = requests.get(url)
    data = json.loads(r.text)['result']

    filtered_to =[{ 'txHash' : x['hash'], 'blockNumber' : x['blockNumber'], 'blockHash': x['blockHash'], 'day': round_unix(int(x['timeStamp'])), 'timeStamp': int(x['timeStamp']), 'value' : int(x['value']), 'decimal': int(x['tokenDecimal']), 'tokenAmount' :  parser.from_custom(int(x['value']), int(x['tokenDecimal']))} for x in data if x['to'].lower() == filtered_farm.lower() and int(x['value']) > 0]
    filtered_from =[{ 'txHash' : x['hash'], 'blockNumber' : x['blockNumber'], 'blockHash': x['blockHash'], 'day': round_unix(int(x['timeStamp'])), 'timeStamp': int(x['timeStamp']), 'value' : int(x['value']), 'decimal': int(x['tokenDecimal']), 'tokenAmount' :  parser.from_custom(int(x['value']), int(x['tokenDecimal']))} for x in data if x['from'].lower() == filtered_farm.lower() and int(x['value']) > 0]

    return {'txFrom': filtered_from, 'txTo' : filtered_to}



transactions = get_historical_transfer('0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f', '0xa9338126a645aca52aa74ce65fbc1092eb67d335', '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', 'bsc')

print(transactions)
