from eth_utils import to_checksum_address
from . import Signature
from web3 import Web3, eth
from hexbytes import HexBytes
w3 = Web3(Web3.AsyncHTTPProvider('https://bsc-dataseed.binance.org/'), modules={'eth': (eth.AsyncEth,)}, middlewares=[])

class Call:
    def __init__(self, target, function, returns=None, _w3=None, _block=None):
        self.target = to_checksum_address(target)

        if isinstance(function, list):
            self.function, *self.args = function
        else:
            self.function = function
            self.args = None

        if _w3 is None:
            self.w3 = w3
        else:
            self.w3 = _w3['connection']
        
        if _block is None:
            self.block = 'latest'
        else:
            self.block = _block

        self.signature = Signature(self.function)
        self.returns = returns

    @property
    def data(self):
        return self.signature.encode_data(self.args)

    def decode_output(self, output):
        decoded = self.signature.decode_data(output)

        if self.returns:
            if len(self.returns[0]) > 2:
                return {
                    name: handler(value, argc) if handler else value
                    for (name, handler, argc), value
                    in zip(self.returns, decoded)
                }
            else:
                return {
                    name: handler(value) if handler else value
                    for (name, handler), value
                    in zip(self.returns, decoded)
                }  
        else:
            return decoded if len(decoded) > 1 else decoded[0]

    async def __call__(self, args=None):
        args = args or self.args
        calldata = self.signature.encode_data(args)
        output = await self.w3.eth.call({'to': self.target, 'data': calldata}, block_identifier=self.block)
        return self.decode_output(output)

    def explorer_archive_calls(self, args=None):
        args = args or self.args
        calldata = self.signature.encode_data(args)
        print(self.target, args, HexBytes(calldata))
        #output = self.w3.eth.call({'to': self.target, 'data': calldata})
        #return self.decode_output(output)