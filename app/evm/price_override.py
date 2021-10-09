from .oracles import get_gmx_price, get_price_from_router, get_price_from_synpool, get_xboo_price, get_xjoe_price, get_blackswan_lp, coingecko_by_address_network_single, return_stable, get_goldbar_price, get_glp_price, get_tranchess_price
from . import routers

class TokenOverride:

    def __init__(self, session=None):
        self.tokens = {
            '0x2c6d91accc5aa38c84653f28a80aec69325bdd12'.lower() : [get_price_from_synpool, {'token_in' : '0x2c6d91accc5aa38c84653f28a80aec69325bdd12','swap_address' : '0xf44938b0125a6662f9536281ad2cd6c499f22004', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'avax'}],
            '0xdd17344f7537df99f212a08f5a5480af9f6c083a'.lower() : [get_price_from_synpool, {'token_in' : '0xdd17344f7537df99f212a08f5a5480af9f6c083a','swap_address' : '0x930d001b7efb225613ac7f35911c52ac9e111fa9', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'bsc'}],
            '0x398a2d1b343d09261df990c2fcc97b5d5d62c1b5'.lower() : [get_price_from_synpool, {'token_in' : '0x398a2d1b343d09261df990c2fcc97b5d5d62c1b5','swap_address' : '0x96cf323E477Ec1E17A4197Bdcc6f72Bb2502756a', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'matic'}],
            '0x08928492691b64e6fe6ff9dead42f557d20a4a18'.lower() : [get_price_from_synpool, {'token_in' : '0x08928492691b64e6fe6ff9dead42f557d20a4a18','swap_address' : '0x1f6A0656Ff5061930076bf0386b02091e0839F9f', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'ftm'}],
            '0x57319d41f71e81f3c65f2a47ca4e001ebafd4f33'.lower() : [get_xjoe_price, {}],
            '0xa48d959AE2E88f1dAA7D5F611E01908106dE7598'.lower() : [get_xboo_price, {}],
            '0x24f6ECAF0B9E99D42413F518812d2c4f3EeFEB12'.lower() : [get_goldbar_price, {}],
            '0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'.lower() : [get_blackswan_lp, {}],
            '0x4277f8F2c384827B5273592FF7CeBd9f2C1ac258'.lower() : [get_glp_price, {}],
            '0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a'.lower() : [get_gmx_price, {'return_token' : '0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a'}],
            '0xf42Ae1D54fd613C9bb14810b0588FaAa09a426cA'.lower() : [get_gmx_price, {'return_token' : '0xf42Ae1D54fd613C9bb14810b0588FaAa09a426cA'}],
            '0xc581b735a1688071a1746c968e0798d642ede491'.lower() : [return_stable, {'token_in' : '0xc581b735a1688071a1746c968e0798d642ede491'}],
            '0xd016caae879c42cb0d74bb1a265021bf980a7e96'.lower() : [get_price_from_router, {'token_in' : '0xd016caae879c42cb0d74bb1a265021bf980a7e96', 'network' : 'matic', 'router' : routers.MATICRouter.APESWAP, 'native' : True, 'bypass_token' : '0x7ceb23fd6bc0add59e62ac25578270cff1b9f619'}],
            '0xddb3bd8645775f59496c821e4f55a7ea6a6dc299'.lower() : [get_price_from_router, {'token_in' : '0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95', 'network' : 'bsc', 'router' : routers.BSCRouter.APESWAP, 'native' : True}],
            '0x080f6aed32fc474dd5717105dba5ea57268f46eb'.lower() : [get_price_from_router, {'token_in' : '0x0f2d719407fdbeff09d87557abb7232601fd9f29', 'network' : 'eth', 'router' : routers.ETHRouter.UNI, 'native' : True, 'return_token' : '0x080f6aed32fc474dd5717105dba5ea57268f46eb'}],
            '0xe55e19fb4f2d85af758950957714292dac1e25b2'.lower() : [get_price_from_router, {'token_in' : '0x0f2d719407fdbeff09d87557abb7232601fd9f29', 'network' : 'eth', 'router' : routers.ETHRouter.UNI, 'native' : True, 'return_token' : '0xe55e19fb4f2d85af758950957714292dac1e25b2'}],
            '0xe304ff0983922787Fd84BC9170CD21bF78B16B10'.lower() : [get_price_from_router, {'token_in' : '0xe304ff0983922787Fd84BC9170CD21bF78B16B10', 'network' : 'bsc', 'router' : routers.BSCRouter.PCSV2, 'token_out' : '0x85E76cbf4893c1fbcB34dCF1239A91CE2A4CF5a7'}],
            '0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4'.lower() : [coingecko_by_address_network_single, {'address' : '0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4', 'network' : 'polygon-pos', 'session' : session}],
            '0x15d0318fddf785ac0d3ba690c0033b3bedf4c648'.lower() : [get_tranchess_price, {'address' : '0x15d0318fddf785ac0d3ba690c0033b3bedf4c648', 'tranch' : 'trancheM', 'session' : session}],
            '0x8cc456b384c8ad06bf430f4f130aa63ef0dc6f85'.lower() : [get_tranchess_price, {'address' : '0x8cc456b384c8ad06bf430f4f130aa63ef0dc6f85', 'tranch' : 'trancheA', 'session' : session}],
            '0x80da8ca6c3dabd3a9f06ca8eeed5d61687fab7ef'.lower() : [get_tranchess_price, {'address' : '0x80da8ca6c3dabd3a9f06ca8eeed5d61687fab7ef', 'tranch' : 'trancheB', 'session' : session}],

}