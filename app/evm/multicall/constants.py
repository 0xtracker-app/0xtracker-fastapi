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
    CRO = 25
    Polis = 333999
    BOBA = 288
    Theta = 361
    Aurora = 1313161554
    Metis = 1088
    Moonbeam = 1284
    Fuse = 122
    Iotex = 4689
    Elastos = 20
    Velas = 106
    SmartBCH = 10000
    Oasis = 42262
    Telos = 40
    RSK = 30
    Astar = 592
    DFK = 53935


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
    Network.Optimism: '0x6ddB0845aeB285eD7ef712768a0E123c8F2Eab0E',
    Network.OKE: '0x6ddB0845aeB285eD7ef712768a0E123c8F2Eab0E',
    Network.ONE: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.AVAX: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.MOON: '0x97570F38917f2A0063b1f85F920B9e149f7a23ed',
    Network.Arbitrum: '0xCf5FA464580Df67E359108B14404EF2204c09842',
    Network.HECO : '0xbaB1DcfE955DFf2Fa0E84419C2d7580Ab926f0F1',
    Network.CELO : '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.Meter: '0x5ECCA15021828115800A933D467C4A1b20c84737',
    Network.CRO: '0x6516953017799626f13aAD59dAa1bCCc68A3A247',
    Network.Polis: '0x1AA8807dA05C959bdD93025118dB57d8796e3e33',
    Network.BOBA: '0x0C8be7B6864538b7086bF5611aB6940b510749a4',
    Network.Theta: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.Aurora: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.Metis: '0x6ddB0845aeB285eD7ef712768a0E123c8F2Eab0E',
    Network.Moonbeam: '0x1AA8807dA05C959bdD93025118dB57d8796e3e33',
    Network.Fuse: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.Iotex: '0xebb3Fb87362A3331a28301A5e282Ad9f649c5f0c',
    Network.Elastos: '0xebb3Fb87362A3331a28301A5e282Ad9f649c5f0c',
    Network.Velas: '0x6516953017799626f13aAD59dAa1bCCc68A3A247',
    Network.SmartBCH: '0x12AB889eb2886d76BC609f930D4DCb759E515bfc',
    Network.Oasis: '0x6516953017799626f13aAD59dAa1bCCc68A3A247',
    Network.Telos: '0x1AA8807dA05C959bdD93025118dB57d8796e3e33',
    Network.RSK: '0x1AA8807dA05C959bdD93025118dB57d8796e3e33',
    Network.Astar: '0x6ddB0845aeB285eD7ef712768a0E123c8F2Eab0E',
    Network.DFK: '0x5b24224dC16508DAD755756639E420817DD4c99E'
}
