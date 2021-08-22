from typing import List

from web3 import Web3

from multicall import Call
from multicall.constants import MULTICALL_ADDRESSES
w3 = { 'connection' : Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/')), 'id' : 56}
#w3 = Web3(Web3.HTTPProvider("http://af77e2e391d3a4e428c3a344bcbe588f-836707142.us-east-1.elb.amazonaws.com:8545"))
class Multicall:
    def __init__(self, calls: List[Call], _w3=None, _block=None, _strict=None):
        self.calls = calls

        if _w3 is None:
            self.w3 = w3
            self.network_id = 56
        else:
            self.w3 = _w3
            self.network_id = _w3['id']
        
        if _block is None:
            self.block = 'latest'
        else:
            self.block = _block
        
        if _strict is None:
            self.strict = True
        else:
            self.strict = False

    def __call__(self):
        aggregate = Call(
            MULTICALL_ADDRESSES[self.network_id],
            'aggregate((address,bytes)[],bool)(uint256,(bool,bytes)[])',
            None,
            self.w3,
            self.block
        )
        args = [[[call.target, call.data] for call in self.calls], self.strict]
        block, outputs = aggregate(args)
        result = {}

        for call, output in zip(self.calls, outputs):
            if output[0] == True:
                r = call.decode_output(output[1])
                result.update(call.decode_output(output[1]))
            #print(r)
        return result
