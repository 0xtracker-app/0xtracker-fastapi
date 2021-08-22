from web3 import Web3

WEB3_NETWORKS = {'bsc': { 'connection' : Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/')), 'id' : 56}, 'matic':  {'connection' : Web3(Web3.HTTPProvider('https://polygon-mainnet.infura.io/v3/d09c293e2cc14290ada8169d29e9b65f')), 'id' : 137}, 'ftm' : {'connection' : Web3(Web3.HTTPProvider('https://rpc.ftm.tools/')), 'id': 250}, 'kcc' : {'connection' : Web3(Web3.HTTPProvider('https://rpc-mainnet.kcc.network')), 'id': 321}}