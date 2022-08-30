from . import farm_templates
from . import external_contracts

class Farms:

    def __init__(self, wallet=None, selected_farm=None):
        self.wallet = wallet
        self.farms = {
    'CosmosStaking' : {
        'name' : 'Cosmos Staking',
        'masterChef' : 'CosmosStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'CosmosStaking', 'net' : 'cosmos'}],
            'vault_args' : [{}]
        }
    },
    'OsmosisStaking' : {
        'name' : 'Osmosis Staking',
        'masterChef' : 'OsmosisStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'OsmosisStaking', 'net' : 'osmosis'}],
            'vault_args' : [{}]
        }
    },
    'AkashStaking' : {
        'name' : 'Akash Staking',
        'masterChef' : 'AkashStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'AkashStaking', 'net' : 'akash'}],
            'vault_args' : [{}]
        }
    },
    'RegenStaking' : {
        'name' : 'Regen Staking',
        'masterChef' : 'RegenStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'RegenStaking', 'net' : 'regen'}],
            'vault_args' : [{}]
        }
    },
    'SentinelStaking' : {
        'name' : 'Sentinel Staking',
        'masterChef' : 'SentinelStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'SentinelStaking', 'net' : 'sentinel'}],
            'vault_args' : [{}]
        }
    },
    'PersistenceStaking' : {
        'name' : 'Persistence Staking',
        'masterChef' : 'PersistenceStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'PersistenceStaking', 'net' : 'persist'}],
            'vault_args' : [{}]
        }
    },
    'IrisStaking' : {
        'name' : 'IRISnet Staking',
        'masterChef' : 'IrisStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'IrisStaking', 'net' : 'iris'}],
            'vault_args' : [{}]
        }
    },
    'CryptoStaking' : {
        'name' : 'Crypto.org Staking',
        'masterChef' : 'CryptoStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'CryptoStaking', 'net' : 'crypto'}],
            'vault_args' : [{}]
        }
    },
    'IovStaking' : {
        'name' : 'Starname Staking',
        'masterChef' : 'IovStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'IovStaking', 'net' : 'iov'}],
            'vault_args' : [{}]
        }
    },
    'JunoStaking' : {
        'name' : 'Juno Staking',
        'masterChef' : 'JunoStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'JunoStaking', 'net' : 'juno'}],
            'vault_args' : [{}]
        }
    },
    'BitcannaStaking' : {
        'name' : 'BitCanna Staking',
        'masterChef' : 'BitcannaStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'BitcannaStaking', 'net' : 'bitcanna'}],
            'vault_args' : [{}]
        }
    },
    'BitsongStaking' : {
        'name' : 'BitSong Staking',
        'masterChef' : 'BitsongStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'BitsongStaking', 'net' : 'bitsong'}],
            'vault_args' : [{}]
        }
    },
    'SecretStaking' : {
        'name' : 'Secret Network Staking',
        'masterChef' : 'SecretStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'SecretStaking', 'net' : 'secret'}],
            'vault_args' : [{}]
        }
    },
    'SifStaking' : {
        'name' : 'Sif Staking',
        'masterChef' : 'SifStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'SifStaking', 'net' : 'sif'}],
            'vault_args' : [{}]
        }
    },
    'ChihuahuaStaking' : {
        'name' : 'Chihuahua Staking',
        'masterChef' : 'ChihuahuaStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'ChihuahuaStaking', 'net' : 'chihuahua'}],
            'vault_args' : [{}]
        }
    },
    'ComdexStaking' : {
        'name' : 'Comdex Staking',
        'masterChef' : 'ComdexStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'ComdexStaking', 'net' : 'comdex'}],
            'vault_args' : [{}]
        }
    },
    'LumStaking' : {
        'name' : 'Lum Network Staking',
        'masterChef' : 'LumStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'LumStaking', 'net' : 'lum'}],
            'vault_args' : [{}]
        }
    },
    'StargazeStaking' : {
        'name' : 'Stargaze Staking',
        'masterChef' : 'StargazeStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'StargazeStaking', 'net' : 'stargaze'}],
            'vault_args' : [{}]
        }
    },
    'DesmosStaking' : {
        'name' : 'Desmos Staking',
        'masterChef' : 'DesmosStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'DesmosStaking', 'net' : 'desmos'}],
            'vault_args' : [{}]
        }
    },
    'BostromStaking' : {
        'name' : 'Bostrom Staking',
        'masterChef' : 'BostromStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'BostromStaking', 'net' : 'bostrom'}],
            'vault_args' : [{}]
        }
    },
    'EmoneyStaking' : {
        'name' : 'e-Money Staking',
        'masterChef' : 'EmoneyStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'EmoneyStaking', 'net' : 'emoney'}],
            'vault_args' : [{}]
        }
    },
    'KavaStaking' : {
        'name' : 'Kava Staking',
        'masterChef' : 'KavaStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'KavaStaking', 'net' : 'kava'}],
            'vault_args' : [{}]
        }
    },
    'DigStaking' : {
        'name' : 'Dig Staking',
        'masterChef' : 'DigStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'DigStaking', 'net' : 'dig'}],
            'vault_args' : [{}]
        }
    },
    'FetchaiStaking' : {
        'name' : 'Fetch.ai Staking',
        'masterChef' : 'FetchaiStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'FetchaiStaking', 'net' : 'fetchai'}],
            'vault_args' : [{}]
        }
    },
    'CheqdStaking' : {
        'name' : 'Cheqd Staking',
        'masterChef' : 'CheqdStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'CheqdStaking', 'net' : 'cheqd'}],
            'vault_args' : [{}]
        }
    },
    'KonstellationStaking' : {
        'name' : 'Konstellation Staking',
        'masterChef' : 'KonstellationStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'KonstellationStaking', 'net' : 'konstellation'}],
            'vault_args' : [{}]
        }
    },
    'CrescentStaking' : {
        'name' : 'Crescent Staking',
        'masterChef' : 'CrescentStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'CrescentStaking', 'net' : 'crescent'}],
            'vault_args' : [{}]
        }
    },
    'MemeStaking' : {
        'name' : 'Meme Staking',
        'masterChef' : 'MemeStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'MemeStaking', 'net' : 'meme'}],
            'vault_args' : [{}]
        }
    },
    'EvmosStaking' : {
        'name' : 'Evmos Staking',
        'masterChef' : 'EvmosStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'EvmosStaking', 'net' : 'evmos'}],
            'vault_args' : [{}]
        }
    },
    'MantleStaking' : {
        'name' : 'AssetMantle Staking',
        'masterChef' : 'MantleStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'MantleStaking', 'net' : 'mantle'}],
            'vault_args' : [{}]
        }
    },
    'GenesisStaking' : {
        'name' : 'GenesisL1 Staking',
        'masterChef' : 'GenesisStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'GenesisStaking', 'net' : 'genesis'}],
            'vault_args' : [{}]
        }
    },
    'AxelarStaking' : {
        'name' : 'Axelar Staking',
        'masterChef' : 'AxelarStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'AxelarStaking', 'net' : 'axelar'}],
            'vault_args' : [{}]
        }
    },
    'BandStaking' : {
        'name' : 'Band Protocol Staking',
        'masterChef' : 'BandStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'BandStaking', 'net' : 'band'}],
            'vault_args' : [{}]
        }
    },
    'CerberusStaking' : {
        'name' : 'Cerberus Staking',
        'masterChef' : 'CerberusStaking',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_delegations],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'CerberusStaking', 'net' : 'cerberus'}],
            'vault_args' : [{}]
        }
    },

    'Osmosis' : {
        'name' : 'osmosis.zone',
        'masterChef' : 'Osmosis',
        'featured' : 2,
        'network' : 'cosmos',
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_osmosis_staking, farm_templates.get_osmosis_unbonded],
            'vaults' : [external_contracts.dummy_vault, external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : 'Osmosis', 'network' : 'osmosis'},
                {'farm_id' : 'Osmosis', 'network' : 'osmosis'}],
            'vault_args' : [{},{}]
        }
    },
    'Sifchain' : {
        'name' : 'sifchain.finance',
        'displayName' : None,
        'url' : None,
        'masterChef' : 'Sifchain',
        'featured' : 2,
        'network' : 'cosmos',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sifchain_assets],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'Sifchain', 'network' : 'sif'}],
            'vault_args' : [{}]
        }
    },
    'JunoSwap' : {
        'name' : 'junoswap.com',
        'masterChef' : 'JunoSwap',
        'displayName' : None,
        'url' : None,
        'featured' : 2,
        'network' : 'cosmos',
        'extraFunctions' : {
            'functions' : [farm_templates.get_junoswap, farm_templates.get_junoswap_locks],
            'vaults' : [external_contracts.junoswap_vaults, external_contracts.junoswap_locks],
            'args' : [{'farm_id' : 'JunoSwap', 'network' : 'juno'}, {'farm_id' : 'JunoSwap', 'network' : 'juno'}],
            'vault_args' : [{},{}]
        }
    },
    'Crescent' : {
        'name' : 'crescent.network',
        'masterChef' : 'Crescent',
        'displayName' : None,
        'url' : None,
        'featured' : 2,
        'network' : 'cosmos',
        'extraFunctions' : {
            'functions' : [farm_templates.get_crescent_farming],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'Crescent', 'network' : 'crescent'}],
            'vault_args' : [{}]
        }
    },
}