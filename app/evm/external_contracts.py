import json
import hjson
import re
import os
import requests
import time
import cloudscraper
from requests.sessions import session
from .utils import make_get, make_get_hson,make_get_json,cf_make_get_json
from .multicall import parsers
from .thegraph import call_graph
from . import poolext
from . import bitquery
import asyncio
import ast


async def get_quickswap_lps(wallet, session):
    x = await call_graph('https://api.thegraph.com/subgraphs/name/sameepsi/quickswap03', {'operationName' : 'liquidityPositions', 'query' : bitquery.quickswap_lps.query, 'variables' : {'user': wallet.lower()}}, session)
    return x

async def get_voltswap(wallet, session):
    geysers = await call_graph('https://newgraph.voltswap.finance/subgraphs/name/meter/geyser-v2', {'operationName' : 'getGeysers', 'query' : bitquery.voltswap.geysers}, session)
    vault = await call_graph('https://newgraph.voltswap.finance/subgraphs/name/meter/geyser-v2', {'operationName' : 'getUserVault', 'query' : bitquery.voltswap.user_vaults, 'variables' : {'user': wallet.lower()}}, session)
    return {'geysers' : geysers['data']['geysers'], 'user_vaults' : vault['data']['user']['vaults']}

async def get_mai_graph(wallet, session):

    obj = """{
    vaults(where: {account: "%s"}) {
    id
    account {
      id
    }
    deposited
    borrowed
        }
    }""" % wallet.lower()


    x = await call_graph('https://api.thegraph.com/subgraphs/name/gallodasballo/mai-finance-quick', {'query': obj, 'variable' : None}, session)
    
    staked = 0
    pending = 0

    for each in x['data']['vaults']:
        staked += parsers.from_wei(int(each['deposited']))
        pending += parsers.from_wei(int(each['borrowed']))

    return {'VAULTS_staked' : staked, 'VAULTS_pending' : pending}

async def get_beefy_bsc(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/bsc_pools.js')
    s2 = "export const bscPools = "

    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]
    vault_data.append({'vault' : '0x6BE4741AB0aD233e4315a10bc783a7B923386b71', 'want' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'})

    return vault_data
        
async def get_beefy_boosts(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/bsc_stake.js')
    s2 = "export const bscStakePools = ["
    
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    x = f'[{regex}]'.replace('partners: ,','').replace('assets: ,','')
    hson = hjson.loads(x)
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t]

async def get_vsafes(session):
    r = await make_get_json(session,'https://api-vfarm.vswap.fi/api/farming-scan/get-farming-scans?group=vsafe')
    return [x['id'] for x in r['data']]

async def get_firebird_vaults():
    r = await make_get_json(session,'https://farm-api-polygon.firebird.finance/api/farming-scan/get-farming-scans?group=fvault')
    return [x['id'] for x in r['data']]

async def get_ele_tokens(session,network=None):
    skip_tokens = ['0x3Ed531BfB3FAD41111f6dab567b33C4db897f991', '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f', '0x0D5BaE8f5232820eF56D98c04B8F531d2742555F', '0xDF098493bB4eeE18BB56BE45DC43BD655a27E1A9', '0x27DD6E51BF715cFc0e2fe96Af26fC9DED89e4BE8', '0x025E2e9113dC1f6549C83E761d70E647c8CDE187', '0x0FFb84A4c29147Bd745AAe0330f4F6f4Cb716c92']
    token = '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'
    headers = {'accept': 'application/vnd.github.v3.raw',
                'authorization': 'token {}'.format(token)}
    r = await make_get(session,'https://raw.githubusercontent.com/Eleven-Finance/elevenfinance/main/src/features/configure/pools.js', kwargs={'headers':headers})
    s2 = "export const pools = "
    text_remove = """\'<b>You aren\\\'t earning the maximum rewards yet.</b><br/><br/>Pool Boosted Rewards are migrating to new \' +\n          \'contract version.<br/><b>Unstake</b> all your tokens and then <b>Stake</b> them again to receive Increased \' +\n          \'Rewards in <b>ELE</b> and <b>MATIC</b><br/><br/><b>IMPORTANT:</b> You don\\\'t need to <b>Withdraw</b> funds, \' +\n          \'just to <b>Unstake</b> them.\'"""
    data = r[r.index(s2) + len(s2) :len(r)-2]
    data = data.replace(text_remove, " ' ' ")
    data = data.replace("+","")
    data = data.replace("depositWarning: '<p>Be aware of <b>4% Deposit fee</b> on this pool.</p>'", "")
    data = data.replace("'<p>The fee is charged by Polycat, Eleven doesn\\'t charge you on the deposit</p>',", "")
    data = hjson.loads(data.replace("\\",""))
    response = json.loads(json.dumps(data))
    if network is None:
        return response
    else:
        return [x['earnedTokenAddress'] for x in response if '11' in x['earnedToken'] and x['network'] == network and x['earnedTokenAddress'] not in skip_tokens]

async def get_ele_staking_matic(session):
    return ['0x0FFb84A4c29147Bd745AAe0330f4F6f4Cb716c92']

async def get_space_pool_bsc(session):
    return ['0xd79dc49Ed716832658ec28FE93dd733e0DFB8d58']

async def get_wault_pools_matic(session):
    round_time = round(time.time())
    url = f'https://polyapi.wault.finance/wpoolsData.js?ts={round_time}'
    r = await make_get(session, url)
    s2 = "var wpoolsData = "
    data = r[r.index(s2) + len(s2) :len(r)]
    r = json.loads(data)
    r = [x['contractAddress'] for x in r]
    return r

async def get_blockmine(session):
    return ['0x8052D595E75c2E6e452bd2302aa1E66eAdBE2b42','0xDbd85332d6f6Edd1b66ba0594355aAAA140c1F07', '0x5e5964dfcbe523387cb86f7fbd283f64acd6c21a']

async def get_farmhero_staking_matic(session):
    return poolext.farmhero.matic_staking

async def get_farmhero_pools_matic(session):
    return poolext.farmhero.matic_pools

async def get_farmhero_staking_bsc(session):
    return poolext.farmhero.bsc_staking

async def get_farmhero_pools_bsc(session):
    return poolext.farmhero.bsc_pools

async def get_farmhero_staking_oke(session):
    return poolext.farmhero.oke_staking

async def get_farmhero_pools_oke(session):
    return poolext.farmhero.oke_pools

async def get_boneswap_pools(session):
    return poolext.boneswap.pools

async def get_boneswap_vaults(session):
    return poolext.boneswap.vaults

async def get_space_pool_poly(session):
    return ['0xBa56A30ec2Ee2B4C3c7EE75e0CFEbcD1b22dE8cd']

async def get_apolyyeld(session):
    return ['0xc49bc7118a73Ca6CB36Bfa454FD40eCAE079a463']

async def panther_jungles(session):
    return ['0x3B5Ed7B0F8bf5D2b485352e15A416092Ca741C2c', '0xf31cbe0b2bb2e704310c90a6f74300b3d4627ce8', '0x85ff09374D1f59288b6978EB9254377a51BE0B7c']

async def get_thunder_pools(session):
    return poolext.thoreum.thunder_pools

async def get_pyq_trove(session):
    return ['0xA2A065DBCBAE680DF2E6bfB7E5E41F1f1710e63b']

async def get_pyq_triple(session):
    return ['0xf2F4326E96cCC834216A7F95b96BD51239880048']

async def get_pyq_double(session):
    return ['0x445098d74B6eB4f3BCF20865989b777ee405a48C']

async def get_pyq_vaults(session):
    return poolext.pyq.pyq_farm_list

async def get_ele_multi(session):
    return ['0xf0a92566Eb2abBf1F33DF407Af16E6cc563768C1']

async def get_ele_staking_bsc(session):
    return ['0x3Ed531BfB3FAD41111f6dab567b33C4db897f991']

async def get_polycrystal_staking(session):
    return ['0x5BaDd6C71fFD0Da6E4C7D425797f130684D057dd']

async def get_ele_staking_avax(session):
    return ['0x399e0348BdAb853576df586027ddeb1cb25Fae2C']

async def dummy_vault(session):
    return ['0xDummy']

async def get_beefy_matic_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/polygon_pools.js')
    s2 = "export const polygonPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    data = re.sub(r'\saddLiquidityUrl:\s.+(\,)', " nothing: '',", data)
    data = re.sub(r'\sbuyTokenUrl:\s.+(\,)', " nothing: '',", data)
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]
    vault_data.append({'vault' : '0x1d23ecC0645B07791b7D99349e253ECEbe43f614', 'want' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'})

    return vault_data

async def get_beefy_fantom_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/fantom_pools.js')
    s2 = "export const fantomPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]
    vault_data.append({'vault' : '0x49c68eDb7aeBd968F197121453e41b8704AcdE0C', 'want' : '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'})

    return vault_data

async def get_beefy_arb_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/arbitrum_pools.js')
    s2 = "export const arbitrumPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

async def get_beefy_avax_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/avalanche_pools.js')
    s2 = "export const avalanchePools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

async def get_qs_vaults(session):
        scraper = cloudscraper.create_scraper(delay=2)
        r = scraper.get('https://quickswap.exchange/staking.json')
        cleaner = r.text[1:-1].replace("\\","")
        cleaned = json.loads(cleaner)
        return [each['stakingRewardAddress'] for each in cleaned if each['ended'] == False]
    
async def get_dfyn_vaults(session):
    tasks = []
    urls = ['https://raw.githubusercontent.com/dfyn/dfyn-farms-info/main/ecosystem-farms.js', 'https://raw.githubusercontent.com/dfyn/dfyn-farms-info/main/popular-farms.js']
    for url in urls:
        task = asyncio.ensure_future(make_get_hson(session, url))
        tasks.append(task)

    maping = await asyncio.gather(*tasks)

    return_list = []

    for each in maping:
        for contract in each:
            if contract['stakingRewardAddress'] not in ['0x98D7c004C54C47b7e65320Bd679CB897Aae6a6D']:
                return_list.append(contract['stakingRewardAddress'])
    
    return return_list

async def get_dfyn_dual(session):
    url = 'https://raw.githubusercontent.com/dfyn/dfyn-farms-info/main/dual-stake.js'
    maping = await make_get_hson(session, url)
    return_list = []

    for each in maping:
        return_list.append(each['stakingRewardAddress'])
    
    return return_list

async def get_hyperjump_vaults(session):
    r = await make_get(session,'https://hyperjump.fi/configs/vaults/bsc_pools.js')
    s2 = "export const bscPools = "
    data = r[r.index(s2) + len(s2) :len(r)-2]
    f = hjson.loads(data)
    return [x['earnedTokenAddress'] for x in json.loads(json.dumps(f))]

async def get_hyperjump_vaults_ftm(session):
    r = await make_get(session,'https://hyperjump.fi/configs/vaults/ftm_pools.js')
    s2 = "export const ftmPools = "
    data = r[r.index(s2) + len(s2) :len(r)-2]
    f = hjson.loads(data)
    return [x['earnedTokenAddress'] for x in json.loads(json.dumps(f))]

async def get_autoshark_vaults(network, session):
    r = await make_get(session,'https://old.autoshark.finance/api/v2/vaults')
    r = json.loads(r)['data']
    return [x['address'] for x in r if x['address'] != '0x85ff09374D1f59288b6978EB9254377a51BE0B7c' and x['network'] == network]

async def get_aperocket_vaults(session):
    r = poolext.aperocket.ape_rockets
    return [x['address'] for x in r if x['address'] != '0xd79dc49Ed716832658ec28FE93dd733e0DFB8d58']

async def get_aperocket_vaults_matic(session):
    r = poolext.aperocket.ape_rockets_matic
    return [x['address'] for x in r if x['address'] != '0xBa56A30ec2Ee2B4C3c7EE75e0CFEbcD1b22dE8cd']

async def get_thunder_pools(session):
    r = poolext.thoreum.thunder_pools
    return r

async def get_acryptos_vaults(session):
    r = await make_get_json(session, 'https://api.unrekt.net/api/v1/acryptos-asset')
    return [r['assets'][x]['addressvault'] for x in r['assets'] if r['assets'][x]['addressvault'] != '0xa82f327bbbf0667356d2935c6532d164b06ceced']

async def pull_koge_vaults(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/kogecoin/vault-contracts/main/vaultaddresses')
    return ast.literal_eval(r)

async def get_pancakebunny_pools(network, session):
    urls = {'bsc' : 'https://us-central1-pancakebunny-finance.cloudfunctions.net/api-bunnyData', 'matic' : 'https://us-central1-bunny-polygon.cloudfunctions.net/api-bunnyData'}
    r = await make_get_json(session, urls[network])
    return [x for x in r['apy'] if x not in ['0x48e198477A4cB41A66B7F4F4aCA2561eBB216d33', '0x4eB4eC9625896fc6d6bB710e6Df61C20f4BAa6d7', '0xE0a20F904f88715431b926c42258480f28886920', '0x4fd0143a3DA1E4BA762D42fF53BE5Fab633e014D']]

async def get_balancer_pools(session):
    balancer_pools = await call_graph('https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-polygon-v2', {'query': bitquery.balancer_pools.query, 'variable' : None}, session)

    return [x['address'] for x in balancer_pools['data']['pools']]

async def get_apeswap_pools_old(session):
    r = await make_get_json(session, 'https://api.apeswap.finance/stats')
    return [x['address'] for x in r['incentivizedPools'] if x['active'] is True and x['id'] < 52]

async def get_apeswap_pools_new(session):
    r = await make_get_json(session,'https://api.apeswap.finance/stats')
    return [x['address'] or x['id'] == 76 for x in r['incentivizedPools'] if x['active'] is True and x['id'] > 52 and x['id'] != 76]

async def get_beefy_boosts_poly(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/polygon_stake.js')
    s2 = "export const polygonStakePools = ["
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    hson = hjson.loads(f'[{regex}]'.replace('partners: ,','').replace('assets: ,',''))
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t if x['status'] == 'active']

async def get_pcs_pools(session, offset):
    r = await make_get(session, 'https://raw.githubusercontent.com/pancakeswap/pancake-frontend/develop/src/config/constants/pools.ts')
    s2 = "const pools: SerializedPoolConfig[] = "
    s_end = "export default pools"
    data = r[r.index(s2) + len(s2) :r.index(s_end)]
    hson = hjson.loads(data)
    t = json.loads(json.dumps(hson))
    pcs_pools = []
    pcs_older = []
    for each in t:
        contract_address = each['contractAddress']['56']
        if contract_address not in ['0x73feaa1eE314F8c655E354234017bE2193C9E24E']:
            if 'isFinished' in each:
                if each['isFinished'] is False and each['sousId'] > 116:
                    pcs_pools.append(contract_address)
                elif each['isFinished'] is False and each['sousId'] < 116:
                    pcs_older.append(contract_address)        
            elif each['sousId'] > 116:
                pcs_pools.append(contract_address)
            else:
                pcs_older.append(contract_address)

    all_pools = [pcs_pools,pcs_older]
    
    return all_pools[offset]

async def get_pcs_auto(session):
    return ['0xa80240Eb5d7E05d3F250cF000eEc0891d00b51CC']

async def get_baby_auto(session):
    return ['0x3e1eaD5cBe817689F4bDB96bceeb112FdBE94dBc']

async def get_pickle_addresses(session,network):
    r = await make_get_json(session, 'https://d38jrn41whs0ud.cloudfront.net/prod/protocol/pools')
    return [x['jarAddress'] for x in r if x['network'] == network]

async def get_wault_pool_contracts(session):
    round_time = round(time.time())
    url = f'https://api.wault.finance/wpoolsData.js?ts={round_time}'
    r = await make_get(session, url)
    s2 = "var wpoolsData = "
    data = r[r.index(s2) + len(s2) :len(r)]
    r = json.loads(data)
    r = [x['contractAddress'] for x in r]
    return r

async def get_paprprintr_vaults(network, session):
    r = await make_get_json(session, 'https://paprprintr-api.herokuapp.com/api/vaults')
    r = [r[x]['config']['vault'] for x in r if r[x]['network'] == network and r[x]['config']['vault'] is not None]
    return r

async def get_superfarm_pools(session):
    r = await make_get_json(session, 'https://superlauncher.io/farms/farms.json')
    return [x['farmAddresses'] for x in r]

async def get_snowball_guage(session):
    balancer_pools = await call_graph('https://snob-backend-api.herokuapp.com/graphql', {'query': bitquery.snowball.query, 'variable' : None}, session)

    return [x['gaugeAddress'] for x in balancer_pools['data']['SnowglobeContracts']]

async def get_snowball_globe(session):
    balancer_pools = await call_graph('https://snob-backend-api.herokuapp.com/graphql', {'query': bitquery.snowball.query, 'variable' : None}, session)

    return [x['snowglobeAddress'] for x in balancer_pools['data']['SnowglobeContracts']]

async def get_curve_gauage(network, session):
    if network == 'matic':
        return poolext.curve.polygon_gauges
    elif network == 'ftm':
        return poolext.curve.ftm_gauges
    else:
        return []
    
async def get_telx(style, session):
    if style == 'single':
        return poolext.telx.single
    elif style == 'double':
        return poolext.telx.double
    else:
        return []

async def get_papr_native_bsc(session):
    return poolext.paprprintr.bsc_natives + poolext.paprprintr.bsc_pools

async def get_papr_print_bsc(session):
    return poolext.paprprintr.bsc_printer

async def get_papr_native_matic(session):
    return poolext.paprprintr.matic_natives

async def get_papr_print_matic(session):
    return poolext.paprprintr.matic_printer

async def get_dino_pools(session):
    return poolext.dinoswap.pools

async def get_superfarm_extra(session):
    return ['0x8C73dC245D2626311dD28319793893460B358F3c']

async def get_pandaswap_farms(session):
    return poolext.pandaswap.farms

async def get_cherry_farms(session):
    return poolext.cherry.pools

async def get_feeder_auto(session):
    return poolext.feeder.auto_staking

async def get_feeder_sfeed(session):
    return poolext.feeder.sfeed
    
async def get_polygonfarm_pools(session):
    return poolext.polygonfarm.pools

async def get_polygonfarm_staking(session):
    return poolext.polygonfarm.staking

async def get_polyfund_vault(session):
    return ['0xdcfd912b50904B4d5745DfFe0D4d7a5097c82849']

async def get_dk_jewel(session):
    return ['0x72Cb10C6bfA5624dD07Ef608027E366bd690048F']

async def get_ironlend_vaults(session):
    return poolext.ironlend.vaults

async def get_ironlend_rewards(session):
    return poolext.ironlend.rewards

async def get_benqi_vaults(session):
    return poolext.benqi.vaults

async def get_zombie_pools(session):
    return poolext.rugzombie.pools

async def get_tengu_stakes(session):
    return ['0xd38cE88CAf05FFDb193Ba95fce552c5129E42C89']

async def get_macaron_syrup(session):
    return ['0xCded81aa5Ab3A433CadF77Fd5aC8B6fD973906e1', '0xF69bdcDB577F98753d4890Cc5aCfF3BE00177584', '0x7DB34B681c759918079C67EeF08868225F34fbcB', '0x13ED683DDf483d1f0bd2AE02b01D4d1D451D6c5b', '0x0f819C8E6A7c0F0906CBc84b9b1e6642f9634E61', '0x903A20CDbAC174250eAcc7437720929f0dE97B99', '0x82cF07a989835b68260989F13Bc853f8fe48ad04', '0xc8De98F603af53a5D52AF6AA153d9e15b0002B2c', '0xf3D514263239672455306D188DD5f045E61deD03', '0xC85C50988AEC8d260853443B345CAE63B7432b7A', '0xF60EDbF7D95E79878f4d448F0CA5622479eB8790']

async def get_macaron_auto(session):
    return ['0x0608A42BA74F2026A88aC2304f6802838F36bEB5', '0xCd59d44E94Dec10Bb666f50f98cD0B1593dC3a3A', '0x6dAc44A858Cb51e0d4d663A6589D2535A746607A', '0xd474366F6c80230507481495F3C1490e62E3093F']

async def get_morpheus_syrup(session):
    return ['0x2854980e1f6526CB5AeC8d53c5028AF486368ea1', '0x415742c217eA4941B706ff358bF6178985590cFA', '0x8b0c89A08045A38A710fd141443d463B960C9aAe', '0x9055064B490604E41593d9271a53603CF48204F4', '0x4bDA0C69f7F15a43Ef35881c2aB3B7f995630A14', '0x5db1AD1E0ECC9EfBF69d3566C54eE650Cd712Fa5', '0x791A8d97FeeF371D1AEc6f25B7C3E4545c847476']

async def get_jetswap_vaults(network, session):
    if network == 'polygon':
        r = await make_get_json(session, 'https://polygon.jetswap.finance/api/vaults.json')
        r = [x['vaultAddresses']['137'] for x in r]
        return r
    elif network == 'bsc':
        r = await make_get_json(session, 'https://jetswap.finance/api/vaults.json')
        r = [x['vaultAddresses']['56'] for x in r]
        return r

async def get_elk_vaults(network, session):
        ROUNDS = 7
        STAKING = {"ftm":{"ELK":"0x6B7E64854e4591f8F8E552b56F612E1Ab11486C3"},"xdai":{"ELK":"0xAd3379b0EcC186ddb842A7895350c4657f151e6e"},"avax":{"ELK":"0xB105D4D17a09397960f2678526A4063A64FAd9bd"},"bsc":{"ELK":"0xD5B9b0DB5f766B1c934B5d890A2A5a4516A97Bc5"},"matic":{"ELK":"0xB8CBce256a713228F690AC36B6A0953EEd58b957"},"heco":{"ELK":"0xdE16c49fA4a4B78071ae0eF04B2E496dF584B2CE"}}
        r = await cf_make_get_json(session, 'https://api.elk.finance/v1/info/farms')
        
        vaults = []

        for round in range(0,ROUNDS):
            a = round + 1

            if network in r[f'round{a}']:
                for vault in r[f'round{a}'][network]:
                    vaults.append(r[f'round{a}'][network][vault]['address'])
        vaults.append(STAKING[network]['ELK'])

        return vaults



async def stadium_farm_info(session):
    return poolext.ext_masterchef.stadium_farm_info

async def darkside_info(session):
    return poolext.ext_masterchef.darkside_farm_info

async def moonpot_contracts(session):
    return poolext.moonpot.moonpot_contracts

async def png_staking(session):
    return poolext.png.staking_rewards

async def yak_vaults(session):
    return poolext.yak.vaults

async def qubit_vaults(session):
    return poolext.qubit.vaults

async def geist_vaults(session):
    return poolext.geist.vaults

async def get_pancakehunny(session):
    return poolext.pancake_hunny.reward_info

async def get_horizon(session):
    return poolext.horizon.horizon_vaults

async def diamond_vaults(session):
    return poolext.diamondhand.diamonds

async def get_merlin_vaults(session):
    return poolext.merlin.magic

async def get_jetfuel_vaults(session):
    return poolext.jetfuel.vaults

async def get_wault_locked(session, network):
    if network == 'bsc':
        return poolext.wault_locked.bsc
    elif network == 'polygon':
        return poolext.wault_locked.polygon

async def gambit_vaults(session):
    return poolext.gambit.gambits

async def gmx_vaults(session):
    return poolext.gmx.vaults

async def squirrel_vaults(session):
    return poolext.squirrel.nuts

async def get_adamant_vaults(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/eepdev/vaults/main/current_vaults.json')
    return json.loads(r)

async def get_adamant_vaults_arb(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/eepdev/vaults/main/arbitrum_vaults.json')
    return json.loads(r)

async def get_adamant_boosts(session):
    return ['0xC5bCD23f21B6288417eB6C760F8AC0fBb4bb8a56']

async def get_adamant_boosts_arb(session):
    return ['0x097b15dC3Bcfa7D08ea246C09B6A9a778e5b007B']

async def get_fortress_vaults(session):
    return poolext.fortress.forts

async def get_dyp(session):
    return poolext.dyp.dypPools

async def get_taodao(session):
    return poolext.taodao.dao

async def get_bishare(session):
    return poolext.bishare.vaults

async def get_buffer_vaults(session):
    return ['0xe65d029AaC2c0a2dF4F61A759b942CCDa4d2EeFC']

async def get_wonderland_bonds(session):
    return []
