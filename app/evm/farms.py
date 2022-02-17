
from . import farm_templates, template_helpers, external_contracts, uniswapv3
from .poolext import ext_masterchef as extra_chef

class Farms:

    def __init__(self, wallet=None, selected_farm=None):
        self.wallet = wallet
        self.farms = {
    '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A' : {
        'name' : 'eleven.finance',
        'rewardToken' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEleven',
        'masterChef' : '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A',
        'perBlock' : 'elevenPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_vault_style_no_want],
            'vaults' : [external_contracts.get_ele_tokens, external_contracts.get_ele_staking_bsc],
            'args' : [
                {
                    'farm_id' : '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A',
                    'network' : 'bsc',
                    '_pps' : 'getPricePerFullShare'
                    },
                {
                    'farm_id' : '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A',
                    'network' : 'bsc',
                    '_pps' : 'tokensPerShare',
                    'want_token' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
                    'pps_decimal' : 12
                    }],
            'vault_args' : [{'network' : 'bsc'}, {}]
        }
    },
    '0x52B8bb74Cde6602AB9e6540e25E0A97f5B3226D7' : {
        'name' : 'eleven.finance',
        'rewardToken' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEleven',
        'masterChef' : '0x52B8bb74Cde6602AB9e6540e25E0A97f5B3226D7',
        'perBlock' : 'elevenPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_vault_style_no_want],
            'vaults' : [external_contracts.get_ele_tokens, external_contracts.get_ele_staking_avax],
            'args' : [
                {
                    'farm_id' : '0x52B8bb74Cde6602AB9e6540e25E0A97f5B3226D7',
                    'network' : 'avax',
                    '_pps' : 'getPricePerFullShare'
                    },
                {
                    'farm_id' : '0x52B8bb74Cde6602AB9e6540e25E0A97f5B3226D7',
                    'network' : 'avax',
                    '_pps' : 'tokensPerShare',
                    'want_token' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
                    'pps_decimal' : 12
                    }],
            'vault_args' : [{'network' : 'avax'}, {}]
        }
    },
    '0xElevenOKE' : {
        'name' : 'eleven.finance',
        'rewardToken' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElevenOKE',
        'featured' : 2,
        'network' : 'oke',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_ele_tokens],
            'args' : [
                {
                    'farm_id' : '0xElevenOKE',
                    'network' : 'oke',
                    '_pps' : 'getPricePerFullShare'
                }],
            'vault_args' : [{'network' : 'okexchain'}]
        }
    },
    '0x8eDCe6D0E0687DA9C07B36591781fB6641A53a12' : {
        'name' : 'eleven.finance',
        'rewardToken' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEleven',
        'masterChef' : '0x8eDCe6D0E0687DA9C07B36591781fB6641A53a12',
        'perBlock' : 'elevenPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_ele_tokens],
            'args' : [
                {
                    'farm_id' : '0x8eDCe6D0E0687DA9C07B36591781fB6641A53a12',
                    'network' : 'ftm',
                    '_pps' : 'getPricePerFullShare'
                }],
            'vault_args' : [{'network' : 'fantom'}]
        }
    },
    '0x7f7Bf15B9c68D23339C31652C8e860492991760d' : {
        'name' : 'farm.br34p.finance',
        'rewardToken' : '0xbda8d53fe0f164915b46cd2ecffd94254b6086a2',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingAUTO',
        'masterChef' : '0x7f7Bf15B9c68D23339C31652C8e860492991760d',
        'perBlock' : 'AUTOPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
    '0x2EBe8CDbCB5fB8564bC45999DAb8DA264E31f24E' : {
        'name' : 'Nerve.fi',
        'rewardToken' : '0x42f6f551ae042cbe50c739158b4f0cac0edb9096',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingNerve',
        'masterChef' : '0x2EBe8CDbCB5fB8564bC45999DAb8DA264E31f24E',
        'perBlock' : 'nervePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
    '0x0895196562C7868C5Be92459FaE7f877ED450452' : {
        'name' : 'autofarm.network',
        'rewardToken' : '0xa184088a740c695E156F91f5cC086a06bb78b827',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingAUTO',
        'masterChef' : '0x0895196562C7868C5Be92459FaE7f877ED450452',
        'death_index' : [331],
        'perBlock' : 'AUTOPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
    '0xDaC4d0EE7B55497E96b73a53b31A2B47ABb7b5a8' : {
        'name' : 'cdo.finance',
        'rewardToken' : '0x9E95cB3D0560f9Cba88991f828322526851BFb56',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCodex',
        'masterChef' : '0xDaC4d0EE7B55497E96b73a53b31A2B47ABb7b5a8',
        'perBlock' : 'codexPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
    '0x33AdBf5f1ec364a4ea3a5CA8f310B597B8aFDee3' : {
        'name' : 'swamp.finance',
        'rewardToken' : '0xc5A49b4CBe004b6FD55B30Ba1dE6AC360FF9765d',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingNATIVE',
        'masterChef' : '0x33AdBf5f1ec364a4ea3a5CA8f310B597B8aFDee3',
        'perBlock' : 'NATIVEPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
    '0x4F04e540A51013aFb6761ee73D71d2fB1F29af80' : {
        'name' : 'swamp.finance',
        'rewardToken' : '0x5f1657896b38c4761dbc5484473c7a7c845910b6',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingNATIVE',
        'masterChef' : '0x4F04e540A51013aFb6761ee73D71d2fB1F29af80',
        'perBlock' : 'NATIVEPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
    '0x073D613b435b5574e988Dc989f467DDf94FB47D4' : {
        'name' : 'swamp.finance',
        'rewardToken' : '0x23cBC7C95a13071562af2C4Fb1Efa7a284d0543a',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingNATIVE',
        'masterChef' : '0x073D613b435b5574e988Dc989f467DDf94FB47D4',
        'perBlock' : 'NATIVEPerBlock',
        'featured' : 2,
        'network' : 'ftm'
    },
    '0x86d77d1CA67358f28BFc57cC85AD59c86c4f092a' : {
        'name' : 'swamp.finance',
        'rewardToken' : '0x3d6386FDE111eC2919cc8871377821b12c7EAE7C',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingNATIVE',
        'masterChef' : '0x86d77d1CA67358f28BFc57cC85AD59c86c4f092a',
        'perBlock' : 'NATIVEPerBlock',
        'featured' : 2,
        'network' : 'avax'
    },
        '0x1C515985c6318550Afb5bC590f4f0843b977250A' : {
        'name' : 'manyswap.io',
        'rewardToken' : '0x2dD6c9c5BCD16816226542688788932c6e79A600',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingMany',
        'masterChef' : '0x1C515985c6318550Afb5bC590f4f0843b977250A',
        'perBlock' : 'manyPerBlock',
        'featured' : 2,
        'network' : 'bsc'
        },

        '0x1FDCA2422668B961E162A8849dc0C2feaDb58915' : {
        'name' : 'fulcrum.trade',
        'rewardToken' : '0xf8E026dC4C0860771f691EcFFBbdfe2fa51c77CF',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBGOV',
        'masterChef' : '0x1FDCA2422668B961E162A8849dc0C2feaDb58915',
        'perBlock' : 'BGOVPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
        '0xd39Ff512C3e55373a30E94BB1398651420Ae1D43' : {
        'name' : 'fulcrum.trade',
        'rewardToken' : '0xd5d84e75f48e75f01fb2eb6dfd8ea148ee3d0feb',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGOV',
        'masterChef' : '0xd39Ff512C3e55373a30E94BB1398651420Ae1D43',
        'perBlock' : 'GOVPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
            '0x69C77Aca910851E61a64b855116888F1c5eD3B75' : {
        'name' : 'polarisdefi.io',
        'rewardToken' : '0x3a5325F0E5Ee4da06a285E988f052D4e45Aa64b4',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPolar',
        'perBlock' : 'polarPerBlock',
        'masterChef' : '0x69C77Aca910851E61a64b855116888F1c5eD3B75',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x367CdDA266ADa588d380C7B970244434e4Dde790' : {
        'name' : 'blizzard.money',
        'rewardToken' : '0x9a946c3cb16c08334b69ae249690c236ebd5583e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingxBLZD',
        'masterChef' : '0x367CdDA266ADa588d380C7B970244434e4Dde790',
        'perBlock' : 'xBLZDPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56' : {
        'name' : 'jetfuel.finance',
        'rewardToken' : '0x2090c8295769791ab7A3CF1CC6e0AA19F35e441A',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingFuel',
        'masterChef' : '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56',
        'perBlock' : 'getCurrentBlockFuel',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_jetfuel_vaults],
            'args' : [
                {
                    'farm_id' : '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56',
                    'network' : 'bsc',
                    '_pps' : 'getPricePerFullShare',
                    'want_token' : 'token'
                }],
            'vault_args' : [{}]
        }
    },
                '0xb04381026F5D4AAf0487aC4336F16E133FA5FB0a' : {
        'name' : 'blueswap.finance',
        'rewardToken' : '0x36c0556c2b15aed79f842675ff030782738ef9e8',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBlue',
        'masterChef' : '0xb04381026F5D4AAf0487aC4336F16E133FA5FB0a',
        'perBlock' : 'bluePerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'add_chefs' : ['0xBDd7E57634eEdAfBb61a12744dd249EBAB69CAB9', '0xbadb507006b72a94F3529e79B3F5a12e0E6A95F3']
    },
                '0xA9C9D9Aed47320835c84090c62dC324FcF24f683' : {
        'name' : 'mochiswap.io',
        'rewardToken' : '0x055daB90880613a556a5ae2903B2682f8A5b8d27',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingMochi',
        'masterChef' : '0xA9C9D9Aed47320835c84090c62dC324FcF24f683',
        'perBlock' : 'mochiPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x58DdaA668d1aDf32b7bdFcc4963105090Ca59540' : {
        'name' : 'rune.farm',
        'rewardToken' : '0x5de72a6fca2144aa134650bbea92cc919244f05d',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingRune',
        'masterChef' : '0x58DdaA668d1aDf32b7bdFcc4963105090Ca59540',
        'perBlock' : 'runePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xBeefy' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0xca3f508b8e4dd382ee878a314789373d80a5190a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefy',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_beefy_bsc, external_contracts.get_beefy_boosts],
            'args' : [{'farm_id' : '0xBeefy', 'network' : 'bsc'}, {'farm_id' : '0xBeefy', 'network' : 'bsc', 'stake_func' : 'stakedToken'}],
            'vault_args' : [{}, {}]
        }
    },
                '0xReaperFTM' : {
        'name' : 'reaper.farm',
        'rewardToken' : '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xReaperFTM',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes],
            'vaults' : [external_contracts.get_reaper_ftm],
            'args' : [{'farm_id' : '0xReaperFTM', 'network' : 'ftm'}],
            'vault_args' : [{}]
        }
    },
                '0x8cf7044DDedbE502892B120aAf8692FeCFb71420' : {
        'name' : 'dragonballfinance.org',
        'rewardToken' : '0xceb2f5e9c7f2d3bcd12a7560d73c56f3396af3f9',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'masterChef' : '0x8cf7044DDedbE502892B120aAf8692FeCFb71420',
        'perBlock' : 'dballPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x3F648151f5D591718327aA27d2EE25edF1b435D8' : {
        'name' : 'goosedefi.com (Vaults)',
        'rewardToken' : '0x5bfE81fCB3708C8fC733BEf60d313CAFCe1FeBEB',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingRewards',
        'masterChef' : '0x3F648151f5D591718327aA27d2EE25edF1b435D8',
        'perBlock' : 'emissionRate',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x045502ee488806bdf22928b6228bdd162b5056f6' : {
        'name' : 'neonic.finance',
        'rewardToken' : '0x94026f0227ce0c9611e8a228f114f9f19cc3fa87',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingNeon',
        'masterChef' : '0x045502ee488806bdf22928b6228bdd162b5056f6',
        'perBlock' : 'neonPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x76bd7145b99FDF84064A082BF86A33198C6e9D09' : {
        'name' : 'hyruleswap.com',
        'rewardToken' : '0x7b0409a3a3f79baa284035d48e1dfd581d7d7654',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'masterChef' : '0x76bd7145b99FDF84064A082BF86A33198C6e9D09',
        'perBlock' : 'rupeePerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'add_chefs' : ['0xd1b3d8ef5ac30a14690fbd05cf08905e1bf7d878']
    },
                '0xd1b3d8ef5ac30a14690fbd05cf08905e1bf7d878' : {
        'name' : 'hyruleswap.com (Goron Vaults)',
        'rewardToken' : '0x8efa59bf5f47c6fe0e97c15cad12f2be6bb899a1',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingGRUPEE',
        'masterChef' : '0xd1b3d8ef5ac30a14690fbd05cf08905e1bf7d878',
        'perBlock' : 'GRUPEEPerBlock',
        'death_index' : [2],
        'show' : False,
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x9b1dfEF15251AAF3540C1d008d4c4Aa6f636339d' : {
        'name' : 'satis.finance',
        'rewardToken' : '0xa1928c0d8f83c0bfb7ebe51b412b1fd29a277893',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSatisfi',
        'masterChef' : '0x9b1dfEF15251AAF3540C1d008d4c4Aa6f636339d',
        'perBlock' : 'satisfiPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xHorizon' : {
        'name' : 'horizonprotocol.com',
        'rewardToken' : '0xC0eFf7749b125444953ef89682201Fb8c6A917CD',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xHorizon',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_telx_single],
            'vaults' : [external_contracts.get_horizon],
            'args' : [{'network_id' : 'bsc', 'farm_id' : '0xHorizon'}],
            'vault_args' : [{}]
        }
    },
                '0x8705eaba437A2DEf65b0e455C025EEc05d1ee4aB' : {
        'name' : 'lokum.finance (old)',
        'rewardToken' : '0x1099E778846bAa6aAD3C6F26Ad42419AA7f95103',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLkm',
        'masterChef' : '0x8705eaba437A2DEf65b0e455C025EEc05d1ee4aB',
        'perBlock' : 'lkmPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xBDd7E57634eEdAfBb61a12744dd249EBAB69CAB9' : {
        'name' : 'blueswap.finance (Green Layer)',
        'rewardToken' : '0xa4fb1f591980e6e4eb4661a0d96df19a13d21aa7',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGreen',
        'masterChef' : '0xBDd7E57634eEdAfBb61a12744dd249EBAB69CAB9',
        'perBlock' : 'greenPerBlock',
        'show' : False,
        'featured' : 2,
        'network' : 'bsc'

    },
                '0xbadb507006b72a94F3529e79B3F5a12e0E6A95F3' : {
        'name' : 'blueswap.finance (Purple Layer)',
        'rewardToken' : '0x3a6f79cecfa4fafbe7514d4d5fa85d3665939e89',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPurple',
        'masterChef' : '0xbadb507006b72a94F3529e79B3F5a12e0E6A95F3',
        'perBlock' : 'purplePerBlock',
        'show' : False,
        'featured' : 2,
        'network' : 'bsc'
    },
                    '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' : {
        'name' : 'bingocash.app',
        'rewardToken' : '0x53f39324fbb209693332b87aa94d5519a1a49ab0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingShare',
        'masterChef' : '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_bingo_board],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{'network' : 'bsc'}],
            'vault_args' : [{}, {}]
        }
    },
                    '0xc9525f505040fecd4b754407De72d7bCf5a8f78F' : {
        'name' : 'bingocash.app (Board Room)',
        'rewardToken' : '0x579A6277a6c2c63a5b25006F63Bce5DC8D9c25e7',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xc9525f505040fecd4b754407De72d7bCf5a8f78F',
        'featured' : 2,
        'show' : False,
        'network' : 'bsc'
    },
                    '0xd56339F80586c08B7a4E3a68678d16D37237Bd96' : {
        'name' : 'bsc.valuedefi.io',
        'rewardToken' : '0x4f0ed527e8A95ecAA132Af214dFd41F30b361600',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0xd56339F80586c08B7a4E3a68678d16D37237Bd96',
        'featured' : 2,
        'network' : 'bsc',
        'perBlock' : 'getCurrentRewardPerBlock',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_vsafes],
            'args' : [{
                'farm_id' : '0xd56339F80586c08B7a4E3a68678d16D37237Bd96',
                'network' : 'bsc',
                '_pps' : 'getPricePerFullShare',
                '_stake' : 'balanceOf',
                'want_token' : 'token'
            }],
            'vault_args' : [{}]
        }
    },
                    '0xE9a8b6ea3e7431E6BefCa51258CB472Df2Dd21d4' : {
        'name' : 'firebird.finance',
        'rewardToken' : '0xd78C475133731CD54daDCb430F7aAE4F03C1E660',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0xE9a8b6ea3e7431E6BefCa51258CB472Df2Dd21d4',
        'featured' : 2,
        'network' : 'matic',
        'perBlock' : 'rewardPerSecond',
        'apy_config' : 'second',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_firebird_vaults],
            'args' : [{
                'farm_id' : '0xd56339F80586c08B7a4E3a68678d16D37237Bd96',
                'network' : 'bsc',
                '_pps' : 'getPricePerFullShare',
                '_stake' : 'balanceOf',
                'want_token' : 'token'
            }],
            'vault_args' : [{'network' : 137}]
        }
    },
                '0xDiamondHands' : {
        'name' : 'diamondhand.fi',
        'rewardToken' : '0x34ea3f7162e6f6ed16bd171267ec180fd5c848da',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xDiamondHands',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_diamond_hands],
            'vaults' : [external_contracts.diamond_vaults],
            'args' : [{}],
            'vault_args' : [{}]
        }
    },
                '0xD4BbC80b9B102b77B21A06cb77E954049605E6c1' : {
        'name' : 'belt.fi',
        'rewardToken' : '0xe0e514c71282b6f4e823703a39374cf58dc3ea4f',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingBELT',
        'masterChef' : '0xD4BbC80b9B102b77B21A06cb77E954049605E6c1',
        'perBlock' : 'BELTPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x7854fb0edd06a880ec8009c62b1aa38e26f9988d' : {
        'name' : 'brickchain.finance',
        'rewardToken' : '0xc4daa5a9f2b832ed0f9bc579662883cd53ea9d61',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBrick',
        'masterChef' : '0x7854fb0edd06a880ec8009c62b1aa38e26f9988d',
        'perBlock' : 'brickPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xe87DE2d5BbB4aF23c665Cf7331eC744B020883bB' : {
        'name' : 'apoyield.com',
        'rewardToken' : '0x66f3704cb9082afde787b09ae95e2e17599e730b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0xe87DE2d5BbB4aF23c665Cf7331eC744B020883bB',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc',
    },
                '0x95030532D65C7344347E61Ab96273B6B110385F2' : {
        'name' : 'deflate.finance',
        'rewardToken' : '0x887bf46573b9a77c4060919e786b881f08f15de4',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingBalloon',
        'masterChef' : '0x95030532D65C7344347E61Ab96273B6B110385F2',
        'perBlock' : 'balloonPerBlock',
        'death_index' : [43],
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D' : {
        'name' : 'wault.finance',
        'rewardToken' : '0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingWex',
        'masterChef' : '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D',
        'perBlock' : 'wexPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_wault_locked, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_wault_locked, external_contracts.get_wault_pool_contracts],
            'args' : [
                {
                    'farm_id' : '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D',
                    'network' : 'bsc'

                },
                {
                    'farm_id' : '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D',
                    'network_id' : 'bsc',
                    'staked' : 'pool',
                    'pending_reward' : 'pendingRewards'
                }],
            'vault_args' : [{'network' : 'bsc'}, {}]
        }
    },
                '0xF1F8E3ff67E386165e05b2B795097E95aaC899F0' : {
        'name' : 'evodefi.com',
        'rewardToken' : '0xb0f2939a1c0e43683e5954c9fe142f7df9f8d967',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGen',
        'masterChef' : '0xF1F8E3ff67E386165e05b2B795097E95aaC899F0',
        'perBlock' : 'genPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d' : {
        'name' : 'evodefi.com (v2)',
        'rewardToken' : '0x9aa18a4e73e1016918fa360eed950d9580c9551d',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGenX',
        'masterChef' : '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d',
        'perBlock' : 'genxPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xPancakeBunny' : {
        'name' : 'pancakebunny.finance',
        'rewardToken' : '0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPancakeBunny',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_bunny_clones],
            'vaults' : [external_contracts.get_pancakebunny_pools],
            'args' : [
                {
                    'farm_id' : '0xPancakeBunny',
                    'network_id' : 'bsc',
                    'dashboard_contract' : '0xb3c96d3c3d643c2318e4cdd0a9a48af53131f5f4',
                    'calculator' : '0xf5bf8a9249e3cc4cb684e3f23db9669323d4fb7d',
                    'native_symbol' : 'BUNNY',
                    '_decode' : 'ten',
                    'native_token' : '0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51'
                    }],
            'vault_args' : [{'network' : 'bsc'}]
        }
    },
                '0xPancakeBunnyMatic' : {
        'name' : 'pancakebunny.finance',
        'rewardToken' : '0x4c16f69302ccb511c5fac682c7626b9ef0dc126a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPancakeBunnyMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_bunny_clones],
            'vaults' : [external_contracts.get_pancakebunny_pools],
            'args' : [
                {
                    'farm_id' : '0xPancakeBunnyMatic',
                    'network_id' : 'matic',
                    'dashboard_contract' : '0xFA71FD547A6654b80c47DC0CE16EA46cECf93C02',
                    'calculator' : '0xe3b11c3bd6d90cfebbb4fb9d59486b0381d38021',
                    'native_symbol' : 'polyBUNNY',
                    '_decode' : 'ten',
                    'native_token' : '0x4c16f69302ccb511c5fac682c7626b9ef0dc126a'
                    }],
            'vault_args' : [{'network' : 'matic'}]
        }
    },
                '0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9' : {
        'name' : 'apeswap.finance',
        'rewardToken' : '0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_apeswap_pools_old, external_contracts.get_apeswap_pools_new],
            'args' : [
                {
                    'farm_id' : '0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9',
                    'network_id' : 'bsc',
                    'staked' : 'stakeToken'
                    },
                {
                    'farm_id' : '0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9',
                    'network_id' : 'bsc',
                    'staked' : 'STAKE_TOKEN',
                    'reward' : 'REWARD_TOKEN'
                    }],
            'vault_args' : [{}, {}]
        }
    },
                '0xGambit' : {
        'name' : 'gambit.financial',
        'rewardToken' : '0xe304ff0983922787Fd84BC9170CD21bF78B16B10',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xGambit',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_gambits],
            'vaults' : [external_contracts.gambit_vaults],
            'args' : [
                {
                    'farm_id' : '0xGambit',
                    'network' : 'bsc'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xGMX' : {
        'name' : 'gmx.io',
        'rewardToken' : '0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xGMX',
        'featured' : 2,
        'network' : 'arb',
        'extraFunctions' : {
            'functions' : [farm_templates.get_gmx],
            'vaults' : [external_contracts.gmx_vaults],
            'args' : [
                {
                    'farm_id' : '0xGMX',
                    'network_id' : 'arb'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x058451C62B96c594aD984370eDA8B6FD7197bbd4' : {
        'name' : 'pantherswap.com',
        'rewardToken' : '0x1f546ad641b56b86fd9dceac473d1c7a357276b7',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPanther',
        'masterChef' : '0x058451C62B96c594aD984370eDA8B6FD7197bbd4',
        'perBlock' : 'pantherPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.panther_jungles],
            'args' : [
                {
                    'farm_id' : '0x058451C62B96c594aD984370eDA8B6FD7197bbd4',
                    'network_id' : 'bsc'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x398d648c58ccf6337dded3dac7cbd7970ae474b8' : {
        'name' : 'cheesecakeswap.com',
        'rewardToken' : '0xc7091aa18598b87588e37501b6ce865263cd67ce',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCcake',
        'masterChef' : '0x398d648c58ccf6337dded3dac7cbd7970ae474b8',
        'perBlock' : 'ccakePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x3E2210E1e40599d3F751EE70667136291505d921' : {
        'name' : 'cheesecakeswap.com',
        'rewardToken' : '0xBC2597D3f1F9565100582CDe02E3712D03B8B0f6',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCcake',
        'masterChef' : '0x3E2210E1e40599d3F751EE70667136291505d921',
        'perBlock' : 'ccakePerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x29A089Fb10d3774EfE952352C3C0A04546D299E1' : {
        'name' : 'quamnetwork.com',
        'rewardToken' : '0x1ade17b4b38b472b5259bbc938618226df7b5ca8',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingQuam',
        'masterChef' : '0x29A089Fb10d3774EfE952352C3C0A04546D299E1',
        'perBlock' : 'quamPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xTaodao' : {
        'name' : 'taodao.finance',
        'rewardToken' : '0x7065dda3f8ec5f6c155648bdee4420c0525d93c6',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xTaodao',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_taodao],
            'vaults' : [external_contracts.get_taodao],
            'args' : [
                {
                    'network' : 'bsc'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x4448336BA564bd620bE90d55078e397c26492a43' : {
        'name' : 'takodefi.com',
        'rewardToken' : '0x2f3391aebe27393aba0a790aa5e1577fea0361c2',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTako',
        'masterChef' : '0x4448336BA564bd620bE90d55078e397c26492a43',
        'perBlock' : 'takoPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'add_chefs' : ['0x8399B18A8f951a84e98366013EcE47F9bcb6D1f5']
    },
                '0x8399B18A8f951a84e98366013EcE47F9bcb6D1f5' : {
        'name' : 'takodefi.com (Vaults)',
        'rewardToken' : '0xb37cad62441ef8b866f3e36f12fd42062b6c0f33',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingInku',
        'masterChef' : '0x8399B18A8f951a84e98366013EcE47F9bcb6D1f5',
        'perBlock' : 'InkuPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'show' : False
    },
                '0xB19300246e19929a617C4260189f7B759597B8d8' : {
        'name' : 'takodefi.com',
        'rewardToken' : '0x6d2a71f4edf10ab1e821b9b373363e1e24e5df6b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTako',
        'masterChef' : '0xB19300246e19929a617C4260189f7B759597B8d8',
        'perBlock' : 'takoPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'add_chefs' : ['0x63645F519d75ca5064400d4f67E6Ca9991F375BE']
    },
                '0x63645F519d75ca5064400d4f67E6Ca9991F375BE' : {
        'name' : 'takodefi.com (Vaults)',
        'rewardToken' : '0x1dd9e9e142f3f84d90af1a9f2cb617c7e08420a4',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingInku',
        'masterChef' : '0x63645F519d75ca5064400d4f67E6Ca9991F375BE',
        'perBlock' : 'InkuPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xc41E3944367814C947C5c53cb1b3FDce1C7BC286' : {
        'name' : 'caramelswap.finance',
        'rewardToken' : '0x7d5bc7796fd62a9a27421198fc3c349b96cdd9dc',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingToken',
        'masterChef' : '0xc41E3944367814C947C5c53cb1b3FDce1C7BC286',
        'perBlock' : 'tokenPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x5d9A3F476D614C7545bBBDc6E3CEDB0300B135B1' : {
        'name' : 'caramelswap.finance (Legacy)',
        'rewardToken' : '0x7ce1e651374ec5324e6f37c4ff312d53428f0d50',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCaramel',
        'masterChef' : '0x5d9A3F476D614C7545bBBDc6E3CEDB0300B135B1',
        'perBlock' : 'caramelPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x30f4cb706e65ABB3cbC3fFC2805E8Ff50eA8fbC8' : {
        'name' : 'thelab.finance',
        'rewardToken' : '0x171401a3d18b21bfa3f9bf4f9637f3691158365a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLabo',
        'masterChef' : '0x30f4cb706e65ABB3cbC3fFC2805E8Ff50eA8fbC8',
        'perBlock' : 'laboPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
    # Old Popsicle
    #                 '0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0' : {
    #     'name' : 'popsicle.finance',
    #     'rewardToken' : '0xf16e81dce15b08f326220742020379b855b87df9',
    #     'decimal' : 18,
    #     'stakedFunction' : 'userInfo',
    #     'pendingFunction' : 'pendingIce',
    #     'masterChef' : '0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0',
    #     'featured' : 2
    # },
                        '0xbf513aCe2AbDc69D38eE847EFFDaa1901808c31c' : {
        'name' : 'popsicle.finance',
        'rewardToken' : '0xf16e81dce15b08f326220742020379b855b87df9',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingIce',
        'masterChef' : '0xbf513aCe2AbDc69D38eE847EFFDaa1901808c31c',
        'perBlock' : 'icePerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'bsc'
    },
                    '0x68c616DCeA206055B85830E641FBf7A20648548D' : {
        'name' : 'koaladefi.finance',
        'rewardToken' : '0xba26397cdff25f0d26e815d218ef3c77609ae7f1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLyptus',
        'masterChef' : '0x68c616DCeA206055B85830E641FBf7A20648548D',
        'perBlock' : 'lyptusPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                    '0xf6948f00FC2BA4cDa934C931628B063ed9091019' : {
        'name' : 'koaladefi.finance',
        'rewardToken' : '0x04f2e3ec0642e501220f32fcd9e26e77924929a9',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingNalis',
        'masterChef' : '0xf6948f00FC2BA4cDa934C931628B063ed9091019',
        'perBlock' : 'nalisPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                    '0x95fABAe2E9Fb0A269cE307550cAC3093A3cdB448' : {
        'name' : 'growthdefi.com',
        'rewardToken' : '0x3ab63309f85df5d4c3351ff8eacb87980e05da4e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x95fABAe2E9Fb0A269cE307550cAC3093A3cdB448',
        'pendingFunction' : 'pendingCake',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                    '0xa7A1A6f7A7f03295E209E3CB5C602a80E10049eC' : {
        'name' : 'phyto.finance',
        'rewardToken' : '0xae63595ed0bcfddeff2ebb74a20ae96727783a67',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPhy',
        'masterChef' : '0xa7A1A6f7A7f03295E209E3CB5C602a80E10049eC',
        'perBlock' : 'phyPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                    '0x51f015e3dEA234039fB536C358781118f36f1745' : {
        'name' : 'pandayield.com',
        'rewardToken' : '0xd909840613fcb0fadc6ee7e5ecf30cdef4281a68',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x51f015e3dEA234039fB536C358781118f36f1745',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                    '0x73feaa1ee314f8c655e354234017be2193c9e24e' : {
        'name' : 'pancakeswap.finance',
        'rewardToken' : '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x73feaa1ee314f8c655e354234017be2193c9e24e',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_syrup_pools, farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_pcs_pools, external_contracts.get_pcs_pools, external_contracts.get_pcs_auto],
            'args' : [
                {
                    'farm_id' : '0x73feaa1ee314f8c655e354234017be2193c9e24e',
                    'network_id' : 'bsc',
                },
                {
                    'farm_id' : '0x73feaa1ee314f8c655e354234017be2193c9e24e',
                    'network_id' : 'bsc',
                    'staked' : 'syrup'
                },
                {
                    'farm_id' : '0x73feaa1ee314f8c655e354234017be2193c9e24e',
                    'network' : 'bsc',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo'
                },                
                ],
            'vault_args' : [{'offset' : 0}, {'offset' : 1}, {}]
        }
    },
                '0xFortress' : {
        'name' : 'fortress.loans',
        'rewardToken' : '0x4437743ac02957068995c48E08465E0EE1769fBE',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xFortress',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_fortress],
            'vaults' : [external_contracts.get_fortress_vaults],
            'args' : [{}],
            'vault_args' : [{}]
        }
    },
                '0x3d8fd880976a3EA0f53cad02463867013D331107' : {
        'name' : 'thegrandbanks.finance',
        'rewardToken' : '0xee814f5b2bf700d2e843dc56835d28d095161dd9',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingGrand',
        'masterChef' : '0x3d8fd880976a3EA0f53cad02463867013D331107',
        'perBlock' : 'GrandPerBlock',
        'featured' : 1,
        'network' : 'bsc'
    },
                '0xcF8070d9fbE3F96f4bFF0F90Cc84BfD30869dAF2' : {
        'name' : 'thegrandbanks.finance',
        'rewardToken' : '0xbcf339df10d78f2b44aa760ead0f715a7a7d7269',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingGrand',
        'masterChef' : '0xcF8070d9fbE3F96f4bFF0F90Cc84BfD30869dAF2',
        'perBlock' : 'grandPerSecond',
        'apy_config' : 'second',
        'featured' : 1,
        'network' : 'matic'
    },
                '0xC6da8165f6f5F0F890c363cD67af1c33Bb540123' : {
        'name' : 'thegrandbanks.finance',
        'rewardToken' : '0xbcf339df10d78f2b44aa760ead0f715a7a7d7269',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : None,
        'masterChef' : '0xC6da8165f6f5F0F890c363cD67af1c33Bb540123',
        'perBlock' : 'grandPerSecond',
        'apy_config' : 'second',
        'featured' : 1,
        'network' : 'moon'
    },
                '0xf6afB97aC5eAfAd60d3ad19c2f85E0Bd6b7eAcCf' : {
        'name' : 'garudaswap.finance',
        'rewardToken' : '0x854086dc841e1bfae50cb615bf41f55bf432a90b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGaruda',
        'masterChef' : '0xf6afB97aC5eAfAd60d3ad19c2f85E0Bd6b7eAcCf',
        'perBlock' : 'garudaPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x303961805A22d76Bac6B2dE0c33FEB746d82544B' : {
        'name' : 'sponge.finance',
        'rewardToken' : '0x849233ff1aea15d80ef658b2871664c9ca994063',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x303961805A22d76Bac6B2dE0c33FEB746d82544B',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'add_chefs' : ['0xED955AE44A5632A0163B72e2f5e1474FB814034F']
    },
                '0xED955AE44A5632A0163B72e2f5e1474FB814034F' : {
        'name' : 'sponge.finance (Layer 1)',
        'rewardToken' : '0xE66556de5ba21393eAd8c2b386cCDf2994098C68',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSoakSink',
        'masterChef' : '0xED955AE44A5632A0163B72e2f5e1474FB814034F',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'show' : False,
        'network' : 'bsc'
    },
                '0xABEE2aaF12E92384274D61d0dbd31bD7Fc35f38c' : {
        'name' : 'shrimpswap.finance',
        'rewardToken' : '0x62ee12e4fe74a815302750913c3c796bca23e40e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingShrimp',
        'masterChef' : '0xABEE2aaF12E92384274D61d0dbd31bD7Fc35f38c',
        'perBlock' : 'getCurrentShrimpPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7' : {
        'name' : 'polispay.org',
        'rewardToken' : '0xb5bea8a26d587cf665f2d78f077cca3c7f6341bd',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPolis',
        'masterChef' : '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7',
        'perBlock' : 'polisPerBlock',
        'poolLength' : 'getRewardsLength',
        'want' : 'rewardsInfo',
        'pool_alloc' :'rewardsInfo(uint256)((address,uint256,uint256,uint256))',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x55Da3b152F48378A42D091be1eef2af37964BE45' : {
        'name' : 'gatorswap.xyz',
        'rewardToken' : '0x88371dec00bc3543231e01089c3dc6d94289d4af',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGator',
        'masterChef' : '0x55Da3b152F48378A42D091be1eef2af37964BE45',
        'perBlock' : 'GatorPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xDYP' : {
        'name' : 'dyp.finance',
        'rewardToken' : '0x961C8c0B1aaD0c0b10a51FeF6a867E3091BCef17',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xDYP',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_dyp],
            'vaults' : [external_contracts.get_dyp],
            'args' : [{'network_id' : 'bsc'}],
            'vault_args' : [{}]
        }
    },
                '0xA625AB01B08ce023B2a342Dbb12a16f2C8489A8F' : {
        'name' : 'alpacafinance.org',
        'rewardToken' : '0x8f0528ce5ef7b51152a59745befdd91d97091d2f',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingAlpaca',
        'masterChef' : '0xA625AB01B08ce023B2a342Dbb12a16f2C8489A8F',
        'perBlock' : 'alpacaPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xA9a438B8b2E41B3bf322DBA139aF9490DC226953' : {
        'name' : 'treedefi.com',
        'rewardToken' : '0x40b34cc972908060d6d527276e17c105d224559d',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTree',
        'masterChef' : '0xA9a438B8b2E41B3bf322DBA139aF9490DC226953',
        'perBlock' : 'treePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xMerlin' : {
        'name' : 'merlinlab.com',
        'rewardToken' : '0xda360309c59cb8c434b28a91b823344a96444278',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xMerlin',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_bunny_clones],
            'vaults' : [external_contracts.get_merlin_vaults],
            'args' : [
                {
                    'farm_id' : '0xMerlin',
                    'network_id' : 'bsc',
                    'dashboard_contract' : '0xfF8B299da344AD8Ff399b4CBd3db01c0c7264bdf',
                    'calculator' : '0xcbC54fEc7a8bCf2E391a93A2ABE02F35f7052088',
                    'native_symbol' : 'MERL',
                    'native_token' : '0xda360309c59cb8c434b28a91b823344a96444278'
                    }],
            'vault_args' : [{}]
        }
    },
                '0xC63eB87ae59B1be4F408AF586c23ee5c213ca9FE' : {
        'name' : 'latteswap.finance',
        'rewardToken' : '0xef6f50fe05f4ead7805835fd1594406d31b96ed8',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0xC63eB87ae59B1be4F408AF586c23ee5c213ca9FE',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x63d6EC1cDef04464287e2af710FFef9780B6f9F5' : {
        'name' : 'jetswap.finance',
        'rewardToken' : '0x0487b824c8261462f88940f97053e65bdb498446',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x63d6EC1cDef04464287e2af710FFef9780B6f9F5',
        'perBlock' : 'cakePerBlock',
        'featured' : 1,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_jetswap_vaults],
            'args' : [
                {
                    'farm_id' : '0x63d6EC1cDef04464287e2af710FFef9780B6f9F5',
                    'network' : 'bsc',
                    '_pps' : 'getPricePerFullShare'
                }
                    ],
            'vault_args' : [{'network' : 'bsc'}]
        }
    },
                '0xd66c5C66Cef05a0fd2F20d087D4DAd3fB48E10Be' : {
        'name' : 'purplemonster.net',
        'rewardToken' : '0xc46889ec6d0deaffbff6545621f82a3e6e0d73a5',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPurpleMonster',
        'masterChef' : '0xd66c5C66Cef05a0fd2F20d087D4DAd3fB48E10Be',
        'perBlock' : 'purpleMonsterPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x8CFD1B9B7478E7B0422916B72d1DB6A9D513D734' : {
        'name' : 'polycat.finance (legacy)',
        'rewardToken' : '0x3a3df212b7aa91aa0402b9035b098891d276572b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingFish',
        'masterChef' : '0x8CFD1B9B7478E7B0422916B72d1DB6A9D513D734',
        'perBlock' : 'fishPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x4ce9Ae2f5983e19AebF5b8Bae4460f2B9EcE811a' : {
        'name' : 'polycat.finance',
        'rewardToken' : '0xbc5b59ea1b6f8da8258615ee38d40e999ec5d74f',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPaw',
        'masterChef' : '0x4ce9Ae2f5983e19AebF5b8Bae4460f2B9EcE811a',
        'perBlock' : 'pawPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'add_chefs' : ['0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904']
    },
                '0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904' : {
        'name' : 'polycat.finance (vaults)',
        'rewardToken' : '0xbc5b59ea1b6f8da8258615ee38d40e999ec5d74f',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : None,
        'masterChef' : '0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904',
        'featured' : 2,
        'network' : 'matic',
        'perBlock' : None,
        'death_index' : [454],
        'show' : False
    },
                '0x864A0B7F8466247A0e44558D29cDC37D4623F213' : {
        'name' : 'autofarm.network',
        'rewardToken' : '0x7f426F6Dc648e50464a0392E60E1BB465a67E9cf',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : None,
        'masterChef' : '0x864A0B7F8466247A0e44558D29cDC37D4623F213',
        'featured' : 2,
        'network' : 'avax',
        'perBlock' : None,
        'death_index' : [67],
    },
                '0xAutoCro' : {
        'name' : 'autofarm.network',
        'rewardToken' : '0x7f426F6Dc648e50464a0392E60E1BB465a67E9cf',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAutoCro',
        'featured' : 2,
        'network' : 'cro',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xAutoCro',
                    'network_id' : 'cro',
                    'farm_data' :{
                        'rewardToken' : '0x7f426F6Dc648e50464a0392E60E1BB465a67E9cf',
                        'decimal' : 18,
                        'stakedFunction' : 'stakedWantTokens',
                        'pendingFunction' : None,
                        'masterChef' : '0x76b8c3ECdF99483335239e66F34191f11534cbAA',
                        'rewardSymbol' : 'AUTO',
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x76b8c3ECdF99483335239e66F34191f11534cbAA' : {
        'name' : 'autofarm.network',
        'rewardToken' : '0x7f426F6Dc648e50464a0392E60E1BB465a67E9cf',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : None,
        'masterChef' : '0x76b8c3ECdF99483335239e66F34191f11534cbAA',
        'featured' : 2,
        'death_index' : [75, 76],
        'network' : 'ftm',
        'perBlock' : None,
    },
                '0xB93C082bCfCCf5BAeA0E0f0c556668E25A41B896' : {
        'name' : 'polyzap.finance',
        'rewardToken' : '0xeb2778f74e5ee038e67aa6c77f0f0451abd748fd',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPZap',
        'masterChef' : '0xB93C082bCfCCf5BAeA0E0f0c556668E25A41B896',
        'perBlock' : 'pZapPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xb03f95E649724dF6bA575C2c6eF062766a7fDb51' : {
        'name' : 'polygaj.finance',
        'rewardToken' : '0xf4b0903774532aee5ee567c02aab681a81539e92',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'masterChef' : '0xb03f95E649724dF6bA575C2c6eF062766a7fDb51',
        'perBlock' : 'gajPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x14790e89a52E207956A90f0ddBcd6C255315Af6B' : {
        'name' : 'blackswap.finance (Aurora)',
        'rewardToken' : '0x0c8c8ae8bc3a69dc8482c01ceacfb588bb516b01',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingAurora',
        'masterChef' : '0x14790e89a52E207956A90f0ddBcd6C255315Af6B',
        'perBlock' : 'auroraPerBlock',
        'featured' : 2,
        'network' : 'matic',
    },                
                '0x74284baEDb904486cec0091002b8E6a602977593' : {
        'name' : 'blackswap.finance (Polysolar)',
        'rewardToken' : '0x5fbccc4acc0b9339d7cdc5d6336a5c88d89e5327',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSolar',
        'masterChef' : '0x74284baEDb904486cec0091002b8E6a602977593',
        'perBlock' : 'solarPerBlock',
        'featured' : 2,
        'network' : 'matic',
    },
                '0x65430393358e55A658BcdE6FF69AB28cF1CbB77a' : {
        'name' : 'iron.finance (Legacy)',
        'rewardToken' : '0xaaa5b9e6c589642f98a1cda99b9d024b8407285a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x65430393358e55A658BcdE6FF69AB28cF1CbB77a',
        'perBlock' : 'rewardPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'add_chefs' : ['0xb444d596273C66Ac269C33c30Fbb245F4ba8A79d', '0xa37DD1f62661EB18c338f18Cf797cff8b5102d8e']
    },
                '0xIronPoly' : {
        'name' : 'iron.finance',
        'rewardToken' : '0x4a81f8796e0c6ad4877a51c86693b0de8093f2ef',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xIronPoly',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xIronPoly',
                    'network_id' : 'matic',
                    'farm_data' :{
                        'name' : 'iron.finance',
                        'rewardToken' : '0x4a81f8796e0c6ad4877a51c86693b0de8093f2ef',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingReward',
                        'masterChef' : '0x1fD1259Fa8CdC60c6E8C86cfA592CA1b8403DFaD',
                        'perBlock' : 'rewardPerBlock',
                        'featured' : 2,
                        'network' : 'matic',
                        'wantFunction' : 'lpToken',
                        'rewardSymbol' : 'ICE',
                        'show' : False
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x1fD1259Fa8CdC60c6E8C86cfA592CA1b8403DFaD' : {
        'name' : 'iron.finance',
        'rewardToken' : '0x4a81f8796e0c6ad4877a51c86693b0de8093f2ef ',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x1fD1259Fa8CdC60c6E8C86cfA592CA1b8403DFaD',
        'perBlock' : 'rewardPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'matic',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'alloc_offset' : 2,
        'pool_alloc' : 'poolInfo(uint256)((uint256,uint256,uint256))',
        'rewardSymbol' : 'ICE',
        'show' : False
    },
                '0xb444d596273C66Ac269C33c30Fbb245F4ba8A79d' : {
        'name' : 'iron.finance',
        'rewardToken' : '0xaaa5b9e6c589642f98a1cda99b9d024b8407285a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0xb444d596273C66Ac269C33c30Fbb245F4ba8A79d',
        'perBlock' : 'rewardPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xa37DD1f62661EB18c338f18Cf797cff8b5102d8e' : {
        'name' : 'iron.finance',
        'rewardToken' : '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
        'decimal' : 6,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0xa37DD1f62661EB18c338f18Cf797cff8b5102d8e',
        'perBlock' : 'rewardPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xIronAVAX' : {
        'name' : 'iron.finance',
        'rewardToken' : '0xfc108f21931576a21d0b4b301935dac80d9e5086',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xIronAVAX',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xIronAVAX',
                    'network_id' : 'avax',
                    'farm_data' :{
                        'name' : 'iron.finance',
                        'rewardToken' : '0xfc108f21931576a21d0b4b301935dac80d9e5086',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingReward',
                        'masterChef' : '0x073667be2bc3efC8c03Caf6C35632EB8aD6DfC47',
                        'perBlock' : 'rewardPerBlock',
                        'featured' : 2,
                        'network' : 'avax',
                        'wantFunction' : 'lpToken',
                        'rewardSymbol' : 'ICE',
                        'show' : False
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xIronFTM' : {
        'name' : 'iron.finance',
        'rewardToken' : '0x260b3e40c714ce8196465ec824cd8bb915081812',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xIronFTM',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xIronFTM',
                    'network_id' : 'ftm',
                    'farm_data' :{
                        'name' : 'iron.finance',
                        'rewardToken' : '0x260b3e40c714ce8196465ec824cd8bb915081812',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingReward',
                        'masterChef' : '0x733A33312FBFFe22C86bf1204264f3Fa06c7aB65',
                        'perBlock' : 'rewardPerBlock',
                        'featured' : 2,
                        'network' : 'ftm',
                        'wantFunction' : 'lpToken',
                        'rewardSymbol' : 'ICE',
                        'show' : False
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x34bc3D36845d8A7cA6964261FbD28737d0d6510f' : {
        'name' : 'polywhale.finance',
        'rewardToken' : '0x05089c9ebffa4f0aca269e32056b1b36b37ed71b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKrill',
        'masterChef' : '0x34bc3D36845d8A7cA6964261FbD28737d0d6510f',
        'perBlock' : 'krillPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'add_chefs' : ['0x0c23DCc118313ceB45a029CE0A4AB744eA4928ef']
    },
                '0x0c23DCc118313ceB45a029CE0A4AB744eA4928ef' : {
        'name' : 'polywhale.finance (Reefs)',
        'rewardToken' : '0x05089c9ebffa4f0aca269e32056b1b36b37ed71b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKRILL',
        'masterChef' : '0x0c23DCc118313ceB45a029CE0A4AB744eA4928ef',
        'perBlock' : 'krillPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xA07fcB5eDf05EA16e681ca7019e696c7DaD2ee4a' : {
        'name' : 'frankenstein.finance',
        'rewardToken' : '0x129e6d84c6cab9b0c2f37ad1d14a9fe2e59dab09',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingNATIVE',
        'masterChef' : '0xA07fcB5eDf05EA16e681ca7019e696c7DaD2ee4a',
        'perBlock' : 'NATIVEPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xDbc1A13490deeF9c3C12b44FE77b503c1B061739' : {
        'name' : 'biswap.org',
        'rewardToken' : '0x965f527d9159dce6288a2219db51fc6eef120dd1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBSW',
        'masterChef' : '0xDbc1A13490deeF9c3C12b44FE77b503c1B061739',
        'perBlock' : 'BSWPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xBeefyMatic' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0xFbdd194376de19a88118e84E279b977f165d01b8',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_beefy_matic_pools, external_contracts.get_beefy_boosts_poly],
            'args' : [{'farm_id' : '0xBeefyMatic', 'network' : 'matic'}, {'farm_id' : '0xBeefyMatic', 'network' : 'matic', 'stake_func' : 'stakedToken'}],
            'vault_args' : [{}, {}]
        }
    },
                '0xBeefyFantom' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0xbF07093ccd6adFC3dEB259C557b61E94c1F66945',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyFantom',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes],
            'vaults' : [external_contracts.get_beefy_fantom_pools],
            'args' : [{'farm_id' : '0xBeefyFantom', 'network' : 'ftm'}],
            'vault_args' : [{}]
        }
    },
                '0xBeefyHarmony' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0xbF07093ccd6adFC3dEB259C557b61E94c1F66945',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyHarmony',
        'featured' : 2,
        'network' : 'harmony',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes],
            'vaults' : [external_contracts.get_beefy_harmony_pools],
            'args' : [{'farm_id' : '0xBeefyHarmony', 'network' : 'harmony'}],
            'vault_args' : [{}]
        }
    },
                '0xBeefyCronos' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0xe6801928061CDbE32AC5AD0634427E140EFd05F9',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyCronos',
        'featured' : 2,
        'network' : 'cro',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_beefy_cronos_pools, external_contracts.get_beefy_boosts_cronos],
            'args' : [{'farm_id' : '0xBeefyCronos', 'network' : 'cro'}, {'farm_id' : '0xBeefyCronos', 'network' : 'cro', 'stake_func' : 'stakedToken'}],
            'vault_args' : [{}, {}]
        }
    },
                '0xBeefyArb' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0x99C409E5f62E4bd2AC142f17caFb6810B8F0BAAE',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyArb',
        'featured' : 2,
        'network' : 'arb',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes],
            'vaults' : [external_contracts.get_beefy_arb_pools],
            'args' : [{'farm_id' : '0xBeefyArb', 'network' : 'arb'}],
            'vault_args' : [{}]
        }
    },
                '0xBeefyFuse' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0x99C409E5f62E4bd2AC142f17caFb6810B8F0BAAE',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyFuse',
        'featured' : 2,
        'network' : 'fuse',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_beefy_fuse_pools, external_contracts.get_beefy_boosts_fuse],
            'args' : [{'farm_id' : '0xBeefyFuse', 'network' : 'fuse'},{'farm_id' : '0xBeefyFuse', 'network' : 'fuse', 'stake_func' : 'stakedToken'}],
            'vault_args' : [{},{}]
        }
    },
                '0xBeefyAVAX' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0xd6070ae98b8069de6B494332d1A1a81B6179D960',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyAVAX',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes],
            'vaults' : [external_contracts.get_beefy_avax_pools],
            'args' : [{'farm_id' : '0xBeefyAVAX', 'network' : 'avax'}],
            'vault_args' : [{}]
        }
    },
                '0xBeefyMoon' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0x173fd7434B8B50dF08e3298f173487ebDB35FD14',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyMoon',
        'featured' : 2,
        'network' : 'moon',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_beefy_moon_pools, external_contracts.get_beefy_boosts_moon],
            'args' : [{'farm_id' : '0xBeefyMoon', 'network' : 'moon'}, {'farm_id' : '0xBeefyMoon', 'network' : 'moon', 'stake_func' : 'stakedToken'}],
            'vault_args' : [{},{}]
        }
    },
    '0xD109D9d6f258D48899D7D16549B89122B0536729' : {
        'name' : 'eleven.finance',
        'rewardToken' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEleven',
        'masterChef' : '0xD109D9d6f258D48899D7D16549B89122B0536729',
        'perBlock' : 'elevenPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_vault_style_no_want, farm_templates.get_multireward],
            'vaults' : [external_contracts.get_ele_tokens, external_contracts.get_ele_staking_matic, external_contracts.get_ele_multi],
            'args' : [
                {
                    'farm_id' : '0xD109D9d6f258D48899D7D16549B89122B0536729',
                    'network' : 'matic',
                    '_pps' : 'getPricePerFullShare'
                    },
                {
                    'farm_id' : '0xD109D9d6f258D48899D7D16549B89122B0536729',
                    'network' : 'matic',
                    '_pps' : 'tokensPerShare',
                    'want_token' : '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0',
                    'pps_decimal' : 12
                    },
                {
                    'farm_id' : '0xD109D9d6f258D48899D7D16549B89122B0536729',
                    'network_id' : 'matic',
                    'farm_data' : extra_chef.eleusd_info
                    }
                ],
            'vault_args' : [{'network' : 'polygon'}, {}, {}]
        }
    },
                '0xaAC5636DbDF8e64dD75d44066990B23085dDC39b' : {
        'name' : 'gocerberus.finance',
        'rewardToken' : '0x8b3268a23131dafbd77165690767f285c1aac6c5',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCerberus',
        'masterChef' : '0xaAC5636DbDF8e64dD75d44066990B23085dDC39b',
        'perBlock' : 'cerberusPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x43404359bb38f5135ab8e25c62902015a49a0074' : {
        'name' : 'alchemistdefi.com (Mist)',
        'rewardToken' : '0x6f8fe12cc34398d15b7d5a5ba933e550da1d099f ',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingMist',
        'masterChef' : '0x43404359bb38f5135ab8e25c62902015a49a0074',
        'perBlock' : 'mistPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x193765551a49eAD3aA8C693F19C4501710cD874d' : {
        'name' : 'alchemistdefi.com (Aurum)',
        'rewardToken' : '0x49207BAA3a7332F0716788aa57B088D499bcc104',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingAurum',
        'masterChef' : '0x193765551a49eAD3aA8C693F19C4501710cD874d',
        'perBlock' : 'aurumPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xD622a8500c2B098F722ec1CCb2EC09B8A8e1016f' : {
        'name' : 'ketchupfinance.com',
        'rewardToken' : '0x714a84632ed7edbbbfeb62dacf02db4beb4c69d9',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKetchup',
        'masterChef' : '0xD622a8500c2B098F722ec1CCb2EC09B8A8e1016f',
        'perBlock' : 'kerPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x5Ee68AF6CCFCEA4F2cdce7BF20D543532E7D63AA' : {
        'name' : 'lokum.finance (new)',
        'rewardToken' : '0xeae41c03dac91d38c88a51a546aeafd2a9f7a5e7',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSlkm',
        'masterChef' : '0x5Ee68AF6CCFCEA4F2cdce7BF20D543532E7D63AA',
        'perBlock' : 'sLkmPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xSquirrel' : {
        'name' : 'squirrel.finance',
        'rewardToken' : '0x8893d5fa71389673c5c4b9b3cb4ee1ba71207556',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSquirrel',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_nuts],
            'vaults' : [external_contracts.squirrel_vaults],
            'args' : [
                {
                    'farm_id' : '0xSquirrel',
                    'network' : 'bsc',
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3' : {
        'name' : 'evo-matic.com',
        'rewardToken' : '0x161c0ece60dcfcdc3e4bdd5f1cde3ed2f68285a9',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGen',
        'masterChef' : '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3',
        'perBlock' : 'genPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x6685C8618298C04b6E42dDAC06400cc5924e917e' : {
        'name' : 'evo-matic.com (v2)',
        'rewardToken' : '0x3ecdeb8fc5023839b92b0c293d049d61069e02b1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGenX',
        'masterChef' : '0x6685C8618298C04b6E42dDAC06400cc5924e917e',
        'perBlock' : 'genxPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xA96dd23a3027818b9657486380ade322798033De' : {
        'name' : 'smellycat.finance',
        'rewardToken' : '0x22fa6143b3e8cd8c928f77a9326f1300adc7b4d7',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPussy',
        'masterChef' : '0xA96dd23a3027818b9657486380ade322798033De',
        'perBlock' : 'pussyPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x3074b9dEa4D4729934846D3aF65147b65Cdd5d55' : {
        'name' : 'prismfinance.net',
        'rewardToken' : '0x2f3c8e38c079e80527e42935298f288c31a4b1fc',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPrism',
        'masterChef' : '0x3074b9dEa4D4729934846D3aF65147b65Cdd5d55',
        'perBlock' : 'prismPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xafb4314cFb1089D875847339Fc77C69971239D64' : {
        'name' : 'prismfinance.net',
        'rewardToken' : '0x2f3c8e38c079e80527e42935298f288c31a4b1fc',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPrism',
        'masterChef' : '0xafb4314cFb1089D875847339Fc77C69971239D64',
        'perBlock' : 'prismPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xAdamant' : {
        'name' : 'adamant.finance',
        'rewardToken' : '0xc3FdbadC7c795EF1D6Ba111e06fF8F16A20Ea539',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAdamant',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_adamant_funds, farm_templates.get_adamant_stakes, farm_templates.get_vault_style_with_rewards],
            'vaults' : [external_contracts.get_adamant_vaults, external_contracts.dummy_vault, external_contracts.get_adamant_boosts],
            'args' : [{},{'farm_id' : '0xAdamant'},{'network_id' : 'matic', 'farm_id' : '0xAdamant'}],
            'vault_args' : [{},{},{}]
        }
    },
                '0xAdamantArb' : {
        'name' : 'adamant.finance',
        'rewardToken' : '0x09ad12552ec45f82be90b38dfe7b06332a680864',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAdamantArb',
        'featured' : 2,
        'network' : 'arb',
        'extraFunctions' : {
            'functions' : [farm_templates.get_adamant_funds_dynamic],
            'vaults' : [external_contracts.get_adamant_vaults_arb],
            'args' : [
                {
                    'calculator' : '0x25c4D57c9eAFA243a8d74249fE70855E50931cE7',
                    'minter' : '0x47D3DCaD6e47C519238Cbe50DA43e6a53C49CFC2',
                    'reward' : '0x82af49447d8a07e3bd95bd0d56f35241523fbab1',
                    'farm_id' : '0xAdamantArb',
                    'reward' : '0x82af49447d8a07e3bd95bd0d56f35241523fbab1',
                    'network' : 'arb',
                }],
            'vault_args' : [{}]
        }
    },
                '0x2e47630f1a7807b596267361f9DD4C534632Ae98' : {
        'name' : 'goldenbull.finance',
        'rewardToken' : '0x3e9b01762a82c12151cde2094f8ef9bcab774c8e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGBull',
        'masterChef' : '0x2e47630f1a7807b596267361f9DD4C534632Ae98',
        'perBlock' : 'gBullPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x46A35829d0a45f5221F211efD7de8591De2527ce' : {
        'name' : 'lazymint.finance',
        'rewardToken' : '0xf4308ae29c84238f3386c01d3cf6266ac6939ade',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLazymint',
        'masterChef' : '0x46A35829d0a45f5221F211efD7de8591De2527ce',
        'perBlock' : 'LazymintPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x00275072A952f7731d507dc5deC9Bcb27c13cfc3' : {
        'name' : 'polylion.exchange',
        'rewardToken' : '0x1da554d34027ca8de74c5b1cd2fa53a8a1492c94',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLion',
        'masterChef' : '0x00275072A952f7731d507dc5deC9Bcb27c13cfc3',
        'perBlock' : 'lionPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xA7f3C3f80Ff6a6f31bB7BaB04E3E8AC4E4dAE0c3' : {
        'name' : 'piratedice.xyz',
        'rewardToken' : '0xd12dc5319808bb31ba95ae5764def2627d5966ce',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBooty',
        'masterChef' : '0xA7f3C3f80Ff6a6f31bB7BaB04E3E8AC4E4dAE0c3',
        'perBlock' : 'bootyPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xe0e400617A20ADee7B2034324C3fa4C37bce97E8' : {
        'name' : 'polygold.finance',
        'rewardToken' : '0x0184316f58b9a44acdd3e683257259dc0cf2202a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'masterChef' : '0xe0e400617A20ADee7B2034324C3fa4C37bce97E8',
        'perBlock' : 'goldPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x984E30Cc6174c61B1210417bcF0b6bE5DaEd7961' : {
        'name' : 'fishswap.app',
        'rewardToken' : '0xd9a0dc07d25ed65da8ed4321c42f7f35de81bf2d',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingFish',
        'masterChef' : '0x984E30Cc6174c61B1210417bcF0b6bE5DaEd7961',
        'perBlock' : 'fishPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x984aFbbbB3B123e948AFed0022F92D76Bf4E2Df6' : {
        'name' : 'kikko.finance',
        'rewardToken' : '0x898ae1b5120d765f8c9b2735bed67ee7c04e13a2',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKikko',
        'masterChef' : '0x984aFbbbB3B123e948AFed0022F92D76Bf4E2Df6',
        'perBlock' : 'kikkoPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x66c901fEBc771A8e0bbe0a9f8A2487C60ba07bf4' : {
        'name' : 'zfarm.finance',
        'rewardToken' : '0x42d1b21eabe04d308148ea9ab90be674b64b4eef',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x66c901fEBc771A8e0bbe0a9f8A2487C60ba07bf4',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xQuickSwap' : {
        'name' : 'quickswap.exchange',
        'rewardToken' : '0x831753dd7087cac61ab5644b308642cc1c33dc13',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xQuickSwap',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style, farm_templates.get_quickswap_lps],
            'vaults' : [external_contracts.get_qs_vaults, external_contracts.get_quickswap_lps],
            'args' : [
                {
                    'farm_id' : '0xQuickSwap',
                    'network' : 'matic'
                },
                {
                    'farm_id' : '0xQuickSwap',
                },
                    ],
            'vault_args' : [{}, {'wallet' : wallet}]
        }
    },
                '0xDFYN' : {
        'name' : 'dfyn.network',
        'rewardToken' : '0xc168e40227e4ebd8c1cae80f7a55a4f0e6d66c97',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xDFYN',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style, farm_templates.get_quickswap_style_multi],
            'vaults' : [external_contracts.get_dfyn_vaults, external_contracts.get_dfyn_dual],
            'args' : [
                {
                    'farm_id' : '0xDFYN',
                    'network' : 'matic'
                },
                {
                    'farm_id' : '0xDFYN',
                    'network' : 'matic'
                },
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0x14d3C919262A0da0B8846507F65fd76f8a1Da6A9' : {
        'name' : 'stonk.farm',
        'rewardToken' : '0x4becdd1704e16962053792fd0d6baa533daaa702',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'masterChef' : '0x14d3C919262A0da0B8846507F65fd76f8a1Da6A9',
        'perBlock' : 'eggPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x3e9f42ce8aCC06bAB8E020b6D259EF501989743C' : {
        'name' : 'polycash.finance',
        'rewardToken' : '0xc22d189ff43868a347fda822842b67b1c8c57612',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCash',
        'masterChef' : '0x3e9f42ce8aCC06bAB8E020b6D259EF501989743C',
        'perBlock' : 'cashPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x6275518a63e891b1bC54FEEBBb5333776E32fAbD' : {
        'name' : 'kogefarm.io',
        'rewardToken' : '0x13748d548d95d78a3c83fe3f32604b4796cffa23',
        'decimal' : 9,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x6275518a63e891b1bC54FEEBBb5333776E32fAbD',
        'perBlock' : 'rewardPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.pull_koge_vaults],
            'args' : [
                {
                    'farm_id' : '0x6275518a63e891b1bC54FEEBBb5333776E32fAbD',
                    'network' : 'matic'
                },
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xKogeFTM' : {
        'name' : 'kogefarm.io',
        'rewardToken' : '0x13748d548d95d78a3c83fe3f32604b4796cffa23',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xKogeFTM',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.pull_koge_vaults_ftm],
            'args' : [
                {
                    'farm_id' : '0xKogeFTM',
                    'network' : 'ftm'
                },
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xKogeMoon' : {
        'name' : 'kogefarm.io',
        'rewardToken' : '0x13748d548d95d78a3c83fe3f32604b4796cffa23',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xKogeMoon',
        'featured' : 2,
        'network' : 'moon',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.pull_koge_vaults_moon],
            'args' : [
                {
                    'farm_id' : '0xKogeMoon',
                    'network' : 'moon'
                },
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xSushiMatic' : {
        'name' : 'sushi.com',
        'rewardToken' : '0x0b3f868e0be5597d5db7feb59e1cadbb0fdda50a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSushiMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sushi_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xSushiMatic',
                    'network_id' : 'matic',
                    'farm_data' :{
                        'masterChef' : '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F',
                        'rewarder' : '0xa3378Ca78633B3b9b2255EAa26748770211163AE',
                        'r0sym' : 'SUSHI',
                        'r1sym' : 'MATIC',
                        'r0t' : '0x0b3f868e0be5597d5db7feb59e1cadbb0fdda50a',
                        'r1t' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
                    }
                }
                    ],
            'vault_args' : [{}]
        }
},
                '0xE9eB13A6bdA835e10BED2e8F9b3BF3a2E72CA687' : {
        'name' : 'sneakerfinance.me',
        'rewardToken' : '0x71fc472b418343905edc609906506c10f6a0b169',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSneaker',
        'masterChef' : '0xE9eB13A6bdA835e10BED2e8F9b3BF3a2E72CA687',
        'perBlock' : 'SneakerPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xFf42AE1A338585316267345E6234fc7E6de15D34' : {
        'name' : 'polysnow.farm',
        'rewardToken' : '0x831ecee0ef97ace95d1f14ad122c0e9f8e5b36aa',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSnow',
        'perBlock' : 'snowPerBlock',
        'masterChef' : '0xFf42AE1A338585316267345E6234fc7E6de15D34',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x4F1818Ff649498a2441aE1AD29ccF55a8E1C6250' : {
        'name' : 'hyperjump.fi',
        'rewardToken' : '0x5ef5994fa33ff4eb6c82d51ee1dc145c546065bd',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingAlloy',
        'masterChef' : '0x4F1818Ff649498a2441aE1AD29ccF55a8E1C6250',
        'perBlock' : 'alloyPerBlock',
        'featured' : 2,
        'network' : 'bsc',
    },
                '0x7A0De9A006129A18AE8d3C4e609fa866EE29A5B3' : {
        'name' : 'hyperjump.app',
        'rewardToken' : '0x130025ee738a66e691e6a7a62381cb33c6d9ae83',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'perBlock' : 'emission_per_second',
        'apy_config' : 'second',
        'alloc_offset' : 3,
        'masterChef' : '0x7A0De9A006129A18AE8d3C4e609fa866EE29A5B3',
        'featured' : 2,
        'network' : 'bsc',
    },
                '0x90Df158ff7c31aD1d81ddDb1D8ab9d0eCBCeDa20' : {
        'name' : 'hyperjump.fi',
        'rewardToken' : '0x0575f8738efda7f512e3654f277c77e80c7d2725',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingOrillium',
        'perBlock' : 'oriPerSecond',
        'apy_config' : 'second',
        'masterChef' : '0x90Df158ff7c31aD1d81ddDb1D8ab9d0eCBCeDa20',
        'featured' : 2,
        'network' : 'ftm',
    },
                '0x2E03284727Ff6E50BB00577381059a11e5Bb01dE' : {
        'name' : 'hyperjump.app',
        'rewardToken' : '0x78de9326792ce1d6eca0c978753c6953cdeedd73',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'perBlock' : 'emission_per_second',
        'apy_config' : 'second',
        'masterChef' : '0x2E03284727Ff6E50BB00577381059a11e5Bb01dE',
        'alloc_offset' : 3,
        'featured' : 2,
        'network' : 'ftm',
    },
                '0xCEd39CF6221a10331e2349224BB1Eeb03A5c146f' : {
        'name' : 'polydragon.io',
        'rewardToken' : '0xe118e8b6dc166cd83695825eb1d30e792435bb00',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingFire',
        'masterChef' : '0xCEd39CF6221a10331e2349224BB1Eeb03A5c146f',
        'perBlock' : 'firePerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xC8Bd86E5a132Ac0bf10134e270De06A8Ba317BFe' : {
        'name' : 'wault.finance',
        'rewardToken' : '0x4c4bf319237d98a30a929a96112effa8da3510eb',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingWex',
        'perBlock' : 'wexPerBlock',
        'masterChef' : '0xC8Bd86E5a132Ac0bf10134e270De06A8Ba317BFe',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_wault_pools_matic],
            'args' : [
                {
                    'farm_id' : '0xC8Bd86E5a132Ac0bf10134e270De06A8Ba317BFe',
                    'network_id' : 'matic',
                    'staked' : 'pool',
                    'pending_reward' : 'pendingRewards'
                },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x89d065572136814230A55DdEeDDEC9DF34EB0B76' : {
        'name' : 'autofarm.network',
        'rewardToken' : '0x7f426F6Dc648e50464a0392E60E1BB465a67E9cf',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : None,
        'masterChef' : '0x89d065572136814230A55DdEeDDEC9DF34EB0B76',
        'perBlock' : None,
        'featured' : 2,
        'network' : 'matic'
    },
                '0xfada8cc923514f1d7b0586ad554b4a0cead4680e' : {
        'name' : 'autofarm.network',
        'rewardToken' : '0x7f426F6Dc648e50464a0392E60E1BB465a67E9cf',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : None,
        'masterChef' : '0xfada8cc923514f1d7b0586ad554b4a0cead4680e',
        'perBlock' : None,
        'featured' : 2,
        'network' : 'moon'
    },
                '0xA794491C95D276DD67A6641D978618BA2598ad09' : {
        'name' : 'stablegaj.finance',
        'rewardToken' : '0x94c7d657f1c8be06a4dc009d2d475bb559d858cb',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'masterChef' : '0xA794491C95D276DD67A6641D978618BA2598ad09',
        'perBlock' : 'sgajPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xAutoShark' : {
        'name' : 'autoshark.finance',
        'rewardToken' : '0xdd97ab35e3c0820215bc85a395e13671d84ccba2',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAutoShark',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_bunny_clones],
            'vaults' : [external_contracts.get_autoshark_vaults],
            'args' : [
                {
                    'farm_id' : '0xAutoShark',
                    'network_id' : 'bsc',
                    'dashboard_contract' : '0xa5251abdb5218699F09360DF17967C0e2ffA6655',
                    'calculator' : '0x41B471F347a7C2C8e6cb7F4F59C570C6D9c69a3C',
                    'native_symbol' : 'JAWS',
                    'native_token' : '0xdd97ab35e3c0820215bc85a395e13671d84ccba2'
                    }],
            'vault_args' : [{'network' : 'bsc'}]
        }
    },
                '0xAutoSharkMatic' : {
        'name' : 'autoshark.finance',
        'rewardToken' : '0xdd97ab35e3c0820215bc85a395e13671d84ccba2',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAutoSharkMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_bunny_clones],
            'vaults' : [external_contracts.get_autoshark_vaults],
            'args' : [
                {
                    'farm_id' : '0xAutoSharkMatic',
                    'network_id' : 'matic',
                    'dashboard_contract' : '0xA96CeA606D206310e4ffaa65577D316D49043cDF',
                    'calculator' : '0xd9bAfd0024d931D103289721De0D43077e7c2B49',
                    'native_symbol' : 'JAWS',
                    'native_token' : '0xdd97ab35e3c0820215bc85a395e13671d84ccba2'
                    }],
            'vault_args' : [{'network' : 'poly'}]
        }
    },
                '0x2DC11B394BD0f1CC6AC0a269cfe3CC0b333601B4' : {
        'name' : 'polyyeld.finance',
        'rewardToken' : '0xd0f3121a190d85de0ab6131f2bcecdbfcfb38891',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingYeld',
        'masterChef' : '0x2DC11B394BD0f1CC6AC0a269cfe3CC0b333601B4',
        'perBlock' : 'YeldPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_apolyyeld],
            'args' : [
                {
                    'farm_id' : '0x2DC11B394BD0f1CC6AC0a269cfe3CC0b333601B4',
                    'network' : 'matic',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo'
                },
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0x1B8deA992Ebb340a151383E18F63c1e89cE180a4' : {
        'name' : 'polyyeld.finance (v2)',
        'rewardToken' : '0x1fd6cf265fd3428f655378a803658942095b4c4e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingYeld',
        'masterChef' : '0x1B8deA992Ebb340a151383E18F63c1e89cE180a4',
        'perBlock' : 'YeldPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x6ad70613d14c34aa69E1604af91c39e0591a132e' : {
        'name' : 'augury.finance',
        'rewardToken' : '0x76e63a3e7ba1e2e61d3da86a87479f983de89a7e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingOmen',
        'masterChef' : '0x6ad70613d14c34aa69E1604af91c39e0591a132e',
        'perBlock' : 'omenPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x574Fe4E8120C4Da1741b5Fd45584de7A5b521F0F' : {
        'name' : 'mai.finance',
        'rewardToken' : '0x580A84C73811E1839F75d86d75d88cCa0c241fF4',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pending',
        'masterChef' : '0x574Fe4E8120C4Da1741b5Fd45584de7A5b521F0F',
        'perBlock' : 'rewardPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_mai_cvault],
            'vaults' : [external_contracts.get_mai_graph],
            'args' : [{'farm_id' : '0x574Fe4E8120C4Da1741b5Fd45584de7A5b521F0F'}],
            'vault_args' : [{'wallet': wallet}]
        }
    },
                '0xAF019F09b887E611Cc7C7263503027787AA46BA6' : {
        'name' : 'polydex.fi',
        'rewardToken' : '0x7a5dc8a09c831251026302c93a778748dd48b4df',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0xAF019F09b887E611Cc7C7263503027787AA46BA6',
        'perBlock' : 'rewardPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x69E7Bbe85db0364397378364458952bEcB886920' : {
        'name' : 'safedollar.fi',
        'rewardToken' : '0xab72ee159ff70b64beecbbb0fbbe58b372391c54',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x69E7Bbe85db0364397378364458952bEcB886920',
        'perBlock' : 'rewardPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'matic',
        'add_chefs' : ['0x17684f4d5385FAc79e75CeafC93f22D90066eD5C', '0x029D14479B9497B95CeD7DE6DAbb023E31b4a1C3']
    },
                '0x029D14479B9497B95CeD7DE6DAbb023E31b4a1C3' : {
        'name' : 'safedollar.fi (SDS v1)',
        'rewardToken' : '0x352db329b707773dd3174859f1047fb4fd2030bc',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x029D14479B9497B95CeD7DE6DAbb023E31b4a1C3',
        'perBlock' : 'rewardPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0x17684f4d5385FAc79e75CeafC93f22D90066eD5C' : {
        'name' : 'safedollar.fi (SDO)',
        'rewardToken' : '0x86bc05a6f65efdada08528ec66603aef175d967f',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x17684f4d5385FAc79e75CeafC93f22D90066eD5C',
        'perBlock' : 'rewardPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xApeRocket' : {
        'name' : 'aperocket.finance',
        'rewardToken' : '0xe486a69e432fdc29622bf00315f6b34c99b45e80',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xApeRocket',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_bunny_clones, farm_templates.get_aperocket_space_pool],
            'vaults' : [external_contracts.get_aperocket_vaults, external_contracts.get_space_pool_bsc],
            'args' : [
                {
                    'farm_id' : '0xApeRocket',
                    'network_id' : 'bsc',
                    'dashboard_contract' : '0xe64AA77B1719eFf35D6740cB99200a193B8d6c97',
                    'calculator' : '0x5D6086f8aae9DaEBAC5674E8F3b867D5743171D3',
                    'native_symbol' : 'SPACE',
                    'native_token' : '0xe486a69e432fdc29622bf00315f6b34c99b45e80'
                },
                {
                    'farm_id' : '0xApeRocket',
                    'network_id' : 'bsc',
                    'rewardtoken' : {'token' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', 'symbol' : 'WBNB', 'decimal' : 18},
                    'profit_offset' : 2
                },
                    
                    
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xApeRocketMatic' : {
        'name' : 'aperocket.finance',
        'rewardToken' : '0xD016cAAe879c42cB0D74BB1A265021bf980A7E96',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xApeRocketMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_bunny_clones, farm_templates.get_aperocket_space_pool],
            'vaults' : [external_contracts.get_aperocket_vaults_matic, external_contracts.get_space_pool_poly],
            'args' : [
                {
                    'farm_id' : '0xApeRocketMatic',
                    'network_id' : 'matic',
                    'dashboard_contract' : '0x6e44fe8d084734cE65DF0d458ACAaB3C20c95937',
                    'calculator' : '0xBE53cB783ff5d63979De124924960e2F193625B2',
                    'native_symbol' : 'pSPACE',
                    'native_token' : '0xD016cAAe879c42cB0D74BB1A265021bf980A7E96'
                },
                {
                    'farm_id' : '0xApeRocketMatic',
                    'network_id' : 'matic',
                    'rewardtoken' : {'token' : '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619', 'symbol' : 'WETH', 'decimal' : 18},
                    'profit_offset' : 2
                },
                    
                    
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0x264A1b3F6db28De4D3dD4eD23Ab31A468B0C1A96' : {
        'name' : 'ten.finance',
        'rewardToken' : '0xd15c444f1199ae72795eba15e8c1db44e47abf62',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingTENFI',
        'perBlock' : 'TENFIPerBlock',
        'masterChef' : '0x264A1b3F6db28De4D3dD4eD23Ab31A468B0C1A96',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d' : {
        'name' : 'polycrystal.finance',
        'rewardToken' : '0x76bf0c28e604cc3fe9967c83b3c3f31c213cfe64',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCrystal',
        'masterChef' : '0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d',
        'perBlock' : 'crystalPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.get_polycrystal_staking, external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d',
                    'network' : 'matic',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo'
                },
                {
                    'farm_id' : '0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d',
                    'network_id' : 'matic',
                    'farm_data' :{
                        'rewardToken' : '0x76bf0c28e604cc3fe9967c83b3c3f31c213cfe64',
                        'decimal' : 18,
                        'stakedFunction' : 'stakedWantTokens',
                        'pendingFunction' : None,
                        'masterChef' : '0xD4d696ad5A7779F4D3A0Fc1361adf46eC51C632d',
                        'rewardSymbol' : 'CRYSTL',
                    }
                }
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xApeSwapMatic' : {
        'name' : 'apeswap.finance',
        'rewardToken' : '0x5d47baba0d66083c52009271faf3f50dcc01023c',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xApeSwapMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_apeswap],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xApeSwapMatic',
                    'network_id' : 'matic'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xA54D10C6666172824Da54C0d90BcdE36B6dAbd85' : {
        'name' : 'bundledao.org',
        'rewardToken' : '0x7ff78e1cab9a2710eb6486ecbf3d94d125039364',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingRewards',
        'masterChef' : '0xA54D10C6666172824Da54C0d90BcdE36B6dAbd85',
        'perBlock' : 'blockRewards',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xf6E62b59DbD8C8395321F886bd06eCf04f57C088' : {
        'name' : 'stablemagnet.finance',
        'rewardToken' : '0xcd734b1f9b0b976ddc46e507d0aa51a4216a1e98',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingMagnet',
        'masterChef' : '0xf6E62b59DbD8C8395321F886bd06eCf04f57C088',
        'perBlock' : 'magnetPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xf6E62b59DbD8C8395321F886bd06eCf04f57C088',
                    'network_id' : 'bsc',
                    'farm_data' :{
                                    'name' : 'stablemagnet.finance',
                                    'rewardToken' : '0xe9e7cea3dedca5984780bafc599bd69add087d56',
                                    'rewardSymbol' : 'BUSD',
                                    'decimal' : 18,
                                    'stakedFunction' : 'userInfo',
                                    'pendingFunction' : 'pendingBusd',
                                    'masterChef' : '0xbb131Ee18cbBEf03bB554F935F9FECed65B67488',
                                    'featured' : 2,
                                    'network' : 'bsc',
                                    'show' : False
                                }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xbb131Ee18cbBEf03bB554F935F9FECed65B67488' : {
        'name' : 'stablemagnet.finance',
        'rewardToken' : '0xe9e7cea3dedca5984780bafc599bd69add087d56',
        'rewardSymbol' : 'BUSD',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBusd',
        'masterChef' : '0xbb131Ee18cbBEf03bB554F935F9FECed65B67488',
        'perBlock' : 'busdPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'show' : False
    },
                '0x2b2929E785374c651a81A63878Ab22742656DcDd' : {
        'name' : 'spookyswap.finance',
        'rewardToken' : '0x841fad6eae12c286d1fd18d1d525dffa75c7effe',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBOO',
        'perBlock' : 'booPerSecond',
        'apy_config' : 'second',
        'masterChef' : '0x2b2929E785374c651a81A63878Ab22742656DcDd',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_spooky_stakes],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0x2b2929E785374c651a81A63878Ab22742656DcDd',
                    'network_id' : 'ftm',
                    'farm_data' : {'masterChef' : '0x2352b745561e7e6FCD03c093cE7220e3e126ace0', 'stakedFunction' : 'userInfo', 'pendingFunction' : 'pendingReward'}
                },],
            'vault_args' : [{}]
        }
    },
                '0xf43261d712cCa4aE55b34B77d9157e773254D1dF' : {
        'name' : 'honestwork.farm',
        'rewardToken' : '0x4da646b71014332ae8370017d05205346d3ca50a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendinghonest',
        'perBlock' : 'honestPerBlock',
        'masterChef' : '0xf43261d712cCa4aE55b34B77d9157e773254D1dF',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x0ac58Fd25f334975b1B61732CF79564b6200A933' : {
        'name' : 'planetfinance.io',
        'rewardToken' : '0x72b7d61e8fc8cf971960dd9cfa59b8c829d91991',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingAQUA',
        'masterChef' : '0x0ac58Fd25f334975b1B61732CF79564b6200A933',
        'perBlock' : 'AQUAPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x9083EA3756BDE6Ee6f27a6e996806FBD37F6F093' : {
        'name' : 'spiritswap.finance',
        'rewardToken' : '0x5cc61a78f164885776aa610fb0fe1257df78e59b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSpirit',
        'perBlock' : 'spiritPerBlock',
        'masterChef' : '0x9083EA3756BDE6Ee6f27a6e996806FBD37F6F093',
        'featured' : 2,
        'network' : 'ftm'
    },
                '0xAcryptos' : {
        'name' : 'acryptos.com',
        'rewardToken' : '0x4197C6EF3879a08cD51e5560da5064B773aa1d29',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAcryptos',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_acryptos_style_boosts],
            'vaults' : [external_contracts.get_acryptos_vaults, external_contracts.get_acryptos_vaults],
            'args' : [
                {
                    'farm_id' : '0xAcryptos',
                    'network' : 'bsc',
                    '_pps' : 'getPricePerFullShare'
                    },
                {
                    'farm_id' : '0xAcryptos',
                    'network' : 'bsc',
                    'caller' : '0xb1fa5d3c0111d8E9ac43A19ef17b281D5D4b474E',
                    'pfunc' : 'pendingSushi'
                    }],
            'vault_args' : [{}, {}]
        }
    },
                '0x9BFD897e3eabFfA738a8F1c4d0B397C07E97E42D' : {
        'name' : 'gemstones.finance',
        'rewardToken' : '0x0d962a1a2a27b402e4d84772dea65ac8592eb6bf',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGemstones',
        'perBlock' : 'gemstonesPerBlock',
        'masterChef' : '0x9BFD897e3eabFfA738a8F1c4d0B397C07E97E42D',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xF4168CD3C00799bEeB9a88a6bF725eB84f5d41b7' : {
        'name' : 'thoreum.finance',
        'rewardToken' : '0x580de58c1bd593a43dadcf0a739d504621817c05',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingThoreum',
        'masterChef' : '0xF4168CD3C00799bEeB9a88a6bF725eB84f5d41b7',
        'perBlock' : 'thoreumPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_thunder_pools],
            'args' : [
                {
                    'farm_id' : '0xF4168CD3C00799bEeB9a88a6bF725eB84f5d41b7',
                    'network_id' : 'bsc',
                    }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xCc7E7c9FC775D25176e9Bfc5A400EdAc212aa81C' : {
        'name' : 'polypup.finance',
        'rewardToken' : '0xcfe2cf35d2bdde84967e67d00ad74237e234ce59',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPup',
        'perBlock' : 'PupPerBlock',
        'masterChef' : '0xCc7E7c9FC775D25176e9Bfc5A400EdAc212aa81C',
        'featured' : 2,
        'network' : 'matic',
        'add_chefs' : ['0x9DcB2D5e7b5212fAF98e4a152827fd76bD55f68b']
    },
                '0x9DcB2D5e7b5212fAF98e4a152827fd76bD55f68b' : {
        'name' : 'polypup.finance (Layer 2)',
        'rewardToken' : '0x6bb45ceac714c52342ef73ec663479da35934bf7',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBone',
        'perBlock' : 'BonePerBlock',
        'masterChef' : '0x9DcB2D5e7b5212fAF98e4a152827fd76bD55f68b',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xB5F383998d4E58C140c15C441c75bB79170b6b45' : {
        'name' : 'polypup.finance (Layer 3)',
        'rewardToken' : '0x883abe4168705d2e5da925d28538b7a6aa9d8419',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBall',
        'masterChef' : '0xB5F383998d4E58C140c15C441c75bB79170b6b45',
        'perBlock' : 'BallPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xPYQ' : {
        'name' : 'polyquity.org',
        'rewardToken' : '0x5a3064cbdccf428ae907796cf6ad5a664cd7f3d8',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPYQ',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pyq_trove, farm_templates.get_pyq_triple_staking, farm_templates.get_pyq_double_staking, farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_pyq_trove, external_contracts.get_pyq_triple, external_contracts.get_pyq_double, external_contracts.get_pyq_vaults],
            'args' : [
                {
                    'farm_id' : '0xPYQ',
                    'network_id' : 'matic',
                },
                {
                    'farm_id' : '0xPYQ',
                    'network_id' : 'matic',
                },
                {
                    'farm_id' : '0xPYQ',
                    'network_id' : 'matic',
                },
                {
                    'farm_id' : '0xPYQ',
                    'network' : 'matic',
                    'want_function' : 'uniToken'
                },
                ],
            'vault_args' : [{}, {}, {}, {}]
        }
    },
                '0x8e5860DF653A467D1cC5b6160Dd340E8D475724E' : {
        'name' : 'farmhero.io',
        'rewardToken' : '0xb82a20b4522680951f11c94c54b8800c1c237693',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingHERO',
        'perBlock' : 'HERORewardPerSecond',
        'apy_config' : 'second',
        'masterChef' : '0x8e5860DF653A467D1cC5b6160Dd340E8D475724E',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_farmhero_staking, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_farmhero_staking_matic, external_contracts.get_farmhero_pools_matic],
            'args' : [
                {
                    'farm_id' : '0x8e5860DF653A467D1cC5b6160Dd340E8D475724E',
                    'network' : 'matic',
                },
                {
                    'farm_id' : '0x8e5860DF653A467D1cC5b6160Dd340E8D475724E',
                    'network' : 'matic',
                },
                ],
            'vault_args' : [{}, {}]
        }
    },
                '0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D' : {
        'name' : 'farmhero.io',
        'rewardToken' : '0x9b26e16377ad29a6ccc01770bcfb56de3a36d8b2',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingHERO',
        'perBlock' : 'HERORewardPerSecond',
        'apy_config' : 'second',
        'masterChef' : '0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_farmhero_staking, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_farmhero_staking_bsc, external_contracts.get_farmhero_pools_bsc],
            'args' : [
                {
                    'farm_id' : '0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D',
                    'network' : 'bsc',
                },
                {
                    'farm_id' : '0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D',
                    'network' : 'bsc',
                },
                ],
            'vault_args' : [{}, {}]
        }
    },
                '0xDb457E7fA88C9818f6134afD673941fCE777F92F' : {
        'name' : 'farmhero.io',
        'rewardToken' : '0xc3bdfee6186849d5509601045af4af567a001c94',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingHERO',
        'perBlock' : 'HERORewardPerSecond',
        'apy_config' : 'second',
        'masterChef' : '0xDb457E7fA88C9818f6134afD673941fCE777F92F',
        'featured' : 2,
        'network' : 'oke',
        'extraFunctions' : {
            'functions' : [farm_templates.get_farmhero_staking, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_farmhero_staking_oke, external_contracts.get_farmhero_pools_oke],
            'args' : [
                {
                    'farm_id' : '0xDb457E7fA88C9818f6134afD673941fCE777F92F',
                    'network' : 'oke',
                },
                {
                    'farm_id' : '0xDb457E7fA88C9818f6134afD673941fCE777F92F',
                    'network' : 'oke',
                },
                ],
            'vault_args' : [{}, {}]
        }
    },
                '0xBalancer' : {
        'name' : 'balancer.fi',
        'rewardToken' : '0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBalancer',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_balancer_user_pools],
            'vaults' : [external_contracts.get_balancer_pools],
            'args' : [
                {
                    'farm_id' : '0xBalancer',
                    'network_id' : 'matic'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x0d17C30aFBD4d29EEF3639c7B1F009Fd6C9f1F72' : {
        'name' : 'boneswap.finance',
        'rewardToken' : '0x80244c2441779361f35803b8c711c6c8fc6054a3',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBone',
        'masterChef' : '0x0d17C30aFBD4d29EEF3639c7B1F009Fd6C9f1F72',
        'featured' : 2,
        'network' : 'matic',
        'perBlock' : 'BONE_PER_BLOCK',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_boneswap_vaults, external_contracts.get_boneswap_pools],
            'args' : [
                {
                    'farm_id' : '0x0d17C30aFBD4d29EEF3639c7B1F009Fd6C9f1F72',
                    'network' : 'matic',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo'
                },
                {
                    'farm_id' : '0x0d17C30aFBD4d29EEF3639c7B1F009Fd6C9f1F72',
                    'network_id' : 'matic',
                    'staked' : 'stakeToken',
                }
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0x8bE82Ab9B6179bE6EB88431E3E4E0fd93b9E607C' : {
        'name' : 'polyvertex.finance',
        'rewardToken' : '0x72572ccf5208b59f4bcc14e6653d8c31cd1fc5a0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'perBlock' : 'eggPerBlock',
        'masterChef' : '0x8bE82Ab9B6179bE6EB88431E3E4E0fd93b9E607C',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x0cc7fb3626c55ce4eff79045e8e7cb52434431d4' : {
        'name' : 'kuswap.finance',
        'rewardToken' : '0x4a81704d8c16d9fb0d7f61b747d0b5a272badf14',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKUS',
        'perBlock' : 'KUSPerBlock',
        'masterChef' : '0x0cc7fb3626c55ce4eff79045e8e7cb52434431d4',
        'featured' : 2,
        'network' : 'kcc'
    },
                '0x11cbc66c3dc50cb6442f3d8c8ce44e1c90cb24bf' : {
        'name' : 'kandyswap.com',
        'rewardToken' : '0x1aAAF8D0588A14f54eD3624f96205989Df091181',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'perBlock' : 'cakePerBlock',
        'masterChef' : '0x11cbc66c3dc50cb6442f3d8c8ce44e1c90cb24bf',
        'featured' : 2,
        'network' : 'kcc'
    },
                '0x4e22399070aD5aD7f7BEb7d3A7b543e8EcBf1d85' : {
        'name' : 'jetswap.finance',
        'rewardToken' : '0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'perBlock' : 'cakePerBlock',
        'masterChef' : '0x4e22399070aD5aD7f7BEb7d3A7b543e8EcBf1d85',
        'featured' : 1,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_jetswap_vaults],
            'args' : [
                {
                    'farm_id' : '0x4e22399070aD5aD7f7BEb7d3A7b543e8EcBf1d85',
                    'network' : 'matic',
                    '_pps' : 'getPricePerFullShare'
                }
                    ],
            'vault_args' : [{'network' : 'polygon'}]
        }
    },
                '0xPickle' : {
        'name' : 'pickle.finance',
        'rewardToken' : '0x2b88ad57897a8b496595925f43048301c37615da',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPickle',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pickle_chef, farm_templates.get_vault_style, farm_templates.get_vault_style],
            'vaults' : [external_contracts.dummy_vault, external_contracts.get_pickle_addresses, external_contracts.get_pickle_addresses_uni],
            'args' : [
                {
                    'farm_id' : '0xPickle',
                    'network_id' : 'matic',
                    'chef' : '0x20B2a3fc7B13cA0cCf7AF81A68a14CB3116E8749',
                    'rewarder' : '0xE28287544005094be096301E5eE6E2A6E6Ef5749'
                },
                {
                    'farm_id' : '0xPickle',
                    'network' : 'matic',
                },
                {
                    'farm_id' : '0xPickle',
                    'network' : 'matic',
                    'want_token' : 'pool'
                }
                    ],
            'vault_args' : [{},{'network' : 'polygon'},{'network' : 'polygon'}]
        }
    },
                '0xCurvePolygon' : {
        'name' : 'curve.fi',
        'rewardToken' : '0x172370d5Cd63279eFa6d502DAB29171933a610AF',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xCurvePolygon',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_curve_gauage],
            'vaults' : [external_contracts.get_curve_gauage],
            'args' : [
                {
                    'farm_id' : '0xCurvePolygon',
                    'network_id' : 'matic',
                },
                    ],
            'vault_args' : [{'network' : 'matic'}]
        }
    },
                '0xCurveFTM' : {
        'name' : 'curve.fi',
        'rewardToken' : '0x1E4F97b9f9F913c46F1632781732927B9019C68b',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xCurveFTM',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_curve_gauage],
            'vaults' : [external_contracts.get_curve_gauage],
            'args' : [
                {
                    'farm_id' : '0xCurveFTM',
                    'network_id' : 'ftm',
                    'rewards' : ['0x1E4F97b9f9F913c46F1632781732927B9019C68b', '0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83', '0xd8321aa83fb0a4ecd6348d4577431310a6e0814d']
                },
                    ],
            'vault_args' : [{'network' : 'ftm'}]
        }
    },
                '0x2c8CA5aD689E0bf86CBfc444aE1cc174300EA8f6' : {
        'name' : 'dojofarm.finance',
        'rewardToken' : '0xca9e4a7617d5fdaaa49beb8dc8e506706324e253',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingDojo',
        'perBlock' : 'dojoPerBlock',
        'masterChef' : '0x2c8CA5aD689E0bf86CBfc444aE1cc174300EA8f6',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x539938D1358a1173D9c5E1073FebfA2dD44f39d1' : {
        'name' : 'dojofarm.finance',
        'rewardToken' : '0x25a604019cf40fd1c7281e0d83856556d7226f45',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingDojo',
        'perBlock' : 'dojoPerBlock',
        'masterChef' : '0x539938D1358a1173D9c5E1073FebfA2dD44f39d1',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xTelx' : {
        'name' : 'telx.network',
        'rewardToken' : '0xdf7837de1f2fa4631d716cf2502f8b230f1dcc32',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xTelx',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_telx_single, farm_templates.get_telx_double],
            'vaults' : [external_contracts.get_telx, external_contracts.get_telx],
            'args' : [
                {
                    'farm_id' : '0xTelx',
                    'network_id' : 'matic',
                },
                {
                    'farm_id' : '0xTelx',
                    'network_id' : 'matic',
                },
                    ],
            'vault_args' : [{'style' : 'single'},{'style' : 'double'}]
        }
    },
                '0xb49036Fb35b4E1572509f301e1b0fd0113771ffa' : {
        'name' : 'harvester.app',
        'rewardToken' : '0x316b4db72ec7eacdb6e998257c4349c2b08ff27d',
        'decimal' : 18,
        'stakedFunction' : 'farmers',
        'pendingFunction' : 'pendingCrops',
        'poolFunction' : 'farmsCount',
        'poolLength' : 'farmsCount',
        'want' : 'farms',
        'alloc_offset' : 2,
        'wantFunction' : 'farms',
        'perBlock' : 'cropPerBlock',
        'rewardSymbol' : '🌾',
        'masterChef' : '0xb49036Fb35b4E1572509f301e1b0fd0113771ffa',
        'featured' : 2,
        'network' : 'matic',
        'show' : False
    },
                '0xHarvester' : {
        'name' : 'harvester.app',
        'rewardToken' : '0x316b4db72ec7eacdb6e998257c4349c2b08ff27d',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xHarvester',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xHarvester',
                    'network_id' : 'matic',
                    'farm_data' : {
                                    'name' : 'harvester.app',
                                    'rewardToken' : '0x316b4db72ec7eacdb6e998257c4349c2b08ff27d',
                                    'decimal' : 18,
                                    'stakedFunction' : 'farmers',
                                    'pendingFunction' : 'pendingCrops',
                                    'poolFunction' : 'farmsCount',
                                    'wantFunction' : 'farms',
                                    'rewardSymbol' : '🌾',
                                    'masterChef' : '0xb49036Fb35b4E1572509f301e1b0fd0113771ffa',
                                    'featured' : 2,
                                    'network' : 'matic',
                                    'show' : False
                                    },
                            },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xBlackSwan' : {
        'name' : 'blackswan.network',
        'rewardToken' : '0xab7589dE4C581Db0fb265e25a8e7809D84cCd7E8',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBlackSwan',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_blackswan_stakes],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [{}],
            'vault_args' : [{}]
        }
    },
                '0xd4DC714a68638ffc5EC24441FE37e9dDa677467a' : {
        'name' : 'robinhoodswap.finance',
        'rewardToken' : '0xd5779f2f9d7d239228e4e78bc78f50768661a081',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingRbh',
        'masterChef' : '0xd4DC714a68638ffc5EC24441FE37e9dDa677467a',
        'perBlock' : 'rbhPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x6CB1Cdbae9a20413e37aF1491507cd5faE2DdD3e' : {
        'name' : 'block-mine.io',
        'rewardToken' : '0xE0B58022487131eC9913C1F3AcFD8F74FC6A6C7E',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x6CB1Cdbae9a20413e37aF1491507cd5faE2DdD3e',
        'perBlock' : 'nuggetPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef, farm_templates.get_syrup_pools, farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault, external_contracts.get_blockmine, external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0x6CB1Cdbae9a20413e37aF1491507cd5faE2DdD3e',
                        'network_id' : 'bsc',
                        'farm_data' : {
                                        'name' : 'block-mine.io refinery',
                                        'rewardToken' : '0xf2f02f60fd1a376270e777aa2a4667329e3984ed',
                                        'decimal' : 18,
                                        'stakedFunction' : 'userInfo',
                                        'pendingFunction' : 'pendingCake',
                                        'masterChef' : '0x2937c747Bc64B9E4DeBe5E7A4bA9bEAE33B91126',
                                        'featured' : 2,
                                        'network' : 'bsc',
                                        'rewardSymbol' : 'GOLDCOIN',
                                        'show' : False
                                    }
                    },
                    {
                        'farm_id' : '0x6CB1Cdbae9a20413e37aF1491507cd5faE2DdD3e',
                        'network_id' : 'bsc',
                        'staked' : 'stakeToken',
                        'reward' : 'rewardToken',
                        'pending_reward' : 'pendingReward'
                    },
                    {
                        'farm_id' : '0x6CB1Cdbae9a20413e37aF1491507cd5faE2DdD3e',
                        'network_id' : 'bsc',
                        'farm_data' : {
                                        'name' : 'block-mine.io refinery',
                                        'rewardToken' : '0x24f6ECAF0B9E99D42413F518812d2c4f3EeFEB12',
                                        'decimal' : 18,
                                        'stakedFunction' : 'userInfo',
                                        'pendingFunction' : 'pendingCake',
                                        'masterChef' : '0x646Bc159130F6bDCbB312ecb9E9984Eea4A67D4b',
                                        'featured' : 2,
                                        'network' : 'bsc',
                                        'rewardSymbol' : 'GOLDBAR',
                                        'show' : False
                                    }
                    },                    
                    ],
            'vault_args' : [{},{},{}]
        }

    },
                '0x2937c747Bc64B9E4DeBe5E7A4bA9bEAE33B91126' : {
        'name' : 'block-mine.io refinery',
        'rewardToken' : '0xf2f02f60fd1a376270e777aa2a4667329e3984ed',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x2937c747Bc64B9E4DeBe5E7A4bA9bEAE33B91126',
        'featured' : 2,
        'network' : 'bsc',
        'rewardSymbol' : 'GOLDCOIN',
        'perBlock' : None,
        'show' : False
    },
                '0xPaprBSC' : {
        'name' : 'paprprintr.finance',
        'rewardToken' : '0x246475dF8703BE0C2bA2f8d0fb7248D95Cc1Ba26',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPaprBSC',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_syrup_pools, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_paprprintr_vaults, external_contracts.get_papr_native_bsc, external_contracts.get_papr_print_bsc],
            'args' : [
                    {
                        'farm_id' : '0xPaprBSC',
                        'network' : 'bsc',
                        '_pps' : 'getPricePerFullShare',
                        '_strict' : True
                    },
                    {
                        'farm_id' : '0xPaprBSC',
                        'network_id' : 'bsc',
                        'staked' : 'trustedDepositTokenAddress',
                        'reward' : 'trustedRewardTokenAddress',
                        'pending_reward' : 'getEstimatedPendingDivs',
                        'user_info' : 'depositedTokens'
                    },
                    {
                        'farm_id' : '0xPaprBSC',
                        'network_id' : 'bsc',
                        'staked' : 'share',
                        'reward' : 'cash',
                        'pending_reward' : 'earned',
                        'user_info' : 'balanceOf'
                    },               
                    ],
            'vault_args' : [{'network': 56},{},{}]
        }
    },
                '0xPaprMatic' : {
        'name' : 'paprprintr.finance',
        'rewardToken' : '0xFbe49330E7B9F58a822788F86c1be38Ab902Bab1',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPaprMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_syrup_pools, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_paprprintr_vaults, external_contracts.get_papr_native_matic, external_contracts.get_papr_print_matic],
            'args' : [
                    {
                        'farm_id' : '0xPaprMatic',
                        'network' : 'matic',
                        '_pps' : 'getPricePerFullShare',
                        '_strict' : True
                    },
                    {
                        'farm_id' : '0xPaprMatic',
                        'network_id' : 'matic',
                        'staked' : 'trustedDepositTokenAddress',
                        'reward' : 'trustedRewardTokenAddress',
                        'pending_reward' : 'getEstimatedPendingDivs',
                        'user_info' : 'depositedTokens'
                    },
                    {
                        'farm_id' : '0xPaprMatic',
                        'network_id' : 'matic',
                        'staked' : 'share',
                        'reward' : 'cash',
                        'pending_reward' : 'earned',
                        'user_info' : 'balanceOf'
                    },               
                    ],
            'vault_args' : [{'network': 137},{},{}]
        }
    },
                '0xPaprKCC' : {
        'name' : 'paprprintr.finance',
        'rewardToken' : '0x4446fc4eb47f2f6586f9faab68b3498f86c07521',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPaprKCC',
        'featured' : 2,
        'network' : 'kcc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_paprprintr_vaults],
            'args' : [
                    {
                        'farm_id' : '0xPaprKCC',
                        'network' : 'kcc',
                        '_pps' : 'getPricePerFullShare',
                        '_strict' : True
                    },     
                    ],
            'vault_args' : [{'network': 321}]
        }
    },
                '0x1948abC5400Aa1d72223882958Da3bec643fb4E5' : {
        'name' : 'dinoswap.exchange',
        'rewardToken' : '0xaa9654becca45b5bdfa5ac646c939c62b527d394',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingDino',
        'masterChef' : '0x1948abC5400Aa1d72223882958Da3bec643fb4E5',
        'perBlock' : 'dinoPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_dino_pools],
            'args' : [
                    {
                        'farm_id' : '0x1948abC5400Aa1d72223882958Da3bec643fb4E5',
                        'network_id' : 'matic',
                        'staked' : 'DINO',
                        'reward' : 'REWARD',
                        'pending_reward' : 'pendingReward'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x3C58EA8D37f4fc6882F678f822E383Df39260937' : {
        'name' : 'polyroll.org',
        'rewardToken' : '0xc68e83a305b0fad69e264a1769a0a070f190d2d6',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingRoll',
        'masterChef' : '0x3C58EA8D37f4fc6882F678f822E383Df39260937',
        'perBlock' : 'rollPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xUniswapETH' : {
        'name' : 'uniswap.org',
        'rewardToken' : '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xUniswapETH',
        'featured' : 2,
        'network' : 'eth',
        'extraFunctions' : {
            'functions' : [uniswapv3.get_uniswap_v3_positions],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0xUniswapETH',
                        'network' : 'eth',
                        'uniswap_nft' : '0xc36442b4a4522e871399cd717abdd847ab11fe88',
                        'uniswap_factory' : '0x1F98431c8aD98523631AE4a59f267346ea31F984',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xb12FeFC21b12dF492609942172412d4b75CbC709' : {
        'name' : 'pearzap.com',
        'rewardToken' : '0xc8bcb58caef1be972c0b638b1dd8b0748fdc8a44',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPear',
        'masterChef' : '0xb12FeFC21b12dF492609942172412d4b75CbC709',
        'perBlock' : 'pearPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xd6D8EBf01b79EE3fC1Ab76Dc3eA79bcB209205E4' : {
        'name' : 'pearzap.com',
        'rewardToken' : '0xdf7c18ed59ea738070e665ac3f5c258dcc2fbad8',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPear',
        'masterChef' : '0xd6D8EBf01b79EE3fC1Ab76Dc3eA79bcB209205E4',
        'perBlock' : 'pearPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x723f61a9bcd6c390474d0d2b3d5e65e1f9ada824' : {
        'name' : 'boneswap.finance',
        'rewardToken' : '0x6C1B568A1D7Fb33DE6707238803F8821E9472539',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBone',
        'masterChef' : '0x723f61a9bcd6c390474d0d2b3d5e65e1f9ada824',
        'perBlock' : 'BONE_PER_BLOCK',
        'featured' : 2,
        'network' : 'kcc'
    },
                '0xSuperFarm' : {
        'name' : 'superlauncher.io',
        'rewardToken' : '0xb5389A679151C4b8621b1098C6E0961A3CFEe8d4',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSuperFarm',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_superfarm_pools, external_contracts.get_superfarm_extra],
            'args' : [
                    {
                        'farm_id' : '0xSuperFarm',
                        'network_id' : 'bsc',
                        'staked' : '_inToken',
                        'reward' : '_rewardToken',
                        'pending_reward' : 'pendingReward',
                        'user_info' : '_userInfo'
                    },
                    {
                        'farm_id' : '0xSuperFarm',
                        'network_id' : 'bsc',
                        'staked' : 'STAKED_TOKEN',
                        'reward' : 'REWARD_TOKEN',
                        'pending_reward' : 'getTotalRewardsBalance',
                        'user_info' : 'balanceOf'
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0xPandaSwap' : {
        'name' : 'pandaex.org',
        'rewardToken' : '0x8eac9d49f71a9393ed38a619038e880c86d5745c',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPandaSwap',
        'featured' : 2,
        'network' : 'oke',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_pandaswap_farms],
            'args' : [
                    {
                        'farm_id' : '0xPandaSwap',
                        'network_id' : 'oke',
                        'staked' : 'lpt',
                        'reward' : 'sharetoken',
                        'pending_reward' : 'earned',
                        'user_info' : 'balanceOf'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x8cddb4cd757048c4380ae6a69db8cd5597442f7b' : {
        'name' : 'cherryswap.net',
        'rewardToken' : '0x8179d97eb6488860d816e3ecafe694a4153f216c',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCherry',
        'masterChef' : '0x8cddb4cd757048c4380ae6a69db8cd5597442f7b',
        'perBlock' : 'cherryPerBlock',
        'featured' : 2,
        'network' : 'oke',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_cherry_farms],
            'args' : [
                    {
                        'farm_id' : '0x8cddb4cd757048c4380ae6a69db8cd5597442f7b',
                        'network_id' : 'oke',
                        'staked' : 'syrup',
                        'reward' : 'rewardToken',
                        'pending_reward' : 'pendingReward',
                        'user_info' : 'userInfo'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xaEBa5C691aF30b7108D9C277d6BB47347387Dc13' : {
        'name' : 'kswap.finance',
        'rewardToken' : '0xab0d1578216A545532882e420A8C61Ea07B00B12',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKst',
        'poolLength' : 'getPairsLength',
        'masterChef' : '0xaEBa5C691aF30b7108D9C277d6BB47347387Dc13',
        'featured' : 2,
        'network' : 'oke',
        'perBlock' : 'kstPerBlock',
        'add_chefs' : ['0x5E6D7c01824C64C4BC7f2FF42C300871ce6Ff555','0x1FcCEabCd2dDaDEa61Ae30a2f1c2D67A05fDDa29']
    },
                '0x5E6D7c01824C64C4BC7f2FF42C300871ce6Ff555' : {
        'name' : 'kswap.finance (Deposit Pool)',
        'rewardToken' : '0xab0d1578216A545532882e420A8C61Ea07B00B12',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKst',
        'poolLength' : 'getTokensLength',
        'masterChef' : '0x5E6D7c01824C64C4BC7f2FF42C300871ce6Ff555',
        'featured' : 2,
        'network' : 'oke',
        'perBlock' : 'kstPerBlock',
        'show' : False
    },
                '0x1FcCEabCd2dDaDEa61Ae30a2f1c2D67A05fDDa29' : {
        'name' : 'kswap.finance (Trading Pool)',
        'rewardToken' : '0xab0d1578216A545532882e420A8C61Ea07B00B12',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKst',
        'poolLength' : 'getPairsLength',
        'masterChef' : '0x1FcCEabCd2dDaDEa61Ae30a2f1c2D67A05fDDa29',
        'featured' : 2,
        'network' : 'oke',
        'perBlock' : 'kstPerBlock',
        'show' : False
    },
                '0x41C4dFA389e8c43BA6220aa62021ed246d441306' : {
        'name' : 'timeleap.finance',
        'rewardToken' : '0x5c59d7cb794471a9633391c4927ade06b8787a90',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTime',
        'masterChef' : '0x41C4dFA389e8c43BA6220aa62021ed246d441306',
        'featured' : 2,
        'perBlock' : 'timePerBlock',
        'network' : 'matic'
    },
                '0x939a890BCdAB6D337af9612EaBbbdaeC5CA3a4FE' : {
        'name' : 'suncrypto.finance',
        'rewardToken' : '0xbF7413FaACAf0099E1BdEb0Cef87C9ec4aAFD434',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingToken',
        'masterChef' : '0x939a890BCdAB6D337af9612EaBbbdaeC5CA3a4FE',
        'perBlock' : 'tokenPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xfcD73006121333C92D770662745146338E419556' : {
        'name' : 'polywantsacracker.farm',
        'rewardToken' : '0xfe1a200637464fbc9b60bc7aecb9b86c0e1d486e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLith',
        'masterChef' : '0xfcD73006121333C92D770662745146338E419556',
        'perBlock' : 'lithPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xd90A8878a2277879600AA2cba0CADC7E1a11354D' : {
        'name' : 'feeder.finance',
        'rewardToken' : '0x67d66e8ec1fd25d98b3ccd3b19b7dc4b4b7fc493',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingFeed',
        'masterChef' : '0xd90A8878a2277879600AA2cba0CADC7E1a11354D',
        'perBlock' : 'feedPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_feeder_style, farm_templates.get_sfeed],
            'vaults' : [external_contracts.get_feeder_auto, external_contracts.get_feeder_sfeed],
            'args' : [
                    {
                        'farm_id' : '0xd90A8878a2277879600AA2cba0CADC7E1a11354D',
                        'network' : 'bsc',
                    },
                    {
                        'farm_id' : '0xd90A8878a2277879600AA2cba0CADC7E1a11354D',
                        'network' : 'bsc',
                        'receipt_token' : '0xEb9902A19Fa1286c8832bF44e9B18E89f682f614'
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0xAcC0a63B1C3DD9D9396BC4e78ea382d30E0DcE21' : {
        'name' : 'cobra.exchange',
        'rewardToken' : '0x2c449ba613873e7b980faf2b686207d7bd205541',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0xAcC0a63B1C3DD9D9396BC4e78ea382d30E0DcE21',
        'perBlock' : 'REWARD_PER_BLOCK',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78' : {
        'name' : 'polygonfarm.finance',
        'rewardToken' : '0xf5ea626334037a2cf0155d49ea6462fddc6eff19',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSpade',
        'masterChef' : '0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78',
        'perBlock' : 'SpadePerBlock',
        'featured' : 2,
        'network' : 'matic',
        'add_chefs' : ['0x0B14C435DC29f2e3F53E203a18077F4A41914870', '0x9581EA83B4BCd5F2c5f1705382FBd80a11E57DcD'],
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_polygonfarm_pools, external_contracts.get_polygonfarm_staking],
            'args' : [
                    {
                        'farm_id' : '0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78',
                        'network_id' : 'matic',
                        'staked' : 'poolInfo',
                        'reward' : 'rewardToken',
                        'pending_reward' : 'pendingReward',
                        'user_info' : 'userInfo'
                    },
                    {
                        'farm_id' : '0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78',
                        'network' : 'matic',
                        '_pps' : 'getPricePerFullShare',
                        '_stake' : 'userInfo'
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0x0B14C435DC29f2e3F53E203a18077F4A41914870' : {
        'name' : 'polyalpha.finance',
        'rewardToken' : '0x0b048d6e01a6b9002c291060bf2179938fd8264c',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingAlpha',
        'masterChef' : '0x0B14C435DC29f2e3F53E203a18077F4A41914870',
        'featured' : 2,
        'network' : 'matic',
        'perBlock' : 'AlphaPerBlock',
        'show' : False,
    },
                '0x9581EA83B4BCd5F2c5f1705382FBd80a11E57DcD' : {
        'name' : 'polybeta.finance',
        'rewardToken' : '0xac3090b7042fca2cdbf233022e4a9823a032600c',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBeta',
        'masterChef' : '0x9581EA83B4BCd5F2c5f1705382FBd80a11E57DcD',
        'perBlock' : 'BetaPerBlock',
        'featured' : 2,
        'network' : 'matic',
        'show' : False,
    },
                '0xF23053191FcA049f04926dBb108F86Cc61A4F77D' : {
        'name' : 'polyyork.finance',
        'rewardToken' : '0x21dE43d96CFddd203DA3352545E0054534776652',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEgg',
        'masterChef' : '0xF23053191FcA049f04926dBb108F86Cc61A4F77D',
        'perBlock' : 'eggPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xdA30Aae916417C9Ad8DE97Bb1d59395f2Dd905e4' : {
        'name' : 'polyfund.finance',
        'rewardToken' : '0x4b0f2da2c4e7cc60f3b918461ec4f16ccc974622',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingToken',
        'masterChef' : '0xdA30Aae916417C9Ad8DE97Bb1d59395f2Dd905e4',
        'featured' : 2,
        'perBlock' : 'getEmissionRate',
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_polyfund_vault],
            'args' : [
                    {
                        'farm_id' : '0xdA30Aae916417C9Ad8DE97Bb1d59395f2Dd905e4',
                        'network' : 'matic',
                        '_pps' : 'getPricePerFullShare',
                        '_stake' : 'userInfo'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xIronLend' : {
        'name' : 'iron.finance (IronLend)',
        'rewardToken' : '0x4A81f8796e0c6Ad4877A51C86693B0dE8093F2ef',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xIronLend',
        'featured' : 2,
        'network' : 'matic',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_lending_protocol, farm_templates.get_just_pending],
            'vaults' : [external_contracts.get_ironlend_vaults, external_contracts.get_ironlend_rewards],
            'args' : [
                    {
                        'farm_id' : '0xIronLend',
                        'network' : 'matic',
                    },
                    {
                        'farm_id' : '0xIronLend',
                        'network' : 'matic',
                        'reward_method' : 'calculateReward',
                        'reward_token' : '0x4A81f8796e0c6Ad4877A51C86693B0dE8093F2ef'
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0x67da5f2ffaddff067ab9d5f025f8810634d84287' : {
        'name' : 'sushi.com',
        'rewardToken' : '0xBEC775Cb42AbFa4288dE81F387a9b1A3c4Bc552A',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0x67da5f2ffaddff067ab9d5f025f8810634d84287',
        'featured' : 2,
        'perBlock' : None,
        'network' : 'harmony',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sushi_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0x67da5f2ffaddff067ab9d5f025f8810634d84287',
                    'network_id' : 'harmony',
                    'farm_data' :{
                        'masterChef' : '0x67da5f2ffaddff067ab9d5f025f8810634d84287',
                        'rewarder' : '0x25836011bbc0d5b6db96b20361a474cbc5245b45',
                        'r0sym' : 'SUSHI',
                        'r1sym' : 'WONE',
                        'r0t' : '0xBEC775Cb42AbFa4288dE81F387a9b1A3c4Bc552A',
                        'r1t' : '0xcf664087a5bb0237a0bad6742852ec6c8d69a27a'
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x8A4f4c7F4804D30c718a76B3fde75f2e0cFd8712' : {
        'name' : 'shibanova.io',
        'rewardToken' : '0x56e344be9a7a7a1d27c854628483efd67c11214f',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingNova',
        'masterChef' : '0x8A4f4c7F4804D30c718a76B3fde75f2e0cFd8712',
        'featured' : 2,
        'network' : 'bsc',
        'perBlock' : 'NovaPerBlock',
        'extraFunctions' : {
            'functions' : [farm_templates.get_moneypot],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0x8A4f4c7F4804D30c718a76B3fde75f2e0cFd8712',
                        'network_id' : 'bsc',
                        'rewards' : [{'address' : '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', 'symbol' : 'WBNB'}, {'address' : '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56', 'symbol' : 'BUSD'}],
                        'contract' : '0xAD07Cf266C99d0cC379D4f460F0FF27b81314238',
                        'token_pair' : '0x0c0bf2bd544566a11f59dc70a8f43659ac2fe7c2'
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0xRugZombie' : {
        'name' : 'rugzombie.io',
        'rewardToken' : '0x50ba8bf9e34f0f83f96a340387d1d3888ba4b3b5',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xRugZombie',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_zombie_masterchef, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.dummy_vault, external_contracts.get_zombie_pools],
            'args' : [
                    {
                        'farm_id' : '0xRugZombie',
                        'network_id' : 'bsc',
                        'chef' : '0x590Ea7699A4E9EaD728F975efC573f6E34a5dC7B'
                    },
                    {
                        'farm_id' : '0xRugZombie',
                        'network_id' : 'bsc',
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0x83C35EA2C32293aFb24aeB62a14fFE920C2259ab' : {
        'name' : 'jswap.finance',
        'rewardToken' : '0x5fac926bf1e638944bb16fb5b787b5ba4bc85b0a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingJf',
        'masterChef' : '0x83C35EA2C32293aFb24aeB62a14fFE920C2259ab',
        'featured' : 2,
        'network' : 'oke',
        'perBlock' : 'jfPerBlock',
        'add_chefs' : ['0x4e864E36Bb552BD1Bf7bcB71A25d8c96536Af7e3', '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4']
    },
                '0x4e864E36Bb552BD1Bf7bcB71A25d8c96536Af7e3' : {
        'name' : 'jswap.finance (Deposit Pool)',
        'rewardToken' : '0x5fac926bf1e638944bb16fb5b787b5ba4bc85b0a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingJf',
        'masterChef' : '0x4e864E36Bb552BD1Bf7bcB71A25d8c96536Af7e3',
        'featured' : 2,
        'network' : 'oke',
        'perBlock' : 'jfPerBlock',
        'show' : False
    },
                '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4' : {
        'name' : 'jswap.finance (Trading Pool)',
        'rewardToken' : '0x5fac926bf1e638944bb16fb5b787b5ba4bc85b0a',
        'decimal' : 18,
        'stakedFunction' : 'userPoolPending',
        'pendingFunction' : 'userPoolPending',
        'masterChef' : '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4',
        'featured' : 2,
        'network' : 'oke',
        'perBlock' : 'jfPerBlock',
        'show' : False
    },
                '0x29e6b6acb00ef1cdfebdc5a2d3731f791b85b207' : {
        'name' : 'tenguswap.com',
        'rewardToken' : '0x6f6350d5d347aa8f7e9731756b60b774a7acf95b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTengu',
        'masterChef' : '0x29e6b6acb00ef1cdfebdc5a2d3731f791b85b207',
        'featured' : 2,
        'perBlock' : 'tenguPerBlock',
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_tengu_stakes],
            'args' : [
                    {
                        'farm_id' : '0x29e6b6acb00ef1cdfebdc5a2d3731f791b85b207',
                        'network_id' : 'bsc'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xStadiumArcadium' : {
        'name' : 'stadiumarcadium.farm',
        'rewardToken' : '0x3f374ed3c8e61a0d250f275609be2219005c021e',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xStadiumArcadium',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_multireward_masterchef],
            'vaults' : [external_contracts.stadium_farm_info],
            'args' : [
                    {
                        'farm_id' : '0xStadiumArcadium',
                        'network_id' : 'matic'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xDarksideFinance' : {
        'name' : 'darkside.finance',
        'rewardToken' : '0x1942b8262a0683b54f4f91d0c08ddd92ed6e8fe6',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xDarksideFinance',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_multireward_masterchef],
            'vaults' : [external_contracts.darkside_info],
            'args' : [
                    {
                        'farm_id' : '0xDarksideFinance',
                        'network_id' : 'matic'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xConvexETH' : {
        'name' : 'convexfinance.com',
        'rewardToken' : '0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xConvexETH',
        'featured' : 2,
        'network' : 'eth',
        'extraFunctions' : {
            'functions' : [farm_templates.get_convex],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0xConvexETH',
                        'network_id' : 'eth',
                        'booster' : '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xc3D910c9D2bB024931a44Cf127B6231aC1F04de3' : {
        'name' : 'honeyfarm.finance',
        'rewardToken' : '0xc3eae9b061aa0e1b9bd3436080dc57d2d63fedc1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingEarnings',
        'masterChef' : '0xc3D910c9D2bB024931a44Cf127B6231aC1F04de3',
        'perBlock' : 'EarningsPerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xMoonPot' : {
        'name' : 'moonpot.com',
        'rewardToken' : '0x3fcca8648651e5b974dd6d3e50f61567779772a8',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xMoonPot',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_moonpot_contracts],
            'vaults' : [external_contracts.moonpot_contracts],
            'args' : [
                    {
                        'farm_id' : '0xMoonPot',
                        'network_id' : 'bsc',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xBb3f43008e277543353588Ca2A4941F12e3CaCC0' : {
        'name' : 'afksystem.finance',
        'rewardToken' : '0xbc7cb585346f4f59d07121bb9ed7358076243539',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingSilver',
        'masterChef' : '0xBb3f43008e277543353588Ca2A4941F12e3CaCC0',
        'death_index' : [51],
        'featured' : 2,
        'perBlock' : 'silverPerBlock',
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0xBb3f43008e277543353588Ca2A4941F12e3CaCC0',
                        'network_id' : 'matic',
                        'farm_data' : {
                                        'name' : 'afksystem.finance (boss fights)',
                                        'rewardToken' : '0xbc7cb585346f4f59d07121bb9ed7358076243539',
                                        'decimal' : 18,
                                        'stakedFunction' : 'userInfo',
                                        'pendingFunction' : 'pendingSilver',
                                        'masterChef' : '0x6A08491e01b36D116c332C87253a78e6480f7f6D',
                                        'featured' : 2,
                                        'rewardSymbol' : 'SILVER',
                                        'network' : 'matic',
                                        'show' : False
                                    },
                            },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x6A08491e01b36D116c332C87253a78e6480f7f6D' : {
        'name' : 'afksystem.finance (boss fights)',
        'rewardToken' : '0xbc7cb585346f4f59d07121bb9ed7358076243539',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSilver',
        'masterChef' : '0x6A08491e01b36D116c332C87253a78e6480f7f6D',
        'featured' : 2,
        'rewardSymbol' : 'SILVER',
        'perBlock' : 'silverPerBlock',
        'network' : 'matic',
        'show' : False
    },
                '0x8AC8ED5839ba269Be2619FfeB3507baB6275C257' : {
        'name' : 'penguinfinance.org',
        'rewardToken' : '0xe896cdeaac9615145c0ca09c8cd5c25bced6384c',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPEFI',
        'perBlock' : 'pefiPerBlock',
        'masterChef' : '0x8AC8ED5839ba269Be2619FfeB3507baB6275C257',
        'featured' : 2,
        'network' : 'avax'
    },
                '0xPNG' : {
        'name' : 'pangolin.exchange',
        'rewardToken' : '0x60781c2586d68229fde47564546784ab3faca982',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPNG',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.png_staking],
            'args' : [
                    {
                        'farm_id' : '0xPNG',
                        'network' : 'avax',
                    }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xTraderJoe' : {
        'name' : 'traderjoexyz.com',
        'rewardToken' : '0x6e84a6216ea6dacc71ee8e6b0a5b7322eebc0fdd',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xTraderJoe',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_traderjoe_masterchef, farm_templates.get_traderjoe_masterchef],
            'vaults' : [external_contracts.dummy_vault, external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0xTraderJoe',
                        'network_id' : 'avax',
                        'masterchef' : '0xd6a4F121CA35509aF06A0Be99093d08462f53052'
                    },
                    {
                        'farm_id' : '0xTraderJoe',
                        'network_id' : 'avax',
                        'masterchef' : '0x188bED1968b795d5c9022F6a0bb5931Ac4c18F00'
                    }
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0x0cf605484A512d3F3435fed77AB5ddC0525Daf5f' : {
        'name' : 'yieldyak.com',
        'rewardToken' : '0x59414b3089ce2AF0010e7523Dea7E2b35d776ec7',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingRewards',
        'masterChef' : '0x0cf605484A512d3F3435fed77AB5ddC0525Daf5f',
        'featured' : 2,
        'perBlock' : 'rewardsPerSecond',
        'apy_config' : 'second',
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style_custom_pps],
            'vaults' : [external_contracts.yak_vaults],
            'args' : [
                    {
                        'farm_id' : '0x0cf605484A512d3F3435fed77AB5ddC0525Daf5f',
                        'network_id' : 'avax',
                    },
                    ],
            'vault_args' : [{}]
        }

    },
                '0xBenqi' : {
        'name' : 'benqi.fi',
        'rewardToken' : '0x8729438eb15e2c8b576fcc6aecda6a148776c0f5',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBenqi',
        'featured' : 2,
        'network' : 'avax',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_lending_protocol],
            'vaults' : [external_contracts.get_benqi_vaults],
            'args' : [
                    {
                        'farm_id' : '0xBenqi',
                        'network' : 'avax',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xSnowball' : {
        'name' : 'snowball.network',
        'rewardToken' : '0xc38f41a296a4493ff429f1238e030924a1542e50',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSnowball',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_snowball_globe, external_contracts.get_snowball_guage],
            'args' : [
                    {
                        'farm_id' : '0xSnowball',
                        'network' : 'avax',
                        '_pps' : 'getRatio',
                        '_stake' : 'balanceOf',
                        'want_token' : 'token'
                    },
                    {
                        'farm_id' : '0xSnowball',
                        'network_id' : 'avax',
                        'staked' : 'TOKEN',
                        'reward' : 'SNOWBALL',
                        'pending_reward' : 'earned',
                        'user_info' : 'balanceOf'
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0x0Ec74989E6f0014D269132267cd7c5B901303306' : {
        'name' : 'polyshield.finance',
        'rewardToken' : '0xf239e69ce434c7fb408b05a0da416b14917d934e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingShield',
        'masterChef' : '0x0Ec74989E6f0014D269132267cd7c5B901303306',
        'perBlock' : 'shieldPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x87f1b38D0C158abe2F390E5E3482FDb97bC8D0C5' : {
        'name' : 'frostfinance.farm',
        'rewardToken' : '0x21c5402c3b7d40c89cc472c9df5dd7e51bbab1b1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTUNDRA',
        'masterChef' : '0x87f1b38D0C158abe2F390E5E3482FDb97bC8D0C5',
        'perBlock' : 'TUNDRAPerBlock',
        'featured' : 2,
        'network' : 'avax'
    },
                '0xA375495919205251a05f3B259B4D3cc30a4d3ED5' : {
        'name' : 'polypulsar.farm (Gamma)',
        'rewardToken' : '0x40ed0565ecfb14ebcdfe972624ff2364933a8ce3',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingGammaPulsar',
        'masterChef' : '0xA375495919205251a05f3B259B4D3cc30a4d3ED5',
        'perBlock' : 'gammaPulsarPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x217cF04C783818E5b15Ae0723b22Ee2415Ab5fe3' : {
        'name' : 'polypulsar.farm (Beta)',
        'rewardToken' : '0x68f044b59d96ec856ac72c29df997348c8c1fff3',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBetaPulsar',
        'masterChef' : '0x217cF04C783818E5b15Ae0723b22Ee2415Ab5fe3',
        'perBlock' : 'betaPulsarPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x7875Af1a6878bdA1C129a4e2356A3fD040418Be5' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0xf8f9efc0db77d8881500bb06ff5d6abc3070e695',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0x7875Af1a6878bdA1C129a4e2356A3fD040418Be5',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x8F5BBB2BB8c2Ee94639E55d5F41de9b4839C1280' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0xa4080f1778e69467e905b8d6f72f6e441f9e9484',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0x8F5BBB2BB8c2Ee94639E55d5F41de9b4839C1280',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0x3a01521F8E7F012eB37eAAf1cb9490a5d9e18249' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0x1f1E7c893855525b303f99bDF5c3c05Be09ca251',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0x3a01521F8E7F012eB37eAAf1cb9490a5d9e18249',
        'featured' : 2,
        'network' : 'avax'
    },
                '0xd10eF2A513cEE0Db54E959eF16cAc711470B62cF' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0x0f2D719407FdBeFF09D87557AbB7232601FD9F29',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0xd10eF2A513cEE0Db54E959eF16cAc711470B62cF',
        'featured' : 2,
        'network' : 'eth'
    },
                '0x73186f2Cf2493f20836b17b21ae79fc12934E207' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0x080f6aed32fc474dd5717105dba5ea57268f46eb',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0x73186f2Cf2493f20836b17b21ae79fc12934E207',
        'featured' : 2,
        'network' : 'arb'
    },
                '0xaeD5b25BE1c3163c907a471082640450F928DDFE' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0xe55e19fb4f2d85af758950957714292dac1e25b2',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0xaeD5b25BE1c3163c907a471082640450F928DDFE',
        'featured' : 2,
        'network' : 'ftm'
    },
                '0xaeD5b25BE1c3163c907a471082640450F928DDFE' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0xE55e19Fb4F2D85af758950957714292DAC1e25B2',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0xaeD5b25BE1c3163c907a471082640450F928DDFE',
        'featured' : 2,
        'network' : 'harmony'
    },
                '0xd5609cD0e1675331E4Fb1d43207C8d9D83AAb17C' : {
        'name' : 'synapseprotocol.com',
        'rewardToken' : '0xb554A55358fF0382Fb21F0a478C3546d1106Be8c',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSynapse',
        'wantFunction' : 'lpToken',
        'want' : 'lpToken',
        'perBlock' : 'synapsePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0xd5609cD0e1675331E4Fb1d43207C8d9D83AAb17C',
        'featured' : 2,
        'network' : 'boba'
    },
                '0xQubit' : {
        'name' : 'qbt.fi',
        'rewardToken' : '0x17b7163cf1dbd286e262ddc68b553d899b93f526',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xQubit',
        'featured' : 2,
        'network' : 'bsc',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_qubit_lending_protocol, farm_templates.get_lending_staked_rewards],
            'vaults' : [external_contracts.qubit_vaults, external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0xQubit',
                        'network' : 'bsc',
                        'snapshot' : 'accountSnapshot'
                    },
                    {
                        'farm_id' : '0xQubit',
                        'network_id' : 'bsc',
                        'accrued_function' : 'accruedQubit',
                        'locked_function' : 'balanceOf',
                        'accrue_contract' : '0xF70314eb9c7Fe7D88E6af5aa7F898b3A162dcd48',
                        'locked_contract' : '0xB8243be1D145a528687479723B394485cE3cE773',
                        'wanted_token' : '0x17b7163cf1dbd286e262ddc68b553d899b93f526'
                    },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0xPancakeHunny' : {
        'name' : 'hunny.finance',
        'rewardToken' : '0x565b72163f17849832a692a3c5928cc502f46d69',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPancakeHunny',
        'featured' : 1,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_pancake_hunny_clones],
            'vaults' : [external_contracts.get_pancakehunny],
            'args' : [
                    {
                        'farm_id' : '0xPancakeHunny',
                        'network_id' : 'bsc',
                        'hive' : '0x24320c20499535d0D7a8F6adFb08e5E3f5694417',
                        'hive_rewards' : '0x5ac6Ca0473FA5a25278898d8b72c7c90E083b32a',
                        'pending_hive' : 'pendingHunny',
                        'hive_token' : 'HUNNY'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xD05B53c621497be947b4302e64c19d01EC8dbB56' : {
        'name' : 'polyquokka.finance',
        'rewardToken' : '0x9469603f3efbcf17e4a5868d81c701bdbd222555',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingQuokka',
        'masterChef' : '0xD05B53c621497be947b4302e64c19d01EC8dbB56',
        'perBlock' : 'quokkaPerBlock',
        'featured' : 2,
        'network' : 'matic'
    },
                '0x1Dc5685088D038CCe7B826BB7688142c7b5c6DeC' : {
        'name' : 'shibcakeswap.finance',
        'rewardToken' : '0x818cee824f8caeaa05fb6a1f195935e364d52af0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x1Dc5685088D038CCe7B826BB7688142c7b5c6DeC',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xBiShare' : {
        'name' : 'bishares.finance',
        'rewardToken' : '0x19A6Da6e382b85F827088092a3DBe864d9cCba73',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBiShare',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_bishare],
            'args' : [
                    {
                        'farm_id' : '0xBiShare',
                        'network_id' : 'bsc',
                        'staked' : 'pool',
                        'stake_override' : {'0xdBf6Afe135e2C4CB599680C2F1554bBDa219CE10' : 'syrup'}
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xf03b75831397D4695a6b9dDdEEA0E578faa30907' : {
        'name' : 'solarbeam.io',
        'rewardToken' : '0x6bd193ee6d2104f14f94e2ca6efefae561a4334b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSolar',
        'masterChef' : '0xf03b75831397D4695a6b9dDdEEA0E578faa30907',
        'perBlock' : 'solarPerBlock',
        'featured' : 2,
        'network' : 'moon',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xf03b75831397D4695a6b9dDdEEA0E578faa30907',
                    'network_id' : 'moon',
                    'farm_data' :{
                        'name' : 'solarbeam.io (Vaults)',
                        'rewardToken' : '0x6bd193ee6d2104f14f94e2ca6efefae561a4334b',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingSolar',
                        'masterChef' : '0x7e6E03822D0077F3C417D33caeAc900Fc2645679',
                        'featured' : 2,
                        'network' : 'moon',
                        'wantFunction' : 'poolInfo',
                        'rewardSymbol' : 'SOLAR',
                        'show' : False
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x8064A0058EfA9af75634635d764939D87700CBa0' : {
        'name' : 'rainbowfarm.finance',
        'rewardToken' : '0xdbadf0143c56f57caf559e1cce45290a4146fda1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingRNBO',
        'masterChef' : '0x8064A0058EfA9af75634635d764939D87700CBa0',
        'featured' : 2,
        'perBlock' : 'rnboPerBlock',
        'network' : 'bsc'
    },
                '0xBufferFinance' : {
        'name' : 'buffer.finance',
        'rewardToken' : '0xa296ad1c47fe6bdc133f39555c1d1177bd51fbc5',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBufferFinance',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_buffer_vaults],
            'args' : [
                    {
                        'farm_id' : '0xBufferFinance',
                        'network_id' : 'bsc',
                        'staked' : '_inToken',
                        'reward' : '_rewardToken',
                        'user_info' : '_userInfo'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xWonderLand' : {
        'name' : 'wonderland.money',
        'rewardToken' : '0xb54f16fB19478766A268F172C9480f8da1a7c9C3',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xWonderLand',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_wonderland],
            'vaults' : [external_contracts.get_wonderland_bonds],
            'args' : [
                    {
                        'farm_id' : '0xWonderLand',
                        'network_id' : 'avax',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                    '0xdfAa0e08e357dB0153927C7EaBB492d1F60aC730' : {
        'name' : 'babyswap.finance',
        'rewardToken' : '0x53e562b9b7e5e94b81f10e96ee70ad06df3d2657',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0xdfAa0e08e357dB0153927C7EaBB492d1F60aC730',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_baby_auto],
            'args' : [
                {
                    'farm_id' : '0xdfAa0e08e357dB0153927C7EaBB492d1F60aC730',
                    'network' : 'bsc',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo'
                },                
                ],
            'vault_args' : [{}]
        }
    },
                '0xF4d73326C13a4Fc5FD7A064217e12780e9Bd62c3' : {
        'name' : 'sushi.com',
        'rewardToken' : '0xd4d42f0b6def4ce0383636770ef773390d85c61a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSushi',
        'masterChef' : '0xF4d73326C13a4Fc5FD7A064217e12780e9Bd62c3',
        'want' : 'lpToken',
        'perBlock' : 'sushiPerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'featured' : 2,
        'network' : 'arb'
    },
                '0x182CD0C6F1FaEc0aED2eA83cd0e160c8Bd4cb063' : {
        'name' : 'sushi.com',
        'rewardToken' : '0x90708b20ccc1eb95a4fa7c8b18fd2c22a0ff9e78',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSushi',
        'masterChef' : '0x182CD0C6F1FaEc0aED2eA83cd0e160c8Bd4cb063',
        'want' : 'lpToken',
        'perBlock' : 'sushiPerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'featured' : 2,
        'network' : 'fuse'
    },
                '0x9180583C1ab03587b545629dd60D2be0bf1DF4f2' : {
        'name' : 'jetswap.finance',
        'rewardToken' : '0x3d8f1accee8e263f837138829b6c4517473d0688',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0x9180583C1ab03587b545629dd60D2be0bf1DF4f2',
        'perBlock' : 'cakePerSecond',
        'apy_config' : 'second',
        'featured' : 1,
        'network' : 'ftm',
    },
                '0xca2DeAc853225f5a4dfC809Ae0B7c6e39104fCe5' : {
        'name' : 'cafeswap.finance',
        'rewardToken' : '0xb5106a3277718ecad2f20ab6b86ce0fee7a21f09',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBrew',
        'perBlock' : 'brewPerBlock',
        'masterChef' : '0xca2DeAc853225f5a4dfC809Ae0B7c6e39104fCe5',
        'featured' : 2,
        'network' : 'matic'
    },
                '0xc772955c33088a97D56d0BBf473d05267bC4feBB' : {
        'name' : 'cafeswap.finance',
        'rewardToken' : '0x790be81c3ca0e53974be2688cdb954732c9862e1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0xc772955c33088a97D56d0BBf473d05267bC4feBB',
        'perBlock' : 'cakePerBlock',
        'featured' : 2,
        'network' : 'bsc'
    },
                '0xTranChess' : {
        'name' : 'tranchess.com',
        'rewardToken' : '0x20de22029ab63cf9A7Cf5fEB2b737Ca1eE4c82A6',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xTranChess',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_tranchess],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0xTranChess',
                        'network_id' : 'bsc',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xElkAVAX' : {
        'name' : 'elk.finance',
        'rewardToken' : '0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElkAVAX',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_elk_vaults],
            'args' : [
                    {
                        'farm_id' : '0xElkAVAX',
                        'network' : 'avax',
                    },
                    ],
            'vault_args' : [{'network' : 'avax'}]
        }
    },
                '0xElkMatic' : {
        'name' : 'elk.finance',
        'rewardToken' : '0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElkMatic',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_elk_vaults],
            'args' : [
                    {
                        'farm_id' : '0xElkMatic',
                        'network' : 'matic',
                    },
                    ],
            'vault_args' : [{'network' : 'matic'}]
        }
    },
                '0xElkFTM' : {
        'name' : 'elk.finance',
        'rewardToken' : '0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElkFTM',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_elk_vaults],
            'args' : [
                    {
                        'farm_id' : '0xElkFTM',
                        'network' : 'ftm',
                    },
                    ],
            'vault_args' : [{'network' : 'ftm'}]
        }
    },
                '0xElkHECO' : {
        'name' : 'elk.finance',
        'rewardToken' : '0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElkHECO',
        'featured' : 2,
        'network' : 'heco',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_elk_vaults],
            'args' : [
                    {
                        'farm_id' : '0xElkHECO',
                        'network' : 'heco',
                    },
                    ],
            'vault_args' : [{'network' : 'heco'}]
        }
    },
                '0xElkXDAI' : {
        'name' : 'elk.finance',
        'rewardToken' : '0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElkXDAI',
        'featured' : 2,
        'network' : 'xdai',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_elk_vaults],
            'args' : [
                    {
                        'farm_id' : '0xElkXDAI',
                        'network' : 'xdai',
                    },
                    ],
            'vault_args' : [{'network' : 'xdai'}]
        }
    },
                '0xElkBSC' : {
        'name' : 'elk.finance',
        'rewardToken' : '0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElkBSC',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_elk_vaults],
            'args' : [
                    {
                        'farm_id' : '0xElkBSC',
                        'network' : 'bsc',
                    },
                    ],
            'vault_args' : [{'network' : 'bsc'}]
        }
    },
                '0xElkFUSE' : {
        'name' : 'elk.finance',
        'rewardToken' : '0xE1C110E1B1b4A1deD0cAf3E42BfBdbB7b5d7cE1C',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xElkFUSE',
        'featured' : 2,
        'network' : 'fuse',
        'extraFunctions' : {
            'functions' : [farm_templates.get_quickswap_style],
            'vaults' : [external_contracts.get_elk_vaults],
            'args' : [
                    {
                        'farm_id' : '0xElkFUSE',
                        'network' : 'fuse',
                    },
                    ],
            'vault_args' : [{'network' : 'fuse'}]
        }
    },
                '0xFcDE390bF7a8B8614EC11fa8bde7565b3E64fe0b' : {
        'name' : 'macaronswap.finance',
        'rewardToken' : '0xacb2d47827c9813ae26de80965845d80935afd0b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingMacaron',
        'masterChef' : '0xFcDE390bF7a8B8614EC11fa8bde7565b3E64fe0b',
        'perBlock' : 'macaronPerBlock',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_macaron_syrup, external_contracts.get_macaron_auto],
            'args' : [
                {
                    'farm_id' : '0xFcDE390bF7a8B8614EC11fa8bde7565b3E64fe0b',
                    'network_id' : 'bsc',
                    'staked' : 'stakingToken'
                },
                {
                    'farm_id' : '0xFcDE390bF7a8B8614EC11fa8bde7565b3E64fe0b',
                    'network' : 'bsc',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo',
                    'want_token' : 'token'
                },                
                ],
            'vault_args' : [{}, {}, {}]
        }
    },
                '0xc7dad2e953Dc7b11474151134737A007049f576E' : {
        'name' : 'morpheusswap.finance',
        'rewardToken' : '0x0789ff5ba37f72abc4d561d00648acadc897b32d',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingMorph',
        'masterChef' : '0xc7dad2e953Dc7b11474151134737A007049f576E',
        'featured' : 2,
        'network' : 'ftm',
        'perBlock' : 'morphPerSec',
        'apy_config' : 'second',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_morpheus_syrup],
            'args' : [
                {
                    'farm_id' : '0xc7dad2e953Dc7b11474151134737A007049f576E',
                    'network_id' : 'ftm',
                    'staked' : 'syrup'
                },           
                ],
            'vault_args' : [{}]
        }
    },
                '0xF43480afE9863da4AcBD4419A47D9Cc7d25A647F' : {
        'name' : 'abracadabra.money',
        'rewardToken' : '0x090185f2135308bad17527004364ebcc2d37e5f6',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingIce',
        'masterChef' : '0xF43480afE9863da4AcBD4419A47D9Cc7d25A647F',
        'perBlock' : 'icePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((address,uint256,uint256,uint32,uint16))',
        'alloc_offset' : 4,
        'featured' : 2,
        'network' : 'eth',
    },
                '0x37Cf490255082ee50845EA4Ff783Eb9b6D1622ce' : {
        'name' : 'abracadabra.money',
        'rewardToken' : '0x468003b688943977e6130f4f68f23aad939a1040',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingIce',
        'masterChef' : '0x37Cf490255082ee50845EA4Ff783Eb9b6D1622ce',
        'perBlock' : 'icePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((address,uint256,uint256,uint32,uint16))',
        'alloc_offset' : 4,
        'featured' : 2,
        'network' : 'ftm',
    },
                '0x839De324a1ab773F76a53900D70Ac1B913d2B387' : {
        'name' : 'abracadabra.money',
        'rewardToken' : '0x3e6648c5a70a150a88bce65f4ad4d506fe15d2af',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingIce',
        'masterChef' : '0x839De324a1ab773F76a53900D70Ac1B913d2B387',
        'perBlock' : 'icePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((address,uint256,uint256,uint32,uint16))',
        'alloc_offset' : 4,
        'featured' : 2,
        'network' : 'arb',
    },
                '0x06408571e0ad5e8f52ead01450bde74e5074dc74' : {
        'name' : 'abracadabra.money',
        'rewardToken' : '0xce1bffbd5374dac86a2893119683f4911a2f7814',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingIce',
        'masterChef' : '0x06408571e0ad5e8f52ead01450bde74e5074dc74',
        'perBlock' : 'icePerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((address,uint256,uint256,uint32,uint16))',
        'alloc_offset' : 4,
        'featured' : 2,
        'network' : 'avax',
    },
                '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a' : {
        'name' : 'marsecosystem.com',
        'rewardToken' : '0x7859B01BbF675d67Da8cD128a50D155cd881B576',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingXMS',
        'masterChef' : '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a',
        'featured' : 2,
        'network' : 'bsc',
        'perBlock' : 'xmsPerBlock',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef, farm_templates.get_single_masterchef, farm_templates.get_single_masterchef, farm_templates.get_single_masterchef, farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault, external_contracts.dummy_vault, external_contracts.dummy_vault, external_contracts.dummy_vault, external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a', 'network_id' : 'bsc', 'farm_data' :{'rewardToken' : '0x7859B01BbF675d67Da8cD128a50D155cd881B576', 'decimal' : 18, 'stakedFunction' : 'stakedWantTokens', 'pendingFunction' : 'pendingToken', 'masterChef' : '0xb7881F5142245531C3fB938a37b5D2489EFd2C01', 'wantFunction' : 'poolInfo', 'rewardSymbol' : 'XMS'}},
                {'farm_id' : '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a', 'network_id' : 'bsc', 'farm_data' :{'rewardToken' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', 'decimal' : 18, 'stakedFunction' : 'userInfo', 'pendingFunction' : 'pendingXMS', 'masterChef' : '0x48C42579D98Aa768cde893F8214371ed607CABE3', 'wantFunction' : 'poolInfo', 'rewardSymbol' : 'WBNB'}},
                {'farm_id' : '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a', 'network_id' : 'bsc', 'farm_data' :{'rewardToken' : '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c', 'decimal' : 18, 'stakedFunction' : 'userInfo', 'pendingFunction' : 'pendingXMS', 'masterChef' : '0xA53b575F9eC7126ba7b43c8c3171Fe4685F2f8b0', 'wantFunction' : 'poolInfo', 'rewardSymbol' : 'BTCB'}},
                {'farm_id' : '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a', 'network_id' : 'bsc', 'farm_data' :{'rewardToken' : '0x2170Ed0880ac9A755fd29B2688956BD959F933F8', 'decimal' : 18, 'stakedFunction' : 'userInfo', 'pendingFunction' : 'pendingXMS', 'masterChef' : '0x4639d936f0a716f234ead073362c5cb272cc4b70', 'wantFunction' : 'poolInfo', 'rewardSymbol' : 'ETH'}},
                {'farm_id' : '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a', 'network_id' : 'bsc', 'farm_data' :{'rewardToken' : '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82', 'decimal' : 18, 'stakedFunction' : 'userInfo', 'pendingFunction' : 'pendingXMS', 'masterChef' : '0x22d8d50454203bd5a41b49ef515891f1ad9f3e53', 'wantFunction' : 'poolInfo', 'rewardSymbol' : 'CAKE'}},
                #{'farm_id' : '0xc7B8285a9E099e8c21CA5516D23348D8dBADdE4a', 'network_id' : 'bsc', 'farm_data' :{'rewardToken' : '0xBb0fA2fBE9b37444f5D1dBD22e0e5bdD2afbbE85', 'decimal' : 18, 'stakedFunction' : 'userInfo', 'pendingFunction' : 'pendingXMS', 'masterChef' : '0x2894786e5292f7F23F6805067Aace92474a226Ee', 'wantFunction' : 'poolInfo', 'rewardSymbol' : 'mUSD'}},            
            ],
            'vault_args' : [{},{},{},{},{},{}]
        }
    },
                '0xSingularFTM' : {
        'name' : 'singular.farm',
        'rewardToken' : '0x53d831e1db0947c74e8a52618f662209ec5de0ce',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSingularFTM',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_singular_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : '0xSingularFTM', 'network_id' : 'ftm', 'farm_data' :{'masterChef' : '0x9ED04B13AB6cae27ee397ee16452AdC15d9d561E', 'reward' : '0x53d831e1db0947c74e8a52618f662209ec5de0ce', 'decimal' : 18, 'rewardSymbol' : 'SING'}},
            ],
            'vault_args' : [{}]
        }
    },
                '0xSingularAVAX' : {
        'name' : 'singular.farm',
        'rewardToken' : '0xf9a075c9647e91410bf6c402bdf166e1540f67f0',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSingularAVAX',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_singular_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : '0xSingularAVAX', 'network_id' : 'avax', 'farm_data' :{'masterChef' : '0xF2599B0c7cA1e3c050209f3619F09b6daE002857', 'reward' : '0xf9a075c9647e91410bf6c402bdf166e1540f67f0', 'decimal' : 18, 'rewardSymbol' : 'SING'}},
            ],
            'vault_args' : [{}]
        }
    },
                '0xSingularBSC' : {
        'name' : 'singular.farm',
        'rewardToken' : '0x23894c0ce2d79b79ea33a4d02e67ae843ef6e563',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSingularBSC',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_singular_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : '0xSingularBSC', 'network_id' : 'bsc', 'farm_data' :{'masterChef' : '0x31B05a72037E91B86393a0f935fE7094141ba0a7', 'reward' : '0x23894c0ce2d79b79ea33a4d02e67ae843ef6e563', 'decimal' : 18, 'rewardSymbol' : 'SING'}},
            ],
            'vault_args' : [{}]
        }
    },
                '0xSingularMATIC' : {
        'name' : 'singular.farm',
        'rewardToken' : '0xcb898b0efb084df14dd8e018da37b4d0f06ab26d',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSingularMATIC',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_singular_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : '0xSingularMATIC', 'network_id' : 'matic', 'farm_data' :{'masterChef' : '0x9762Fe3ef5502dF432de41E7765b0ccC90E02e92', 'reward' : '0xcb898b0efb084df14dd8e018da37b4d0f06ab26d', 'decimal' : 18, 'rewardSymbol' : 'SING'}},
            ],
            'vault_args' : [{}]
        }
    },
                '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924' : {
        'name' : 'defikingdoms.com',
        'rewardToken' : '0x72Cb10C6bfA5624dD07Ef608027E366bd690048F',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924',
        'featured' : 2,
        'network' : 'harmony',
        'perBlock' : 'REWARD_PER_BLOCK',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sfeed],
            'vaults' : [external_contracts.get_dk_jewel],
            'args' : [
                    {
                        'farm_id' : '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924',
                        'network' : 'harmony',
                        'receipt_token' : '0xA9cE83507D872C5e1273E745aBcfDa849DAA654F'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xVoltSwap' : {
        'name' : 'voltswap.finance',
        'rewardToken' : '0x8Df95e66Cb0eF38F91D2776DA3c921768982fBa0',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xVoltSwap',
        'featured' : 2,
        'network' : 'meter',
        'extraFunctions' : {
            'functions' : [farm_templates.get_voltswap],
            'vaults' : [external_contracts.get_voltswap],
            'args' : [
                    {
                        'farm_id' : '0xVoltSwap',
                        'network_id' : 'meter',
                    },
                    ],
            'vault_args' : [{'wallet' : wallet}]
        }
    },
                '0xVoltSwapTheta' : {
        'name' : 'voltswap.finance',
        'rewardToken' : '0x3050ca9d00559cfbde6d8b796cef2af07e17725f',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xVoltSwapTheta',
        'featured' : 2,
        'network' : 'theta',
        'extraFunctions' : {
            'functions' : [farm_templates.get_voltswap],
            'vaults' : [external_contracts.get_voltswap_theta],
            'args' : [
                    {
                        'farm_id' : '0xVoltSwapTheta',
                        'network_id' : 'theta',
                    },
                    ],
            'vault_args' : [{'wallet' : wallet}]
        }
    },
                '0xVoltSwapMoon' : {
        'name' : 'voltswap.finance',
        'rewardToken' : '0x3050ca9d00559cfbde6d8b796cef2af07e17725f',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xVoltSwapMoon',
        'featured' : 2,
        'network' : 'moonbeam',
        'extraFunctions' : {
            'functions' : [farm_templates.get_voltswap],
            'vaults' : [external_contracts.get_voltswap_moon],
            'args' : [
                    {
                        'farm_id' : '0xVoltSwapMoon',
                        'network_id' : 'moonbeam',
                    },
                    ],
            'vault_args' : [{'wallet' : wallet}]
        }
    },
                '0x43d78BA76dc2C5dF8C1cF3423C5b8Db7f476f33a' : {
        'name' : 'towerfinance.io',
        'rewardToken' : '0x88a3acac5c48f93121d4d7771a068a1fcde078bc',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x43d78BA76dc2C5dF8C1cF3423C5b8Db7f476f33a',
        'featured' : 2,
        'network' : 'matic',
        'perBlock' : 'rewardPerBlock',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0x43d78BA76dc2C5dF8C1cF3423C5b8Db7f476f33a',
                    'network_id' : 'matic',
                    'farm_data' :{
                        'rewardToken' : '0x88a3acac5c48f93121d4d7771a068a1fcde078bc',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingReward',
                        'masterChef' : '0x4696B1A198407BFb8bB8dd59030Bf30FaC258f1D',
                        'network' : 'matic',
                        'rewardSymbol' : 'IVORY',
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x35cA0e02C4c16c94c4cC8B67D13d660b78414f95' : {
        'name' : 'nasdex.xyz',
        'rewardToken' : '0xE8d17b127BA8b9899a160D9a07b69bCa8E08bfc6',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingNSDX',
        'masterChef' : '0x35cA0e02C4c16c94c4cC8B67D13d660b78414f95',
        'featured' : 2,
        'network' : 'matic',
        'perBlock' : 'nsdxPerBlock',
    },
                '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F' : {
        'name' : 'sushi.com',
        'rewardToken' : '0xd15ec721c2a896512ad29c671997dd68f9593226',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F',
        'featured' : 2,
        'network' : 'celo',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sushi_masterchef],
            'vaults' : [external_contracts.dummy_vault, external_contracts.dummy_vault],
            'args' : [
                # {
                #     'farm_id' : '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F',
                #     'network_id' : 'celo',
                #     'farm_data' :{
                #         'masterChef' : '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F',
                #         'rewarder' : '0x1be211D8DA40BC0ae8719c6663307Bfc987b1d6c',
                #         'r0sym' : 'SUSHI',
                #         'r1sym' : 'CELO',
                #         'dead_pools' : [],
                #         'r0t' : '0xd15ec721c2a896512ad29c671997dd68f9593226',
                #         'r1t' : '0x471EcE3750Da237f93B8E339c536989b8978a438'
                #     }
                # },
                {
                    'farm_id' : '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F',
                    'network_id' : 'celo',
                    'farm_data' :{
                        'masterChef' : '0x8084936982D089130e001b470eDf58faCA445008',
                        'rewarder' : '0xfa3de59edd2500ba725dad355b98e6a4346ada7d',
                        'r0sym' : 'SUSHI',
                        'r1sym' : 'CELO',
                        'r0t' : '0xd15ec721c2a896512ad29c671997dd68f9593226',
                        'r1t' : '0x471EcE3750Da237f93B8E339c536989b8978a438'
                    }
                }
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0xEuler' : {
        'name' : 'euler.tools',
        'rewardToken' : '0x3920123482070c1a2dff73aad695c60e7c6f6862',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xEuler',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_euler_staking],
            'vaults' : [external_contracts.euler_staking],
            'args' : [
                {
                    'farm_id' : '0xEuler',
                    'network_id' : 'bsc',
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xa0488F956D7fe05b1798e9FaF0cE5F1133d23822' : {
        'name' : 'smartcoin.farm',
        'rewardToken' : '0xCC2f1d827b18321254223dF4e84dE399D9Ff116c',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTokens',
        'masterChef' : '0xa0488F956D7fe05b1798e9FaF0cE5F1133d23822',
        'perBlock' : 'joePerSec',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'avax',
    },
                '0x1495b7e8d7E9700Bd0726F1705E864265724f6e2' : {
        'name' : 'smartcoin.farm v2',
        'rewardToken' : '0x6D923f688C7FF287dc3A5943CAeefc994F97b290',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTokens',
        'masterChef' : '0x1495b7e8d7E9700Bd0726F1705E864265724f6e2',
        'perBlock' : 'joePerSec',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'avax',
    },
                '0xBeethoven' : {
        'name' : 'beethovenx.io',
        'rewardToken' : '0xf24bcf4d1e507740041c9cfd2dddb29585adce1e',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeethoven',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xBeethoven',
                    'network_id' : 'ftm',
                    'farm_data' :{
                        'name' : 'beethovenx.io',
                        'rewardToken' : '0xf24bcf4d1e507740041c9cfd2dddb29585adce1e',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingBeets',
                        'masterChef' : '0x8166994d9ebBe5829EC86Bd81258149B87faCfd3',
                        'featured' : 2,
                        'network' : 'ftm',
                        'wantFunction' : 'lpTokens',
                        'rewardSymbol' : 'BEETS',
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xbCEf0849DDd928835A6Aa130aE527C2703CD832C' : {
        'name' : 'scarecrow.fi',
        'rewardToken' : '0x46e1ee17f51c52661d04238f1700c547de3b84a1',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingScare',
        'masterChef' : '0xbCEf0849DDd928835A6Aa130aE527C2703CD832C',
        'perBlock' : 'scarePerBlock',
        'featured' : 2,
        'network' : 'ftm',
    },
                '0x1f4b7660b6AdC3943b5038e3426B33c1c0e343E6' : {
        'name' : 'huckleberry.finance',
        'rewardToken' : '0x9a92b5ebf1f6f6f7d93696fcd44e5cf75035a756',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x1f4b7660b6AdC3943b5038e3426B33c1c0e343E6',
        'perBlock' : 'finnPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'moon',
    },
                '0xcc0a87F7e7c693042a9Cc703661F5060c80ACb43' : {
        'name' : 'tomb.finance',
        'rewardToken' : '0x4cdf39285d7ca8eb3f090fda0c069ba5f4145b37',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingShare',
        'masterChef' : '0xcc0a87F7e7c693042a9Cc703661F5060c80ACb43',
        'featured' : 2,
        'perBlock' : 'tSharePerSecond',
        'apy_config' : 'second',
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_balance_earn],
            'vaults' : [external_contracts.tomb_staking],
            'args' : [
                {
                    'farm_id' : '0xcc0a87F7e7c693042a9Cc703661F5060c80ACb43',
                    'network' : 'ftm',
                    'want_function' : 'share',
                    'reward_info' : {'token' : '0x6c021ae822bea943b2e66552bde1d2696a53fbb7', 'symbol' : 'TOMB', 'decimal' : 18}
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0x89dcd1DC698Ad6A422ad505eFE66261A4320D8B5' : {
        'name' : 'bouje.finance',
        'rewardToken' : '0x37f70aa9fefc8971117bd53a1ddc2372aa7eec41',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBouje',
        'masterChef' : '0x89dcd1DC698Ad6A422ad505eFE66261A4320D8B5',
        'featured' : 2,
        'network' : 'ftm',
        'perBlock' : 'boujePerBlock',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.bouje_staking, external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0x89dcd1DC698Ad6A422ad505eFE66261A4320D8B5',
                    'network_id' : 'ftm',
                    'staked' : 'stakeToken'
                },
                {
                    'farm_id' : '0x89dcd1DC698Ad6A422ad505eFE66261A4320D8B5',
                    'network_id' : 'ftm',
                    'farm_data' :{
                        'rewardToken' : '0xe509db88b3c26d45f1fff45b48e7c36a8399b45a',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingVive',
                        'masterChef' : '0x1277dd1dCbe60d597aAcA80738e1dE6cB95dCB54',
                        'rewardSymbol' : 'VIVE',
                    }
                }
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0x876F890135091381c23Be437fA1cec2251B7c117' : {
        'name' : 'yieldwolf.finance',
        'rewardToken' : '0x9a92b5ebf1f6f6f7d93696fcd44e5cf75035a756',
        'decimal' : 18,
        'stakedFunction' : 'stakedTokens',
        'pendingFunction' : None,
        'masterChef' : '0x876F890135091381c23Be437fA1cec2251B7c117',
        'perBlock' : None,
        'featured' : 2,
        'network' : 'ftm',
    },
                '0xd3ab90ce1eecf9ab3cbae16a00acfbace30ebd75' : {
        'name' : 'yieldwolf.finance',
        'rewardToken' : '0x9a92b5ebf1f6f6f7d93696fcd44e5cf75035a756',
        'decimal' : 18,
        'stakedFunction' : 'stakedTokens',
        'pendingFunction' : None,
        'masterChef' : '0xd3ab90ce1eecf9ab3cbae16a00acfbace30ebd75',
        'featured' : 2,
        'perBlock' : None,
        'network' : 'bsc',
    },
                '0xBF65023BcF48Ad0ab5537Ea39C9242de499386c9' : {
        'name' : 'yieldwolf.finance',
        'rewardToken' : '0x9a92b5ebf1f6f6f7d93696fcd44e5cf75035a756',
        'decimal' : 18,
        'stakedFunction' : 'stakedTokens',
        'pendingFunction' : None,
        'masterChef' : '0xBF65023BcF48Ad0ab5537Ea39C9242de499386c9',
        'featured' : 2,
        'perBlock' : None,
        'network' : 'matic',
    },
                '0xd54AA6fEeCc289DeceD6cd0fDC54f78079495E79' : {
        'name' : 'yieldwolf.finance',
        'rewardToken' : '0x9a92b5ebf1f6f6f7d93696fcd44e5cf75035a756',
        'decimal' : 18,
        'stakedFunction' : 'stakedTokens',
        'pendingFunction' : None,
        'masterChef' : '0xd54AA6fEeCc289DeceD6cd0fDC54f78079495E79',
        'featured' : 2,
        'perBlock' : None,
        'network' : 'celo',
    },
                '0x3dB01570D97631f69bbb0ba39796865456Cf89A5' : {
        'name' : 'sushi.com',
        'rewardToken' : '0xf390830df829cf22c53c8840554b98eafc5dcbc2',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0x3dB01570D97631f69bbb0ba39796865456Cf89A5',
        'featured' : 2,
        'network' : 'moon',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sushi_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0x3dB01570D97631f69bbb0ba39796865456Cf89A5',
                    'network_id' : 'moon',
                    'farm_data' :{
                        'masterChef' : '0x3dB01570D97631f69bbb0ba39796865456Cf89A5',
                        'rewarder' : '0x1334c8e873e1cae8467156e2a81d1c8b566b2da1',
                        'r0sym' : 'SUSHI',
                        'r1sym' : 'WMOVR',
                        'r0t' : '0xf390830df829cf22c53c8840554b98eafc5dcbc2',
                        'r1t' : '0x98878B06940aE243284CA214f92Bb71a2b032B8A'
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xE50cb76A71b0c52Ab091860cD61b9BA2FA407414' : {
        'name' : 'knightswap.financial',
        'rewardToken' : '0xd23811058eb6e7967d9a00dc3886e75610c4abba',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingKnight',
        'masterChef' : '0xE50cb76A71b0c52Ab091860cD61b9BA2FA407414',
        'featured' : 2,
        'network' : 'bsc',
        'perBlock' : 'KnightPerBlock',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.knight_staking],
            'args' : [
                {
                    'farm_id' : '0xE50cb76A71b0c52Ab091860cD61b9BA2FA407414',
                    'network_id' : 'bsc',
                },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xGrim' : {
        'name' : 'grim.finance',
        'rewardToken' : '0x7eC94C4327dC757601B4273cD67014d7760Be97E',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xGrim',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_grim_vaults],
            'args' : [
                {
                    'farm_id' : '0xGrim',
                    'network' : 'ftm',
                    '_pps' : 'getPricePerFullShare',
                    'want_token' : 'want',
                    'decimal_from' : False,
                }],
            'vault_args' : [{}]
        }
    },
                '0x342bffa41D7120C2c3ed746F80286EcD025272c5' : {
        'name' : 'hadesswap.finance',
        'rewardToken' : '0xf1498e8103359fd96c5e08fb34b4c249b619025a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSoul',
        'masterChef' : '0x342bffa41D7120C2c3ed746F80286EcD025272c5',
        'featured' : 2,
        'perBlock' : 'soulPerBlock',
        'network' : 'polis',
    },
                '0x77ea4a4cF9F77A034E4291E8f457Af7772c2B254' : {
        'name' : 'cronaswap.org',
        'rewardToken' : '0xadbd1231fb360047525bedf962581f3eee7b49fe',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCrona',
        'masterChef' : '0x77ea4a4cF9F77A034E4291E8f457Af7772c2B254',
        'featured' : 2,
        'network' : 'cro',
        'perBlock' : 'cronaPerSecond',
        'apy_config' : 'second',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_vault_style],
            'vaults' : [external_contracts.crona_vaults, external_contracts.crona_staking],
            'args' : [
                {
                    'farm_id' : '0x77ea4a4cF9F77A034E4291E8f457Af7772c2B254',
                    'network_id' : 'cro',
                },
                {
                    'farm_id' : '0x77ea4a4cF9F77A034E4291E8f457Af7772c2B254',
                    'network' : 'cro',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo'
                }, 
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xDccd6455AE04b03d785F12196B492b18129564bc' : {
        'name' : 'vvs.finance',
        'rewardToken' : '0x2d03bece6747adc00e1a131bba1469c15fd11e03',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingVVS',
        'masterChef' : '0xDccd6455AE04b03d785F12196B492b18129564bc',
        'perBlock' : 'vvsPerBlock',
        'featured' : 2,
        'network' : 'cro',
        'perBlock' : '',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools, farm_templates.get_vault_style],
            'vaults' : [external_contracts.vvs_vaults, external_contracts.vvs_staking],
            'args' : [
                {
                    'farm_id' : '0xDccd6455AE04b03d785F12196B492b18129564bc',
                    'network_id' : 'cro',
                },
                {
                    'farm_id' : '0xDccd6455AE04b03d785F12196B492b18129564bc',
                    'network' : 'cro',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo'
                }, 
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xCroDex' : {
        'name' : 'crodex.app',
        'rewardToken' : '0xdf7837de1f2fa4631d716cf2502f8b230f1dcc32',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xCroDex',
        'featured' : 2,
        'network' : 'cro',
        'extraFunctions' : {
            'functions' : [farm_templates.get_telx_single],
            'vaults' : [external_contracts.crodex_vaults],
            'args' : [
                {
                    'farm_id' : '0xCroDex',
                    'network_id' : 'cro',
                },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x7abc67c8d4b248a38b0dc5756300630108cb48b4' : {
        'name' : 'viper.exchange',
        'rewardToken' : '0xEa589E93Ff18b1a1F1e9BaC7EF3E86Ab62addc79',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingReward',
        'masterChef' : '0x7abc67c8d4b248a38b0dc5756300630108cb48b4',
        'featured' : 2,
        'perBlock' : 'REWARD_PER_BLOCK',
        'network' : 'harmony'
    },
                '0x31B9FBd965397d697D2dAa434EbD219aB878E49B' : {
        'name' : 'oolongswap.com',
        'rewardToken' : '0x5008f837883ea9a07271a1b5eb0658404f5a9610',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingOolong',
        'masterChef' : '0x31B9FBd965397d697D2dAa434EbD219aB878E49B',
        'perBlock' : 'oolongPerSec',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'boba'
    },
                '0x958C0d0baA8F220846d3966742D4Fb5edc5493D3' : {
        'name' : 'axial.exchange',
        'rewardToken' : '0xcf8419a615c57511807236751c0af38db4ba3351',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTokens',
        'masterChef' : '0x958C0d0baA8F220846d3966742D4Fb5edc5493D3',
        'featured' : 2,
        'perBlock' : 'axialPerSec',
        'apy_config' : 'second',
        'network' : 'avax',
    },
                '0x4dF0dDc29cE92106eb8C8c17e21083D4e3862533' : {
        'name' : 'crystl.finance',
        'rewardToken' : '0x7f426F6Dc648e50464a0392E60E1BB465a67E9cf',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : None,
        'masterChef' : '0x4dF0dDc29cE92106eb8C8c17e21083D4e3862533',
        'perBlock' : None,
        'featured' : 2,
        'network' : 'cro',
    },
                '0xEF6d860B22cEFe19Ae124b74eb80F0c0eb8201F4' : {
        'name' : 'annex.finance',
        'rewardToken' : '0x98936bde1cf1bff1e7a8012cee5e2583851f2067',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingAnnex',
        'masterChef' : '0xEF6d860B22cEFe19Ae124b74eb80F0c0eb8201F4',
        'perBlock' : 'annexPerBlock',
        'want' : 'getPoolInfo',
        'pool_alloc' : 'getPoolInfo(uint256)((address,uint256,uint256,uint256))',
        'alloc_offset' : 2,
        'featured' : 2,
        'network' : 'cro',
    },
                '0xAnnexBSC' : {
        'name' : 'annex.finance (Lending)',
        'rewardToken' : '0x98936Bde1CF1BFf1e7a8012Cee5e2583851f2067',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAnnexBSC',
        'featured' : 2,
        'network' : 'bsc',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_lending_protocol],
            'vaults' : [external_contracts.get_annex_vaults],
            'args' : [
                    {
                        'farm_id' : '0xAnnexBSC',
                        'network' : 'bsc',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xAaveMatic' : {
        'name' : 'aave.com',
        'rewardToken' : '0xd6df932a45c0f255f85145f286ea0b292b21c90b',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xAaveMatic',
        'featured' : 2,
        'network' : 'matic',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_aave_protocol],
            'vaults' : [external_contracts.get_aave_matic],
            'args' : [
                    {
                        'farm_id' : '0xAaveMatic',
                        'network' : 'matic',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xVenusBSC' : {
        'name' : 'venus.io (Lending)',
        'rewardToken' : '0xcf6bb5389c92bdda8a3747ddb454cb7a64626c63',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xVenusBSC',
        'featured' : 2,
        'network' : 'bsc',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_lending_protocol],
            'vaults' : [external_contracts.get_venus_vaults],
            'args' : [
                    {
                        'farm_id' : '0xVenusBSC',
                        'network' : 'bsc',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x9c821500eaBa9f9737fDAadF7984Dff03edc74d1' : {
        'name' : 'annex.finance',
        'rewardToken' : '0x98936bde1cf1bff1e7a8012cee5e2583851f2067',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingAnnex',
        'perBlock' : 'annexPerBlock',
        'want' : 'getPoolInfo',
        'pool_alloc' : 'getPoolInfo(uint256)((address,uint256,uint256,uint256))',
        'alloc_offset' : 2,
        'masterChef' : '0x9c821500eaBa9f9737fDAadF7984Dff03edc74d1',
        'featured' : 2,
        'network' : 'bsc',
    },
                '0x6eC89CCcDb563Ac442d2370F6E47bC1C78e023fC' : {
        'name' : 'stormswap.finance',
        'rewardToken' : '0x48713151e5afb7b4cc45f3653c1c59cf81e88d4b',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingStorm',
        'masterChef' : '0x6eC89CCcDb563Ac442d2370F6E47bC1C78e023fC',
        'perBlock' : 'StormPerBlock',
        'featured' : 2,
        'network' : 'cro',
    },
                '0xe5AFC91CEA5df74748A2b07e1d48E4e01aacF52B' : {
        'name' : 'fastyield.app',
        'rewardToken' : '0x0299461ee055bbb6de11fafe5a0636a0c3bd5e8d',
        'decimal' : 18,
        'stakedFunction' : 'stakedWantTokens',
        'pendingFunction' : 'pendingNATIVE',
        'masterChef' : '0xe5AFC91CEA5df74748A2b07e1d48E4e01aacF52B',
        'perBlock' : 'NATIVEPerSecond',
        'apy_config' : 'second',
        'featured' : 2,
        'network' : 'ftm',
    },
                '0xJadeProtocol' : {
        'name' : 'jadeprotocol.io',
        'rewardToken' : '0x7ad7242A99F21aa543F9650A56D141C57e4F6081',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xJadeProtocol',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_ohm],
            'vaults' : [external_contracts.get_jade_ohm],
            'args' : [
                    {
                        'farm_id' : '0xJadeProtocol',
                        'network_id' : 'bsc',
                        'reward_symbol' : 'JADE'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xOHM' : {
        'name' : 'olympusdao.finance',
        'rewardToken' : '0x64aa3364f17a4d01c6f1751fd97c2bd3d7e7f1d5',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xOHM',
        'featured' : 2,
        'network' : 'eth',
        'extraFunctions' : {
            'functions' : [farm_templates.get_native_ohm],
            'vaults' : [external_contracts.get_ohm_ohm],
            'args' : [
                    {
                        'farm_id' : '0xOHM',
                        'network_id' : 'eth',
                        'reward_symbol' : 'OHM'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xNidhi' : {
        'name' : 'nidhidao.finance',
        'rewardToken' : '0x057e0bd9b797f9eeeb8307b35dbc8c12e534c41e',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xNidhi',
        'featured' : 2,
        'network' : 'matic',
        'extraFunctions' : {
            'functions' : [farm_templates.get_ohm],
            'vaults' : [external_contracts.get_nidhi_ohm],
            'args' : [
                    {
                        'farm_id' : '0xNidhi',
                        'network_id' : 'matic',
                        'reward_symbol' : 'GURU'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xf046e84439813bb0a26fb26944001c7bb4490771' : {
        'name' : 'wagmidao.io',
        'rewardToken' : '0x8750F5651AF49950b5419928Fecefca7c82141E3',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingWagmi',
        'masterChef' : '0xf046e84439813bb0a26fb26944001c7bb4490771',
        'perBlock' : 'wagmiPerBlock',
        'featured' : 2,
        'network' : 'harmony',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style, farm_templates.get_wagmi_bonds],
            'vaults' : [external_contracts.get_wagmi, external_contracts.get_wagmi_ohm],
            'args' : [
                {
                    'farm_id' : '0xf046e84439813bb0a26fb26944001c7bb4490771',
                    'network' : 'harmony',
                    '_pps' : 'getPricePerFullShare',
                    '_stake' : 'userInfo',
                    'want_token' : 'wagmi'
                },
                {
                    'farm_id' : '0xf046e84439813bb0a26fb26944001c7bb4490771',
                    'network_id' : 'harmony',
                    'reward_symbol' : 'GMI'
                },
                    ],
            'vault_args' : [{}, {}]
        }
    },
                '0xTranquilLending' : {
        'name' : 'tranquil.finance (lending)',
        'rewardToken' : '0xcf1709ad76a79d5a60210f23e81ce2460542a836',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xTranquilLending',
        'featured' : 2,
        'network' : 'harmony',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_lending_protocol],
            'vaults' : [external_contracts.get_tranquil_vaults],
            'args' : [
                    {
                        'farm_id' : '0xTranquilLending',
                        'network' : 'harmony',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
    #             '0xTranquilLendingStaking' : {
    #     'name' : 'tranquil.finance',
    #     'rewardToken' : '0xcf1709ad76a79d5a60210f23e81ce2460542a836',
    #     'decimal' : 18,
    #     'stakedFunction' : None,
    #     'pendingFunction' : None,
    #     'masterChef' : '0xTranquilLendingStaking',
    #     'featured' : 2,
    #     'network' : 'harmony',
    #     'extraFunctions' : {
    #         'functions' : [farm_templates.get_lending_protocol],
    #         'vaults' : [external_contracts.get_tranquil_vaults],
    #         'args' : [
    #                 {
    #                     'farm_id' : '0xTranquilLendingStaking',
    #                     'network' : 'harmony',
    #                 },
    #                 ],
    #         'vault_args' : [{}]
    #     }
    # },
                '0x138c4dB5D4Ab76556769e4ea09Bce1D452c2996F' : {
        'name' : 'xmas-past.com',
        'rewardToken' : '0xd3111fb8bdf936b11ffc9eba3b597bea21e72724',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingXpast',
        'perBlock' : 'XpastPerSecond',
        'apy_config' : 'second',
        'masterChef' : '0x138c4dB5D4Ab76556769e4ea09Bce1D452c2996F',
        'featured' : 2,
        'network' : 'ftm',
    },
                '0xVikings' : {
        'name' : 'vikings.finance',
        'rewardToken' : '0xe0474c15bc7f8213ee5bfb42f9e68b2d6be2e136',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xVikings',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_ohm],
            'vaults' : [external_contracts.get_viking_ohm],
            'args' : [
                    {
                        'farm_id' : '0xVikings',
                        'network_id' : 'avax',
                        'reward_symbol' : 'VAL'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x6bE34986Fdd1A91e4634eb6b9F8017439b7b5EDc' : {
        'name' : 'mm.finance',
        'rewardToken' : '0x97749c9b61f878a880dfe312d2594ae07aed7656',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingMeerkat',
        'perBlock' : 'meerkatPerBlock',
        'masterChef' : '0x6bE34986Fdd1A91e4634eb6b9F8017439b7b5EDc',
        'featured' : 2,
        'network' : 'cro',
    },
                '0x31D3966DA1cAB3dE7E9221ed016484E4Bb03Ba02' : {
        'name' : 'libredefi.io',
        'rewardToken' : '0x63db060697b01c6f4a26561b1494685dcbbd998c',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLib',
        'perBlock' : 'libPerBlock',
        'masterChef' : '0x31D3966DA1cAB3dE7E9221ed016484E4Bb03Ba02',
        'featured' : 2,
        'network' : 'bsc',
    },
                '0xE6DCE53f17FBF673f4FA60A38746F110517457B2' : {
        'name' : 'libredefi.io',
        'rewardToken' : '0x8afa62fa8dde8888405c899d7da077a61a87eed3',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLib',
        'perBlock' : 'libPerBlock',
        'masterChef' : '0xE6DCE53f17FBF673f4FA60A38746F110517457B2',
        'featured' : 2,
        'network' : 'avax',
    },
                '0x6Bb9EAb44Dc7f7e0a0454107F9e46Eedf0aA0285' : {
        'name' : 'libredefi.io',
        'rewardToken' : '0xF52d69BC301BE21cbed7D3ca652D1708FF8a1162',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingLib',
        'perBlock' : 'libPerBlock',
        'masterChef' : '0x6Bb9EAb44Dc7f7e0a0454107F9e46Eedf0aA0285',
        'featured' : 2,
        'network' : 'matic',
    },
                '0x1f1Ed214bef5E83D8f5d0eB5D7011EB965D0D79B' : {
        'name' : 'trisolaris.io',
        'rewardToken' : '0xFa94348467f64D5A457F75F8bc40495D33c65aBB',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTri',
        'perBlock' : 'triPerBlock',
        'masterChef' : '0x1f1Ed214bef5E83D8f5d0eB5D7011EB965D0D79B',
        'featured' : 2,
        'network' : 'aurora',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sfeed],
            'vaults' : [external_contracts.get_tri_staking],
            'args' : [
                    {
                        'farm_id' : '0x1f1Ed214bef5E83D8f5d0eB5D7011EB965D0D79B',
                        'network' : 'aurora',
                        'receipt_token' : '0x802119e4e253D5C19aA06A5d567C5a41596D6803'
                    },
                    ],
            'vault_args' : [{}]
        }

    },
                '0x2B2e72C232685fC4D350Eaa92f39f6f8AD2e1593' : {
        'name' : 'wannaswap.finance',
        'rewardToken' : '0x7faa64faf54750a2e3ee621166635feaf406ab22',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingWanna',
        'masterChef' : '0x2B2e72C232685fC4D350Eaa92f39f6f8AD2e1593',
        'featured' : 2,
        'perBlock' : 'wannaPerBlock',
        'network' : 'aurora',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sfeed],
            'vaults' : [external_contracts.get_wanna_staking],
            'args' : [
                    {
                        'farm_id' : '0x2B2e72C232685fC4D350Eaa92f39f6f8AD2e1593',
                        'network' : 'aurora',
                        'receipt_token' : '0x5205c30bf2E37494F8cF77D2c19C6BA4d2778B9B'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xVaporwave' : {
        'name' : 'vaporwave.farm',
        'rewardToken' : '0xca3f508b8e4dd382ee878a314789373d80a5190a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xVaporwave',
        'featured' : 2,
        'network' : 'aurora',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes],
            'vaults' : [external_contracts.get_vaporware_vaults],
            'args' : [{'farm_id' : '0xVaporwave', 'network' : 'aurora'}],
            'vault_args' : [{}]
        }
    },
                '0x35CC71888DBb9FfB777337324a4A60fdBAA19DDE' : {
        'name' : 'auroraswap.finance',
        'rewardToken' : '0x7faa64faf54750a2e3ee621166635feaf406ab22',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingBRL',
        'masterChef' : '0x35CC71888DBb9FfB777337324a4A60fdBAA19DDE',
        'featured' : 2,
        'perBlock' : 'BRLPerBlock',
        'network' : 'aurora',
    },
                '0x2aeF68F92cfBAFA4b542F60044c7596e65612D20' : {
        'name' : 'nearpad.io',
        'rewardToken' : '0x885f8CF6E45bdd3fdcDc644efdcd0AC93880c781',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSushi',
        'masterChef' : '0x2aeF68F92cfBAFA4b542F60044c7596e65612D20',
        'featured' : 2,
        'perBlock' : 'sushiPerBlock',
        'network' : 'aurora',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sfeed],
            'vaults' : [external_contracts.get_nearpad_staking],
            'args' : [
                    {
                        'farm_id' : '0x2aeF68F92cfBAFA4b542F60044c7596e65612D20',
                        'network' : 'aurora',
                        'receipt_token' : '0x5a9B5fE4fAb31280A6397e3D87F3565BbfeEb995'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x13cc0A2644f4f727db23f5B9dB3eBd72134085b7' : {
        'name' : 'pickle.finance',
        'rewardToken' : '0x291c8fceaca3342b29cc36171deb98106f712c66',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPickle',
        'perBlock' : 'picklePerSecond',
        'apy_config' : 'second',
        'want' : 'lpToken',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0x13cc0A2644f4f727db23f5B9dB3eBd72134085b7',
        'featured' : 2,
        'network' : 'aurora',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_pickle_addresses],
            'args' : [
                {
                    'farm_id' : '0x13cc0A2644f4f727db23f5B9dB3eBd72134085b7',
                    'network' : 'aurora',
                }
                    ],
            'vault_args' : [{'network' : 'aurora'}]
        }
    },
                '0xPickleOKEX' : {
        'name' : 'pickle.finance',
        'rewardToken' : '0xf290f3d843826d00f8176182fd76550535f6dbb4',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPickleOKEX',
        'featured' : 2,
        'network' : 'oke',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sushi_masterchef, farm_templates.get_vault_style],
            'vaults' : [external_contracts.dummy_vault, external_contracts.get_pickle_addresses],
            'args' : [
                {
                    'farm_id' : '0xPickleOKEX',
                    'network_id' : 'oke',
                    'pending_function' : 'pendingPickle',
                    'farm_data' :{
                        'masterChef' : '0x7446BF003b98B7B0D90CE84810AC12d6b8114B62',
                        'rewarder' : '0x48394297ed0a9e9edcc556faaf4222a932605c56',
                        'r0sym' : 'PICKLE',
                        'r1sym' : 'WOKT',
                        'r0t' : '0xf290f3d843826d00f8176182fd76550535f6dbb4',
                        'r1t' : '0x8f8526dbfd6e38e3d8307702ca8469bae6c56c15'
                    }
                },
                {
                    'farm_id' : '0xPickleOKEX',
                    'network' : 'oke',
                }
                    ],
            'vault_args' : [{},{'network' : 'okex'}]
        }
    },
                '0x7ecc7163469f37b777d7b8f45a667314030ace24' : {
        'name' : 'pickle.finance',
        'rewardToken' : '0x965772e0e9c84b6f359c8597c891108dcf1c5b1a',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingPickle',
        'perBlock' : 'picklePerSecond',
        'apy_config' : 'second',
        'want' : 'lpToken',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'masterChef' : '0x7ecc7163469f37b777d7b8f45a667314030ace24',
        'featured' : 2,
        'network' : 'arb',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_pickle_addresses],
            'args' : [
                {
                    'farm_id' : '0x7ecc7163469f37b777d7b8f45a667314030ace24',
                    'network' : 'arb',
                }
                    ],
            'vault_args' : [{'network' : 'arbitrum'}]
        }
    },
                '0xPickleMoon' : {
        'name' : 'pickle.finance',
        'rewardToken' : '0x965772e0e9c84b6f359c8597c891108dcf1c5b1a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPickleMoon',
        'featured' : 2,
        'network' : 'moon',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_pickle_addresses],
            'args' : [
                {
                    'farm_id' : '0xPickleMoon',
                    'network' : 'moon',
                }
                    ],
            'vault_args' : [{'network' : 'moonriver'}]
        }
    },
                '0xPickleCro' : {
        'name' : 'pickle.finance',
        'rewardToken' : '0x965772e0e9c84b6f359c8597c891108dcf1c5b1a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPickleCro',
        'featured' : 2,
        'network' : 'cro',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_pickle_addresses],
            'args' : [
                {
                    'farm_id' : '0xPickleCro',
                    'network' : 'cro',
                }
                    ],
            'vault_args' : [{'network' : 'cronos'}]
        }
    },
                '0x871d68cFa4994170403D9C1c7b3D3E037c76437d' : {
        'name' : 'thorus.fi',
        'rewardToken' : '0xae4aa155d2987b454c29450ef4f862cf00907b61',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingThorus',
        'masterChef' : '0x871d68cFa4994170403D9C1c7b3D3E037c76437d',
        'featured' : 2,
        'perBlock' : 'thorusPerSecond',
        'apy_config' : 'second',
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_thorus_auto],
            'args' : [
                {
                    'farm_id' : '0x871d68cFa4994170403D9C1c7b3D3E037c76437d',
                    'network' : 'avax',
                    'want_token' : 'thorus',
                    '_pps' : 'getPricePerFullShare'
                },
                {
                    'farm_id' : '0x871d68cFa4994170403D9C1c7b3D3E037c76437d',
                    'network_id' : 'avax',
                    'staked' : 'thorus',
                    'reward' : 'thorus',
                    'pending_reward' : 'claimablePayout'
                },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0xEeB84a24e10502D8A5c97B11df381D1550B25b9d' : {
        'name' : 'thorus.fi',
        'rewardToken' : '0x735abe48e8782948a37c7765ecb76b98cde97b0f',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingThorus',
        'masterChef' : '0xEeB84a24e10502D8A5c97B11df381D1550B25b9d',
        'featured' : 2,
        'perBlock' : 'thorusPerSecond',
        'apy_config' : 'second',
        'network' : 'moonbeam',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_thorus_mb],
            'args' : [
                {
                    'farm_id' : '0xEeB84a24e10502D8A5c97B11df381D1550B25b9d',
                    'network' : 'moonbeam',
                    'want_token' : 'thorus',
                    '_pps' : 'getPricePerFullShare'
                },
                {
                    'farm_id' : '0xEeB84a24e10502D8A5c97B11df381D1550B25b9d',
                    'network_id' : 'moonbeam',
                    'staked' : 'thorus',
                    'reward' : 'thorus',
                    'pending_reward' : 'claimablePayout'
                },
                    ],
            'vault_args' : [{},{}]
        }
    },
                '0xMetaReserve' : {
        'name' : 'metareserve.finance',
        'rewardToken' : '0x000c6322df760155bbe4f20f2edd8f4cd35733a6',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xMetaReserve',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_ohm],
            'vaults' : [external_contracts.get_metareserve_ohm],
            'args' : [
                    {
                        'farm_id' : '0xMetaReserve',
                        'network_id' : 'bsc',
                        'reward_symbol' : 'POWER'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xPegasusDAO' : {
        'name' : 'pegasusdao.finance',
        'rewardToken' : '0x000c6322df760155bbe4f20f2edd8f4cd35733a6',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPegasusDAO',
        'featured' : 2,
        'network' : 'cro',
        'extraFunctions' : {
            'functions' : [farm_templates.get_ohm],
            'vaults' : [external_contracts.get_pegasus_ohm],
            'args' : [
                    {
                        'farm_id' : '0xPegasusDAO',
                        'network_id' : 'cro',
                        'reward_symbol' : 'SUS'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xc027dd6fc63e73b59425b10b6e26d6e458889ca9' : {
        'name' : 'themanor.farm',
        'rewardToken' : '0x276b440fdb4c54631c882cac9e4317929e751ff8',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingRevolution',
        'masterChef' : '0xc027dd6fc63e73b59425b10b6e26d6e458889ca9',
        'featured' : 2,
        'perBlock' : 'revolutionPerBlock',
        'pool_alloc' : 'poolInfo(uint256)((address,address,uint256))',
        'alloc_offset' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_manorfarm_pools],
            'args' : [
                {
                    'farm_id' : '0xc027dd6fc63e73b59425b10b6e26d6e458889ca9',
                    'network_id' : 'bsc',
                    'pending_reward' : 'earned',
                    'user_info' : 'balanceOf'
                }],
            'vault_args' : [{}]
        }
    },
                '0x9d1dbB49b2744A1555EDbF1708D64dC71B0CB052' : {
        'name' : 'netswap.io',
        'rewardToken' : '0x90fe084f877c65e1b577c7b2ea64b8d8dd1ab278',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTokens',
        'masterChef' : '0x9d1dbB49b2744A1555EDbF1708D64dC71B0CB052',
        'featured' : 2,
        'perBlock' : 'nettPerSec',
        'apy_config' : 'second',
        'network' : 'metis',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_netswap_stakes],
            'args' : [
                {
                    'farm_id' : '0x9d1dbB49b2744A1555EDbF1708D64dC71B0CB052',
                    'network_id' : 'metis',
                    'staked' : 'stakingToken',
                    'reward' : 'rewardsToken',
                    'pending_reward' : 'earned',
                    'user_info' : 'balanceOf'
                },     
                ],
            'vault_args' : [{}]
        }
    },
                '0x54A8fB8c634dED694D270b78Cb931cA6bF241E21' : {
        'name' : 'tethys.finance',
        'rewardToken' : '0x69fdb77064ec5c84fa2f21072973eb28441f43f3',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingTethys',
        'masterChef' : '0x54A8fB8c634dED694D270b78Cb931cA6bF241E21',
        'featured' : 2,
        'perBlock' : 'tethysPerSecond',
        'apy_config' : 'second',
        'network' : 'metis',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sfeed],
            'vaults' : [external_contracts.get_tethys_staking],
            'args' : [
                    {
                        'farm_id' : '0x54A8fB8c634dED694D270b78Cb931cA6bF241E21',
                        'network' : 'metis',
                        'receipt_token' : '0x716678968fd6E518cb1d56C9720fC8eeEBA6CeAb'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x23423292396a37c0c2e4d384dce7ab67738bec28' : {
        'name' : 'standard.tech',
        'rewardToken' : '0xc12cac7090baa48ec750cceec57c80768f6ee58e',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSushi',
        'masterChef' : '0x23423292396a37c0c2e4d384dce7ab67738bec28',
        'perBlock' : 'sushiPerBlock',
        'want' : 'lpToken',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'featured' : 2,
        'network' : 'metis',
        },
                '0xBA438A6F03c03fb1Cf86567F6bb866CCFc9B2da7' : {
        'name' : 'hakuswap.com',
        'rewardToken' : '0x695Fa794d59106cEbd40ab5f5cA19F458c723829',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCake',
        'masterChef' : '0xBA438A6F03c03fb1Cf86567F6bb866CCFc9B2da7',
        'featured' : 2,
        'perBlock' : 'cakePerSecond',
        'apy_config' : 'second',
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sfeed],
            'vaults' : [external_contracts.get_haku_staking],
            'args' : [
                    {
                        'farm_id' : '0xBA438A6F03c03fb1Cf86567F6bb866CCFc9B2da7',
                        'network' : 'avax',
                        'receipt_token' : '0xa95c238b5a72f481f6abd50f951f01891130b441'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xHunnyDAO' : {
        'name' : 'dao.hunny.finance',
        'rewardToken' : '0x9505dbd77dacd1f6c89f101b98522d4b871d88c5',
        'decimal' : 9,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xHunnyDAO',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_ohm],
            'vaults' : [external_contracts.get_hunny_ohm],
            'args' : [
                    {
                        'farm_id' : '0xHunnyDAO',
                        'network_id' : 'bsc',
                        'reward_symbol' : 'LOVE'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0x3A3Ef6912d8D5b4E770f80F69635dcc9Ca1d7311' : {
        'name' : 'starstream.finance',
        'rewardToken' : '0xb26f58f0b301a077cfa779c0b0f8281c7f936ac0',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingSushi',
        'masterChef' : '0x3A3Ef6912d8D5b4E770f80F69635dcc9Ca1d7311',
        'featured' : 2,
        'want' : 'lpToken',
        'perBlock' : 'sushiPerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'network' : 'metis',
        'extraFunctions' : {
            'functions' : [farm_templates.get_vault_style],
            'vaults' : [external_contracts.get_starstream_vaults],
            'args' : [
                    {
                        'farm_id' : '0x3A3Ef6912d8D5b4E770f80F69635dcc9Ca1d7311',
                        'network' : 'metis',
                        '_pps' : 'getPricePerFullShare'
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xC3842B2d35dd249755f170dD8F0f83b8BF967E21' : {
        'name' : 'avtocross.finance',
        'rewardToken' : '0x6ef20ca7e493c52095e892dab78a7fd0e7e2a279',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingCross',
        'masterChef' : '0xC3842B2d35dd249755f170dD8F0f83b8BF967E21',
        'featured' : 2,
        'want' : 'lpToken',
        'perBlock' : 'crossPerSecond',
        'apy_config' : 'second',
        'pool_alloc' : 'poolInfo(uint256)((uint128,uint64,uint64))',
        'alloc_offset' : 2,
        'network' : 'cro',
        },
                '0xBeefyMetis' : {
        'name' : 'beefy.finance',
        'rewardToken' : '0xca3f508b8e4dd382ee878a314789373d80a5190a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xBeefyMetis',
        'featured' : 2,
        'network' : 'metis',
        'extraFunctions' : {
            'functions' : [farm_templates.get_beefy_style_stakes, farm_templates.get_fh_pools],
            'vaults' : [external_contracts.get_beefy_metis_pools, external_contracts.get_beefy_metis_boosts],
            'args' : [{'farm_id' : '0xBeefyMetis', 'network' : 'metis'}, {'farm_id' : '0xBeefyMetis', 'network' : 'metis', 'stake_func' : 'stakedToken'}],
            'vault_args' : [{}, {}]
        }
    },
                '0xStrongBlock' : {
        'name' : 'strongblock.com',
        'rewardToken' : '0xca3f508b8e4dd382ee878a314789373d80a5190a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xStrongBlock',
        'featured' : 2,
        'network' : 'eth',
        'extraFunctions' : {
            'functions' : [farm_templates.get_strong_block, farm_templates.get_strong_block, farm_templates.get_strong_block],
            'vaults' : [external_contracts.dummy_vault, external_contracts.dummy_vault, external_contracts.dummy_vault],
            'args' : [
                {'farm_id' : '0xStrongBlock', 'network_id' : 'eth', 'contract' : '0xfbddadd80fe7bda00b901fbaf73803f2238ae655', 'reward_function' : 'getReward(address,uint128)'},
                {'farm_id' : '0xStrongBlock', 'network_id' : 'eth', 'contract' : '0xc5622f143972a5da6aabc5f5379311ee5eb48568', 'reward_function' : 'getNodeReward(address,uint256)'},
                {'farm_id' : '0xStrongBlock', 'network_id' : 'eth', 'contract' : '0xF9D986340EfBf992cA1E7ce074db1D3b8EECf578', 'reward_function' : 'getReward(address,uint128)'},
                ],
            'vault_args' : [{},{},{}]
        }
    },
                '0xGMXAvax' : {
        'name' : 'gmx.io',
        'rewardToken' : '0x62edc0692BD897D2295872a9FFCac5425011c661',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xGMXAvax',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_gmx],
            'vaults' : [external_contracts.gmx_avax_vaults],
            'args' : [
                {
                    'farm_id' : '0xGMXAvax',
                    'network_id' : 'avax'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xEDFB330F5FA216C9D2039B99C8cE9dA85Ea91c1E' : {
        'name' : 'stellaswap.com',
        'rewardToken' : '0x0e358838ce72d5e61e0018a2ffac4bec5f4c88d2',
        'decimal' : 18,
        'stakedFunction' : 'userInfo',
        'pendingFunction' : 'pendingStella',
        'masterChef' : '0xEDFB330F5FA216C9D2039B99C8cE9dA85Ea91c1E',
        'perBlock' : 'stellaPerBlock',
        'featured' : 2,
        'network' : 'moonbeam',
        'extraFunctions' : {
            'functions' : [farm_templates.get_single_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xEDFB330F5FA216C9D2039B99C8cE9dA85Ea91c1E',
                    'network_id' : 'moonbeam',
                    'farm_data' :{
                        'rewardToken' : '0x0e358838ce72d5e61e0018a2ffac4bec5f4c88d2',
                        'decimal' : 18,
                        'stakedFunction' : 'userInfo',
                        'pendingFunction' : 'pendingStella',
                        'masterChef' : '0x54e2d14Df9348B3FBA7E372328595b9F3Ae243fE',
                        'rewardSymbol' : 'STELLA',
                    }
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xThorNodes' : {
        'name' : 'thor.financial',
        'rewardToken' : '0x8F47416CaE600bccF9530E9F3aeaA06bdD1Caa79',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xThorNodes',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_node_layout],
            'vaults' : [external_contracts.thor_nodes],
            'args' : [
                {
                    'farm_id' : '0xThorNodes',
                    'network_id' : 'avax'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xPowerNodes' : {
        'name' : 'powernode.io',
        'rewardToken' : '0x131c7afb4E5f5c94A27611f7210dfEc2215E85Ae',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xPowerNodes',
        'featured' : 2,
        'network' : 'ftm',
        'extraFunctions' : {
            'functions' : [farm_templates.get_node_layout],
            'vaults' : [external_contracts.power_nodes],
            'args' : [
                {
                    'farm_id' : '0xPowerNodes',
                    'network_id' : 'ftm'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xUniv' : {
        'name' : 'univ.money',
        'rewardToken' : '0x959b88966fC5B261dF8359961357d34F4ee27b4a',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xUniv',
        'featured' : 2,
        'network' : 'avax',
        'extraFunctions' : {
            'functions' : [farm_templates.get_planets],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                {
                    'farm_id' : '0xUniv',
                    'network_id' : 'avax',
                    'contract' : '0x89323f00a621d4ed6a56a93295c5f10f4df57ffa',
                    'reward_symbol' : 'UNIV',
                    'reward_token' : '0x959b88966fC5B261dF8359961357d34F4ee27b4a'
                }
                    ],
            'vault_args' : [{}]
        }
    },
                '0xSpinTop' : {
        'name' : 'spintop.network',
        'rewardToken' : '0x6AA217312960A21aDbde1478DC8cBCf828110A67',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xSpinTop',
        'featured' : 2,
        'network' : 'bsc',
        'extraFunctions' : {
            'functions' : [farm_templates.get_syrup_pools],
            'vaults' : [external_contracts.get_spintop_pools],
            'args' : [
                {
                    'farm_id' : '0xSpinTop',
                    'network_id' : 'bsc',
                    'pending_reward' : 'earned',
                    'user_info' : 'balanceOf',
                    'staked' : 'stakingToken',
                    'reward' : 'rewardsToken'
                }],
            'vault_args' : [{}]
        }
    },
                '0xVoltageFuse' : {
        'name' : 'voltage.finance',
        'rewardToken' : '0x0be9e53fd7edac9f859882afdda116645287c629',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xVoltageFuse',
        'featured' : 2,
        'network' : 'fuse',
        'extraFunctions' : {
            'functions' : [farm_templates.get_voltage_single],
            'vaults' : [external_contracts.get_voltage_vaults],
            'args' : [
                {
                    'farm_id' : '0xVoltageFuse',
                    'network_id' : 'fuse',
                    'reward_token' : '0x0be9e53fd7edac9f859882afdda116645287c629',
                }],
            'vault_args' : [{'network' : 'fuse'}]
        }
    },
                '0xOla' : {
        'name' : 'ola.finance',
        'rewardToken' : '0x0be9e53fd7edac9f859882afdda116645287c629',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xOla',
        'featured' : 2,
        'network' : 'fuse',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_lending_protocol],
            'vaults' : [external_contracts.get_ola_vaults],
            'args' : [
                    {
                        'farm_id' : '0xOla',
                        'network' : 'fuse',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xf730af26e87D9F55E46A6C447ED2235C385E55e0' : {
        'name' : 'sovryn.app',
        'rewardToken' : '0xEFc78fc7d48b64958315949279Ba181c2114ABBd',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'poolLength' : 'getPoolLength',
        'total_alloc' : 'totalAllocationPoint',
        'masterChef' : '0xf730af26e87D9F55E46A6C447ED2235C385E55e0',
        'featured' : 2,
        'want' : 'poolInfoList',
        'perBlock' : 'rewardTokensPerBlock',
        'pool_alloc' : 'poolInfoList(uint256)((address,uint96,uint256,uint256))',
        'alloc_offset' : 1,
        'network' : 'rsk',
        'extraFunctions' : {
            'functions' : [farm_templates.get_sovryn_masterchef],
            'vaults' : [external_contracts.dummy_vault],
            'args' : [
                    {
                        'farm_id' : '0xf730af26e87D9F55E46A6C447ED2235C385E55e0',
                        'masterchef' : '0xf730af26e87D9F55E46A6C447ED2235C385E55e0',
                        'reward_token' : '0xEFc78fc7d48b64958315949279Ba181c2114ABBd',
                        'reward_symbol' : 'SOV',
                        'network_id' : 'rsk',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
                '0xApeLendingBSC' : {
        'name' : 'apeswap.finance',
        'rewardToken' : '0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95',
        'decimal' : 18,
        'stakedFunction' : None,
        'pendingFunction' : None,
        'masterChef' : '0xApeLendingBSC',
        'featured' : 2,
        'network' : 'bsc',
        'type' : 'lending',
        'extraFunctions' : {
            'functions' : [farm_templates.get_lending_protocol],
            'vaults' : [external_contracts.get_apeswap_lending],
            'args' : [
                    {
                        'farm_id' : '0xApeLendingBSC',
                        'network' : 'bsc',
                    },
                    ],
            'vault_args' : [{}]
        }
    },
}



