from enum import IntEnum


class Network(IntEnum):
    Mainnet = 1
    Kovan = 42
    Rinkeby = 4
    Görli = 5
    xDai = 100
    BSC = 56
    Matic = 137
    Fantom = 250
    KCC = 321
    Optimism = 10
    OKE = 66
    ONE = 1666600000
    AVAX = 43114
    MOON = 1285
    Arbitrum = 42161
    HECO = 128
    CELO = 42220
    Meter = 82


MULTICALL_ADDRESSES = {
    Network.Mainnet: '0x5eb3fa2dfecdde21c950813c665e9364fa609bd2',
    Network.Kovan: '0x2cc8688C5f75E365aaEEb4ea8D6a480405A48D2A',
    Network.Rinkeby: '0x42Ad527de7d4e9d9d011aC45B31D8551f8Fe9821',
    Network.Görli: '0x77dCa2C955b15e9dE4dbBCf1246B4B85b651e50e',
    Network.xDai: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.BSC: '0x6Cf63cC81660Dd174A49e0C61A1f916456Ee1471',
    Network.Matic: '0x8a233a018a2e123c0D96435CF99c8e65648b429F',
    Network.Fantom: '0x08AB4aa09F43cF2D45046870170dd75AE6FBa306',
    Network.KCC: '0x08ab4aa09f43cf2d45046870170dd75ae6fba306',
    Network.Optimism: '',
    Network.OKE: '0x6ddB0845aeB285eD7ef712768a0E123c8F2Eab0E',
    Network.ONE: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.AVAX: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.MOON: '0x97570F38917f2A0063b1f85F920B9e149f7a23ed',
    Network.Arbitrum: '0xCf5FA464580Df67E359108B14404EF2204c09842',
    Network.HECO : '0xbaB1DcfE955DFf2Fa0E84419C2d7580Ab926f0F1',
    Network.CELO : '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.Meter: '0x5ECCA15021828115800A933D467C4A1b20c84737'

}
