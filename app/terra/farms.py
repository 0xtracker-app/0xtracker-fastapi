from . import farm_templates, external_contracts

class Farms:

    def __init__(self, wallet=None, selected_farm=None):
        self.wallet = wallet
        self.farms = {
    '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A' : {
        'name' : 'valkyrieprotocol.com',
        'masterChef' : '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A',
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_valkyrie_staking,],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A',
                    'network' : 'terra',
                    },],
            'vault_args' : [{}]
        }
    },
}