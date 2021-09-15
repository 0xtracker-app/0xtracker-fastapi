from .oracles import get_price_from_router, get_price_from_synpool, get_xjoe_price, get_blackswan_lp
from . import routers

tokens = {
    # '0x10a520829c1e9631ef9e60e37eea3916092caa99'.lower() : [get_price_from_router, {'token_in' : '0x10a520829c1e9631ef9e60e37eea3916092caa99', 'network' : 'bsc', 'router' : routers.BSCRouter.ARBX, 'native' : True}],
    # '0x818cee824f8caeaa05fb6a1f195935e364d52af0'.lower() : [get_price_from_router, {'token_in' : '0x818cee824f8caeaa05fb6a1f195935e364d52af0', 'network' : 'bsc', 'router' : routers.BSCRouter.SHIBCAKE, 'native' : True}],
    '0x2c6d91accc5aa38c84653f28a80aec69325bdd12'.lower() : [get_price_from_synpool, {'token_in' : '0x2c6d91accc5aa38c84653f28a80aec69325bdd12','swap_address' : '0xf44938b0125a6662f9536281ad2cd6c499f22004', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'avax'}],
    '0xdd17344f7537df99f212a08f5a5480af9f6c083a'.lower() : [get_price_from_synpool, {'token_in' : '0xdd17344f7537df99f212a08f5a5480af9f6c083a','swap_address' : '0x930d001b7efb225613ac7f35911c52ac9e111fa9', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'bsc'}],
    '0x398a2d1b343d09261df990c2fcc97b5d5d62c1b5'.lower() : [get_price_from_synpool, {'token_in' : '0x398a2d1b343d09261df990c2fcc97b5d5d62c1b5','swap_address' : '0x96cf323E477Ec1E17A4197Bdcc6f72Bb2502756a', 'token_out_index' : 0, 'decimal' : 18, 'network' : 'matic'}],
    '0x57319d41f71e81f3c65f2a47ca4e001ebafd4f33'.lower() : [get_xjoe_price, {}],
    # '0x56e344be9a7a7a1d27c854628483efd67c11214f'.lower() : [get_price_from_router, {'token_in' : '0x56e344be9a7a7a1d27c854628483efd67c11214f', 'network' : 'bsc', 'router' : routers.BSCRouter.SHIB, 'native' : True}],
    # '0xa649325aa7c5093d12d6f98eb4378deae68ce23f'.lower() : [get_price_from_router, {'token_in' : '0xa649325aa7c5093d12d6f98eb4378deae68ce23f', 'network' : 'matic', 'router' : routers.MATICRouter.APESWAP, 'native' : True}],
    # '0x2c449ba613873e7b980faf2b686207d7bd205541'.lower() : [get_price_from_router, {'token_in' : '0x2c449ba613873e7b980faf2b686207d7bd205541', 'network' : 'bsc', 'router' : routers.BSCRouter.COBRA, 'native' : True}],
    # '0xb5389a679151c4b8621b1098c6e0961a3cfee8d4'.lower() : [get_price_from_router, {'token_in' : '0xb5389a679151c4b8621b1098c6e0961a3cfee8d4', 'network' : 'bsc', 'router' : routers.BSCRouter.PCS_V2, 'native' : True}],
    # '0xc623d9e8bf6812852a7aeded140d479095cfd941'.lower() : [get_price_from_router, {'token_in' : '0xc623d9e8bf6812852a7aeded140d479095cfd941', 'network' : 'bsc', 'router' : routers.BSCRouter.PCS_V2, 'native' : True}],
    # '0x7d5bc7796fd62a9a27421198fc3c349b96cdd9dc'.lower() : [get_price_from_router, {'token_in' : '0x7d5bc7796fd62a9a27421198fc3c349b96cdd9dc', 'network' : 'bsc', 'router' : routers.BSCRouter.MELSWAP}],
    '0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'.lower() : [get_blackswan_lp, {}],
    '0xd016caae879c42cb0d74bb1a265021bf980a7e96'.lower() : [get_price_from_router, {'token_in' : '0xd016caae879c42cb0d74bb1a265021bf980a7e96', 'network' : 'matic', 'router' : routers.MATICRouter.APESWAP, 'native' : True, 'bypass_token' : '0x7ceb23fd6bc0add59e62ac25578270cff1b9f619'}],
    '0xddb3bd8645775f59496c821e4f55a7ea6a6dc299'.lower() : [get_price_from_router, {'token_in' : '0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95', 'network' : 'bsc', 'router' : routers.BSCRouter.APESWAP, 'native' : True}],
    # '0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25'.lower() : [get_price_from_router, {'token_in' : '0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25', 'network' : 'matic', 'router' : routers.MATICRouter.JETSWAP, 'native' : True}],
    # '0x72b7d61e8fc8cf971960dd9cfa59b8c829d91991'.lower() : [get_price_from_router, {'token_in' : '0x72b7d61e8fc8cf971960dd9cfa59b8c829d91991', 'network' : 'bsc', 'router' : routers.BSCRouter.PLANET, 'native' : True}],
    # '0x63041a8770c4cfe8193d784f3dc7826eab5b7fd2'.lower() : [get_price_from_router, {'token_in' : '0x63041a8770c4cfe8193d784f3dc7826eab5b7fd2', 'network' : 'bsc', 'router' : routers.BSCRouter.WSWAP, 'native' : True}],
    # '0xcd734b1f9b0b976ddc46e507d0aa51a4216a1e98'.lower() : [get_price_from_router, {'token_in' : '0xcd734b1f9b0b976ddc46e507d0aa51a4216a1e98', 'network' : 'bsc', 'router' : routers.BSCRouter.PCS_V2, 'native' : True}],
    # '0x76bf0c28e604cc3fe9967c83b3c3f31c213cfe64'.lower() : [get_price_from_router, {'token_in' : '0x76bf0c28e604cc3fe9967c83b3c3f31c213cfe64', 'network' : 'matic', 'router' : routers.MATICRouter.APESWAP, 'native' : True}],
    # '0x1f546ad641b56b86fd9dceac473d1c7a357276b7'.lower() : [get_price_from_router, {'token_in' : '0x1f546ad641b56b86fd9dceac473d1c7a357276b7', 'network' : 'bsc', 'router' : routers.BSCRouter.PANTHER, 'native' : True}],
    # '0xdd97ab35e3c0820215bc85a395e13671d84ccba2'.lower() : [get_price_from_router, {'token_in' : '0xdd97ab35e3c0820215bc85a395e13671d84ccba2', 'network' : 'bsc', 'router' : routers.BSCRouter.AUTOSHARK, 'native' : True}],
    # '0xd78C475133731CD54daDCb430F7aAE4F03C1E660'.lower() : [get_price_from_router, {'token_in' : '0xd78C475133731CD54daDCb430F7aAE4F03C1E660', 'network' : 'matic', 'router' : routers.MATICRouter.FIREBIRD, 'native' : True}],
    # '0x965f527d9159dce6288a2219db51fc6eef120dd1'.lower() : [get_price_from_router, {'token_in' : '0x965f527d9159dce6288a2219db51fc6eef120dd1', 'network' : 'bsc', 'router' : routers.BSCRouter.BISWAP, 'native' : True}],
    # '0x0487b824c8261462f88940f97053e65bdb498446'.lower() : [get_price_from_router, {'token_in' : '0x0487b824c8261462f88940f97053e65bdb498446', 'network' : 'bsc', 'router' : routers.BSCRouter.JETSWAP, 'native' : True}],
    # '0xef6f50fe05f4ead7805835fd1594406d31b96ed8'.lower() : [get_price_from_router, {'token_in' : '0xef6f50fe05f4ead7805835fd1594406d31b96ed8', 'network' : 'bsc', 'router' : routers.BSCRouter.PCS_V2, 'native' : True}],
    # '0x62ee12e4fe74a815302750913c3c796bca23e40e'.lower() : [get_price_from_router, {'token_in' : '0x62ee12e4fe74a815302750913c3c796bca23e40e', 'network' : 'bsc', 'router' : routers.BSCRouter.PCS_V1, 'native' : True}],
    # '0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4'.lower() : [get_price_from_router, {'token_in' : '0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4', 'network' : 'matic', 'router' : routers.MATICRouter.DFYN, 'native' : True}],
    # '0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90'.lower() : [get_price_from_router, {'token_in' : '0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90', 'network' : 'bsc', 'router' : routers.BSCRouter.WSWAP, 'native' : True}],
    # '0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21'.lower() : [get_price_from_router, {'token_in' : '0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21', 'network' : 'bsc', 'router' : routers.BSCRouter.WSWAP, 'native' : True}],
    '0xe304ff0983922787Fd84BC9170CD21bF78B16B10'.lower() : [get_price_from_router, {'token_in' : '0xe304ff0983922787Fd84BC9170CD21bF78B16B10', 'network' : 'bsc', 'router' : routers.BSCRouter.PCS_V2, 'token_out' : '0x85E76cbf4893c1fbcB34dCF1239A91CE2A4CF5a7'}],
}