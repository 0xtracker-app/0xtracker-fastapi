import evm.routers as routers

class NativeToken():
    BSC = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'
    MATIC = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
    FTM = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
    KCC = '0x4446fc4eb47f2f6586f9faab68b3498f86c07521'

class StableToken():
    BSC = '0xe9e7cea3dedca5984780bafc599bd69add087d56'
    MATIC = '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'
    FTM = '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3Eb'
    KCC = None

class DefaultRouter():
    BSC = routers.BSCRouter.PCS_V2
    MATIC= routers.MATICRouter.QUICKSWAP
    FTM = routers.FTMRouter.SPOOKY
    KCC = routers.KCCRouter.KUSWAP