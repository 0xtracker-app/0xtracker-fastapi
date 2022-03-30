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
    '0xLoopr' : {
        'name' : 'loop.markets',
        'masterChef' : '0xLoopr',
        'rewardToken' : 'terra1s5eczhe0h0jutf46re52x5z4r03c8hupacxmdr',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_loop_farming, farm_templates.get_loop_staking, farm_templates.get_loop_farming],
            'vaults' : [external_contracts.dummy_vault, external_contracts.loopr_staking_contract, external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xLoopr',
                    'network' : 'terra',
                    'query_contract' : 'terra1cr7ytvgcrrkymkshl25klgeqxfs48dq4rv8j26'
                },
                {
                    'farm_id' : '0xLoopr',
                    'network' : 'terra',
                    'staking_token' : 'terra1nef5jf6c7js9x6gkntlehgywvjlpytm7pcgkn4'
                },
                {
                    'farm_id' : '0xLoopr',
                    'network' : 'terra',
                    'query_contract' : 'terra1swgnlreprmfjxf2trul495uh4yphpkqucls8fv'
                },           
                ],
            'vault_args' : [{},{},{}]
        }
    },
    '0xMirror' : {
        'name' : 'mirrorprotocol.app',
        'masterChef' : '0xMirror',
        'rewardToken' : 'terra15gwkyepfc6xgca5t5zefzwy42uts8l2m4g40k6',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_mirror_farming],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xMirror',
                    'network' : 'terra',
                    'query_contract' : 'terra17f7zu97865jmknk7p2glqvxzhduk78772ezac5',
                    'reward_token' : 'terra15gwkyepfc6xgca5t5zefzwy42uts8l2m4g40k6'
                },        
                ],
            'vault_args' : [{}]
        }
    },
    '0xMirrorLending' : {
        'name' : 'mirrorprotocol.app',
        'masterChef' : '0xMirrorLending',
        'rewardToken' : 'terra15gwkyepfc6xgca5t5zefzwy42uts8l2m4g40k6',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_mirror_lending],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xMirrorLending',
                    'network' : 'terra',
                    'query_contract' : 'terra1wfz7h3aqf4cjmjcvc6s8lxdhh7k30nkczyf0mj',
                },        
                ],
            'vault_args' : [{}]
        }
    },
    '0xAstroport' : {
        'name' : 'astroport.fi',
        'masterChef' : '0xAstroport',
        'rewardToken' : 'terra1xj49zyqrwpv5k928jwfpfy2ha668nwdgkwlrg3',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_astroport_locks, farm_templates.get_xastro_staking],
            'vaults' : [external_contracts.dummy_vault, external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xAstroport',
                    'network' : 'terra',
                },
                {
                    'farm_id' : '0xAstroport',
                    'network' : 'terra',
                    'contract' : 'terra14lpnyzc9z4g3ugr4lhm8s4nle0tq8vcltkhzh7',
                    'native' : 'terra1xj49zyqrwpv5k928jwfpfy2ha668nwdgkwlrg3',
                    'staking' : 'terra1f68wt2ch3cx2g62dxtc8v68mkdh5wchdgdjwz7'
                },          
                ],
            'vault_args' : [{}, {}]
        }
    },
    '0xAnchorLending' : {
        'name' : 'anchorprotocol.com (Lending)',
        'masterChef' : '0xAnchorLending',
        'rewardToken' : 'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_anchor_lending],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xAnchorLending',
                    'network' : 'terra',
                },        
                ],
            'vault_args' : [{}]
        }
    },
    '0xAnchor' : {
        'name' : 'anchorprotocol.com',
        'masterChef' : '0xAnchor',
        'rewardToken' : 'terra14z56l0fp2lsf86zy3hty2z47ezkhnthtr9yq76',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_anchor_staking],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xAnchor',
                    'network' : 'terra',
                },        
                ],
            'vault_args' : [{}]
        }
    },
    '0xKujiBlue' : {
        'name' : 'blue.kujira.app',
        'masterChef' : '0xKujiBlue',
        'rewardToken' : 'terra1xfsdgcemqwxp4hhnyk4rle6wr22sseq7j07dnn',
        'decimal' : 6,
        'featured' : 2,
        'network' : 'terra',
        'extraFunctions' : {
            'functions' : [farm_templates.get_kujira_staking],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xKujiBlue',
                    'network' : 'terra',
                },   
                ],
            'vault_args' : [{}]
        }
    },
}