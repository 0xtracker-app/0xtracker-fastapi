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
            'args' : [{'farm_id' : 'CosmosStaking'}],
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
            'functions' : [farm_templates.get_osmosis_staking],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'Osmosis', 'network' : 'osmosis'}],
            'vault_args' : [{}]
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