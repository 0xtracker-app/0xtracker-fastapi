from web3 import Web3

WEB3_NETWORKS = {'bsc': { 'connection' : Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/')), 'id' : 56},
                'matic':  {'connection' : Web3(Web3.HTTPProvider('https://polygon-mainnet.infura.io/v3/d09c293e2cc14290ada8169d29e9b65f')), 'id' : 137},
                'ftm' : {'connection' : Web3(Web3.HTTPProvider('https://rpc.ftm.tools/')), 'id': 250},
                'kcc' : {'connection' : Web3(Web3.HTTPProvider('https://rpc-mainnet.kcc.network')), 'id': 321}, 
                'optimism': { 'connection' : Web3(Web3.HTTPProvider('https://optimism-mainnet.infura.io/v3/d09c293e2cc14290ada8169d29e9b65f')), 'id' : 10},
                'eth': { 'connection' : Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d09c293e2cc14290ada8169d29e9b65f')), 'id' : 1},
                'oke': { 'connection' : Web3(Web3.HTTPProvider('https://exchainrpc.okex.org')), 'id' : 66},
                'harmony': { 'connection' : Web3(Web3.HTTPProvider('https://api.harmony.one')), 'id' : 1666600000},
                'avax': { 'connection' : Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc')), 'id' : 43114},                
                }

SCAN_APIS = {'bsc' : {'address' : 'bscscan.com', 'api_key' : '4VRVI4YKCSN4YN33MQ2BDCWXAQPHMBCZ4D', 'native_token' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c_BNB_18', 'cg_name' : 'binance-smart-chain'},
'matic' : {'address' : 'polygonscan.com', 'api_key' : 'U8KZPYXSDCJQJ1S1N84Y2P3RFR78BR8AIP', 'native_token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270_MATIC_18', 'cg_name' : 'polygon-pos'},
'ftm' : {'address' : 'ftmscan.com', 'api_key' : 'J3DT48CI882HS9JX8FNVVSYFHR5UDRQZUK', 'native_token' : '0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83_FTM_18', 'cg_name' : 'fantom'},
'eth' : {'address' : 'etherscan.io', 'api_key' : 'U8IWIUBBNDBJAIUIQDQMM4ITZKDATV4QYY', 'native_token' : '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2_ETH_18', 'cg_name' : 'ethereum'},
 }