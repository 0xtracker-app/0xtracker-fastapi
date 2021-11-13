from .oracles import get_price_from_uni3, get_gmx_price, get_price_from_firebird, get_price_from_router, get_price_from_synpool, get_synth_price, get_xboo_price, get_xjoe_price, get_blackswan_lp, coingecko_by_address_network_single, get_ygg_price, return_stable, get_goldbar_price, get_glp_price, get_tranchess_price
from . import routers

class TokenOverride:

    def __init__(self, session=None):
        self.tokens = {
            '0x2c6d91accc5aa38c84653f28a80aec69325bdd12'.lower() : [get_price_from_synpool, {'token_in' : '0x2c6d91accc5aa38c84653f28a80aec69325bdd12','swap_address' : '0xED2a7edd7413021d440b09D654f3b87712abAB66', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'avax'}],
            '0xdd17344f7537df99f212a08f5a5480af9f6c083a'.lower() : [get_price_from_synpool, {'token_in' : '0xdd17344f7537df99f212a08f5a5480af9f6c083a','swap_address' : '0x28ec0B36F0819ecB5005cAB836F4ED5a2eCa4D13', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'bsc'}],
            '0x398a2d1b343d09261df990c2fcc97b5d5d62c1b5'.lower() : [get_price_from_synpool, {'token_in' : '0x398a2d1b343d09261df990c2fcc97b5d5d62c1b5','swap_address' : '0x85fCD7Dd0a1e1A9FCD5FD886ED522dE8221C3EE5', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'matic'}],
            '0x08928492691b64e6fe6ff9dead42f557d20a4a18'.lower() : [get_price_from_synpool, {'token_in' : '0x08928492691b64e6fe6ff9dead42f557d20a4a18','swap_address' : '0x2913E812Cf0dcCA30FB28E6Cac3d2DCFF4497688', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'ftm'}],
            '0xF1FD0b04b9508B7e9498C7bB389D3452Cc008757'.lower() : [get_price_from_synpool, {'token_in' : '0xF1FD0b04b9508B7e9498C7bB389D3452Cc008757','swap_address' : '0x0Db3FE3B770c95A0B99D1Ed6F2627933466c0Dd8', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'arb'}],
            '0x57319d41f71e81f3c65f2a47ca4e001ebafd4f33'.lower() : [get_xjoe_price, {}],
            '0xa48d959AE2E88f1dAA7D5F611E01908106dE7598'.lower() : [get_xboo_price, {}],
            '0x24f6ECAF0B9E99D42413F518812d2c4f3EeFEB12'.lower() : [get_goldbar_price, {}],
            '0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'.lower() : [get_blackswan_lp, {}],
            '0x4277f8F2c384827B5273592FF7CeBd9f2C1ac258'.lower() : [get_glp_price, {}],
            '0x63cf309500d8be0b9fdb8f1fb66c821236c0438c'.lower() : [get_ygg_price, {}],
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
            '0x88a3acac5c48f93121d4d7771a068a1fcde078bc'.lower() : [get_price_from_firebird, {'token_in' : '0x88a3acac5c48f93121d4d7771a068a1fcde078bc', 'token_out' : '0x2791bca1f2de4661ed88a30c99a7a9449aa84174', 'out_d' : 6, 'amount' : 1 * 10 ** 18, 'session' : session}],
            '0x0F83287FF768D1c1e17a42F44d644D7F22e8ee1d'.lower() : [get_synth_price, {'address' : '0x0F83287FF768D1c1e17a42F44d644D7F22e8ee1d', 'aggregator' : '0x7c8719f3683585a242a67c73f6f3c98362004da4', 'network' : 'eth'}],
            '0x31d4eb09a216e181ec8a43ce79226a487d6f0ba9'.lower() : [get_price_from_uni3, {'return_token' : '0x31d4eb09a216e181ec8a43ce79226a487d6f0ba9', 'pool' : '0x7342C20D7F62B4D1a09d5022d883c7a796721443', 'network' : 'eth', 'token_decimals' : [18,6]}],
            '0xCA87BF3ec55372D9540437d7a86a7750B42C02f4'.lower() : [get_price_from_synpool, {'token_in' : '0xCA87BF3ec55372D9540437d7a86a7750B42C02f4','swap_address' : '0xED2a7edd7413021d440b09D654f3b87712abAB66', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'avax'}],
            '0xa4b7Bc06EC817785170C2DbC1dD3ff86CDcdcc4C'.lower() : [get_price_from_synpool, {'token_in' : '0xa4b7Bc06EC817785170C2DbC1dD3ff86CDcdcc4C','swap_address' : '0x28ec0B36F0819ecB5005cAB836F4ED5a2eCa4D13', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'bsc'}],
            '0x7479e1Bc2F2473f9e78c89B4210eb6d55d33b645'.lower() : [get_price_from_synpool, {'token_in' : '0x7479e1Bc2F2473f9e78c89B4210eb6d55d33b645','swap_address' : '0x85fCD7Dd0a1e1A9FCD5FD886ED522dE8221C3EE5', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'matic'}],
            '0x464d121D3cA63cEEfd390D76f19364D3Bd024cD2'.lower() : [get_price_from_synpool, {'token_in' : '0x464d121D3cA63cEEfd390D76f19364D3Bd024cD2','swap_address' : '0x2913E812Cf0dcCA30FB28E6Cac3d2DCFF4497688', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'ftm'}],
            '0xADeac0343C2Ac62DFE5A5f51E896AefFF5Ab513E'.lower() : [get_price_from_synpool, {'token_in' : '0xADeac0343C2Ac62DFE5A5f51E896AefFF5Ab513E','swap_address' : '0x0Db3FE3B770c95A0B99D1Ed6F2627933466c0Dd8', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'arb'}],
}