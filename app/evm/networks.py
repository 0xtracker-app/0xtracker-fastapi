from web3 import Web3, eth
import os
from dotenv import load_dotenv

load_dotenv()

WEB3_NETWORKS_NON_ASYNC = {'bsc': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("BSC_RPC"))), 'id' : 56},
                'matic':  {'connection' : Web3(Web3.HTTPProvider(os.getenv("MATIC_RPC"))), 'id' : 137},
                'ftm' : {'connection' : Web3(Web3.HTTPProvider(os.getenv("FTM_RPC"))), 'id': 250},
                'kcc' : {'connection' : Web3(Web3.HTTPProvider(os.getenv("KCC_RPC"))), 'id': 321}, 
                'optimism': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("OPTIMISM_RPC"))), 'id' : 10},
                'eth': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("ETH_RPC"))), 'id' : 1},
                'oke': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("OKE_RPC"))), 'id' : 66},
                'harmony': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("HARMONY_RPC"))), 'id' : 1666600000},
                'avax': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("AVAX_RPC"))), 'id' : 43114},
                'moon': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("MOON_RPC"))), 'id' : 1285},
                'arb': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("ARB_RPC"))), 'id' : 42161},
                'celo': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("CELO_RPC"))), 'id' : 42220},
                'xdai': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("XDAI_RPC"))), 'id' : 100},
                'heco': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("HECO_RPC"))), 'id' : 128},
                'meter': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("METER_RPC"))), 'id' : 82},
                'cro': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("CRO_RPC"))), 'id' : 25},
                'polis': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("POLIS_RPC"))), 'id' : 333999},
                'boba': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("BOBA_RPC"))), 'id' : 288},
                'theta': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("THETA_RPC"))), 'id' : 361},
                'aurora': { 'connection' : Web3(Web3.HTTPProvider(os.getenv("AURORA_RPC"))), 'id' : 1313161554},             
                }

WEB3_NETWORKS = {'bsc': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("BSC_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 56},
                'matic':  {'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("MATIC_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 137},
                'ftm' : {'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("FTM_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id': 250},
                'kcc' : {'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("KCC_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id': 321}, 
                'optimism': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("OPTIMISM_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 10},
                'eth': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("ETH_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 1},
                'oke': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("OKE_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 66},
                'harmony': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("HARMONY_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 1666600000},
                'avax': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("AVAX_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 43114},
                'moon': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("MOON_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 1285},
                'arb': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("ARB_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 42161},                
                'celo': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("CELO_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 42220},
                'xdai': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("XDAI_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 100},
                'heco': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("HECO_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 128},
                'meter': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("METER_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 82},
                'cro': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("CRO_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 25},
                'polis': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("POLIS_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 333999},
                'boba': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("BOBA_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 288},
                'theta': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("THETA_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 361},
                'aurora': { 'connection' : Web3(Web3.AsyncHTTPProvider(os.getenv("AURORA_RPC")), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 1313161554},
                }

SCAN_APIS = {'bsc' : {'address' : 'bscscan.com', 'api_key' : os.getenv("BSC_SCAN"), 'native_token' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c_BNB_18', 'cg_name' : 'binance-smart-chain'},
'matic' : {'address' : 'polygonscan.com', 'api_key' : os.getenv("MATIC_SCAN"), 'native_token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270_MATIC_18', 'cg_name' : 'polygon-pos'},
'ftm' : {'address' : 'ftmscan.com', 'api_key' : os.getenv("FTM_SCAN"), 'native_token' : '0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83_FTM_18', 'cg_name' : 'fantom'},
'eth' : {'address' : 'etherscan.io', 'api_key' : os.getenv("ETH_SCAN"), 'native_token' : '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2_ETH_18', 'cg_name' : 'ethereum'},
'arb' : {'address' : 'arbiscan.io', 'api_key' : os.getenv("ARB_SCAN"), 'native_token' : '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1', 'cg_name' : 'arbitrum-one'},
 }