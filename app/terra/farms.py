from . import farm_templates, external_contracts

class Farms:

    def __init__(self, wallet=None, selected_farm=None):
        self.wallet = wallet
        self.farms = {
    '0xValkyrie' : {
        'name' : 'valkyrieprotocol.com',
        'masterChef' : '0xValkyrie',
        'rewardToken' : 'terra1dy9kmlm4anr92e42mrkjwzyvfqwz66un00rwr5',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_valkyrie_staking,],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xValkyrie',
                    'network' : 'terra',
                    },],
            'vault_args' : [{}]
        }
    },
    '0xLunaStaking' : {
        'name' : 'Luna Staking',
        'masterChef' : '0xLunaStaking',
        'rewardToken' : 'uluna',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_luna_staking,],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xLunaStaking',
                    'network' : 'terra',
                    },],
            'vault_args' : [{}]
        }
    },
    '0xSpectrum' : {
        'name' : 'spec.finance',
        'masterChef' : '0xSpectrum',
        'rewardToken' : 'terra1s5eczhe0h0jutf46re52x5z4r03c8hupacxmdr',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_spectrum_farms,farm_templates.get_spectrum_staking],
            'vaults' : [external_contracts.spectrum_farm_contract, external_contracts.spectrum_staking_contract],
            'args' : [
                {
                    'farm_id' : '0xSpectrum',
                    'network' : 'terra',
                },
                {
                    'farm_id' : '0xSpectrum',
                    'network' : 'terra',
                    'want_token' : 'terra1s5eczhe0h0jutf46re52x5z4r03c8hupacxmdr'
                },                
                
                ],
            'vault_args' : [{},{}]
        }
    },
}