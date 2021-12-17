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
}