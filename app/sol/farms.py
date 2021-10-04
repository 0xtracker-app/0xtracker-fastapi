from . import farm_templates
from . import external_contracts
from . import constants

class Farms:

    def __init__(self, wallet=None, selected_farm=None):
        self.wallet = wallet
        self.farms = {
    'Raydium' : {
        'name' : 'raydium.io',
        'masterChef' : 'Raydium',
        'featured' : 2,
        'network' : 'solana',
        'extraFunctions' : {
            'functions' : [farm_templates.get_farming_from_program],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'farm_id' : 'Raydium', 'program' : constants.PROGRAMS.RAYDIUM_PROGRAM, 'offset' : 40}],
            'vault_args' : [{}]
        }
    },
}