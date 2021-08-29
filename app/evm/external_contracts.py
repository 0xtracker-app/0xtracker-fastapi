import json
import hjson
import re
import os
import requests
import time
import cloudscraper
from . utils import make_get,make_get_json

async def get_beefy_bsc(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/bsc_pools.js')
    s2 = "export const bscPools = "

    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    return [x['earnedTokenAddress'] for x in cleaned_up]
        
async def get_beefy_boosts(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/bsc_stake.js')
    data = r.replace('_', '-')
    return [x['earnContractAddress'] for x in json.loads(json.dumps(hjson.loads(data[67:-2])))]

def get_vsafes():
    r = requests.get('https://api-vfarm.vswap.fi/api/farming-scan/get-farming-scans?group=vsafe')
    return json.loads(r.text)['data']

def get_firebird_vaults():
    r = requests.get('https://farm-api-polygon.firebird.finance/api/farming-scan/get-farming-scans?group=fvault')
    return json.loads(r.text)['data']

def get_ele_tokens(network=None):
    skip_tokens = ['0x3Ed531BfB3FAD41111f6dab567b33C4db897f991', '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f', '0x0D5BaE8f5232820eF56D98c04B8F531d2742555F', '0xDF098493bB4eeE18BB56BE45DC43BD655a27E1A9', '0x27DD6E51BF715cFc0e2fe96Af26fC9DED89e4BE8', '0x025E2e9113dC1f6549C83E761d70E647c8CDE187']
    token = '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'
    headers = {'accept': 'application/vnd.github.v3.raw',
                'authorization': 'token {}'.format(token)}
    r = requests.get('https://raw.githubusercontent.com/Eleven-Finance/elevenfinance/main/src/features/configure/pools.js', headers=headers)
    r = r.text
    s2 = "export const pools = "
    data = r[r.index(s2) + len(s2) :len(r)-2]
    data = data.replace("+","")
    data = data.replace("depositWarning: '<p>Be aware of <b>4% Deposit fee</b> on this pool.</p>'", "")
    data = data.replace("'<p>The fee is charged by Polycat, Eleven doesn\\'t charge you on the deposit</p>',", "")
    data = hjson.loads(data.replace("\\",""))
    response = json.loads(json.dumps(data))
    if network is None:
        return response
    else:
        return [x['earnedTokenAddress'] for x in response if '11' in x['earnedToken'] and x['network'] == network and x['earnedTokenAddress'] not in skip_tokens]

def get_beefy_matic_pools():
    r = requests.get('https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/polygon_pools.js')
    r = r.text
    s2 = "export const polygonPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    
    return hjson.loads(data.replace("\\",""))

def get_beefy_fantom_pools():
    r = requests.get('https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/fantom_pools.js')
    r = r.text
    s2 = "export const fantomPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    return [x['earnedTokenAddress'] for x in cleaned_up]

def get_beefy_avax_pools():
    r = requests.get('https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/avalanche_pools.js')
    r = r.text
    s2 = "export const avalanchePools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    return [x['earnedTokenAddress'] for x in cleaned_up]

def get_quickswap_vaults():
    try:
        scraper = cloudscraper.create_scraper()
        r = scraper.get('https://quickswap.exchange/staking.json')
        cleaner = r.text[1:-1].replace("\\","")
        cleaned = json.loads(cleaner)
        return [each['stakingRewardAddress'] for each in cleaned if each['ended'] == False]
    except:
        file_path = os.path.join('app','evm','poolext', 'quick_swap.json')
        r = open(file_path, 'r').read()
        cleaner = r[1:-1].replace("\\","")
        cleaned = json.loads(cleaner)
        return [each['stakingRewardAddress'] for each in cleaned if each['ended'] == False]

def get_dfyn_vaults():
    urls = ['https://raw.githubusercontent.com/dfyn/dfyn-farms-info/main/ecosystem-farms.js', 'https://raw.githubusercontent.com/dfyn/dfyn-farms-info/main/popular-farms.js']

    return_list = []

    for each in maping:
        for contract in each:
            if contract['stakingRewardAddress'] not in ['0x98D7c004C54C47b7e65320Bd679CB897Aae6a6D']:
                return_list.append(contract['stakingRewardAddress'])
    
    return return_list

def get_dfyn_dual():
    url = 'https://raw.githubusercontent.com/dfyn/dfyn-farms-info/main/dual-stake.js'

    return_list = []

    for each in maping:
        return_list.append(each['stakingRewardAddress'])
    
    return return_list

def get_iron_vaults():
    r = requests.get('https://api.iron.finance/farms')
    r = json.loads(r.text)['pools']

    data = { x['masterChef']+'_'+str(x['id']) : x for x in r }

    return data

def get_hyperjump_vaults():
    r = requests.get('https://hyperjump.fi/configs/vaults/bsc_pools.js')
    r = r.text
    s2 = "export const bscPools = "
    data = r[r.index(s2) + len(s2) :len(r)-2]
    f = hjson.loads(data)
    return json.loads(json.dumps(f))

def get_hyperjump_vaults_ftm():
    r = requests.get('https://hyperjump.fi/configs/vaults/ftm_pools.js')
    r = r.text
    s2 = "export const ftmPools = "
    data = r[r.index(s2) + len(s2) :len(r)-2]
    f = hjson.loads(data)
    return json.loads(json.dumps(f))

def get_autoshark_vaults(network):
    r = json.loads(requests.get('https://old.autoshark.finance/api/v2/vaults').text)['data']
    return [x['address'] for x in r if x['address'] != '0x85ff09374D1f59288b6978EB9254377a51BE0B7c' and x['network'] == network]

def get_aperocket_vaults():
    r = ape_rockets
    return [x['address'] for x in r if x['address'] != '0xd79dc49Ed716832658ec28FE93dd733e0DFB8d58']

def get_aperocket_vaults_matic():
    r = ape_rockets_matic
    return [x['address'] for x in r if x['address'] != '0xBa56A30ec2Ee2B4C3c7EE75e0CFEbcD1b22dE8cd']

def get_acryptos_vaults():
    r = json.loads(requests.get('https://api.unrekt.net/api/v1/acryptos-asset').text)
    return [r['assets'][x]['addressvault'] for x in r['assets'] if r['assets'][x]['addressvault'] != '0xa82f327bbbf0667356d2935c6532d164b06ceced']

def pull_koge_vaults():
    r = requests.get('https://raw.githubusercontent.com/kogecoin/vault-contracts/main/vaultaddresses').text
    return r

def get_pancakebunny_pools(network):
    urls = {'bsc' : 'https://us-central1-pancakebunny-finance.cloudfunctions.net/api-bunnyData', 'matic' : 'https://us-central1-bunny-polygon.cloudfunctions.net/api-bunnyData'}
    r = json.loads(requests.get(urls[network]).text)['apy']
    return [x for x in r if x not in ['0x48e198477A4cB41A66B7F4F4aCA2561eBB216d33', '0x4eB4eC9625896fc6d6bB710e6Df61C20f4BAa6d7', '0xE0a20F904f88715431b926c42258480f28886920']]

def get_balancer_pools():
    balancer_pools = call_graph('https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-polygon-v2', {'query': balancer_pools.query, 'variable' : None})

    return [x['address'] for x in balancer_pools['data']['pools']]

def get_apeswap_pools():
    r = json.loads(requests.get('https://api.apeswap.finance/stats').text)
    return ([x['address'] for x in r['incentivizedPools'] if x['active'] is True and x['id'] < 52], [x['address'] or x['id'] == 76 for x in r['incentivizedPools'] if x['active'] is True and x['id'] > 52 and x['id'] != 76])

def get_beefy_boosts_poly():
    r = requests.get('https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/polygon_stake.js').text
    s2 = "export const polygonStakePools = ["
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    hson = hjson.loads(f'[{regex}]'.replace('partners: ,',''))
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t if x['status'] == 'active']

def get_pcs_pools():
    r = requests.get('https://raw.githubusercontent.com/pancakeswap/pancake-frontend/develop/src/config/constants/pools.ts').text
    s2 = "const pools: PoolConfig[] = "
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

    
    return pcs_pools,pcs_older

def get_pickle_addresses(network):
    r = json.loads(requests.get('https://d38jrn41whs0ud.cloudfront.net/prod/protocol/pools').text)
    
    return [x['jarAddress'] for x in r if x['network'] == network]

def get_wault_pool_contracts():
    r = requests.get('https://api.wault.finance/wpoolsData.js?ts=%s' % (round(time.time()))).text
    s2 = "var wpoolsData = "
    data = r[r.index(s2) + len(s2) :len(r)]
    r = json.loads(data)
    r = [x['contractAddress'] for x in r]
    return r

def get_paprprintr_vaults(network):
    r = json.loads(requests.get('https://paprprintr-api.herokuapp.com/api/vaults').text)
    r = [r[x]['config']['vault'] for x in r if r[x]['network'] == network and r[x]['config']['vault'] is not None]
    return r

def get_superfarm_pools():
    r = json.loads(requests.get('https://superlauncher.io/farms/farms.json').text)
    return [x['farmAddresses'] for x in r]

def get_snowball_guage():
    balancer_pools = call_graph('https://snob-backend-api.herokuapp.com/graphql', {'query': bitquery.snowball.query, 'variable' : None})

    return [x['gaugeAddress'] for x in balancer_pools['data']['SnowglobeContracts']]

def get_snowball_globe():
    balancer_pools = call_graph('https://snob-backend-api.herokuapp.com/graphql', {'query': bitquery.snowball.query, 'variable' : None})

    return [x['snowglobeAddress'] for x in balancer_pools['data']['SnowglobeContracts']]

# hyperjump_vault_list = [x['earnedTokenAddress'] for x in get_hyperjump_vaults()]

# beefyVaults = json.loads(json.dumps(getBeefyVaults()))
# beefyCheck = {x['earnedTokenAddress'].lower() : x for x in beefyVaults}

# beefyBoosts = json.loads(json.dumps(getBeefyBoosts()))
# bBoostsCheck = {x['id'].lower() : x for x in beefyBoosts if x['status'] == 'active'}

# catchENRV = {x['earnedTokenAddress'] : x for x in extNerve}