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
        'displayName' : None,
        'url' : None,
        'extraFunctions' : {
            'functions' : [farm_templates.get_farming_from_program, farm_templates.get_farming_from_program_dual, farm_templates.get_farming_from_program_dual],
            'vaults' : [external_contracts.dummy_vault, external_contracts.dummy_vault, external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : 'Raydium', 'program' : constants.PROGRAMS.RAYDIUM_PROGRAM, 'offset' : 40},
                {'farm_id' : 'Raydium', 'program' : constants.PROGRAMS.RAYDIUM_PROGRAM_V4, 'offset' : 40, 'reward_dec' : 1e9},
                {'farm_id' : 'Raydium', 'program' : constants.PROGRAMS.RAYDIUM_PROGRAM_V5, 'offset' : 40, 'reward_dec' : 1e15},
                ],
            'vault_args' : [{},{},{}]
        }
    },
}