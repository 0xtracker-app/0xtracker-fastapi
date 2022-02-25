from typing import List
from web3 import Web3, eth
from evm.multicall import Call
from evm.multicall.constants import MULTICALL_ADDRESSES

w3 = { 'connection' : Web3(Web3.AsyncHTTPProvider('https://bsc-dataseed.binance.org/'), modules={'eth': (eth.AsyncEth,)}, middlewares=[]), 'id' : 56}

class Multicall:
    def __init__(self, calls: List[Call], _w3=None, _block=None, _strict=None, _list=None):
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

        if _list is None:
            self.list = False
        else:
            self.list = _list
        


    async def __call__(self):
        aggregate = Call(
            MULTICALL_ADDRESSES[self.network_id],
            'aggregate((address,bytes)[],bool)(uint256,(bool,bytes)[])',
            None,
            self.w3,
            self.block
        )
        args = [[[call.target, call.data] for call in self.calls], self.strict]
        block, outputs = await aggregate(args)
        result = {}
        result_list = []

        for call, output in zip(self.calls, outputs):
            if output[0] == True and output[1]:
                #print(call.returns,output)
                if call.returns:
                    result.update(call.decode_output(output[1]))
                else:
                    result_list.append(call.decode_output(output[1]))

        if self.list:
            return result_list
        else:
            return result