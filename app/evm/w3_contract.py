from web3 import Web3
from .networks import WEB3_NETWORKS_NON_ASYNC

def set_pool(abi, address, network=None):
    if network == None:
        w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))
    else:
        w3 = WEB3_NETWORKS_NON_ASYNC[network]['connection']
    contract = w3.eth.contract(address=address, abi=abi)
    poolFunctions = contract.functions
    return(poolFunctions)