from web3 import Web3
from abi.wswap import wSwapABI
w3 = Web3(Web3.HTTPProvider("http://af77e2e391d3a4e428c3a344bcbe588f-836707142.us-east-1.elb.amazonaws.com:8545"))


contract = w3.eth.contract(address=Web3.toChecksumAddress('0xD48745E39BbED146eEC15b79cBF964884F9877c2'), abi=wSwapABI)
