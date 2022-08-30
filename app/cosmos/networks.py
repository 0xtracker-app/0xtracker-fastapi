import bech32

def from_atom(atom_addr, network):
    atom_tuple = bech32.bech32_decode(atom_addr)
    data = atom_tuple[1]
    network_addr = bech32.bech32_encode(network,data)    
    return network_addr

class CosmosNetwork:

    def __init__(self, wallet=None):
        self.cosmos_wallet = wallet
        self.supported_networks = ['genesis', 'axelar', 'mantle', 'evmos', 'meme','crescent', 'konstellation', 'cheqd', 'dig' ,'stargaze','osmosis', 'cosmos', 'akash', 'regen', 'sentinel', 'persist', 'iris', 'crypto', 'iov', 'secret', 'sif', 'chihuahua', 'comdex', 'lum', 'desmos', 'bostrom', 'emoney', 'juno', 'kava', 'fetchai']
        self.network_wallet = ''
        self.network_config = {}
        self.all_networks = {
            'osmosis': {
                'wallet': from_atom(wallet, 'osmo'),
                'rpc': 'https://rpc-osmosis.keplr.app',
                'rest': 'https://rest-osmosis.ecostake.com',
                #            'rest' : 'https://lcd-osmosis.cosmostation.io',
                'chain_id': 'osmosis-1',
                'chain_name': 'Osmosis',
                'explorer': 'https://www.mintscan.io/osmosis/txs/',
                'bech_prefix': 'osmo',
                'stake_token': {
                    'denom': 'uosmo',
                    'symbol': 'OSMO',
                    'decimals': 6,
                    'coin_gecko_id': 'osmosis'
                }
            },
            'cosmos': {
                'wallet': from_atom(wallet, 'cosmos'),
                'rpc': 'https://rpc-cosmoshub.keplr.app',
                'rest': 'https://cosmos-lcd.quickapi.com',
                'chain_id': 'cosmoshub-4',
                'chain_name': 'Cosmos Hub',
                'explorer': 'https://www.mintscan.io/cosmos/txs/',
                'bech_prefix': 'cosmos',
                'stake_token': {
                    'denom': 'uatom',
                    'symbol': 'ATOM',
                    'decimals': 6,
                    'coin_gecko_id': 'cosmos'
                }
            },
            'akash': {
                'wallet': from_atom(wallet, 'akash'),
                'rpc': 'https://rpc-akash.keplr.app',
                'rest': 'https://lcd-akash.cosmostation.io',
                'chain_id': 'akashnet-2',
                'chain_name': 'Akash',
                'explorer': 'https://www.mintscan.io/akash/txs/',
                'bech_prefix': 'akash',
                'stake_token': {
                    'denom': 'uakt',
                    'symbol': 'AKT',
                    'decimals': 6,
                    'coin_gecko_id': 'akash-network'
                }
            },
            'regen': {
                'wallet': from_atom(wallet, 'regen'),
                'rpc': 'https://rpc-regen.keplr.app',
                'rest': 'https://lcd-regen.keplr.app',
                'chain_id': 'regen-1',
                'chain_name': 'Regen Network',
                'explorer': 'https://regen.aneka.io/txs/',
                'bech_prefix': 'regen',
                'stake_token': {
                    'denom': 'uregen',
                    'symbol': 'REGEN',
                    'decimals': 6,
                    'coin_gecko_id': 'regen'
                }
            },
            'sentinel': {
                'wallet': from_atom(wallet, 'sent'),
                'rpc': 'https://rpc-sentinel.keplr.app',
                'rest': 'https://lcd-sentinel.cosmostation.io',
                'chain_id': 'sentinelhub-2',
                'chain_name': 'Sentinel',
                'explorer': 'https://www.mintscan.io/sentinel/txs/',
                'bech_prefix': 'sent',
                'stake_token': {
                    'denom': 'udvpn',
                    'symbol': 'DVPN',
                    'decimals': 6,
                    'coin_gecko_id': 'sentinel'
                }
            },
            'persist': {
                'wallet': from_atom(wallet, 'persistence'),
                'rpc': 'https://rpc-persistence.keplr.app',
                'rest': 'https://lcd-persistence.keplr.app',
                'chain_id': 'core-1',
                'chain_name': 'Persistence',
                'explorer': 'https://www.mintscan.io/persistence/txs/',
                'bech_prefix': 'persistence',
                'stake_token': {
                    'denom': 'uxprt',
                    'symbol': 'XPRT',
                    'decimals': 6,
                    'coin_gecko_id': 'persistence'
                }
            },
            'iris': {
                'wallet': from_atom(wallet, 'iaa'),
                'rpc': 'https://rpc-iris.keplr.app',
                'rest': 'https://api-irisnet-ia.notional.ventures',
                'chain_id': 'irishub-1',
                'chain_name': 'IRISnet',
                'explorer': 'https://www.mintscan.io/iris/txs/',
                'bech_prefix': 'iaa',
                'stake_token': {
                    'denom': 'uiris',
                    'symbol': 'IRIS',
                    'decimals': 6,
                    'coin_gecko_id': 'iris-network'
                }
            },
            'crypto': {
                'wallet': from_atom(wallet, 'cro'),
                'rpc': 'https://rpc-crypto-org.keplr.app',
                'rest': 'https://lcd-crypto-org.keplr.app',
                'chain_id': 'crypto-org-chain-mainnet-1',
                'chain_name': 'Crypto.org',
                'explorer': 'https://www.mintscan.io/crypto-org/txs/',
                'bech_prefix': 'cro',
                'stake_token': {
                    'denom': 'basecro',
                    'symbol': 'CRO',
                    'decimals': 8,
                    'coin_gecko_id': 'crypto-com-chain'
                }
            },
            'iov': {
                'wallet': from_atom(wallet, 'star'),
                'rpc': 'https://rpc-iov.keplr.app',
                'rest': 'https://lcd-iov.keplr.app',
                'chain_id': 'iov-mainnet-ibc',
                'chain_name': 'Starname',
                'explorer': 'https://www.mintscan.io/starname/txs/',
                'bech_prefix': 'star',
                'stake_token': {
                    'denom': 'uiov',
                    'symbol': 'IOV',
                    'decimals': 6,
                    'coin_gecko_id': 'starname'
                }
            },
            'juno': {
                'wallet': from_atom(wallet, 'juno'),
                'rpc': 'https://rpc.juno.pupmos.network',
                'rest': 'https://api.juno.pupmos.network',
                'chain_id': 'juno-1',
                'chain_name': 'Juno Mainnet',
                'explorer': 'https://www.mintscan.io/juno',
                'bech_prefix': 'juno',
                'stake_token': {
                    'denom': 'ujuno',
                    'symbol': 'JUNO',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
            'terra': {
                'wallet': from_atom(wallet, 'terra'),
                'rpc': 'https://rpc-columbus.keplr.app',
                'rest': 'https://lcd-columbus.keplr.app',
                'chain_id': 'columbus-5',
                'chain_name': 'Terra',
                'explorer': 'https://finder.terra.money/columbus-5/',
                'bech_prefix': 'terra',
                'stake_token': {
                    'denom': 'uluna',
                    'symbol': 'LUNA',
                    'decimals': 6,
                    'coin_gecko_id': 'terra-luna'
                }
            },
            'bitcanna': {
                'wallet': from_atom(wallet, 'bcna'),
                'rpc': 'https://rpc.bitcanna.io',
                'rest': 'https://lcd.bitcanna.io',
                'chain_id': 'bitcanna-1',
                'chain_name': 'BitCanna',
                'explorer': 'https://www.mintscan.io/bitcanna/txs/',
                'bech_prefix': 'bcna',
                'stake_token': {
                    'denom': 'ubcna',
                    'symbol': 'BCNA',
                    'decimals': 6,
                    'coin_gecko_id': 'bitcanna'
                }
            },
            'bitsong': {
                'wallet': from_atom(wallet, 'bitsong'),
                'rpc': 'https://rpc.explorebitsong.com',
                'rest': 'https://lcd.explorebitsong.com',
                'chain_id': 'bitsong-2b',
                'chain_name': 'BitSong',
                'explorer': 'https://explorebitsong.com/transactions/',
                'bech_prefix': 'bitsong',
                'stake_token': {
                    'denom': 'ubtsg',
                    'symbol': 'BTSG',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:ubtsg'
                }
            },
            'secret': {
                'wallet': from_atom(wallet, 'secret'),
                'rpc': 'https://rpc-secret.keplr.app',
                'rest': 'https://lcd-secret.keplr.app',
                'chain_id': 'secret-4',
                'chain_name': 'Secret Network',
                'explorer': 'https://secretnodes.com/secret/chains/secret-4/transactions/',
                'bech_prefix': 'secret',
                'stake_token': {
                    'denom': 'uscrt',
                    'symbol': 'SCRT',
                    'decimals': 6,
                    'coin_gecko_id': 'secret'
                }
            },
            'sif': {
                'wallet': from_atom(wallet, 'sif'),
                'rpc': 'https://rpc-sifchain.keplr.app',
                'rest': 'https://lcd-sifchain.keplr.app',
                'chain_id': 'sifchain-1',
                'chain_name': 'Sifchain',
                'explorer': 'https://secretnodes.com/secret/chains/secret-4/transactions/',
                'bech_prefix': 'sif',
                'stake_token': {
                    'denom': 'rowan',
                    'symbol': 'ROWAN',
                    'decimals': 18,
                    'coin_gecko_id': 'sifchain'
                }
            },
            'chihuahua': {
                'wallet': from_atom(wallet, 'chihuahua'),
                'rpc': 'https://rpc.chihuahua.wtf',
                'rest': 'https://api-chihuahua-ia.notional.ventures',
                'chain_id': 'chihuahua-1',
                'chain_name': 'Chihuahua',
                'explorer': 'https://www.mintscan.io/chihuahua',
                'bech_prefix': 'chihuahua',
                'stake_token': {
                    'denom': 'uhuahua',
                    'symbol': 'HUAHUA',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:uhuahua'
                }
            },
            'comdex': {
                'wallet': from_atom(wallet, 'comdex'),
                'rpc': 'https://rpc.comdex.one',
                'rest': 'https://rest.comdex.one',
                'chain_id': 'comdex-1',
                'chain_name': 'Comdex',
                'explorer': 'https://www.mintscan.io/comdex/txs/',
                'bech_prefix': 'comdex',
                'stake_token': {
                    'denom': 'ucmdx',
                    'symbol': 'CMDX',
                    'decimals': 6,
                    'coin_gecko_id': 'comdex'
                }
            },
            'lum': {
                'wallet': from_atom(wallet, 'lum'),
                'rpc': 'https://node0.mainnet.lum.network/rpc',
                'rest': 'https://lcd-lum.cosmostation.io',
                'chain_id': 'lum-network-1',
                'chain_name': 'Lum Network',
                'explorer': 'https://www.mintscan.io/lum/txs',
                'bech_prefix': 'lum',
                'stake_token': {
                    'denom': 'ulum',
                    'symbol': 'LUM',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:ulum'
                }
            },
            'stargaze': {
                'wallet': from_atom(wallet, 'stars'),
                'rpc': 'https://rpc.stargaze.publicawesome.dev',
                'rest': 'https://lcd-stargaze.cosmostation.io',
                'chain_id': 'stargaze-1',
                'chain_name': 'Stargaze',
                'explorer': 'https://www.mintscan.io/stargaze/txs',
                'bech_prefix': 'stars',
                'stake_token': {
                    'denom': 'ustars',
                    'symbol': 'STARS',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:ustars'
                }
            },
            'desmos': {
                'wallet': from_atom(wallet, 'desmos'),
                'rpc': 'https://rpc.mainnet.desmos.network',
                'rest': 'https://api.mainnet.desmos.network',
                'chain_id': 'desmos-1',
                'chain_name': 'Desmos',
                'explorer': 'https://www.mintscan.io/desmos/txs',
                'bech_prefix': 'desmos',
                'stake_token': {
                    'denom': 'udsm',
                    'symbol': 'DSM',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:ustars'
                }
            },
            'bostrom': {
                'wallet': from_atom(wallet, 'bostrom'),
                'rpc': 'https://rpc.bostrom.cybernode.ai',
                'rest': 'https://lcd.bostrom.cybernode.ai',
                'chain_id': 'bostrom',
                'chain_name': 'Bostrom',
                'explorer': 'https://cyb.ai/network/bostrom/tx',
                'bech_prefix': 'bostrom',
                'stake_token': {
                    'denom': 'boot',
                    'symbol': 'BOOT',
                    'decimals': 0,
                    'coin_gecko_id': 'pool:boot'
                }
            },
            'emoney': {
                'wallet': from_atom(wallet, 'emoney'),
                'rpc': 'https://rpc-emoney.keplr.app',
                'rest': 'https://lcd-emoney.keplr.app',
                'chain_id': 'emoney-3',
                'chain_name': 'e-Money',
                'explorer': 'https://www.mintscan.io/emoney',
                'bech_prefix': 'emoney',
                'stake_token': {
                    'denom': 'ungm',
                    'symbol': 'NGM',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:boot'
                }
            },
            'kava': {
                'wallet': from_atom(wallet, 'kava'),
                'rpc': 'https://rpc-kava.cosmostation.io',
                'rest': 'https://lcd-kava.cosmostation.io',
                'chain_id': 'kava-7',
                'chain_name': 'kava',
                'explorer': 'https://www.mintscan.io/emoney',
                'bech_prefix': 'kava',
                'stake_token': {
                    'denom': 'ukava',
                    'symbol': 'KAVA',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:boot'
                }
            },
            'dig': {
                'wallet': from_atom(wallet, 'dig'),
                'rpc': 'https://rpc-1-dig.notional.ventures',
                'rest': 'https://api-1-dig.notional.ventures',
                'chain_id': 'dig-1',
                'chain_name': 'Dig',
                'explorer': 'https://ping.pub/dig/tx/',
                'bech_prefix': 'dig',
                'stake_token': {
                    'denom': 'udig',
                    'symbol': 'DIG',
                    'decimals': 6,
                    'coin_gecko_id': 'pool:udig'
                }
            },
            'fetchai': {
                'wallet': from_atom(wallet, 'fetch'),
                'rpc': 'https://rpc-fetchai.cosmostation.io',
                'rest': 'https://lcd-fetchai.cosmostation.io',
                'chain_id': 'fetchhub-3',
                'chain_name': 'fetch.ai',
                'explorer': 'https://ping.pub/dig/tx/',
                'bech_prefix': 'fetch',
                'stake_token': {
                    'denom': 'afet',
                    'symbol': 'FET',
                    'decimals': 18,
                    'coin_gecko_id': 'fetch-ai'
                }
            },
            'cheqd': {
                'wallet': from_atom(wallet, 'cheqd'),
                'rpc': 'https://rpc.cheqd.net',
                'rest': 'https://api.cheqd.net',
                'chain_id': 'cheqd-mainnet-1',
                'chain_name': 'cheqd',
                'explorer': 'https://ping.pub/dig/tx/',
                'bech_prefix': 'cheqd',
                'stake_token': {
                    'denom': 'ncheq',
                    'symbol': 'CHEQ',
                    'decimals': 9,
                    'coin_gecko_id': ''
                }
            },
            'konstellation': {
                'wallet': from_atom(wallet, 'darc'),
                'rpc': 'https://node1.konstellation.tech:26657',
                'rest': 'https://lcd-konstellation.cosmostation.io',
                'chain_id': 'darchub',
                'chain_name': 'konstellation',
                'explorer': 'https://www.mintscan.io/konstellation/',
                'bech_prefix': 'darc',
                'stake_token': {
                    'denom': 'udarc',
                    'symbol': 'DARC',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
            'crescent': {
                'wallet': from_atom(wallet, 'cre'),
                'rpc': '',
                'rest': 'https://crescent-api.polkachu.com',
                'chain_id': 'crescent-1',
                'chain_name': 'crescent',
                'explorer': 'https://www.mintscan.io/crescent/',
                'bech_prefix': 'cre',
                'stake_token': {
                    'denom': 'ucre',
                    'symbol': 'CRE',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
            'meme': {
                'wallet': from_atom(wallet, 'meme'),
                'rpc': 'https://rpc-meme-1.meme.sx',
                'rest': 'https://api-meme-1.meme.sx',
                'chain_id': 'meme-1',
                'chain_name': 'meme',
                'explorer': 'https://explorer.meme.sx/meme',
                'bech_prefix': 'meme',
                'stake_token': {
                    'denom': 'umeme',
                    'symbol': 'MEME',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
            'evmos': {
                'wallet': from_atom(wallet, 'evmos'),
                'rpc': 'https://rpc-evmos.whispernode.com',
                'rest': 'https://lcd-evmos.whispernode.com',
                'chain_id': 'evmos_9001-2',
                'chain_name': 'evmos',
                'explorer': 'https://explorer.meme.sx/meme',
                'bech_prefix': 'evmos',
                'stake_token': {
                    'denom': 'aevmos',
                    'symbol': 'EVMOS',
                    'decimals': 18,
                    'coin_gecko_id': ''
                }
            },
            'mantle': {
                'wallet': from_atom(wallet, 'mantle'),
                'rpc': 'https://rpc.assetmantle.one',
                'rest': 'https://rest.assetmantle.one',
                'chain_id': 'mantle-1',
                'chain_name': 'assetmantle',
                'explorer': 'https://www.mintscan.io/asset-mantle',
                'bech_prefix': 'mantle',
                'stake_token': {
                    'denom': 'mntl',
                    'symbol': 'MNTL',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
            'genesis': {
                'wallet': from_atom(wallet, 'genesis'),
                'rpc': 'https://26657.genesisl1.org',
                'rest': 'https://api.genesisl1.org',
                'chain_id': 'genesis_29-2',
                'chain_name': 'genesisl1',
                'explorer': 'https://explorer.meme.sx/meme',
                'bech_prefix': 'genesis',
                'stake_token': {
                    'denom': 'el1',
                    'symbol': 'L1',
                    'decimals': 18,
                    'coin_gecko_id': ''
                }
            },
            'axelar': {
                'wallet': from_atom(wallet, 'axelar'),
                'rpc': 'https://rpc-axelar-ia.notional.ventures',
                'rest': 'https://axelar-lcd.quickapi.com:443',
                'chain_id': 'axelar-dojo-1',
                'chain_name': 'axelar',
                'explorer': 'https://api-axelar-ia.notional.ventures',
                'bech_prefix': 'axelar',
                'stake_token': {
                    'denom': 'uaxl',
                    'symbol': 'AXL',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
            'band': {
                'wallet': from_atom(wallet, 'band'),
                'rpc': 'https://rpc-bandchain-ia.notional.ventures',
                'rest': 'https://api-bandchain-ia.notional.ventures',
                'chain_id': 'laozi-mainnet',
                'chain_name': 'Band Protocol',
                'explorer': 'https://api-axelar-ia.notional.ventures',
                'bech_prefix': 'band',
                'stake_token': {
                    'denom': 'uband',
                    'symbol': 'BAND',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
            'cerberus': {
                'wallet': from_atom(wallet, 'cerberus'),
                'rpc': 'https://rpc-cerberus.ecostake.com',
                'rest': 'https://api-cerberus-ia.notional.ventures',
                'chain_id': 'cerberus-chain-1',
                'chain_name': 'Cerberus',
                'explorer': 'https://api-axelar-ia.notional.ventures',
                'bech_prefix': 'cerberus',
                'stake_token': {
                    'denom': 'ucrbrus',
                    'symbol': 'CRBRUS',
                    'decimals': 6,
                    'coin_gecko_id': ''
                }
            },
        }

    def set_network(self, name):
        self.network_config = self.all_networks[name]
        self.network_wallet = from_atom(self.cosmos_wallet,self.network_config['bech_prefix'])






