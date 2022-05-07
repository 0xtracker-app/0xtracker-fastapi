import json
import hjson
import re
import os
import requests
import time
import js2py
import cloudscraper
from requests.sessions import session
from ..redis.cache import cache_function
from .utils import make_get, make_get_hson,make_get_json,cf_make_get_json
from .multicall import parsers
from .thegraph import call_graph
from . import poolext
from . import bitquery
import asyncio
import ast
from dotenv import load_dotenv

load_dotenv()

CONTRACTS_TTL = os.getenv("CACHE_TTL_CONTRACTS", 86400)

async def get_quickswap_lps(wallet, session):
    x = await call_graph('https://api.thegraph.com/subgraphs/name/sameepsi/quickswap03', {'operationName' : 'liquidityPositions', 'query' : bitquery.quickswap_lps.query, 'variables' : {'user': wallet.lower()}}, session)
    return x

async def get_voltswap(wallet, session):
    geysers = await call_graph('https://newgraph.voltswap.finance/subgraphs/name/meter/geyser-v2', {'operationName' : 'getGeysers', 'query' : bitquery.voltswap.geysers}, session)
    vault = await call_graph('https://newgraph.voltswap.finance/subgraphs/name/meter/geyser-v2', {'operationName' : 'getUserVault', 'query' : bitquery.voltswap.user_vaults, 'variables' : {'user': wallet.lower()}}, session)
    if vault['data']['user']:
        return {'geysers' : geysers['data']['geysers'], 'user_vaults' : vault['data']['user']['vaults']}
    else:
        return {'geysers' : [], 'user_vaults' : []}

async def get_voltswap_theta(wallet, session):
    geysers = await call_graph('https://geyser-graph-on-theta.voltswap.finance/subgraphs/name/theta/geyser-v2', {'operationName' : 'getGeysers', 'query' : bitquery.voltswap.geysers}, session)
    vault = await call_graph('https://geyser-graph-on-theta.voltswap.finance/subgraphs/name/theta/geyser-v2', {'operationName' : 'getUserVault', 'query' : bitquery.voltswap.user_vaults, 'variables' : {'user': wallet.lower()}}, session)
    if vault['data']['user']:
        return {'geysers' : geysers['data']['geysers'], 'user_vaults' : vault['data']['user']['vaults']}
    else:
        return {'geysers' : [], 'user_vaults' : []}

async def get_voltswap_moon(wallet, session):
    geysers = await call_graph('https://geyser-graph-on-moonbeam.voltswap.finance/subgraphs/name/moonbeam/token-geyser-v2', {'operationName' : 'getGeysers', 'query' : bitquery.voltswap.geysers}, session)
    vault = await call_graph('https://geyser-graph-on-moonbeam.voltswap.finance/subgraphs/name/moonbeam/token-geyser-v2', {'operationName' : 'getUserVault', 'query' : bitquery.voltswap.user_vaults, 'variables' : {'user': wallet.lower()}}, session)
    if vault['data']['user']:
        return {'geysers' : geysers['data']['geysers'], 'user_vaults' : vault['data']['user']['vaults']}
    else:
        return {'geysers' : [], 'user_vaults' : []}

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

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_reaper_ftm(session):
    r = await make_get_json(session, 'https://yzo0r3ahok.execute-api.us-east-1.amazonaws.com/dev/api/crypts')

    vault_data = [{'vault' : x['cryptContent']['vault']['address'], 'want' : x['cryptContent']['lpToken']['address']} for x in r['data']]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_bsc(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/bsc_pools.js')
    s2 = "export const bscPools = "

    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]
    vault_data.append({'vault' : '0x6BE4741AB0aD233e4315a10bc783a7B923386b71', 'want' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'})

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_vaporware_vaults(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/VaporwaveFinance/vwave-app-pub/c87be24cfaa2ba13914b18f11ac8d8c17bc19585/src/features/configure/vault/aurora_pools.js')
    s2 = "export const auroraPools = "

    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x if x['status'] == 'active']

    return vault_data
 
@cache_function(ttl=CONTRACTS_TTL, keyparams=0)        
async def get_beefy_boosts(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/bsc_stake.js')
    s2 = "export const bscStakePools = ["
    
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    x = f'[{regex}]'.replace('partners: ,','').replace('assets: ,','')
    hson = hjson.loads(x)
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_boosts_fuse(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/fuse_stake.js')
    s2 = "export const fuseStakePools = ["
    
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    x = f'[{regex}]'.replace('partners: ,','').replace('assets: ,','')
    hson = hjson.loads(x)
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_metis_boosts(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/metis_stake.js')
    s2 = "export const metisStakePools = ["
    
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    x = f'[{regex}]'.replace('partners: ,','').replace('assets: ,','')
    hson = hjson.loads(x)
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_vsafes(session):
    try:
        r = await make_get_json(session,'https://api-vfarm.vswap.fi/api/farming-scan/get-farming-scans?group=vsafe')
    except:
        return []
    return [x['id'] for x in r['data']]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_grim_vaults(session):
    r = await make_get_json(session,'https://api.grim.finance/vaults')
    return [x['earnedTokenAddress'] for x in r]

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_firebird_vaults(network, session):
    r = await make_get_json(session,f'https://api-be.firebird.finance/api/apy?group=vault&chain_id={network}')
    return [x['farmingContractAddress'] for x in r['data']]

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_ele_tokens(network=None, session=None):
    skip_tokens = ['0x3Ed531BfB3FAD41111f6dab567b33C4db897f991', '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f', '0x0D5BaE8f5232820eF56D98c04B8F531d2742555F', '0xDF098493bB4eeE18BB56BE45DC43BD655a27E1A9', '0x27DD6E51BF715cFc0e2fe96Af26fC9DED89e4BE8', '0x025E2e9113dC1f6549C83E761d70E647c8CDE187', '0x0FFb84A4c29147Bd745AAe0330f4F6f4Cb716c92']
    token = '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'
    headers = {'accept': 'application/vnd.github.v3.raw',
                'authorization': 'token {}'.format(token)}
    r = await make_get(session,'https://raw.githubusercontent.com/Eleven-Finance/elevenfinance/main/src/features/configure/pools.js', kwargs={'headers':headers})
    # s2 = "export const pools = "
    # text_remove = """\'<b>You aren\\\'t earning the maximum rewards yet.</b><br/><br/>Pool Boosted Rewards are migrating to new \' +\n          \'contract version.<br/><b>Unstake</b> all your tokens and then <b>Stake</b> them again to receive Increased \' +\n          \'Rewards in <b>ELE</b> and <b>MATIC</b><br/><br/><b>IMPORTANT:</b> You don\\\'t need to <b>Withdraw</b> funds, \' +\n          \'just to <b>Unstake</b> them.\'"""
    # data = r[r.index(s2) + len(s2) :len(r)-2]
    # data = data.replace(text_remove, " ' ' ")
    # data = data.replace("+","")
    # data = data.replace("depositWarning: '<p>Be aware of <b>4% Deposit fee</b> on this pool.</p>'", "")
    # data = data.replace("'<p>The fee is charged by Polycat, Eleven doesn\\'t charge you on the deposit</p>',", "")
    # data = hjson.loads(data.replace("\\",""))
    data = r.split('export const pools = ')[1]
    response = list(js2py.eval_js(data))
    # response = json.loads(json.dumps(data))
    if network is None:
        return response
    else:
        return [x['earnedTokenAddress'] for x in response if 'earnedToken' in x and '11' in x['earnedToken'] and x['network'] == network and x['earnedTokenAddress'] not in skip_tokens]

async def get_ele_staking_matic(session):
    return ['0x0FFb84A4c29147Bd745AAe0330f4F6f4Cb716c92']

async def get_space_pool_bsc(session):
    return ['0xd79dc49Ed716832658ec28FE93dd733e0DFB8d58']

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_wault_pools_matic(session):
    round_time = round(time.time())
    url = f'https://polyapi.wault.finance/wpoolsData.js?ts={round_time}'
    r = await make_get(session, url)
    s2 = "var wpoolsData = "
    data = r[r.index(s2) + len(s2) :len(r)]
    r = json.loads(data)
    r = [x['contractAddress'] for x in r if x['tvl'] > 1]
    return r

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_thorus_bonds(session):
    round_time = round(time.time())
    url = f'https://api.thorus.fi/bonds.json?t={round_time}'
    r = await make_get_json(session, url)

    r = [x['address'] for x in r]
    return r

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_thorus_bonds_moonbeam(session):
    round_time = round(time.time())
    url = f'https://api.thorus.fi/moonbeam_bonds.json?t={round_time}'
    r = await make_get_json(session, url)

    r = [x['address'] for x in r]
    return r

async def get_blockmine(session):
    return [
        '0x45E6729373db693e1422FbBdF0EaF530E09Bd388',
        '0x7794318ddbcd30287f77F54a500a04494Af7C174',
        '0x8052D595E75c2E6e452bd2302aa1E66eAdBE2b42',
        '0xDbd85332d6f6Edd1b66ba0594355aAAA140c1F07',
        '0x5e5964dfcbe523387cb86f7fbd283f64acd6c21a',
        '0xa3eb5952Db45dB016C62333d91aF087cB44ac51e',
        '0x690d605a6f6fEA6069e5B946D1226d443421e870',
        '0x0c85C19a0ad8317Ce1b5d0A31097F8d0B4cd8981',
        '0x9cd3208AdB17F5976e949b0D0c5A37797B44f9a0',
        '0x0E512e81d5A686d5921eB116DAE7F706b58A726f',
        '0x089854958ade4e0a911feac1a7e70b7885999b07',
        '0xb0510fb98b645d2326ab7c93842468ecb35bd807',
        '0x3b55ffeab855cfb7a94ff086440d3a19421bfe04',
        '0x5563615982b07d26b9490f79f5ad69a89826bd5f',
        '0xae71336966a20d86dd785ab20d92506e928e168a',
        '0x9c44b5c305bcc4ffdfa5eab946a6cf11e5d7c9e6',
        '0x02e212c49df633b9cf26f01d182984741cd91454'
        ]

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

async def get_starstream_vaults(session):
    return [
        '0xFB050923d8fd638c4d03eeB9B6d2e5234892dE8C',
        '0x4fa0594B5347a0e1640ABf167aefE58AD610be63',
        '0x4ba560e193f928df42350944540215639cbB4614',
        '0xa18B53d8E700708a399d63Dff5704D84F54A35ce',
        '0xC28Be7A75ab513543d166B6B41dEbF0A3Cd3FFa2',
        '0xABBF10582632C5460859A2877f063DFb23B1f7Bf',
        '0xCDaBe937bcFb7aB18FBB021fE4D4308E0662191e',
        '0xAc7D4805f12e57594FC5EB7FE5E5bff0Cbb4712f',
        '0x8377eb57113919086d41F0511f97474D57dDd8e9',
        '0x5Ec8Bd9Fc606A0a5AbC7937CfA99ca22c0040266'
        ]

async def get_apolyyeld(session):
    return ['0xc49bc7118a73Ca6CB36Bfa454FD40eCAE079a463']

async def get_wagmi(session):
    return ['0xaa2c3396cc6b3dc7b857e6bf1c30eb9717066366']

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

async def euler_staking(session):
    return ['0xb18faB4C6f054e734EA169561787CC87928f54Ee']

async def tomb_staking(session):
    return ['0x8764DE60236C5843D9faEB1B638fbCE962773B67']

async def bouje_staking(session):
    return ['0x5BE35C02996320688F9E5968148dE5bC31635f15']

async def knight_staking(session):
    return ['0xe790a0683b669089AdC199996F89Bd40FEd4C559', '0x3b8B92D882127b5e14c9476615374a69e55d4Ca1', '0xF928BB46273043F98cc731CeFFc16A1ccC177707']

async def crona_staking(session):
    return ['0xDf3EBc46F283eF9bdD149Bb24c9b201a70d59389']

async def crona_vaults(session):
    return ['0x507Ee4C2dA5fdc12Fa7DDDb66a338230D5ED1f41', '0xc0Ace9DEF4b1cCE2c91A6c90BB720a90718ecf80']

async def vvs_staking(session):
    return ['0xA6fF77fC8E839679D4F7408E8988B564dE1A2dcD']

async def vvs_vaults(session):
    return ['0xc0Ace9DEF4b1cCE2c91A6c90BB720a90718ecf80']

async def crodex_vaults(session):
    return [
    "0xDb752eB155F6075d4Ba0e09c371eB5eBB0D4bAA5",
    "0xc2FF850F3921C1dbeD263aa1Fa94FE2A898870a8",
    "0x681E1dC139FEB9024F1C63b37673cFCD630817Bb",
    "0xcdd27c1C74631700CA0Fa165f3450435C8D009f4",
    "0x81E200976B7928aEFD34CE51544e65FE73e88bE4",
    "0x8857591ea846cB23795538a7521c868f0E0D6844",
    "0x0f1e250f10F6AEb95A1B73DFd1d7f47a420236C4",
    "0x5d05Ce6ae9FDC9dC3fBba240a98320Bc604f80a7",
    "0x55B0FC13045B0bf6CD74631246b92f7abCFcCca2",
    "0x12EE4bc798Fd985195b0d293c2c61fBf3DcDfe04",
  ]

async def polkaex_vaults(session):
    return [
    "0x9F519083A069Cee2585cB4931C77C6EA21c3517E",
    "0x34f0DB653A0CF8487D942223e5C347f3a2526039",
    "0x228a56F238F5441B1469B3bc6F64ddd362a3a0AF",
    "0x367545a43B89A81d1a3816F13505cC7bB840c1f6"
  ]

async def blindex_vaults(session):
    return [
    "0xDaA561E04D0e73808B1A430FB360d3e497DE52c2",
    "0x6a804de5D61fD6CFf8061214aBbc8Ce75463cf5b",
    "0x4d97F81C75a28763e858a109AC19933027aF3684",
    "0xeFaCb88E4f5bF53F13F74D267E853099CE89ac4C",
    '0x67E795c3ebCd0d26225cD1582af90B590f5Ade54',
    '0x314cb69F6463e1289F0dB95A525B1a6D1eE4e428',
    '0x051c9D1E376a7e4230562656D19DF6AD12900E5f',
    '0xC237ccD60b386617CAF5EF4ca415CD789461Dec0',
    '0x4b9A981B32904C3B5e0A468528035B7DE4461cdf',
    '0x750159AC3854ebb58bcE36c3Acbb4148eF7bE14A'
  ]

async def dummy_vault(session):
    return ['0xDummy']

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
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

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_fantom_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/fantom_pools.js')
    s2 = "export const fantomPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]
    vault_data.append({'vault' : '0x49c68eDb7aeBd968F197121453e41b8704AcdE0C', 'want' : '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'})

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_moon_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/moonriver_pools.js')
    s2 = "export const moonriverPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_metis_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/metis_pools.js')
    s2 = "export const metisPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_arb_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/arbitrum_pools.js')
    s2 = "export const arbitrumPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_fuse_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/fuse_pools.js')
    s2 = "export const fusePools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_harmony_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/harmony_pools.js')
    s2 = "export const harmonyPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_cronos_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/cronos_pools.js')
    s2 = "export const cronosPools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_avax_pools(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/vault/avalanche_pools.js')
    s2 = "export const avalanchePools = "
    
    data = r[r.index(s2) + len(s2) :len(r)-2]
    cleaned_up = json.loads(json.dumps(hjson.loads(data.replace("\\",""))))

    vault_data = [{'vault' : x['earnedTokenAddress'], 'want' : x['tokenAddress']} for x in cleaned_up if 'tokenAddress' in x]

    return vault_data

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_qs_vaults(session):
        scraper = cloudscraper.create_scraper(delay=2)
        r = scraper.get('https://quickswap.exchange/staking.json')
        cleaner = r.text[1:-1].replace("\\","")
        cleaned = json.loads(cleaner)
        return [each['stakingRewardAddress'] for each in cleaned if each['ended'] == False and each['stakingRewardAddress'] != '0x0000000000000000000000000000000000000000']

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)    
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

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_dfyn_dual(session):
    url = 'https://raw.githubusercontent.com/dfyn/dfyn-farms-info/main/dual-stake.js'
    maping = await make_get_hson(session, url)
    return_list = []

    for each in maping:
        return_list.append(each['stakingRewardAddress'])
    
    return return_list

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_hyperjump_vaults(session):
    r = await make_get(session,'https://hyperjump.fi/configs/vaults/bsc_pools.js')
    s2 = "export const bscPools = "
    data = r[r.index(s2) + len(s2) :len(r)-2]
    f = hjson.loads(data)
    return [x['earnedTokenAddress'] for x in json.loads(json.dumps(f))]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_hyperjump_vaults_ftm(session):
    r = await make_get(session,'https://hyperjump.fi/configs/vaults/ftm_pools.js')
    s2 = "export const ftmPools = "
    data = r[r.index(s2) + len(s2) :len(r)-2]
    f = hjson.loads(data)
    return [x['earnedTokenAddress'] for x in json.loads(json.dumps(f))]

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_autoshark_vaults(network, session):
    r = await make_get(session,'https://autoshark.finance/.netlify/functions/vaults')
    r = json.loads(r)['data']
    return [x['address'] for x in r if x['address'] != '0x85ff09374D1f59288b6978EB9254377a51BE0B7c' and x['network'] == network and x['active'] == True]

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_solidex_vaults(network, session):
    r = await make_get(session,f'https://api.solidexfinance.com/api/getLPDetails?v={network}')
    r = json.loads(r)['data']['poolDetailsAll']
    return [x['poolAddress'] for x in r if x['isPoolWhitelisted']]  

async def get_aperocket_vaults(session):
    r = poolext.aperocket.ape_rockets
    return [x['address'] for x in r if x['address'] != '0xd79dc49Ed716832658ec28FE93dd733e0DFB8d58']

async def get_aperocket_vaults_matic(session):
    r = poolext.aperocket.ape_rockets_matic
    return [x['address'] for x in r if x['address'] != '0xBa56A30ec2Ee2B4C3c7EE75e0CFEbcD1b22dE8cd']

async def get_thunder_pools(session):
    r = poolext.thoreum.thunder_pools
    return r

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_acryptos_vaults(session):
    r = await make_get_json(session, 'https://api.unrekt.info/api/v1/acryptos-asset')
    if r:
        return [r['assets'][x]['addressvault'] for x in r['assets'] if r['assets'][x]['addressvault'] not in ['0xa82f327bbbf0667356d2935c6532d164b06ceced',''] and r['assets'][x]['addressvault'] != 'none']
    else:
        return []

@cache_function(ttl=CONTRACTS_TTL, keyparams=0, kwargsForKey=['network'])
async def get_voltage_vaults(session, network):
    r = await make_get(session, 'https://raw.githubusercontent.com/fuseio/fuse-lp-rewards/master/config/default.json')
    r = json.loads(r)
    return [r['contracts'][network][x]['contractAddress'] for x in r['contracts'][network]]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def pull_koge_vaults(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/kogecoin/vault-contracts/main/vaultaddresses')
    return ast.literal_eval(r)

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def pull_koge_vaults_ftm(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/kogecoin/vault-contracts/main/ftm_vault_addresses.json')
    r = ast.literal_eval(r)
    return [x['vault'] for x in r]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def pull_koge_vaults_moon(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/kogecoin/vault-contracts/main/movr_vault_addresses.json')
    r = ast.literal_eval(r)
    return [x['vault'] for x in r]

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_pancakebunny_pools(network, session):
    urls = {'bsc' : 'https://us-central1-pancakebunny-finance.cloudfunctions.net/api-bunnyData', 'matic' : 'https://us-central1-bunny-polygon.cloudfunctions.net/api-bunnyData'}
    r = await make_get_json(session, urls[network])
    return [x for x in r['apy'] if x not in ['0xfb8358f34133c275B0393E3883BDd8764Cb610DE','0xe0fB5Cd342BCA2229F413DA7a2684506b0397fF3','0xb04D1A8266Ff97Ee9f48d48Ad2F2868b77F1C668','0xD75f3E4e8ed51ec98ED57386Cb47DF457308Ad08','0x8626Af388F0B69BB15C36422cE67f9638BA2B800','0x12B7b4BEc740A7F438367ff3117253507eF605A7','0x4aA9B812BB65eB31f22068eE6a7C92442Af37eA9', '0x48e198477A4cB41A66B7F4F4aCA2561eBB216d33', '0x4eB4eC9625896fc6d6bB710e6Df61C20f4BAa6d7', '0xE0a20F904f88715431b926c42258480f28886920', '0x4fd0143a3DA1E4BA762D42fF53BE5Fab633e014D', '0x4beB900C3a642c054CA57EfCA7090464082e904F', '0xf301A9A9A75996631d55708764aF0294c1A39b02']]

async def get_mm_pools(session):
    return [
"0x692db42F84bb6cE6A6eA62495c804C71aA6887A7",
"0x443ec402BeC44dA7138a54413b6e09037Cf9CF41",
"0xB130a35acD62eb4604c6Ba6479D660D97a0A5aBE",
"0x7D35398F35F1dAD6e7a48d6f6E470CB11C77fc46",
"0xD2B3BDd43Bf5f6f28bD8b12d432afA46a3B20234",
"0xFf89646FE7Ee62EA96050379A7A8c532dD431d10",
"0x7A42441f5Cf40cF0fBdA98F494fA2cc500177e86",
"0x08d7EBb6fd9dC10EA21a6AA788693aB763616951",
"0xe2ca90FC315356DecF71133Ba5938153596433f3",
"0x00Db5925892274F276846F25C7fE81DEc3F3B769",
"0x55B5540B5C48a27FD17ebe2B9E6a06911f8aa45A",
"0x34375b4c4094eCaAb494E22DFFe1f88f1D5143af",
"0xe4bc967855Eb076fA971a40c0Aa4B16Ba206aec2",
"0xc385C326133078Be00cd32D3587c21934E29c2aB",
"0x1B27765F0606904eD8ebB5a915df22981ea4A261",
"0xcA37dcfC10D0366DBA41B19e9EBe7354bbF1aEC2",
]



@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_balancer_pools(session):
    balancer_pools = await call_graph('https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-polygon-v2', {'query': bitquery.balancer_pools.query, 'variable' : None}, session)
    if 'errors' not in balancer_pools:
        return [x['address'] for x in balancer_pools['data']['pools']]
    else:
        return []

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_apeswap_pools_old(session):
    r = await make_get_json(session, 'https://api.apeswap.finance/stats')
    return [x['address'] for x in r['incentivizedPools'] if x['active'] is True and x['id'] < 52]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_apeswap_pools_new(session):
    r = await make_get_json(session,'https://api.apeswap.finance/stats')
    return [x['address'] or x['id'] == 76 for x in r['incentivizedPools'] if x['active'] is True and x['id'] > 52 and x['id'] != 76]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_boosts_poly(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/polygon_stake.js')
    s2 = "export const polygonStakePools = ["
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    hson = hjson.loads(f'[{regex}]'.replace('partners: ,','').replace('assets: ,',''))
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t if x['status'] == 'active']

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_boosts_cronos(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/cronos_stake.js')
    s2 = "export const cronosStakePools = ["
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    hson = hjson.loads(f'[{regex}]'.replace('partners: ,','').replace('assets: ,',''))
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t if x['status'] == 'active']

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_beefy_boosts_moon(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/beefyfinance/beefy-app/master/src/features/configure/stake/moonriver_stake.js')
    s2 = "export const moonriverStakePools = ["
    data = r[r.index(s2) + len(s2) :len(r)-3].strip()
    regex = re.sub(r'\[.*?\]', '', data,flags=re.DOTALL)
    hson = hjson.loads(f'[{regex}]'.replace('partners: ,','').replace('assets: ,',''))
    t = json.loads(json.dumps(hson))

    return [x['earnContractAddress'] for x in t if x['status'] == 'active']

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['offset'])
async def get_pcs_pools(offset, session):
    r = await make_get(session, 'https://raw.githubusercontent.com/pancakeswap/pancake-frontend/develop/src/config/constants/pools.tsx')
    s2 = "const pools: SerializedPoolConfig[] = "
    s_end = ".filter((p) => !!p.contractAddress[CHAIN_ID])"
    data = r[r.index(s2) + len(s2) :r.index(s_end)]
    hson = hjson.loads(data)
    t = json.loads(json.dumps(hson))
    pcs_pools = []
    pcs_older = []
    for each in t:
        contract_address = each['contractAddress']['56']
        if contract_address not in ['0x73feaa1eE314F8c655E354234017bE2193C9E24E', '0xa5f8C5Dbd5F286960b9d90548680aE5ebFf07652']:
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
    return ['0xa80240Eb5d7E05d3F250cF000eEc0891d00b51CC', '0x45c54210128a065de780C4B0Df3d16664f7f859e']

async def get_baby_auto(session):
    return ['0x3e1eaD5cBe817689F4bDB96bceeb112FdBE94dBc']

async def get_thorus_mb(session):
    return ['0x4c4BF319237D98a30A929A96112EfFa8DA3510EB']

async def get_thorus_auto(session):
    return ['0x63468133ed352E602bEB61DD254D6060Ad2fe419']

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_pickle_addresses(network,session):
    r = await make_get_json(session, 'https://api.pickle.finance/prod/protocol/pools')

    if r and 'message' not in r:
        return [x['jarAddress'] for x in r if x['network'] == network and 'univ3' not in x['identifier']]
    else:
        return []

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_pickle_addresses_uni(network,session):
    r = await make_get_json(session, 'https://api.pickle.finance/prod/protocol/pools')
    
    if r and 'message' not in r:
        return [x['jarAddress'] for x in r if x['network'] == network and 'univ3' in x['identifier']]
    else:
        return []

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_wault_pool_contracts(session):
    round_time = round(time.time())
    url = f'https://api.wault.finance/wpoolsData.js?ts={round_time}'
    r = await make_get(session, url)
    s2 = "var wpoolsData = "
    data = r[r.index(s2) + len(s2) :len(r)]
    r = json.loads(data)
    r = [x['contractAddress'] for x in r]
    return r

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_paprprintr_vaults(network, session):
    r = await make_get_json(session, 'https://paprprintr-api.herokuapp.com/api/vaults')
    if r:
        r = [r[x]['config']['vault'] for x in r if r[x]['network'] == network and r[x]['config']['vault'] is not None]
        return r
    else:
        return []

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_superfarm_pools(session):
    r = await make_get_json(session, 'https://superlauncher.io/farms/farms.json')
    return [x['farmAddresses'] for x in r if '56' not in x['farmAddresses']]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_snowball_guage(session):
    balancer_pools = await call_graph('https://api.snowapi.net/graphql', {'query': bitquery.snowball.query, 'variable' : None}, session)

    return [x['gaugeAddress'] for x in balancer_pools['data']['SnowglobeContracts']]

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_aave_matic(session):
    markets = await call_graph('https://cache-api-polygon.aave.com/graphql', {'operationName' : 'Main', 'query' : bitquery.aave_markets.aave_markets, 'variables' : {'lendingPool': '0xd05e3e715d945b59290df0ae8ef85c1bdb684744'}}, session)
    return markets['data']['protocolData']['reserves']

async def get_aave_harmony(session):
    markets = await call_graph('https://cache-api-1.aave.com/graphql', {'operationName' : 'Main', 'query' : bitquery.aave_markets.aave_markets, 'variables' : {'lendingPool': '0xb53c1a33016b2dc2ff3653530bff1848a515c8c5'}}, session)
    return markets['data']['protocolData']['reserves']

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_snowball_globe(session):
    balancer_pools = await call_graph('https://api.snowapi.net/graphql', {'query': bitquery.snowball.query, 'variable' : None}, session)

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

async def get_dk_crystal(session):
    return ['0x04b9dA42306B023f3572e106B11D82aAd9D32EBb']

async def get_snowball_staking(session):
    return ['0xc38f41a296a4493ff429f1238e030924a1542e50']

async def get_wanna_staking(session):
    return ['0x7faA64Faf54750a2E3eE621166635fEAF406Ab22']

async def get_tri_staking(session):
    return ['0xFa94348467f64D5A457F75F8bc40495D33c65aBB']

async def get_nearpad_staking(session):
    return ['0x885f8CF6E45bdd3fdcDc644efdcd0AC93880c781']

async def get_tethys_staking(session):
    return ['0x69fdb77064ec5c84fa2f21072973eb28441f43f3']

async def get_haku_staking(session):
    return ['0x695fa794d59106cebd40ab5f5ca19f458c723829']

async def get_ironlend_vaults(session):
    return poolext.ironlend.vaults

async def get_ironlend_rewards(session):
    return poolext.ironlend.rewards

async def get_benqi_vaults(session):
    return poolext.benqi.vaults

async def get_ola_vaults(session):
    return poolext.ola.vaults

async def get_apeswap_lending(session):
    return poolext.apeswap.vaults

async def get_tranquil_vaults(session):
    return poolext.tranquil.vaults

async def get_annex_vaults(session):
    return poolext.annexbsc.vaults

async def get_venus_vaults(session):
    return [
    {'address' : '0xecA88125a5ADbe82614ffC12D0DB554E2e2867C8', 'decimal' : 18, 'want' : '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d', 'collat_rate' : .8},
    {'address' : '0xfD5840Cd36d94D7229439859C0112a4185BC0255', 'decimal' : 18, 'want' : '0x55d398326f99059ff775485246999027b3197955', 'collat_rate' : .8},
    {'address' : '0x95c78222B3D6e262426483D42CfA53685A67Ab9D', 'decimal' : 18, 'want' : '0xe9e7cea3dedca5984780bafc599bd69add087d56', 'collat_rate' : .8},
    {'address' : '0x2fF3d0F6990a40261c66E1ff2017aCBc282EB6d0', 'decimal' : 18, 'want' : '0x47bead2563dcbf3bf2c9407fea4dc236faba485a', 'collat_rate' : .5},
    {'address' : '0x151B1e2635A717bcDc836ECd6FbB62B674FE3E1D', 'decimal' : 18, 'want' : '0xcf6bb5389c92bdda8a3747ddb454cb7a64626c63', 'collat_rate' : .6},
    {'address' : '0xA07c5b74C9B40447a954e1466938b865b6BBea36', 'decimal' : 18, 'want' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', 'collat_rate' : .8},
    {'address' : '0x882C173bC7Ff3b7786CA16dfeD3DFFfb9Ee7847B', 'decimal' : 18, 'want' : '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', 'collat_rate' : .8},
    {'address' : '0xf508fCD89b8bd15579dc79A6827cB4686A3592c8', 'decimal' : 18, 'want' : '0x2170ed0880ac9a755fd29b2688956bd959f933f8', 'collat_rate' : .8},
    {'address' : '0x57A5297F2cB2c0AaC9D554660acd6D385Ab50c6B', 'decimal' : 18, 'want' : '0x4338665cbb7b2485a8855a139b75d5e34ab0db94', 'collat_rate' : .6},
    {'address' : '0xB248a295732e0225acd3337607cc01068e3b9c10', 'decimal' : 18, 'want' : '0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe', 'collat_rate' : .6},
    {'address' : '0x5F0388EBc2B94FA8E123F404b79cCF5f40b29176', 'decimal' : 18, 'want' : '0x8ff795a6f4d97e7887c79bea79aba5cc76444adf', 'collat_rate' : .6},
    {'address' : '0x1610bc33319e9398de5f57B33a5b184c806aD217', 'decimal' : 18, 'want' : '0x7083609fce4d1d8dc0c979aab8c869ea2c873402', 'collat_rate' : .6},
    {'address' : '0x650b940a1033B8A1b1873f78730FcFC73ec11f1f', 'decimal' : 18, 'want' : '0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd', 'collat_rate' : .6},
    {'address' : '0x334b3eCB4DCa3593BCCC3c7EBD1A1C1d1780FBF1', 'decimal' : 18, 'want' : '0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3', 'collat_rate' : .6},
    {'address' : '0xf91d58b5aE142DAcC749f58A49FCBac340Cb0343', 'decimal' : 18, 'want' : '0x0d8ce2a99bb6e3b7db580ed848240e4a0f9ae153', 'collat_rate' : .6},
    {'address' : '0x972207A639CC1B374B893cc33Fa251b55CEB7c07', 'decimal' : 18, 'want' : '0x250632378e573c6be1ac2f97fcdf00515d0aa91b', 'collat_rate' : .6},
    {'address' : '0xeBD0070237a0713E8D94fEf1B728d3d993d290ef', 'decimal' : 18, 'want' : '0x20bff4bbeda07536ff00e073bd8359e5d80d733d', 'collat_rate' : .0},
    {'address' : '0x9A0AF7FDb2065Ce470D72664DE73cAE409dA28Ec', 'decimal' : 18, 'want' : '0x3ee2200efb3400fabb9aacf31297cbdd1d435d47', 'collat_rate' : .6},
    {'address' : '0xec3422Ef92B2fb59e84c8B02Ba73F1fE84Ed8D71', 'decimal' : 8, 'want' : '0xba2ae424d960c26247dd6c32edc70b295c744c43', 'collat_rate' : .4},
    {'address' : '0x5c9476FcD6a4F9a3654139721c949c2233bBbBc8', 'decimal' : 18, 'want' : '0xcc42724c6683b7e57334c4e856f4c9965ed682bd', 'collat_rate' : .6},
    {'address' : '0x86aC3974e2BD0d60825230fa6F355fF11409df5c', 'decimal' : 18, 'want' : '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82', 'collat_rate' : .55},
    {'address' : '0x26DA28954763B92139ED49283625ceCAf52C6f94', 'decimal' : 18, 'want' : '0xfb6115445bff7b52feb98650c87f44907e58f802', 'collat_rate' : .55},
    {'address' : '0x08CEB3F4a7ed3500cA0982bcd0FC7816688084c3', 'decimal' : 18, 'want' : '0x14016e85a25aeb13065688cafb43044c2ef86784', 'collat_rate' : .8},
    {'address' : '0x61eDcFe8Dd6bA3c891CB9bEc2dc7657B3B422E93', 'decimal' : 18, 'want' : '0x85eac5ac2f758618dfa09bdbe0cf174e7d574d5b', 'collat_rate' : .6},]

async def get_market_vaults(session):
    return [{'address': '0xe1d87ae311c06ee6684b5294d0290cf79e660dd2', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.8},
{'address': '0x051b82448a521bc32ac7007a7a76f9dec80f6ba2', 'decimal': 18, 'want': '0x6c021ae822bea943b2e66552bde1d2696a53fbb7', 'collat_rate': 0.65},
{'address': '0xd60fbafc954bfbd594c7723c980003c196bdf02f', 'decimal': 18, 'want': '0x4cdf39285d7ca8eb3f090fda0c069ba5f4145b37', 'collat_rate': 0.6},
{'address': '0xf18f4847a5db889b966788dcbdbcbfa72f22e5a6', 'decimal': 18, 'want': '0xa48d959ae2e88f1daa7d5f611e01908106de7598', 'collat_rate': 0.6},
{'address': '0xb595c02147bcede84e0e85d9e95727cf38c02b07', 'decimal': 18, 'want': '0xee3a7c885fd3cc5358ff583f2dab3b8bc473316f', 'collat_rate': 0.65},
{'address': '0x588125bfa39a137c7ae05a744e589673b4bbd4a5', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.7},
{'address': '0x522af22237c40e000925f4baf714482cd417a8dd', 'decimal': 18, 'want': '0x15dd4398721733d8273fd4ed9ac5eadc6c018866', 'collat_rate': 0.5},
{'address': '0x3f4f523acf811e713e7c34852b24e927d773a9e5', 'decimal': 18, 'want': '0x27c77411074ba90ca35e6f92a79dad577c05a746', 'collat_rate': 0.55},
{'address': '0x872c847056e11cf75d1d9636b522d077e8c9f653', 'decimal': 18, 'want': '0xae94e96bf81b3a43027918b138b71a771d381150', 'collat_rate': 0.5},
{'address': '0x3e92100dc678ad1f249c06f75c8393f50294ed71', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.8},
{'address': '0x413f1815d32e5aca0d8984fa89e50e83ddac0bbe', 'decimal': 18, 'want': '0x5d2ef803d6e255ef4d1c66762cbc8845051b54db', 'collat_rate': 0.65},
{'address': '0x10a814e68ccac71611e98243fb94697df15e099a', 'decimal': 18, 'want': '0x11d4d27364952b972ac74fb6676dbbfa67fda72f', 'collat_rate': 0.6},
{'address': '0xd3af91f21f791f29fc664cd5cd61180edc263191', 'decimal': 18, 'want': '0xd8dd2ea228968f7f043474db610a20af887866c7', 'collat_rate': 0.65},
{'address': '0x03c20569c2c78cd48f491415a4cdeac02608db7e', 'decimal': 18, 'want': '0xa4e2ee5a7ff51224c27c98098d8db5c770baadbe', 'collat_rate': 0.65},
{'address': '0xcb99178c671761482097f32595cb79fb28a49fd8', 'decimal': 18, 'want': '0x5cc61a78f164885776aa610fb0fe1257df78e59b', 'collat_rate': 0.5},
{'address': '0xe95c747a5c053b13e9056f45abaa0f1cb64d1711', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.7},
{'address': '0xedf25e618e4946b05df1e33845993ffebb427a0f', 'decimal': 18, 'want': '0x7345a537a975d9ca588ee631befddfef34fd5e8f', 'collat_rate': 0.4},
{'address': '0x0168656379cd66aab3f42a4fb17ed3624da54720', 'decimal': 18, 'want': '0x794cead3c864b5390254ffca7ecd6a9ae868661a', 'collat_rate': 0.45},
{'address': '0x2a081abff657fa727e2f1740974f83253c228279', 'decimal': 18, 'want': '0x30a9eb3ec69ed8e68c147b47b9c2e826380024a3', 'collat_rate': 0.6},
{'address': '0xb670fb8203baae8eb81235d388de56f832e0e866', 'decimal': 18, 'want': '0xad48320c7e3d3e9ff0c7e51608869cbbffe7422c', 'collat_rate': 0.55},
{'address': '0x5a25dc3b15259dc1e15cfa2ec398dd6129c6aef1', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.7},
{'address': '0xa99777140769f72dc33c9a3bfe68e21cfc6cef0c', 'decimal': 6, 'want': '0x1b6ecda7fd559793c0def1f1d90a2df4887b9718', 'collat_rate': 0.65},
{'address': '0xd85d7760edd67b64fcd3ca2d1be064bbcc0217b3', 'decimal': 18, 'want': '0x92d2ddf8eed6f2bdb9a7890a00b07a48c9c7a658', 'collat_rate': 0.6},
{'address': '0xa887302a5eb00de03edde8af29a82d86fcc5e0b5', 'decimal': 18, 'want': '0x38da23ef41333be0d309cd63166035ff3b7e2000', 'collat_rate': 0.6},
{'address': '0xc1f080c5001127f3a6cc3d365103422fc526b996', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.7},
{'address': '0x73d39850b5ac33b52113dc2add2f6643be43e36e', 'decimal': 18, 'want': '0xdc301622e621166bd8e82f2ca0a26c13ad0be355', 'collat_rate': 0.7},
{'address': '0xe11fe2584ec0a315da6dd4d2f73548e528cd48eb', 'decimal': 6, 'want': '0x04068da6c83afcfa0e13ba15a6696662335d5b75', 'collat_rate': 0.7},
{'address': '0xead7c77fb39f067f9be238b8473928fa8bbabf97', 'decimal': 18, 'want': '0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83', 'collat_rate': 0.6},
{'address': '0x0afdea6b939067e3e5ff704e2dc93a834ecc2ad9', 'decimal': 6, 'want': '0x049d68029688eabf473097a2fc38ef61633a3c7a', 'collat_rate': 0.65},
{'address': '0x8957c84f5db0e5730ffc6e85a79a2ea7d7eee04d', 'decimal': 18, 'want': '0x82f0b8b456c1a451378467398982d4834b6829c1', 'collat_rate': 0.65},
{'address': '0x52a4691e510d03d3c21f33fad7faba39857444df', 'decimal': 18, 'want': '0x74b23882a30290451a17c44f4f05243b6b58c76d', 'collat_rate': 0.6},
{'address': '0x788e826484650d69c2a5cbbc627dc244989bd910', 'decimal': 18, 'want': '0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e', 'collat_rate': 0.7},
{'address': '0xed8ff01143213a44a31c33c7dff62ba76098682e', 'decimal': 18, 'want': '0xdc301622e621166bd8e82f2ca0a26c13ad0be355', 'collat_rate': 0.65},
{'address': '0xa8ebdb42f968756b24af884ff95962a605785020', 'decimal': 18, 'want': '0x8316b990de26eb530b7b1bb0d87f5b0a304637cd', 'collat_rate': 0.6},
{'address': '0x4b56c89e3bbd915822b3e034eab43d4a287af78a', 'decimal': 18, 'want': '0xa3e3af161943cfb3941b631676134bb048739727', 'collat_rate': 0.5},
{'address': '0xe564b2564616433688a14169aa91474677add7eb', 'decimal': 18, 'want': '0x2a30c5e0d577108f694d2a96179cd73611ee069b', 'collat_rate': 0.5},
{'address': '0x6af13383a08e8ac56913f9c84bdde9303837c0ef', 'decimal': 18, 'want': '0x5d89017d2465115007aba00da1e6446df2c19f34', 'collat_rate': 0.6},
{'address': '0x1290578d565e98ba99d47dd767407bef194854d0', 'decimal': 18, 'want': '0x41d44b276904561ac51855159516fd4cb2c90968', 'collat_rate': 0.6},
{'address': '0x414148187910f7dc6d0766e84669d7ee89833f2a', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.7},
{'address': '0x4a913f10bfdfd12e0be3225b7485bcc260442da4', 'decimal': 18, 'want': '0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e', 'collat_rate': 0.7},
{'address': '0x021a22df029f1b4c336b3f5691320b57b4c0664c', 'decimal': 18, 'want': '0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83', 'collat_rate': 0.5},
{'address': '0x2511cf5807551dda6add97a2cbfcdab6cd042c49', 'decimal': 18, 'want': '0xfb98b335551a418cd0737375a2ea0ded62ea213b', 'collat_rate': 0.75},
{'address': '0x1a44bedfa5735ee94a4ebfb41edc6ba87172dc31', 'decimal': 18, 'want': '0x10b620b2dbac4faa7d7ffd71da486f5d44cd86f9', 'collat_rate': 0.6},
{'address': '0x8aa0d26a9915229d03e3c43b25a48e86b0d88464', 'decimal': 18, 'want': '0xc5713b6a0f26bf0fdc1c52b90cd184d950be515c', 'collat_rate': 0.46},
{'address': '0x7426ac4d2ffeedcdab8708320fa7a78b1de8efc0', 'decimal': 18, 'want': '0x3f569724cce63f7f24c5f921d5ddcfe125add96b', 'collat_rate': 0.4},
{'address': '0x8c722f18cd119f9f7b709a78fdf74908159ce38c', 'decimal': 18, 'want': '0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83', 'collat_rate': 0.65}]

async def get_zombie_pools(session):
    return poolext.rugzombie.pools

async def get_tengu_stakes(session):
    return ['0xd38cE88CAf05FFDb193Ba95fce552c5129E42C89']

async def get_netswap_stakes(session):
    return ['0x4d2F0f5409B51172dc229b3c8dCaa1365a9C9C27']

async def get_macaron_syrup(session):
    return ['0xCded81aa5Ab3A433CadF77Fd5aC8B6fD973906e1', '0xF69bdcDB577F98753d4890Cc5aCfF3BE00177584', '0x7DB34B681c759918079C67EeF08868225F34fbcB', '0x13ED683DDf483d1f0bd2AE02b01D4d1D451D6c5b', '0x0f819C8E6A7c0F0906CBc84b9b1e6642f9634E61', '0x903A20CDbAC174250eAcc7437720929f0dE97B99', '0x82cF07a989835b68260989F13Bc853f8fe48ad04', '0xc8De98F603af53a5D52AF6AA153d9e15b0002B2c', '0xf3D514263239672455306D188DD5f045E61deD03', '0xC85C50988AEC8d260853443B345CAE63B7432b7A', '0xF60EDbF7D95E79878f4d448F0CA5622479eB8790']

async def get_olimpus_syrup(session):
    return [
        '0x8bec5eD28a6F409c4B2a4D3f8C59F03f5326b46E',
        '0xd67524014DB1Ef6E27139f79Eb68FF31BE9Eace4'
        ]

async def get_svn_oasis(session):
    return [
        '0x2CcbFD9598116cdF9B94fF734ece9dCaF4c9d471',
        ]

async def get_macaron_auto(session):
    return ['0x0608A42BA74F2026A88aC2304f6802838F36bEB5', '0xCd59d44E94Dec10Bb666f50f98cD0B1593dC3a3A', '0x6dAc44A858Cb51e0d4d663A6589D2535A746607A', '0xd474366F6c80230507481495F3C1490e62E3093F']

async def get_olimpus_auto(session):
    return ['0xAF629b4bf5d8916Fe0b925ae30e8569c1d4E73FA']

async def get_morpheus_syrup(session):
    return ['0x2854980e1f6526CB5AeC8d53c5028AF486368ea1', '0x415742c217eA4941B706ff358bF6178985590cFA', '0x8b0c89A08045A38A710fd141443d463B960C9aAe', '0x9055064B490604E41593d9271a53603CF48204F4', '0x4bDA0C69f7F15a43Ef35881c2aB3B7f995630A14', '0x5db1AD1E0ECC9EfBF69d3566C54eE650Cd712Fa5', '0x791A8d97FeeF371D1AEc6f25B7C3E4545c847476']

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_jetswap_vaults(network, session):
    if network == 'polygon':
        r = await make_get_json(session, 'https://polygon.jetswap.finance/api/vaults.json')
        r = [x['vaultAddresses']['137'] for x in r]
        return r
    elif network == 'bsc':
        r = await make_get_json(session, 'https://jetswap.finance/api/vaults.json')
        r = [x['vaultAddresses']['56'] for x in r]
        return r

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_elk_vaults(network, session):
        ROUNDS = 10
        STAKING = {"fuse":{"ELK":"0xA83FF3b61c7b5812d6f0B39d5C7dDD920B2bDa61"},"ftm":{"ELK":"0x6B7E64854e4591f8F8E552b56F612E1Ab11486C3"},"xdai":{"ELK":"0xAd3379b0EcC186ddb842A7895350c4657f151e6e"},"avax":{"ELK":"0xB105D4D17a09397960f2678526A4063A64FAd9bd"},"bsc":{"ELK":"0xD5B9b0DB5f766B1c934B5d890A2A5a4516A97Bc5"},"matic":{"ELK":"0xB8CBce256a713228F690AC36B6A0953EEd58b957"},"heco":{"ELK":"0xdE16c49fA4a4B78071ae0eF04B2E496dF584B2CE"}}
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

@cache_function(ttl=CONTRACTS_TTL, keyparams=[0], kwargsForKey=['network'])
async def get_wault_locked(network, session):
    if network == 'bsc':
        return poolext.wault_locked.bsc
    elif network == 'polygon':
        return poolext.wault_locked.polygon

async def gambit_vaults(session):
    return poolext.gambit.gambits

async def gmx_vaults(session):
    return poolext.gmx.vaults

async def gmx_avax_vaults(session):
    return poolext.gmx.vaults_avax

async def thor_nodes(session):
    return {'nodes' : [
        '0xbA4400C4619Cd15267c2FeCd4Dbc39d310CEe3f1',
        '0x37DA69aa9b436D3Bf6cC7530E11Ef98A5a052441',
        '0x79190a9c108F6cc1CE956eA8f7ba03cD4e3260b9',
        '0x9C0200F3e9673BCfe6D80076aa976F446d74758A'],
        'reward_token' : '0x8F47416CaE600bccF9530E9F3aeaA06bdD1Caa79',
        'reward_symbol' : 'THOR'
        }

async def power_nodes(session):
    return {'nodes' : [
        '0x0033FA9888028dD4BC5905241cbf312a8d0b21B3',
        '0xFb717Be387F0FAB42A55772ef5CC55B4c324DabD',
        '0x928a833b65d967fb0b785ecdce6ccf1a867f3c28',
        '0xC8007751603bB3E45834A59af64190Bb618b4a83'],
        'reward_token' : '0x131c7afb4E5f5c94A27611f7210dfEc2215E85Ae',
        'reward_symbol' : 'POWER'
        }

#HEIMDALL : 0xbA4400C4619Cd15267c2FeCd4Dbc39d310CEe3f1
#THOR : 0x37DA69aa9b436D3Bf6cC7530E11Ef98A5a052441
#FREYA : 0x79190a9c108F6cc1CE956eA8f7ba03cD4e3260b9
#ODIN: 0x9C0200F3e9673BCfe6D80076aa976F446d74758A


async def squirrel_vaults(session):
    return poolext.squirrel.nuts

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_adamant_vaults(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/eepdev/vaults/main/current_vaults.json')
    return [each for each in json.loads(r) if each['vaultAddress'] != '0xe938A5D0fEbDbfEbf2bD11B8d012C9e055D4AB92']

@cache_function(ttl=CONTRACTS_TTL, keyparams=0)
async def get_adamant_vaults_arb(session):
    r = await make_get(session, 'https://raw.githubusercontent.com/eepdev/vaults/main/arbitrum_vaults.json')
    return json.loads(r)

async def get_adamant_boosts(session):
    return ['0xC5bCD23f21B6288417eB6C760F8AC0fBb4bb8a56']

async def get_adamant_boosts_arb(session):
    return ['0x097b15dC3Bcfa7D08ea246C09B6A9a778e5b007B']

async def get_manorfarm_pools(session):
    return [
        '0xa9a079f4a5b7fdc127df64f3a84f3fab3a0eb46e',
        ]

async def get_spintop_pools(session):
    return [
        '0x6D28F46E0698a2F217c72fF4e86DBFBAc422B1C4',
        '0xB15655401E3018B7BF3F8c12BdD24A0936636Bc0',
        '0x6bf651c0989dFd34a4E0Cc8A5Ed41ebB344f8ca6',
        '0x7d84EC280352523bFe8A706597bf461e53796e89',
        '0xb6361352eE2CDcFC3fc4098be10EA8EC9b8d2D7F',
        '0x0a3a5e2a2ADA7b153961f710077235f631F44119',
        '0x5386E748b19Aaf510acc93DCbf1d6900E94563fC',
        '0xf6F2e973D05A2FFeB2984293e6dfCbA55a6579CE',

        '0x06F2bA50843e2D26D8FD3184eAADad404B0F1A67',
        '0x97523C0e91ede98a67E092D9600B37DC3188a8B2',
        '0xEDCBBdb897E7A375CBA6B543698EfF8758505f1c',
        '0x21D83d19Ed8927BFF5dB09Ac7CaC39d2D5Aca631',
        '0x85D9803B8Ca95714C3dc125Fa59b07081ba23180',
        '0x46A89b88E83F1a626B26451954714a10411446e3',
        '0xB77d750540A09D44ECE146a2eeDCDE8d2710c51f',
        '0x084b528744117564D35c3879e7557D80f95465CD'
        ]

async def get_spintop_vaults(session):
    return [
        '0x03447d28FC19cD3f3cB449AfFE6B3725b3BCdA77',
        ]

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

async def get_jade_ohm(session):
    return {
        'BONDS' : ['0xD6C73ef5e71A350f8AE642C01Aad3d7637a0c1C8', '0xB855Ee49DE8F05A441104C4E053A3be7FF45ae56', '0x266a93EA88C002ff223E81E40300056289938142'],
        'MEMO_ADDRESS' : '0x94CEA04C51E7d3EC0a4A97Ac0C3B3c9254c2aD41',
        'TIME_ADDRESS' : '0x7ad7242A99F21aa543F9650A56D141C57e4F6081',
        'OHM_CONTRACT' : '0x097d72e1D9bbb8d0263477f9b20bEBF66f243AF4',
        'OHM_FUNCTION' : 'sOHM'
    }

async def get_metareserve_ohm(session):
    return {
        'BONDS' : ['0xec788d7fa07adb9ca488032172f3bb3437e017b6', '0xeea8075f0ada3c7a6af4bbb1497a73ed372c6e7e'],
        'MEMO_ADDRESS' : '0x0955f99963b1aec8d0fe18a35ad830f562b113bc',
        'TIME_ADDRESS' : '0x000c6322df760155bbe4f20f2edd8f4cd35733a6',
        'OHM_CONTRACT' : '0x5c643737AF2aD7A0B9ae62158b715793505967bE',
        'OHM_FUNCTION' : 'HONOR'
    }

async def get_pegasus_ohm(session):
    return {
        'BONDS' : ['0xD2f78eDAb0Ab0425577C92Bc42a23EE29A3c8f95', '0xE66b63907527DF5fd02f85be9fd3E8c01890568a'],
        'MEMO_ADDRESS' : '0x304857afdd16da07a2e61ca2f2b5103deedcf000',
        'TIME_ADDRESS' : '0x5b5fe1238aca91c65683acd7f9d9bf922e271eaa',
        'OHM_CONTRACT' : '0x423159bdCa615c718F8C23b373DBf03d1A96D3C1',
        'OHM_FUNCTION' : 'sSUS'
    }

async def get_nidhi_ohm(session):
    return {
        'BONDS' : ['0xbbA07bd5B20B63249398b831082ace6415afB7E0', '0xFDAACD04f8ad605e928F4A44864FF825dCd4796d'],
        'MEMO_ADDRESS' : '0x04568467f0AAe5fb85Bf0e031ee66FF2C200a6Fb',
        'TIME_ADDRESS' : '0x057e0bd9b797f9eeeb8307b35dbc8c12e534c41e',
        'OHM_CONTRACT' : '0x4Eef9cb4D2DA4AB2A76a4477E9d2b07f403f0675',
        'OHM_FUNCTION' : 'sGURU'
    }

async def get_hunny_ohm(session):
    return {
        'BONDS' : ['0x5b669D9cCb3208eD9c7CbDD09f88357C1cB90Efb'],
        'MEMO_ADDRESS' : '0x153629b8ce84f5e6dd6044af779aa37adb431393',
        'TIME_ADDRESS' : '0x9505dbd77dacd1f6c89f101b98522d4b871d88c5',
        'OHM_CONTRACT' : '0x31dd9Be51cC7A96359cAaE6Cb4f5583C89D81985',
        'OHM_FUNCTION' : 'HUG'
    }

async def get_viking_ohm(session):
    return {
        'BONDS' : ['0xbc5299aa63cf9ce9f30b7274845207668d4a1304', '0x46d81a637ea28134439b4922ec4a34660aec057d'],
        'MEMO_ADDRESS' : '0x91D680545a1ff4411C1ff4C927f86CD34ADB932a',
        'TIME_ADDRESS' : '0xe0474c15bc7f8213ee5bfb42f9e68b2d6be2e136',
        'OHM_CONTRACT' : '0x743DE042c7be8C415effa75b960A2A7bB5fc0704',
        'OHM_FUNCTION' : 'Memories'
    }

async def get_wagmi_ohm(session):
    return {
        'BONDS' : ['0xe443f63564216f60625520465f1324043fcc47b9', '0x8c4300a7a71eff73b24dcd8f849f82a8b36b5d8a', '0xa31a22d9dec269f512cf62b83039190fbe67f7d2', '0x08d44c114e3c0102ace43e9656f478dd4a71cd1d', '0xefb7dde5261100a32657c9606507a130257d93c6'],
        'REWARD' : '0x8750f5651af49950b5419928fecefca7c82141e3',
    }

async def get_ohm_ohm(session):
    return {
        'BONDS' : ['0xc60a6656e08b62dd2644dc703d7855301363cc38', '0x99e9b0a9dc965361c2cbc07525ea591761aeaa53'],
        'OHM_ADDRESS' : '0x64aa3364f17a4d01c6f1751fd97c2bd3d7e7f1d5',
        'SOHM_ADDRESS' : '0x04906695d6d12cf5459975d7c3c03356e4ccd460',
        'GOHM_ADDRESS' : '0x0ab87046fbb341d058f17cbc4c1133f25a20a52f',
        'OHM_CONTRACT' : '0xb63cac384247597756545b500253ff8e607a8020',
        'SOHM_FUNCTION' : 'sOHM',
        'GOHM_FUNCTION' : 'gOHM'
    }

async def get_strongblock(session):
    return {
     "" :  {
            'token' : '',
            'contract' : '',
        }
    }

async def get_strongblock_nodes(session, wallet):
    markets = await call_graph('https://gql.strongblock.com', {'query' : """query ($cursor: Int, $take: Int = 15, $address: String, $search: String, $orderBy: NodesOrderBy) {
  nodes(
    cursor: $cursor
    take: $take
    address: $address
    search: $search
    orderBy: $orderBy
  ) {
    cursor
    totalItems
    hasMoreItems
    items {
      id
      uid
      type
      address
      node_id
      node_type
      name
      description
      location
      logo
      staked_nft
      rpc_url
      ws_url
      web_url
      json_url
      dvpn_address
      created_at
      added_at
      city {
        name
        state
        country
        __typename
      }
      __typename
    }
    __typename
  }
}
""", 'variables' : {
  "take": 400,
  "address": wallet
}}, session)
    return markets