import bech32

def from_atom(atom_addr, network):
    atom_tuple = bech32.bech32_decode(atom_addr)
    data = atom_tuple[1]
    network_addr = bech32.bech32_encode(network,data)    
    return network_addr

class CosmosNetwork:

    def __init__(self, wallet=None):
        self.cosmos_wallet = wallet
        self.supported_networks = ['osmosis', 'cosmos', 'akash', 'regen', 'sentinel', 'persist', 'iris', 'crypto', 'iov', 'juno']
        self.network_wallet = ''
        self.network_config = {}
        self.all_networks = {
        'osmosis' : {
            'wallet' : from_atom(wallet,'osmo'),
            'rpc' : 'https://rpc-osmosis.keplr.app',
            'rest' : 'https://lcd-osmosis.keplr.app',
            'chain_id' : 'osmosis-1',
            'chain_name' : 'Osmosis',
            'explorer' : 'https://www.mintscan.io/osmosis/txs/',
            'bech_prefix' : 'osmo',
            'stake_token' : {
                'denom' : 'uosmo',
                'symbol' : 'OSMO',
                'decimals' : 6,
                'coin_gecko_id' : 'osmosis'
            }
        },
            'cosmos' : {
            'wallet' : from_atom(wallet,'cosmos'),
            'rpc' : 'https://rpc-cosmoshub.keplr.app',
            'rest' : 'https://lcd-cosmoshub.keplr.app',
            'chain_id' : 'cosmoshub-4',
            'chain_name' : 'Cosmos Hub',
            'explorer' : 'https://www.mintscan.io/cosmos/txs/',
            'bech_prefix' : 'cosmos',
            'stake_token' : {
                'denom' : 'uatom',
                'symbol' : 'ATOM',
                'decimals' : 6,
                'coin_gecko_id' : 'cosmos'
            }
        },
            'akash' : {
            'wallet' : from_atom(wallet,'akash'),
            'rpc' : 'https://rpc-akash.keplr.app',
            'rest' : 'https://lcd-akash.keplr.app',
            'chain_id' : 'akashnet-2',
            'chain_name' : 'Akash',
            'explorer' : 'https://www.mintscan.io/akash/txs/',
            'bech_prefix' : 'akash',
            'stake_token' : {
                'denom' : 'uakt',
                'symbol' : 'AKT',
                'decimals' : 6,
                'coin_gecko_id' : 'akash-network'
            }
        },
            'regen' : {
            'wallet' : from_atom(wallet,'regen'),
            'rpc' : 'https://rpc-regen.keplr.app',
            'rest' : 'https://lcd-regen.keplr.app',
            'chain_id' : 'regen-1',
            'chain_name' : 'Regen Network',
            'explorer' : 'https://regen.aneka.io/txs/',
            'bech_prefix' : 'regen',
            'stake_token' : {
                'denom' : 'uregen',
                'symbol' : 'REGEN',
                'decimals' : 6,
                'coin_gecko_id' : 'regen'
            }
        },
            'sentinel' : {
            'wallet' : from_atom(wallet,'sent'),
            'rpc' : 'https://rpc-sentinel.keplr.app',
            'rest' : 'https://lcd-sentinel.keplr.app',
            'chain_id' : 'sentinelhub-2',
            'chain_name' : 'Sentinel',
            'explorer' : 'https://www.mintscan.io/sentinel/txs/',
            'bech_prefix' : 'sent',
            'stake_token' : {
                'denom' : 'udvpn',
                'symbol' : 'DVPN',
                'decimals' : 6,
                'coin_gecko_id' : 'sentinel'
            }
        },
            'persist' : {
            'wallet' : from_atom(wallet,'persistence'),
            'rpc' : 'https://rpc-persistence.keplr.app',
            'rest' : 'https://lcd-persistence.keplr.app',
            'chain_id' : 'core-1',
            'chain_name' : 'Persistence',
            'explorer' : 'https://www.mintscan.io/persistence/txs/',
            'bech_prefix' : 'persistence',
            'stake_token' : {
                'denom' : 'uxprt',
                'symbol' : 'XPRT',
                'decimals' : 6,
                'coin_gecko_id' : 'persistence'
            }
        },
            'iris' : {
            'wallet' : from_atom(wallet,'iaa'),
            'rpc' : 'https://rpc-iris.keplr.app',
            'rest' : 'https://lcd-iris.keplr.app',
            'chain_id' : 'irishub-1',
            'chain_name' : 'IRISnet',
            'explorer' : 'https://www.mintscan.io/iris/txs/',
            'bech_prefix' : 'iaa',
            'stake_token' : {
                'denom' : 'uiris',
                'symbol' : 'IRIS',
                'decimals' : 6,
                'coin_gecko_id' : 'iris-network'
            }
        },
            'crypto' : {
            'wallet' : from_atom(wallet,'cro'),
            'rpc' : 'https://rpc-crypto-org.keplr.app',
            'rest' : 'https://lcd-crypto-org.keplr.app',
            'chain_id' : 'crypto-org-chain-mainnet-1',
            'chain_name' : 'Crypto.org',
            'explorer' : 'https://www.mintscan.io/crypto-org/txs/',
            'bech_prefix' : 'cro',
            'stake_token' : {
                'denom' : 'basecro',
                'symbol' : 'CRO',
                'decimals' : 8,
                'coin_gecko_id' : 'crypto-com-chain'
            }
        },
            'iov' : {
            'wallet' : from_atom(wallet,'star'),
            'rpc' : 'https://rpc-iov.keplr.app',
            'rest' : 'https://lcd-iov.keplr.app',
            'chain_id' : 'iov-mainnet-ibc',
            'chain_name' : 'Starname',
            'explorer' : 'https://www.mintscan.io/starname/txs/',
            'bech_prefix' : 'star',
            'stake_token' : {
                'denom' : 'uiov',
                'symbol' : 'IOV',
                'decimals' : 6,
                'coin_gecko_id' : 'starname'
            }
        },
            'juno' : {
            'wallet' : from_atom(wallet,'juno'),
            'rpc' : 'https://rpc-juno.itastakers.com',
            'rest' : 'https://lcd-juno.itastakers.com',
            'chain_id' : 'juno-1',
            'chain_name' : 'Juno Mainnet',
            'explorer' : 'https://www.mintscan.io/juno',
            'bech_prefix' : 'juno',
            'stake_token' : {
                'denom' : 'ujuno',
                'symbol' : 'JUNO',
                'decimals' : 6,
                'coin_gecko_id' : ''
            }
        },
            'terra' : {
            'wallet' : from_atom(wallet,'terra'),
            'rpc' : 'https://rpc-columbus.keplr.app',
            'rest' : 'https://lcd-columbus.keplr.app',
            'chain_id' : 'columbus-5',
            'chain_name' : 'Terra',
            'explorer' : 'https://finder.terra.money/columbus-5/',
            'bech_prefix' : 'terra',
            'stake_token' : {
                'denom' : 'uluna',
                'symbol' : 'LUNA',
                'decimals' : 6,
                'coin_gecko_id' : 'terra-luna'
            }
        },
            'bitcanna' : {
            'wallet' : from_atom(wallet,'bcna'),
            'rpc' : 'https://rpc.bitcanna.io',
            'rest' : 'https://lcd.bitcanna.io',
            'chain_id' : 'bitcanna-1',
            'chain_name' : 'BitCanna',
            'explorer' : 'https://www.mintscan.io/bitcanna/txs/',
            'bech_prefix' : 'bcna',
            'stake_token' : {
                'denom' : 'ubcna',
                'symbol' : 'BCNA',
                'decimals' : 6,
                'coin_gecko_id' : 'bitcanna'
            }
        },
            'bitsong' : {
            'wallet' : from_atom(wallet,'bitsong'),
            'rpc' : 'https://rpc.explorebitsong.com',
            'rest' : 'https://lcd.explorebitsong.com',
            'chain_id' : 'bitsong-2b',
            'chain_name' : 'BitSong',
            'explorer' : 'https://explorebitsong.com/transactions/',
            'bech_prefix' : 'bitsong',
            'stake_token' : {
                'denom' : 'ubtsg',
                'symbol' : 'BTSG',
                'decimals' : 6,
                'coin_gecko_id' : 'pool:ubtsg'
            }
        },
    }

    def set_network(self, name):
        self.network_config = self.all_networks[name]
        self.network_wallet = from_atom(self.cosmos_wallet,self.network_config['bech_prefix'])






