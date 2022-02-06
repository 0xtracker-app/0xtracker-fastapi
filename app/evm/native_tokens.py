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
    ARB = '0x82af49447d8a07e3bd95bd0d56f35241523fbab1'
    CELO = '0x471EcE3750Da237f93B8E339c536989b8978a438'
    XDAI = '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d'
    HECO = '0x5545153ccfca01fbd7dd11c0b23ba694d9509a6f'
    METER = '0x228ebBeE999c6a7ad74A6130E81b12f9Fe237Ba3'
    CRO = '0x5C7F8A570d578ED84E63fdFA7b1eE72dEae1AE23'
    POLIS = '0x6FC851B8D66116627Fb1137b9D5FE4E2e1BeA978'
    BOBA = '0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000'
    THETA = '0x4dc08b15ea0e10b96c41aec22fab934ba15c983e'
    AURORA = '0xC42C30aC6Cc15faC9bD938618BcaA1a1FaE8501d'
    METIS = '0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000'
    MOONBEAM = '0xAcc15dC74880C9944775448304B263D191c6077F'

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
    ARB = 'AETH'
    CELO = 'CELO'
    XDAI = 'XDAI'
    HECO = 'HT'
    METER = 'MTG'
    CRO = 'CRO'
    POLIS = 'POLIS'
    BOBA = 'ETH'
    THETA = 'TFUEL'
    AURORA = 'ETH'
    METIS = 'METIS'
    MOONBEAM = 'GLMR'

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
    ARB = 18
    CELO = 18
    XDAI = 18
    HECO = 18
    METER = 18
    CRO = 18
    POLIS = 18
    BOBA = 18
    THETA = 18
    AURORA = 24
    METIS = 18
    MOONBEAM = 18

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
    ARB = '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8'
    CELO = '0x64dEFa3544c695db8c535D289d843a189aa26b98'
    XDAI = '0xddafbb505ad214d7b80b1f830fccc89b60fb7a83'
    HECO = '0xa71edc38d189767582c38a3145b5873052c3e47a'
    METER = '0xd86e243fc0007e6226b07c9a50c9d70d78299eb5'
    CRO = '0xc21223249CA28397B4B6541dfFaEcC539BfF0c59'
    POLIS = '0x247123e806a27ea322bfd93e0273d04602dc942d'
    BOBA = '0x66a2A913e447d6b4BF33EFbec43aAeF87890FBbc'
    THETA = '0x3ca3fefa944753b43c751336a5df531bdd6598b6'
    AURORA = '0xB12BFcA5A55806AaF64E99521918A4bf0fC40802'
    METIS = '0xea32a96608495e54156ae48931a7c20f0dcc1a21'
    MOONBEAM = '0x818ec0A7Fe18Ff94269904fCED6AE3DaE6d6dC0b'

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
    ARB = 6
    CELO = 18
    XDAI = 6
    HECO = 18
    METER = 6
    CRO = 6
    POLIS = 18
    BOBA = 6
    THETA = 6
    AURORA = 6
    METIS = 6
    MOONBEAM = 6

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
    ARB = routers.ArbRouter.SUSHI
    CELO = routers.CeloRouter.UBE
    XDAI = routers.DaiRouter.HONEY
    HECO = routers.HecoRouter.MDEX
    METER = routers.MeterRouter.VOLT
    CRO = routers.CroRouter.CRONA
    POLIS = routers.PolisRouter.HADES
    BOBA = routers.BobaRouter.OOLONG
    THETA = routers.ThetaRouter.VOLT
    AURORA = routers.AuroraRouter.TRI
    METIS = routers.MetisRouter.NETSWAP
    MOONBEAM = routers.MoonbeamRouter.STELLA

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
    ARB = routers.ArbRouter
    CELO = routers.CeloRouter
    XDAI = routers.DaiRouter
    HECO = routers.HecoRouter
    METER = routers.MeterRouter
    CRO = routers.CroRouter
    POLIS = routers.PolisRouter
    BOBA = routers.BobaRouter
    THETA = routers.ThetaRouter
    AURORA = routers.AuroraRouter
    METIS = routers.MetisRouter
    MOONBEAM = routers.MoonbeamRouter

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
    ARB = 'arbitrum-one'
    CELO = 'celo'
    XDAI = 'xdai'
    HECO = 'huobi-token'
    METER = ''
    CRO = ''
    POLIS = ''
    BOBA = ''
    THETA = ''
    AURORA = ''
    METIS = ''
    MOONBEAM = ''

class LiqCheck():
    BSC = '0xd6aa1dc078e282ecd8e574b3233eed36dc2837c1'
    MATIC= '0x4c432ec34cee974e2f26163a2950388779b25183'
    FTM = '0x3f0b450c9453c4d49675af2016abe17e08e1f0fb'
    KCC = '0xebb3fb87362a3331a28301a5e282ad9f649c5f0c'
    AVAX = '0xc0bebd9b58d04602e241160ae0f66c843010ceea'
    ETH = '0x97570f38917f2a0063b1f85f920b9e149f7a23ed'
    OKE = '0x3f0b450c9453c4d49675af2016abe17e08e1f0fb'
    HARMONY = '0x6516953017799626f13aad59daa1bccc68a3a247'
    MOON = '0x0C8be7B6864538b7086bF5611aB6940b510749a4'
    ARB = '0x731083adec06c95a3c9ffca54828cb3ea0935e86'
    CELO = '0x6516953017799626f13aAD59dAa1bCCc68A3A247'
    XDAI = '0x6516953017799626f13aAD59dAa1bCCc68A3A247'
    HECO = '0x6204688D31C627423B153486FEe40390A8381a5A'
    METER = '0x3C25ef83448EEBFAb5055040EB58a35f94940E6f'
    CRO = '0x1AA8807dA05C959bdD93025118dB57d8796e3e33'
    POLIS = '0x6516953017799626f13aAD59dAa1bCCc68A3A247'
    BOBA = '0xCf5FA464580Df67E359108B14404EF2204c09842'
    THETA = '0x6516953017799626f13aAD59dAa1bCCc68A3A247'
    AURORA = '0x6516953017799626f13aAD59dAa1bCCc68A3A247'
    METIS = '0x3f0b450c9453c4d49675AF2016ABe17E08E1f0fB'
    MOONBEAM = '0x6ddB0845aeB285eD7ef712768a0E123c8F2Eab0E'

class MinLiq():
    BSC = 49999
    MATIC = 49999
    FTM = 49999
    KCC = 9999
    AVAX = 49999
    ETH = 49999
    OKE = 9999
    HARMONY = 9999
    MOON = 9999
    ARB = 9999
    CELO = 9999
    XDAI = 9999
    HECO = 9999
    METER = 9999
    CRO = 9999
    POLIS = 9999
    BOBA = 9999
    THETA = 9999
    AURORA = 9999
    METIS = 9999
    MOONBEAM = 9999

class YearlyBlocks():
    BSC = 10407920.792079208
    MATIC = 14334545.454545453
    FTM = 35433707.86516854
    KCC = 0
    AVAX = 15768000
    ETH = 2425846.153846154
    OKE = 0
    HARMONY = 15768000
    MOON = 2522880
    ARB = 9010285.714285715
    CELO = 6307200
    XDAI = 0
    HECO = 10512000
    METER = 0
    CRO = 5532631.578947368
    POLIS = 0
    BOBA = 612349.5145631068
    THETA = 0
    AURORA = 0
    METIS = 0
    MOONBEAM = 0


class DeadTokens():
    BSC = ['0x000000000000000000000000000000000000dEaD', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000001', '0x0000000000000000000000000000000000000002', '0x0000000000000000000000000000000000000003', '0x0000000000000000000000000000000000000004', '0x0000000000000000000000000000000000000005']
    MATIC = ['0x000000000000000000000000000000000000dEaD', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000001', '0x0000000000000000000000000000000000000002', '0x0000000000000000000000000000000000000003']
    FTM = ['0x000000000000000000000000000000000000dEaD', '0x0000000000000000000000000000000000000000', '0x0000000000000000000000000000000000000001', '0x0000000000000000000000000000000000000002']
    KCC = []
    AVAX = []
    ETH = ['0x000000000000000000000000000000000000dEaD', '0x0000000000000000000000000000000000000001', '0x0000000000000000000000000000000000000002', '0x0000000000000000000000000000000000000003', '0x0000000000000000000000000000000000000004']
    OKE = []
    HARMONY = ['0x7bdef7bdef7bdef7bdef7bdef7bdef7bdef6e7ad']
    MOON = []
    ARB = []
    CELO = []
    XDAI = ['0x000000000000000000000000000000000000dEaD', '0x0000000000000000000000000000000000000000']
    HECO = []
    METER = []
    CRO = []
    POLIS = []
    BOBA = []
    THETA = []
    AURORA = []
    METIS = []
    MOONBEAM = []

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
        self.liqcheck = getattr(LiqCheck, network.upper())
        self.minliq = getattr(MinLiq, network.upper())
        self.dead = getattr(DeadTokens, network.upper())
        self.bpy = getattr(YearlyBlocks, network.upper())