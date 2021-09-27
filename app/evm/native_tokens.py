from . import routers
from .networks import WEB3_NETWORKS

class NativeToken():
    BSC = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'
    MATIC = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
    FTM = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
    KCC = '0x4446fc4eb47f2f6586f9faab68b3498f86c07521'
    AVAX = '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7'
    ETH = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
    OKE = '0x8f8526dbfd6e38e3d8307702ca8469bae6c56c15'
    HARMONY = '0xcf664087a5bb0237a0bad6742852ec6c8d69a27a'
    MOON = '0x98878B06940aE243284CA214f92Bb71a2b032B8A'

class NativeSymbol():
    BSC = 'BNB'
    MATIC = 'MATIC'
    FTM = 'FTM'
    KCC = 'KCS'
    AVAX = 'AVAX'
    ETH = 'ETH'
    OKE = 'OKT'
    HARMONY = 'ONE'
    MOON = 'MOVR'

class NativeDecimal():
    BSC = 18
    MATIC = 18
    FTM = 18
    KCC = 18
    AVAX = 18
    ETH = 18
    OKE = 18
    HARMONY = 18
    MOON = 18

class StableToken():
    BSC = '0xe9e7cea3dedca5984780bafc599bd69add087d56'
    MATIC = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
    FTM = '0x04068da6c83afcfa0e13ba15a6696662335d5b75'
    KCC = '0x0039f574ee5cc39bdd162e9a88e3eb1f111baf48'
    AVAX = '0xd586E7F844cEa2F87f50152665BCbc2C279D8d70'
    ETH = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
    OKE = '0x382bb369d343125bfb2117af9c149795c6c65c50'
    HARMONY = '0x985458e523db3d53125813ed68c274899e9dfab4'
    MOON = '0xE3F5a90F9cb311505cd691a46596599aA1A0AD7D'

class StableDecimal():
    BSC = 18
    MATIC = 6
    FTM = 6
    KCC = 18
    AVAX = 18
    ETH = 6
    OKE = 18
    HARMONY = 6
    MOON = 6

class DefaultRouter():
    BSC = routers.BSCRouter.PCSV2
    MATIC= routers.MATICRouter.QUICKSWAP
    FTM = routers.FTMRouter.SPOOKY
    KCC = routers.KCCRouter.KUSWAP
    AVAX = routers.AVAXRouter.PNG
    ETH = routers.ETHRouter.UNI
    OKE = routers.OKERouter.CHERRY
    HARMONY = routers.ONERouter.SUSHI
    MOON = routers.MoonRouter.SOLAR

class RouteClass():
    BSC = routers.BSCRouter
    MATIC= routers.MATICRouter
    FTM = routers.FTMRouter
    KCC = routers.KCCRouter
    AVAX = routers.AVAXRouter
    ETH = routers.ETHRouter
    OKE = routers.OKERouter
    HARMONY = routers.ONERouter
    MOON = routers.MoonRouter

class CoinGecko():
    BSC = 'binance-smart-chain'
    MATIC= 'polygon-pos'
    FTM = 'fantom'
    KCC = 'kucoin-community-chain'
    AVAX = 'avalanche'
    ETH = 'ethereum'
    OKE = 'okex-chain'
    HARMONY = 'harmony-shard-0'
    MOON = ''


class NetworkRoutes():

    def __init__(self, network=None):
        self.network_conn = WEB3_NETWORKS[network]
        self.native = getattr(NativeToken, network.upper())
        self.snative = getattr(NativeSymbol, network.upper())
        self.dnative = getattr(NativeDecimal, network.upper())
        self.stable = getattr(StableToken, network.upper())
        self.dstable = getattr(StableDecimal, network.upper())
        self.default_router = getattr(DefaultRouter, network.upper())
        self.router = getattr(RouteClass, network.upper())
        self.lrouters = [attr for attr in dir(self.router()) if not callable(getattr(self.router(),attr)) and not attr.startswith("__")]
        self.coingecko = getattr(CoinGecko, network.upper())
