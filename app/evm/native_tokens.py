from . import routers
from .networks import WEB3_NETWORKS

class NativeToken():
    BSC = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'
    MATIC = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
    FTM = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
    KCC = '0x4446fc4eb47f2f6586f9faab68b3498f86c07521'
    AVAX = '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7'

class StableToken():
    BSC = '0xe9e7cea3dedca5984780bafc599bd69add087d56'
    MATIC = '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'
    FTM = '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3Eb'
    KCC = None
    AVAX = '0xd586E7F844cEa2F87f50152665BCbc2C279D8d70'

class DefaultRouter():
    BSC = routers.BSCRouter.PCS_V2
    MATIC= routers.MATICRouter.QUICKSWAP
    FTM = routers.FTMRouter.SPOOKY
    KCC = routers.KCCRouter.KUSWAP
    AVAX = routers.AVAXRouter.PNG

class RouteClass():
    BSC = routers.BSCRouter
    MATIC= routers.MATICRouter
    FTM = routers.FTMRouter
    KCC = routers.KCCRouter
    AVAX = routers.AVAXRouter

class NetworkRoutes():

    def __init__(self, network=None):
        self.network_conn = WEB3_NETWORKS[network]
        self.native = getattr(NativeToken, network.upper())
        self.stable = getattr(StableToken, network.upper())
        self.default_router = getattr(DefaultRouter, network.upper())
        self.router = getattr(RouteClass, network.upper())
        self.lrouters = [attr for attr in dir(self.router()) if not callable(getattr(self.router(),attr)) and not attr.startswith("__")]
