from evm.oracles import coingecko_by_address_network, fantom_router_prices, get_price_from_router,kcc_router_prices,oke_router_prices,harmony_router_prices, avax_router_prices
from evm.multicall import Call, Multicall
from evm.farms import farms
import json
import asyncio
import requests
import hjson
from aiohttp import ClientSession, ClientTimeout
from evm.poolext.elevenpools import pools as e11pools
from evm.poolext.fulcrumpools import pools as fulcrumpools
from evm.poolext.elevennerve import extNerve
from evm.poolext.horizon import extHorizon
from evm.poolext.ironfoundry import foundry
from evm.poolext.diamondhand import diamonds
from evm.poolext.apoyield import thirdParty
from evm.poolext.jetfuelVaults import fuelVaults
from evm.poolext.pancakebunny import bunnies
from evm.poolext.gambit import gambits
from evm.poolext.taodao import dao
from evm.poolext.fortress import forts
from evm.poolext.dyp import dypPools
from evm.poolext.alpacaTokens import alpacas
from evm.poolext.merlin import magic
from evm.poolext.beefy_new import beefy_v6
from evm.poolext.squirrel import nuts
from evm.poolext.adamant import adamant_deployers
from evm.poolext.kogefarm import koge_vaults
from evm.poolext.aperocket import ape_rockets, ape_rockets_matic
from evm.poolext.thoreum import thunder_pools
from evm.poolext.pyq import pyq_farm_list
from evm.poolext.pancake_bunny_matic import bunny_matic_vaults
import evm.poolext.png as png
import evm.poolext.curve
import evm.poolext.boneswap
import evm.poolext.telx as telx
import evm.poolext.paprprintr as papr
import evm.poolext.dinoswap as dino
import evm.poolext.superfarm as superfarm
import evm.poolext.pandaswap as pandaswap
import evm.poolext.feeder as feeder
import evm.poolext.polygonfarm as polygonfarm
import evm.poolext.ironlend as ironlend
import evm.poolext.farmhero as farmhero
import evm.poolext.rugzombie as rugzombie
import evm.poolext.jetswap_vaults as jetswapvaults
import evm.poolext.ext_masterchef as ext_masterchef
import evm.poolext.moonpot as moonpot
import evm.poolext.yak as yak
import evm.poolext.benqi as benqi
import evm.uniswapv3 as uniswapv3
import evm.multicall.parsers as parser
import evm.farm_templates as farm_templates
import evm.template_helpers as template_helpers
from evm.thegraph import call_graph
from web3 import Web3
from evm.abi.uranium import uraniumABI
from evm.abi.nrveth import nrvethABI
from evm.abi.wswap import wSwapABI
from evm.abi.gambit import gambitABI
from evm.abi.pcs1 import pcsRouter
from evm.abi.pcs2 import pcs2Router
from evm.abi.jets import jetsRouter
from evm.abi.biswap import biswap_router
from evm.abi.firebird import firebird_abi
from evm.abi.add_rewards import reward_abi
from evm.abi.farmhero import multi_fee_v2
from evm.abi.balancer_vault import balancer_vault_abi
import evm.bitquery.balancer_pools as balancer_pools_query
from evm.bitquery.walletquery import query, variables
import evm.bitquery.quickswap_lps as quickswap_lps
import time
#import nest_asyncio
from pymongo import MongoClient
#import grequests
import os
import evm.routers as routers
import ast
import cloudscraper
import re
from evm.networks import WEB3_NETWORKS

#nest_asyncio.apply()

## Constants
DUST_FILTER = 0.00000000001
INCH_SUPPORTED = ['bsc','matic','eth']
ellCheck = {x['tokenAddress'].lower() : x for x in e11pools}
fulcrmCheck = {x['address'].lower() : x for x in fulcrumpools}
client = MongoClient('mongodb+srv://xtracker:FkIIpyj3hdUWpuEl@cluster0.wrato.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mongo = client.xtracker
tokenDB = mongo.full_tokens

# Used For Testing
# selectedPools = ['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', '0x7f7Bf15B9c68D23339C31652C8e860492991760d', '0x2EBe8CDbCB5fB8564bC45999DAb8DA264E31f24E', '0x0895196562C7868C5Be92459FaE7f877ED450452']
# wallet = '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f'

### MultiCalls

def token_router(wanted_token, farm_address):
    farm_network = farms[farm_address]['network']
    try:
        return {**getLP(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'lp'}}
    except:
        try:
            return {**getUniswapPool(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'uniswapv3'}}
        except:
            try:
                return {**getSwap(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'swap'}}
            except:
                try:
                    return {**get_curve_token(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'curve'}}
                except:
                    try:
                        return {**get_curve_token_two(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'curve'}}
                    except:
                        try:
                            return {**getBeltToken(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'belt'}}
                        except:
                            try:
                                return {**get_picklejars(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'pickle'}}
                            except:
                                try:
                                    return {**getGrowToken(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'grow'}}
                                except:
                                    try:
                                        return {**kashi_token(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'kashi'}}
                                    except:
                                        try:
                                            return {**get_balancer_token(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'balancer'}}
                                        except:
                                            return {**getSingle(wanted_token, farm_address), **{'tokenID' : wanted_token, 'network' : farm_network, 'type' : 'single'}}

def getLP(token, farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]

    try:
        return getSwap(token, farm_id)
    except:
        try:
            return get_curve_token(token,farm_id)
        except:
            multiLP = Multicall([
                Call(token, 'symbol()(string)', [['symbol', None]]),
                Call(token, 'token0()(address)', [['token0', None]]),
                Call(token, 'token1()(address)', [['token1', None]]),
                Call(token, 'totalSupply()(uint256)', [['totalSupply', from_wei]]),
                Call(token, 'getReserves()((uint112,uint112))', [['reserves', parseReserves]])
            ], network_chain)

            lpPool = multiLP()


            lpTokens = Multicall([
                Call(lpPool['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
                Call(lpPool['token1'], 'decimals()(uint8)', [['tkn1d', None]]),
                Call(lpPool['token0'], 'symbol()(string)', [['tkn0s', None]]),
                Call(lpPool['token1'], 'symbol()(string)', [['tkn1s', None]])
            ], network_chain)

            return {**lpPool, **lpTokens(),  **{'lpToken' : token}}

def getUniswapPool(token, farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]


    multiLP = Multicall([
        Call(token, 'tickSpacing()(int24)', [['tickSpacing', None]]),
        Call(token, 'token0()(address)', [['token0', None]]),
        Call(token, 'token1()(address)', [['token1', None]]),
        # Call(token, 'slot0()((uint160,int24,uint16,uint16,uint16,uint8,bool))', [[f'slot0',parser.parse_slot_0]])
    ], network_chain)

    lpPool = multiLP()


    lpTokens = Multicall([
        Call(lpPool['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
        Call(lpPool['token1'], 'decimals()(uint8)', [['tkn1d', None]]),
        Call(lpPool['token0'], 'symbol()(string)', [['tkn0s', None]]),
        Call(lpPool['token1'], 'symbol()(string)', [['tkn1s', None]])
    ], network_chain)

    return {**lpPool, **lpTokens(),  **{'uniswapPool' : token}}

def getSingle(token, farm_id):

        network = farms[farm_id]['network']
        network_chain = WEB3_NETWORKS[network]
        
        if token in catchENRV:
            token = catchENRV[token]['tokenAddress']
        
        try:
            token = Call(token, 'loanTokenAddress()(address)', [['loan', None]], network_chain)()['loan']
        except:
            token = token
        
        single = Multicall([
                        Call(token, 'symbol()(string)', [['tkn0s', None]]),
                        Call(token, 'decimals()(uint8)', [['tkn0d', None]]),
                    ], network_chain)

        add = {'token0' : token}

        return {**add, **single()}
        
        # try:
        #     return getSwap(token, farm_id)
        # except:
        #     try:
        #         return getBeltToken(token, farm_id)
        #     except:
        #         try:
        #             return getGrowToken(token, farm_id)
        #         except:
        #             single = Multicall([
        #                 Call(token, 'symbol()(string)', [['tkn0s', None]]),
        #                 Call(token, 'decimals()(uint8)', [['tkn0d', None]]),
        #             ], network_chain)

        #             add = {'token0' : token}

        #             return {**add, **single()}

def get_curve_token(token, farm_id):
    
    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]
    
    swap = Multicall([
            Call(token, 'minter()(address)', [['curve_minter', None]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
        ], network_chain)

    swap=swap()

    if token in ['0x55088b82748ac28e31e0677241dbbe0a663d7e40', '0xe7419b94082a87c04ffb298805ec07f745d9d216']:
        tokenIndex = 1
    else:
        tokenIndex = 0


    if token.lower() in ['0x5b5cfe992adac0c9d48e05854b2d91c73a003858'.lower(),'0x8096ac61db23291252574D49f036f0f9ed8ab390'.lower(), '0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171'.lower()]:
        token_0 = 'coins'
    else:
        token_0 = 'underlying_coins'

    try:
        swap_token = Call(swap['curve_minter'], [f'coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()
    except:
        swap_token = Call(swap['curve_minter'], [f'underlying_coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()

    swapToken = Multicall([
            Call(swap['curve_minter'], 'get_virtual_price()(uint256)', [['virtualPrice', from_wei]]),
        ], network_chain)
    
    swapCalls = swapToken()

    singleSwap = getSingle(swap_token['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap, **swap_token, **{'curve_pool_token': token}}

    final.update(swap)
    final['tkn0s'] = swap['tkn0s']

    return final

def get_curve_token_two(token, farm_id):
    
    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]
    
    swap = Multicall([
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
        ], network_chain)

    swap=swap()

    if token in ['0x55088b82748ac28e31e0677241dbbe0a663d7e40', '0xe7419b94082a87c04ffb298805ec07f745d9d216']:
        tokenIndex = 1
    else:
        tokenIndex = 0


    if token.lower() in ['0x8096ac61db23291252574D49f036f0f9ed8ab390'.lower(), '0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171'.lower(), '0x92D5ebF3593a92888C25C0AbEF126583d4b5312E'.lower(), '0x27e611fd27b276acbd5ffd632e5eaebec9761e40'.lower(), '0xFD5dB7463a3aB53fD211b4af195c5BCCC1A03890'.lower()]:
        token_0 = 'coins'
    else:
        token_0 = 'underlying_coins'

    try:
        swap_token = Call(token, [f'coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()
    except:
        swap_token = Call(token, [f'underlying_coins(uint256)(address)', tokenIndex], [['swapToken', None]], network_chain)()

    swapToken = Multicall([
            Call(token, 'get_virtual_price()(uint256)', [['virtualPrice', from_wei]])
        ], network_chain)
    
    swapCalls = swapToken()

    singleSwap = getSingle(swap_token['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap, **swap_token, **{'curve_pool_token': token}}

    final.update(swap)
    final['tkn0s'] = swap['tkn0s']

    return final

def getSwap(token, farm_id):
    
    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]
    
    swap = Multicall([
            Call(token, 'swap()(address)', [['swap', None]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
        ], network_chain)

    swap=swap()

    if token in ['0x55088b82748ac28e31e0677241dbbe0a663d7e40', '0xe7419b94082a87c04ffb298805ec07f745d9d216','0x3d479ce22d8f091df67f8fb8f579251d1b1b3152']:
        tokenIndex = 1
    else:
        tokenIndex = 0

    swapToken = Multicall([
            Call(swap['swap'], 'getVirtualPrice()(uint256)', [['virtualPrice', from_wei]]),
            Call(swap['swap'], ['getToken(uint8)(address)', tokenIndex], [['swapToken', None]]),
        ], network_chain)
    
    swapCalls = swapToken()

    singleSwap = getSingle(swapCalls['swapToken'], farm_id)

    final = {**swapCalls, **singleSwap}

    final.update(swap)

    return final

def getBeltToken(token, farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]

    try:
        belt = Multicall([
                Call(token, 'getPricePerFullShare()(uint256)', [['getPricePerFullShare', from_wei]]),
                Call(token, 'symbol()(string)', [['tkn0s', None]]),
                Call(token, 'token()(address)', [['token0', None]])
            ], network_chain)

        belt=belt()
    except:
        try:
            belt = Multicall([
                    Call(token, 'getPricePerFullShare()(uint256)', [['getPricePerFullShare', from_wei]]),
                    Call(token, 'symbol()(string)', [['tkn0s', None]]),
                    Call(token, 'want()(address)', [['token0', None]])
                ], network_chain)

            belt=belt()
        except:
            belt = Multicall([
                    Call(token, 'getPricePerFullShare()(uint256)', [['getPricePerFullShare', from_wei]]),
                    Call(token, 'symbol()(string)', [['tkn0s', None]]),
                    Call(token, 'wmatic()(address)', [['token0', None]])
                ], network_chain)

            belt=belt()      

    try:
        wrappedCalls = getLP(belt['token0'], farm_id)
        return {**wrappedCalls, **{'getPricePerFullShare': belt['getPricePerFullShare']}}
    except:
        wrappedToken = Multicall([
                Call(belt['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
            ], network_chain)
        
        wrappedCalls = wrappedToken()

        return {**wrappedCalls, **belt}

def getGrowToken(token, farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]

    grow = Multicall([
            Call(token, 'reserveToken()(address)', [['reserveToken', None]]),
            Call(token, 'totalReserve()(uint256)', [['growTotalReserve', from_wei]]),
            Call(token, 'totalSupply()(uint256)', [['growTotalSupply', from_wei]])
        ], network_chain)

    grow=grow()

    try:
        wrappedCalls = getLP(grow['reserveToken'], farm_id)
        #return {**wrappedCalls, **{'getPricePerFullShare': (grow['growTotalReserve'] / grow['growTotalSupply'])}, **grow}
        return {**wrappedCalls, **grow}
    except:
        wrappedCalls = getSingle(grow['reserveToken'], farm_id)
        #return {**wrappedCalls, **{'getPricePerFullShare': (grow['growTotalReserve'] / grow['growTotalSupply'])}, **grow}
        return {**wrappedCalls, **grow}

def kashi_token(token,farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]
    token_decimal = Call(token, 'decimals()(uint256)', None, network_chain)()

    call = Multicall([
            Call(token, 'asset()(address)', [['kashiAsset', None]]),
            Call(token, 'totalAsset()(uint256)', [['kashiTotalAsset', from_custom, token_decimal]]),
            Call(token, 'totalBorrow()(uint256)', [['kashiTotalBorrow', from_custom, token_decimal]]),
            Call(token, 'totalSupply()(uint256)', [['kashiTotalSupply', from_custom, token_decimal]]),

        ], network_chain)

    calls=call()

    wrappedCalls = getSingle(calls['kashiAsset'], farm_id)
    
    return {**wrappedCalls, **calls}

def get_picklejars(token, farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]


    call = Multicall([
            Call(token, 'getRatio()(uint256)', [['getRatio', from_wei]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
            Call(token, 'token()(address)', [['token0', None]])
        ], network_chain)

    calls=call()      

    try:
        wrappedCalls = getLP(calls['token0'], farm_id)
        return {**wrappedCalls, **{'getRatio': calls['getRatio']}}
    except:
        wrappedToken = Multicall([
                Call(calls['token0'], 'decimals()(uint8)', [['tkn0d', None]]),
            ], network_chain)
        
        wrappedCalls = wrappedToken()

        return {**wrappedCalls, **calls}

async def getPoolLengths(pools, wallet):

    bsc_calls = []
    matic_calls = []
    ftm_calls = []
    kcc_calls = []
    oke_calls = []
    eth_calls = []
    harmony_calls = []
    avax_calls = []


    final = {}
    for pool in pools:
        
        if farms[pool]['network'] == 'bsc':
            calls = bsc_calls
        elif farms[pool]['network'] == 'matic':
            calls = matic_calls
        elif farms[pool]['network'] == 'ftm':
            calls = ftm_calls
        elif farms[pool]['network'] == 'kcc':
            calls = kcc_calls
        elif farms[pool]['network'] == 'oke':
            calls = oke_calls
        elif farms[pool]['network'] == 'eth':
            calls = eth_calls
        elif farms[pool]['network'] == 'harmony':
            calls = harmony_calls
        elif farms[pool]['network'] == 'avax':
            calls = avax_calls

        if 'poolLength' in farms[pool]:
            pool_length = farms[pool]['poolLength']
        else:
            pool_length = 'poolLength'

        
        if farms[pool]['stakedFunction'] is not None and pool.lower() not in ['0x97bdB4071396B7f60b65E0EB62CE212a699F4B08'.lower(), '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7'.lower()]:
            calls.append(Call(pool, f'{pool_length}()(uint256)', [[pool, None]]))
        elif pool.lower() in ['0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7'.lower()]:
            calls.append(Call(pool, 'getRewardsLength()(uint256)', [[pool, None]]))


        final[pool] = {'name' : farms[pool]['name'], 'network' : farms[pool]['network'], 'wallet' : wallet, 'userData' : {}}

    if '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' in pools:
        poolLengths = {**await Multicall(bsc_calls, WEB3_NETWORKS['bsc'])(),
        **await Multicall(matic_calls, WEB3_NETWORKS['matic'])(), 
        **{'0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' : 3}, 
        **await Multicall(ftm_calls, WEB3_NETWORKS['ftm'])(), 
        **await Multicall(kcc_calls, WEB3_NETWORKS['kcc'])(), 
        **await Multicall(oke_calls, WEB3_NETWORKS['oke'])(),
        **await Multicall(eth_calls, WEB3_NETWORKS['eth'])(),
        **await Multicall(harmony_calls, WEB3_NETWORKS['harmony'])(),
        **await Multicall(avax_calls, WEB3_NETWORKS['avax'])()
        }
    else:
        poolLengths = {**await Multicall(bsc_calls, WEB3_NETWORKS['bsc'])(),
        **await Multicall(matic_calls, WEB3_NETWORKS['matic'])(),
        **await Multicall(ftm_calls, WEB3_NETWORKS['ftm'])(),
        **await Multicall(kcc_calls, WEB3_NETWORKS['kcc'])(), 
        **await Multicall(oke_calls, WEB3_NETWORKS['oke'])(),
        **await Multicall(eth_calls, WEB3_NETWORKS['eth'])(),
        **await Multicall(harmony_calls, WEB3_NETWORKS['harmony'])(),
        **await Multicall(avax_calls, WEB3_NETWORKS['avax'])()         
         }

    return poolLengths, final

async def getOnlyStaked(pools, wallet):
    
    bsc_calls = []
    matic_calls = []
    ftm_calls = []
    kcc_calls = []
    oke_calls = []
    eth_calls = []
    harmony_calls = []
    avax_calls = []

    final = pools[1]
    
    for pool in pools[0]:

        if farms[pool]['network'] == 'bsc':
            calls = bsc_calls
        elif farms[pool]['network'] == 'matic':
            calls = matic_calls
        elif farms[pool]['network'] == 'ftm':
            calls = ftm_calls
        elif farms[pool]['network'] == 'kcc':
            calls = kcc_calls
        elif farms[pool]['network'] == 'oke':
            calls = oke_calls
        elif farms[pool]['network'] == 'eth':
            calls = eth_calls
        elif farms[pool]['network'] == 'harmony':
            calls = harmony_calls
        elif farms[pool]['network'] == 'avax':
            calls = avax_calls
        


        stakedFunction = farms[pool]['stakedFunction']
        rng = 1 if pool in ['0x0895196562C7868C5Be92459FaE7f877ED450452'] else 0
        end = 3 if pool in [''] else pools[0][pool]
        for i in range(rng, end):
            if pool == '0xd1b3d8ef5ac30a14690fbd05cf08905e1bf7d878' and i == 2:
                continue
            elif pool == '0x0895196562C7868C5Be92459FaE7f877ED450452' and i == 331:
                continue
            elif pool == '0x95030532D65C7344347E61Ab96273B6B110385F2' and i == 43:
                continue
            elif pool == '' and i == 0:
                continue
            else:
                if pool == '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4': 
                    calls.append(Call(pool, ['%s(address,uint256)(uint256)' % (stakedFunction), wallet, i], [['%s_%s' % (pool, i), None]]))
                else:
                    calls.append(Call(pool, ['%s(uint256,address)(uint256)' % (stakedFunction), i, wallet], [['%s_%s' % (pool, i), None]]))
    stakes = await {**Multicall(bsc_calls, WEB3_NETWORKS['bsc'])(),
    **Multicall(matic_calls, WEB3_NETWORKS['matic'])(),
    **Multicall(ftm_calls, WEB3_NETWORKS['ftm'])(),
    **Multicall(kcc_calls, WEB3_NETWORKS['kcc'])(), 
    **Multicall(oke_calls, WEB3_NETWORKS['oke'])(),
    **Multicall(eth_calls, WEB3_NETWORKS['eth'])(),
    **Multicall(harmony_calls, WEB3_NETWORKS['harmony'])(),
    **Multicall(avax_calls, WEB3_NETWORKS['avax'])()
    
    }

    if '0xBeefy' in final:
        beefy = []
        for i, pool in enumerate(beefyCheck):
            beefy.append(Call(beefyCheck[pool]['earnedTokenAddress'], ['balanceOf(address)(uint256)', wallet], [['%s_%s_%s' % ('0xBeefy', i, beefyCheck[pool]['earnedTokenAddress']), None]]))
        
        beefyStakes = await Multicall(beefy)()

        stakes = {**stakes, **beefyStakes}
        


    filteredStakes = []
    #print(stakes)
    for stake in stakes:
        if stakes[stake] > 2:
            addPool = stake.split('_')
            if addPool[0] == '0x1FcCEabCd2dDaDEa61Ae30a2f1c2D67A05fDDa29':
                final[addPool[0]]['userData'][int(addPool[1])] = {'staked': 0}
            else:
                final[addPool[0]]['userData'][int(addPool[1])] = {'staked': stakes[stake]}
            filteredStakes.append({stake : stakes[stake]})
    #print(filteredStakes)
    return filteredStakes, final

async def getPendingWant(stakes, wallet):
    bsc_calls = []
    matic_calls = []
    ftm_calls = []
    kcc_calls = []
    oke_calls = []
    eth_calls = []
    harmony_calls = []
    avax_calls = []

    final = stakes[1]
    beefy_stakes = {}

    for stake in stakes[0]:
        key = next(iter(stake.keys()))
        address = key.split('_')[0]
        poolID = int(key.split('_')[1])


        if farms[address]['network'] == 'bsc':
            calls = bsc_calls
        elif farms[address]['network'] == 'matic':
            calls = matic_calls
        elif farms[address]['network'] == 'ftm':
            calls = ftm_calls
        elif farms[address]['network'] == 'kcc':
            calls = kcc_calls
        elif farms[address]['network'] == 'oke':
            calls = oke_calls
        elif farms[address]['network'] == 'eth':
            calls = eth_calls
        elif farms[address]['network'] == 'harmony':
            calls = harmony_calls
        elif farms[address]['network'] == 'avax':
            calls = avax_calls

        if farms[address]['pendingFunction'] is not None:
            pendingFunction = farms[address]['pendingFunction']
            if address not in ['0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904', '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4']:
                calls.append(Call(address, ['%s(uint256,address)(uint256)' % (pendingFunction), poolID, wallet], [['%s_%s_pending' % (address, poolID), None]]))
            
            if address in ['0x0B29065f0C5B9Db719f180149F0251598Df2F1e4']:
                calls.append(Call(address, [f'{pendingFunction}(address,uint256)(uint256)', wallet, poolID], [['%s_%s_pending' % (address, poolID), None]]))


        if farms[address]['stakedFunction'] is not None:
            if address in ['0xF1F8E3ff67E386165e05b2B795097E95aaC899F0', '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3', '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d', '0x6685C8618298C04b6E42dDAC06400cc5924e917e']:
                calls.append(Call(address, ['poolInfo(uint256)((uint256,address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), None]]))
            elif address == '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7':
                calls.append(Call(address, ['rewardsInfo(uint256)((address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parseWanted]]))
            elif address == '0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904':
                calls.append(Call(address, ['poolInfo(uint256)((address,address))', poolID], [['%s_%s_want' % (address, poolID), parseWanted]]))
            elif address in ['0x0769fd68dFb93167989C6f7254cd0D766Fb2841F','0x67da5f2ffaddff067ab9d5f025f8810634d84287']:
                calls.append(Call(address, ['lpToken(uint256)(address)', poolID], [['%s_%s_want' % (address, poolID), None]]))         
            else:
                calls.append(Call(address, ['poolInfo(uint256)((address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parseWanted]]))

        if address == '0x89d065572136814230A55DdEeDDEC9DF34EB0B76':
            calls.append(Call(address, ['poolInfo(uint256)((address,uint256,uint256,uint256))', poolID], [['%s_%s_want' % (address, poolID), parseWanted]]))

        if address in ['0xBeefy']:
            dictKey = '%s_%s_want' % (address, poolID)
            beefy_stakes.update({dictKey : key.split('_')[2] })

    stakes = await {**Multicall(bsc_calls, WEB3_NETWORKS['bsc'])(),
    **Multicall(matic_calls, WEB3_NETWORKS['matic'])(),
    **beefy_stakes,
    **Multicall(ftm_calls, WEB3_NETWORKS['ftm'])(),
    **Multicall(kcc_calls, WEB3_NETWORKS['kcc'])(),
    **Multicall(oke_calls, WEB3_NETWORKS['oke'])(),
    **Multicall(eth_calls, WEB3_NETWORKS['eth'])(),
    **Multicall(harmony_calls, WEB3_NETWORKS['harmony'])(),
    **Multicall(avax_calls, WEB3_NETWORKS['avax'])()
    }      
        



    if type(stakes) is dict:
        for stake in stakes:
                addPool = stake.split('_')
                
                if addPool[2] == 'want':
                    
                    raw_stakes = final[addPool[0]]['userData'][int(addPool[1])]['staked']
                    final[addPool[0]]['userData'][int(addPool[1])]['rawStakes'] = raw_stakes
                    
                    wanted_token = stakes[stake][1] if addPool[0] in ['0xF1F8E3ff67E386165e05b2B795097E95aaC899F0', '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3', '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d', '0x6685C8618298C04b6E42dDAC06400cc5924e917e'] else stakes[stake]
                    
                    if wanted_token.lower() in ['0x4f22aaf124853fdaed264746e9d7b21b2df86b90'.lower(),'0x5b8d0f56ea36270bb0eaf5fcbd72ea5ab98ba4af'.lower(),'0xe4b3c431e29b15978556f55b2cd046be614f558d'.lower(),'0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'.lower(), '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'.lower(), '0x299FA358763037657Bea14825CD06ff390C2a634'.lower(), '0x2e1a74a16e3a9f8e3d825902ab9fb87c606cb13f'.lower(), '0x18d755c981a550b0b8919f1de2cdf882f489c155'.lower()]:
                        final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 6)
                    elif wanted_token.lower() in ['0x62b728ced61313f17c8b784740aa0fc20a8cffe7'.lower(),'0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6'.lower(), '0xF84BD51eab957c2e7B7D646A3427C5A50848281D'.lower(), '0xa599e42a39dea9230a8164dec8316c2522c9ccd7'.lower(), '0x97ebf27d40d306ad00bb2922e02c58264b295a95'.lower()]:
                        final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 8)
                    elif wanted_token.lower() in ['0x033d942A6b495C4071083f4CDe1f17e986FE856c'.lower()]:
                        final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 4)
                    elif wanted_token.lower() in ['0x13748d548d95d78a3c83fe3f32604b4796cffa23'.lower()]:
                        final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_custom(raw_stakes, 9)
                    else:
                        final[addPool[0]]['userData'][int(addPool[1])]['staked'] = from_wei(raw_stakes)
                
                if addPool[0] in ['0xF1F8E3ff67E386165e05b2B795097E95aaC899F0', '0xdd44c3aefe458B5Cb6EF2cb674Cd5CC788AF11D3', '0xbb093349b248c8EDb20b6d846a25bF4c21d46a3d', '0x6685C8618298C04b6E42dDAC06400cc5924e917e'] and addPool[2] == 'want':                   
                    final[addPool[0]]['userData'][int(addPool[1])][addPool[2]] = stakes[stake][1]
                    stakes[stake] == stakes[stake][1]
                    stakes.update({stake: stakes[stake][1]})
                else:
                    final[addPool[0]]['userData'][int(addPool[1])][addPool[2]] = stakes[stake]

    else:
        stakes = {}
    return stakes, final

def get_token_data(data):

    bsc_calls = []
    matic_calls = []
    ftm_calls = []
    kcc_calls = []
    oke_calls = []
    eth_calls = []
    harmony_calls = []
    avax_calls = []

    for each in data[0]:

        breakdown = each.split('_')
        farm_address = breakdown[0]

        try:
            pool_id = int(breakdown[1])
        except:
            pool_id = breakdown[1]

        variable = breakdown[2]

        wanted = data[0][each]

        if 'want' in each:    
            #print(wanted)
            farm_network = farms[farm_address]['network']

            found_token = tokenDB.find_one({'tokenID' : wanted, 'network' : farm_network}, {'_id': False})
            
            if farm_network == 'bsc':
                calls = bsc_calls
            elif farm_network == 'matic':
                calls = matic_calls
            elif farm_network == 'ftm':
                calls = ftm_calls
            elif farm_network == 'kcc':
                calls = kcc_calls
            elif farm_network == 'oke':
                calls = oke_calls
            elif farm_network == 'eth':
                calls = eth_calls
            elif farm_network == 'harmony':
                calls = harmony_calls
            elif farm_network == 'avax':
                calls = avax_calls

            if found_token is not None:
                data[1][farm_address]['userData'][pool_id].update(found_token)
                if 'lpToken' in found_token:
                    calls.append(Call(found_token['lpToken'], 'totalSupply()(uint256)', [[f'{each}_totalSupply', from_wei]]))
                    calls.append(Call(found_token['lpToken'], 'getReserves()((uint112,uint112))', [[f'{each}_reserves', parseReserves]]))
                if 'getPricePerFullShare' in found_token:
                    calls.append(Call(found_token['tokenID'], 'getPricePerFullShare()(uint256)', [[f'{each}_getPricePerFullShare', from_wei]]))
                if 'swap' in found_token:
                    calls.append(Call(found_token['swap'], 'getVirtualPrice()(uint256)', [[f'{each}_virtualPrice', from_wei]]))
                if 'reserveToken' in found_token:
                    calls.append(Call(found_token['tokenID'], 'totalReserve()(uint256)', [[f'{each}_growTotalReserve', from_wei]]))
                    calls.append(Call(found_token['tokenID'], 'totalSupply()(uint256)', [[f'{each}_growTotalSupply', from_wei]]))
                if 'kashiAsset' in found_token:
                    token_decimal = found_token['tkn0d']
                    calls.append(Call(found_token['tokenID'], 'totalAsset()(uint256)', [[f'{each}_kashiTotalAsset', from_custom, token_decimal]]))
                    calls.append(Call(found_token['tokenID'], 'totalBorrow()(uint256)', [[f'{each}_kashiTotalBorrow', from_custom, token_decimal]]))
                    calls.append(Call(found_token['tokenID'], 'totalSupply()(uint256)', [[f'{each}_kashiTotalSupply', from_custom, token_decimal]]))
                if 'balancerBalances' in found_token:
                    calls.append(Call(found_token['tokenID'], [f'totalSupply()(uint256)'], [[f'{each}_totalSupply', from_wei]]))
                    calls.append(Call('0xBA12222222228d8Ba445958a75a0704d566BF2C8', ['getPoolTokens(bytes32)(address[],uint256[],uint256)', bytes.fromhex(found_token['balancerPoolID'])], [[f'{each}_balancerTokens', None],[f'{each}_balancerBalances', None]]))
                if 'curve_minter' in found_token:
                    calls.append(Call(found_token['curve_minter'], 'get_virtual_price()(uint256)', [[f'{each}_virtualPrice', from_wei]]))
                if 'getRatio' in found_token:
                    calls.append(Call(found_token['tokenID'], 'getRatio()(uint256)', [[f'{each}_getRatio', from_wei]]))
            else:
                token_data = token_router(wanted, farm_address)
                data[1][farm_address]['userData'][pool_id].update(token_data) 
                tokenDB.update_one({'tokenID' : wanted, 'network' : farm_network}, { "$set": token_data }, upsert=True)

        else:
            if variable == 'pending':
                data[1][farm_address]['userData'][pool_id][variable] = from_wei(wanted)
                data[1][farm_address]['userData'][pool_id]['rawPending'] = wanted
                data[1][farm_address]['userData'][pool_id]['poolID'] = pool_id
                data[1][farm_address]['userData'][pool_id]['contractAddress'] = farm_address

    token_calls = {**Multicall(bsc_calls, WEB3_NETWORKS['bsc'])(),
    **Multicall(matic_calls, WEB3_NETWORKS['matic'])(),
    **Multicall(ftm_calls, WEB3_NETWORKS['ftm'])(),
    **Multicall(kcc_calls, WEB3_NETWORKS['kcc'])(), 
    **Multicall(oke_calls, WEB3_NETWORKS['oke'])(),
    **Multicall(eth_calls, WEB3_NETWORKS['eth'])(),
    **Multicall(harmony_calls, WEB3_NETWORKS['harmony'])(),
    **Multicall(avax_calls, WEB3_NETWORKS['avax'])() 
    }

    for token_data in token_calls:
        breakdown = token_data.split('_')
        farm_address = breakdown[0]
        try:
            pool_id = int(breakdown[1])
        except:
            pool_id = breakdown[1]
        variable = breakdown[3]
        #print(variable,token_calls[token_data])
        data[1][farm_address]['userData'][pool_id][variable] = token_calls[token_data]

        if variable == 'growTotalReserve':
            grow_supply = (breakdown[0], breakdown[1], breakdown[2], 'growTotalSupply')
            grow_key = '_'.join(grow_supply)
            data[1][farm_address]['userData'][pool_id]['getPricePerFullShare'] = ( token_calls[token_data] / token_calls[grow_key])

        if variable == 'kashiTotalAsset':
            total_borrow = (breakdown[0], breakdown[1], breakdown[2], 'kashiTotalBorrow')
            total_supply = (breakdown[0], breakdown[1], breakdown[2], 'kashiTotalSupply')
            borrow_key = '_'.join(total_borrow)
            supply_key = '_'.join(total_supply)
            data[1][farm_address]['userData'][pool_id]['getPricePerFullShare'] = (token_calls[token_data] + token_calls[borrow_key]) / token_calls[supply_key]

        if variable == 'balancerBalances':
            balances = (breakdown[0], breakdown[1], breakdown[2], 'balancerBalances')
            balances_key = '_'.join(balances)
            data[1][farm_address]['userData'][pool_id]['balancerBalances'] = [str(x) for x in token_calls[balances_key]]
    
    return data[1]

def getLPBalances(staked, totalSupply, reserves, token0, tkn0d, tkn1d, prices):

    if token0.lower() == '0x670De9f45561a2D02f283248F65cbd26EAd861C8'.lower():
        quotePrice = getURNprice()
    else:
        quotePrice = prices[token0]

    userPct = staked / totalSupply
    lp1val = (userPct * int(reserves[0])) / (10**tkn0d)
    lp2val = (userPct * int(reserves[1])) / (10**tkn1d)

    return {'lpTotal': '%s/%s' % (round(lp1val, 2), round(lp2val, 2)), 'lpPrice' : round((lp1val * quotePrice) * 2, 2)}

def getEBalances(staked, totalSupply, reserves, token0, tkn0d, tkn1d, pricePer, eToken, prices):

    quotePrice = prices[token0]

    #Check for E11
    if token0.lower() == '0xAcD7B3D9c10e97d0efA418903C0c7669E702E4C0'.lower():
        actualStaked = staked * (pricePer / (10**12))
    else:
        actualStaked = staked * from_wei(pricePer)

    userPct = actualStaked / totalSupply
    lp1val = (userPct * int(reserves[0])) / (10**tkn0d)
    lp2val = (userPct * int(reserves[1])) / (10**tkn1d)

    return {'lpTotal': round(actualStaked, 4), 'lpPrice' : round((lp1val * quotePrice) * 2, 2), 'elevenBalance' : '(%s/%s)' % (round(lp1val, 2), round(lp2val, 2))}

def get_balancer_token(pool_token,farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]

    vault = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'


    try:
        calls = []
        calls.append(Call(pool_token, [f'getPoolId()(bytes32)'], [[f'pool_id', None]]))
        calls.append(Call(pool_token, [f'totalSupply()(uint256)'], [[f'totalSupply', from_wei]]))
        calls.append(Call(pool_token, [f'getNormalizedWeights()(uint256[])'], [[f'pool_weights', parse_pool_weights]]))

        pool_info = Multicall(calls,WEB3_NETWORKS[network])()
    except:
        calls = []
        calls.append(Call(pool_token, [f'getPoolId()(bytes32)'], [[f'pool_id', None]]))
        calls.append(Call(pool_token, [f'totalSupply()(uint256)'], [[f'totalSupply', from_wei]]))

        pool_info = Multicall(calls,WEB3_NETWORKS[network])()

    balancer_vault = setPool(balancer_vault_abi,vault,network)
    
    vault_info = balancer_vault.getPoolTokens(pool_info['pool_id']).call()

    calls = []

    for token in vault_info[0]:
        calls.append(Call(token, [f'symbol()(string)'], [[f'{token}_symbol', None]]))
        calls.append(Call(token, [f'decimals()(uint256)'], [[f'{token}_decimal', None]]))

    tokens_info = Multicall(calls,WEB3_NETWORKS[network])()

    token_symbols = []
    token_decimals = []
    for each in tokens_info:
        if 'symbol' in each:
            token_symbols.append(tokens_info[each])
        elif 'decimal' in each:
            token_decimals.append(tokens_info[each])

    if 'pool_weights' not in pool_info:
        pool_weights = []
        pool_lengths = len(vault_info[0])
        for each in vault_info[0]:
            pool_weights.append(1/pool_lengths)
    else:
        pool_weights = pool_info['pool_weights']

    token_data = { 
    "balancerPoolID" : pool_info['pool_id'].hex(),
    "balancerBalances" :  [str(x) for x in vault_info[1]],
    "balancerWeights" : pool_weights,
    "balancerSymbols" : token_symbols,
    "balancerDecimals" : token_decimals,
    'balancerTokens' : vault_info[0],
    "tkn0d" : token_decimals[0], 
    "tkn0s" : '/'.join(token_symbols), 
    "token0" : vault_info[0][0], 
    "totalSupply" : pool_info['totalSupply']
    }

    return token_data

def get_balancer_ratio(token_data,quote_price):

    userPct = token_data['staked'] / token_data['totalSupply']

    lp_multiplier = 1 / token_data['balancerWeights'][0]

    lp_values = []
    
    for i, each in enumerate(token_data['balancerBalances']):
        lpvalue = (userPct * int(each)) / (10**token_data['balancerDecimals'][i])
        lp_values.append(lpvalue)
    
    lp_price = 0

    for i,lp_balance in enumerate(lp_values):
        token_address = token_data['balancerTokens'][i]
        token_price = quote_price[token_address]
        print(lp_price,lp_balance * token_price)
        lp_price += lp_balance * token_price

    return {'lpTotal': '/'.join([str(round(x,2)) for x in lp_values]), 'lpPrice' : lp_price}

### Pool Extensions
def getElevenNerve(wallet):
    calls = []
    nrvCheck = {x['id'] : x for x in extNerve}
    for each in extNerve:
        calls.append(Call(each['earnedTokenAddress'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (each['id']), from_wei]]))
        if each['earnedTokenAddress'] == '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f':
            ethNRV = getETHrewards(wallet)
        else:
            calls.append(Call(each['earnedTokenAddress'], ['pendingEleven(address)(uint256)', wallet], [['%s_pending' % (each['id']), from_wei]]))
            calls.append(Call(each['earnedTokenAddress'], ['pendingNerve(address)(uint256)', wallet], [['%s_pendingNerve' % (each['id']), from_wei]]))
        
    stakes = { **Multicall(calls)(), **ethNRV }

    filteredStakes = []
    elevenNest = {'0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A': 
    { 'userData': { } } }

    poolIDs = {}
    
    nerveMultipler = Call('0x54f4D5dd6164B99603E77C8E13FFC3B239F63147', 'getPricePerFullShare()(uint256)', [['nrvPPS', from_wei]])()
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')

            if addPool[0] not in elevenNest['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData']:
                elevenNest['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': nrvCheck[addPool[0]]['earnedTokenAddress'], 'nerveMultipler' : nerveMultipler['nrvPPS'] }
                poolIDs['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A_%s_want' % (addPool[0])] = nrvCheck[addPool[0]]['earnedTokenAddress']
            else:    
                elevenNest['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, elevenNest    
    else:
        return None

def getETHrewards(wallet):
    
    router = setPool(nrvethABI, Web3.toChecksumAddress('0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f'))
    pendingEleven = router.pendingEleven(Web3.toChecksumAddress(wallet)).call({'from' : Web3.toChecksumAddress(wallet)})
    pendingNerve = router.pendingNerve(Web3.toChecksumAddress(wallet)).call({'from' : Web3.toChecksumAddress(wallet)})

    return { 'nerveeth_pending': from_wei(pendingEleven), 'nerveeth_pendingNerve' : from_wei(pendingNerve) }

def getHorizonStakes(wallet):
    
    calls = []
    hznCheck = {x['id'] : x for x in extHorizon}
    for each in extHorizon:
        calls.append(Call(each['stakingContract'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (each['id']), from_wei]]))
        calls.append(Call(each['stakingContract'], ['earned(address)(uint256)', wallet], [['%s_pending' % (each['id']), from_wei]]))
        #calls.append(Call(each['stakingContract'], ['rewardsToken()(address)'], [['%s_rewardToken' % (each['id']), None]]))
    stakes = Multicall(calls)()

    filteredStakes = []
    hznNest = {'0xHorizon': 
    { 'userData': { 
        } 
    }}

    poolIDs = {}
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')
            if addPool[0] not in hznNest['0xHorizon']['userData']:
                hznNest['0xHorizon']['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': hznCheck[addPool[0]]['tokenAddress'] }
                poolIDs['0xHorizon_%s_want' % (addPool[0])] = hznCheck[addPool[0]]['tokenAddress']
            else:
                hznNest['0xHorizon']['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, hznNest     
    else:
        return None

def getBeefyBoosts(wallet):
    
    calls = []
    for each in bBoostsCheck:
        poolID = bBoostsCheck[each]['earnContractAddress']
        calls.append(Call(poolID, ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (each), from_wei]]))
        calls.append(Call(poolID, ['earned(address)(uint256)', wallet], [['%s_pending' % (each), from_wei]]))
    stakes = Multicall(calls)()

    filteredStakes = []
    boostNest = {'0xBeefy': 
    { 'userData': { 
        } 
    }}

    poolIDs = {}
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')
            if addPool[0] not in boostNest['0xBeefy']['userData']:
                boostNest['0xBeefy']['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want' : bBoostsCheck[addPool[0]]['tokenAddress'], 'boostedReward': bBoostsCheck[addPool[0]]['earnedOracleId'], 'rewardSymbol' : bBoostsCheck[addPool[0]]['earnedToken'] }
                poolIDs['0xBeefy_%s_want' % (addPool[0])] = bBoostsCheck[addPool[0]]['tokenAddress']
            else:
                boostNest['0xBeefy']['userData'][addPool[0]].update({addPool[1]: stakes[stake]})


    if len(poolIDs) > 0:
        return poolIDs, boostNest     
    else:
        return None

def getMoneyPot(wallet):
    
    calls = []

    moneyTokens = [{'token' : '0xe9e7cea3dedca5984780bafc599bd69add087d56', 'symbol' : 'BUSD'}, {'token' : '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', 'symbol' : 'WBNB' }]
    potContract = '0x020Fa682C4249eF7d242691d04cf6Ff0A609B941'
    u235 = '0x28d2E3BB1Ec54A6eE8b3Bee612F03A85d3Ec0C0c'
    lenMoney = len(moneyTokens)

    for i, each in enumerate(moneyTokens):
        calls.append(Call(potContract, ['pendingTokenRewardsAmount(address,address)(uint256)', each['token'], wallet], [['%s_pending' % (each['symbol']), from_wei]]))
        if i+1 == lenMoney:
            calls.append(Call(u235, ['balanceOf(address)(uint256)', wallet], [['u235balance', from_wei]]))
    stakes = Multicall(calls)()

    filteredStakes = []
    moneyNest = {'0xF3ca45633B2b2C062282ab38de74EAd2B76E8800': 
    { 'userData': { 
        } 
    }}

    return stakes

def getbingoBoard(wallet):

    bingoKey = '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08'
    boardRoom = '0xc9525f505040fecd4b754407De72d7bCf5a8f78F'
    nestName = 'bingoBoard'
    calls = []

    calls.append(Call(boardRoom, ['balanceOf(address)(uint256)', wallet], [['%s_staked' % (nestName), from_wei]]))
    calls.append(Call(boardRoom, ['earned(address)(uint256)', wallet], [['%s_pending' % (nestName), from_wei]]))
        
    stakes=Multicall(calls)()

    filteredStakes = []
    
    bingoNest = {bingoKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in bingoNest[bingoKey]['userData']:
                bingoNest[bingoKey]['userData'][nestName] = {addPool[1]: stakes[stake], 'want': '0x53F39324Fbb209693332B87aA94D5519A1a49aB0' }
                poolIDs['%s_%s_want' % (bingoKey, nestName)] = '0x53F39324Fbb209693332B87aA94D5519A1a49aB0'
            else:    
                bingoNest[bingoKey]['userData'][nestName].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, bingoNest    
    else:
        return None

def getIronFinance(wallet, vaults, farm_id, network):
    
    poolKey = farm_id
    calls = []

    for vault in vaults:
        breakdown = vault.split('_')
        masterchef = breakdown[0]
        pool_id = int(breakdown[1])

        calls.append(Call(masterchef, ['userInfo(uint256,address)(uint256)', pool_id, wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(masterchef, ['poolInfo(uint256)(address)', pool_id], [[f'{vault}_want', None]]))
        calls.append(Call(masterchef, ['pendingReward(uint256,address)(uint256)', pool_id, wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(masterchef, ['rewardToken()(address)'], [[f'{vault}_rewardToken', None]]))
    
    stakes=Multicall(calls, network)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                pool_key = f'{breakdown[0]}_{breakdown[1]}'
                no_unders = f'{breakdown[0]}-{breakdown[1]}'
                staked = stakes[each]
                want_token = stakes[f'{pool_key}_want']
                pending = stakes[f'{pool_key}_pending']
                reward_token = stakes[f'{pool_key}_rewardToken']
                reward_symbol = vaults[pool_key]['rewardToken'].upper()

                poolNest[poolKey]['userData'][no_unders] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol}
                poolIDs['%s_%s_want' % (poolKey, no_unders)] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getDiamondHands(wallet):

    poolKey = '0xDiamondHands'
    calls = []

    for pool in diamonds:
        if pool['contract'] in ['0xe5476aA8f9b0D22580bb7c796c53493BAD942Db4', '0xF26a92c8281e83Ec7E09C64C70e649e74dB22Ad4', '0x22210d79264B77c3545eb3E12415796AE2CA108c']:
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % (pool['contract']), from_wei]])) 
        else:
            calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['stakedFunction']), 0, wallet], [['%s_staked' % (pool['contract']), from_wei]]))
            calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['rewardFunction']), 0, wallet], [['%s_pending' % (pool['contract']), from_wei]]))        
    stakes=Multicall(calls)()

    filteredStakes = []


    
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolCheck = {x['contract'] : x for x in diamonds}
    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'rewardToken' : poolCheck[addPool[0]]['rewardToken'], 'rewardSymbol' : poolCheck[addPool[0]]['rewardSymbol'] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getApoyield(wallet):

    poolKey = '0xe87DE2d5BbB4aF23c665Cf7331eC744B020883bB'
    calls = []

    for pool in thirdParty:
        # if pool['contract'] == '0x9Ef9a563C5639349e211450Bfcf59E7f7453ab90':
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % (pool['contract']), from_wei]])) 
        # else:
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['stakedFunction']), 0, wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['rewardFunction']), 0, wallet], [['%s_pending' % (pool['contract']), from_wei]]))        
    stakes=Multicall(calls)()

    filteredStakes = []


    
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolCheck = {x['contract'] : x for x in thirdParty}
    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'rewardToken' : poolCheck[addPool[0]]['rewardToken'], 'rewardSymbol' : poolCheck[addPool[0]]['rewardSymbol'] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getFuelVaults(wallet):

    poolKey = '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56'
    calls = []

    for pool in fuelVaults:
        # if pool['contract'] == '0x9Ef9a563C5639349e211450Bfcf59E7f7453ab90':
        calls.append(Call(pool, ['%s(address)(uint256)' % ('balanceOf'), wallet], [['%s_staked' % (pool), from_wei]])) 
        # else:
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['stakedFunction']), 0, wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        # calls.append(Call(pool['contract'], ['%s(uint8,address)(uint256)' % (pool['rewardFunction']), 0, wallet], [['%s_pending' % (pool['contract']), from_wei]]))        
    stakes=Multicall(calls)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getBunnyPools(wallet):

    poolKey = '0xPancakeBunny'
    bunnyHop = '0xb3c96d3c3d643c2318e4cdd0a9a48af53131f5f4'
    calls = []

    for pool in bunnies:
        contract = pool
        calls.append(Call(bunnyHop, ['infoOfPool(address,address)((address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256))', contract, wallet], [['%s_userInfo' % (contract), parseBunny]]))
        calls.append(Call(contract, ['rewardsToken()(address)'], [['%s_rewardToken' % (contract), None]]))
        calls.append(Call(contract, ['stakingToken()(address)'], [['%s_want' % (contract), None]]))        
    
    stakes=Multicall(calls)()

    filteredStakes = []

    #print(stakes)
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolIDs = {}

    for stake in stakes:
        if 'userInfo' in stake:
            if stakes[stake]['userInfo']['staked'] > 0:
                #print(stake)
                addPool = stake.split('_')
                poolWant = addPool[0] + '_' + 'want'
                poolReward = addPool[0] + '_' + 'rewardToken'
                #print(addPool[0], stakes[poolReward])
                #print(addPool[0],stakes[poolReward])
                try:
                    rewardSy = Call(stakes[poolReward], 'symbol()(string)', [['symbol', None]])()
                except:
                    rewardSy = {'symbol' : '?'}     
                if addPool[0] not in poolNest[poolKey]['userData']:
                    poolNest[poolKey]['userData'][addPool[0]] = stakes[stake]['userInfo']
                    poolIDs['%s_%s_want' % (poolKey, addPool[0])] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['want'] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardToken'] = stakes[poolReward]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardSymbol'] = rewardSy['symbol']
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getWaultLocked(wallet):

    poolKey = '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D'
    locked = '0x52a2b3beafa46ba51a4792793a7447396d09423f'
    lockedx = '0x06747f6501611baE9dD054cCC37ad076e9Ea2465'
    lockedwex = '0xF4E0943C1D55e883E3C6310CD641970A36a7f870'
    lockedEuler = '0x38Ab2128327107D075a13E6Ed66Bd6184E4Cc20c'
    wault = '0x6ff2d9e5891a7a7c554b80e0d1b791483c78bce9'
    waultx = '0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21'
    euler = '0x3920123482070c1a2dff73aad695c60e7c6f6862'
    wex='0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90'
    lockedVaults = 3
    lockedxVaults = 1
    lockedeVaults = 1
    lockedwexVaults = 1
    calls = []

    for i in range(0,lockedVaults):
        calls.append(Call(locked, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['wault%s_staked' % (i), from_wei]])) 
        calls.append(Call(locked, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['wault%s_pending' % (i), from_wei]]))

    for i in range(0,lockedxVaults):
        calls.append(Call(lockedx, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['waultx%s_staked' % (i), from_wei]]))
        calls.append(Call(lockedx, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['waultx%s_pending' % (i), from_wei]]))

    for i in range(0,lockedeVaults):
        calls.append(Call(lockedEuler, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['euler%s_staked' % (i), from_wei]]))
        calls.append(Call(lockedEuler, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['euler%s_pending' % (i), from_wei]]))

    for i in range(0,lockedwexVaults):
        calls.append(Call(lockedwex, ['%s(uint256,address)(uint256)' % ('userInfo'), i, wallet], [['wex%s_staked' % (i), from_wei]]))
        calls.append(Call(lockedwex, ['%s(uint256,address)(uint256)' % ('pendingRewards'), i, wallet], [['wex%s_pending' % (i), from_wei]]))
    


    stakes=Multicall(calls)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        addPool = stake.split('_')
        if 'staked' in addPool[1]:
            if stakes[stake] > 0:
                poolType = addPool[0][:-1]

                if poolType == 'wault':
                    wanted = wault
                    rewarded = wault
                    rewardSym = 'WAULT'
                elif poolType == 'waultx':
                    wanted = waultx
                    rewarded = waultx
                    rewardSym = 'WAULTX'
                elif poolType == 'euler':
                    wanted = euler 
                    rewarded = euler
                    rewardSym = 'EULER'
                elif poolType == 'wex':
                    wanted = wex 
                    rewarded = wex
                    rewardSym = 'WEX'

                if addPool[0] not in poolNest[poolKey]['userData']:
                    poolNest[poolKey]['userData'][addPool[0]] = {'staked': stakes[stake], 'want': wanted, 'rewardToken' : rewarded, 'rewardSymbol' : rewardSym, 'pending' : stakes['%s_pending' % (addPool[0])] }
                    poolIDs['%s_%s_want' % (poolKey, addPool[0])] = wanted

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getValueSafes(wallet):
    poolKey = '0xd56339F80586c08B7a4E3a68678d16D37237Bd96'
    calls = []

    for pool in getvSafes():
        calls.append(Call(pool['id'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % pool['id'], from_wei]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_user_firebird_vaults(wallet):
    poolKey = '0xE9a8b6ea3e7431E6BefCa51258CB472Df2Dd21d4'
    calls = []

    for pool in get_firebird_vaults():
        calls.append(Call(pool['id'], ['balanceOf(address)(uint256)', wallet], [['%s_staked' % pool['id'], from_wei]]))
    
    stakes=Multicall(calls, WEB3_NETWORKS['matic'])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getGambits(wallet):

    poolKey = '0xGambit'
    calls = []

    for pool in gambits:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        for i, reward in enumerate(pool['rewards']):
            calls.append(Call(reward['yieldTracker'], ['%s(address)(uint256)' % (reward['rewardFunction']), wallet], [['%s_pending_%s_%s' % (pool['contract'], reward['symbol'], reward['rewardToken']), from_wei]]))

    stakes=Multicall(calls)()

    filteredStakes = []


    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    poolCheck = {x['contract'] : x for x in gambits}

    #print(stakes)
    for stake in stakes:
    # if stakes[stake] > 0:
        addPool = stake.split('_')       
        if addPool[0] not in poolNest[poolKey]['userData']:
            poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'gambitRewards' : [] }
            poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
        else:
            if 'pending' in addPool[1]:     
                poolNest[poolKey]['userData'][addPool[0]]['gambitRewards'].append({addPool[1]: stakes[stake], 'symbol' : addPool[2], 'token' : addPool[3]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getTaoDao(wallet):
    poolKey = '0xTaodao'
    calls = []

    for pool in dao:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % pool['stakeToken'], from_tao if pool['decimal'] == 9 else from_wei ]]))
        if pool['rewardFunction'] is not None:
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['rewardFunction']), wallet], [['%s_pending' % pool['stakeToken'], from_tao]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getPop(wallet):
    poolKey = '0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0'
    epsChef = '0xcce949De564fE60e7f96C85e55177F8B9E4CF61b'
    wantToken = '0x049d68029688eAbF473097a2fC38ef61633A3C7A'
    calls = []

    calls.append(Call(epsChef, ['%s(uint256,address)(uint256)' % ('userInfo'), 2, wallet], [['%s_staked' % (epsChef), from_wei ]]))
    calls.append(Call(epsChef, ['%s(uint256,address)(uint256)' % ('claimableReward'), 2, wallet], [['%s_pending' % (epsChef), from_wei]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': wantToken }
                poolIDs['%s_%s_want' % (poolKey, epsChef)] = wantToken
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getFortress(wallet):

    faiVault = '0x066807c7B22c6c0a7fa370A2cA812e5Fc22DBef6'
    poolKey = '0xFortress'
    calls = []

    for fort in forts:
        calls.append(Call(fort, ['%s(address)((uint256,uint256,uint256,uint256))' % ('getAccountSnapshot'), wallet], [['%s_staked' % (fort), parseAccountSnapshot ]]))
        if fort != '0xE24146585E882B6b59ca9bFaaaFfED201E4E5491':
            calls.append(Call(fort, 'underlying()(address)', [['%s_want' % fort, None]]))
    
    calls.append(Call(faiVault, ['%s(address)(uint256)' % ('userInfo'), wallet], [['%s_staked' % (faiVault), from_wei ]]))
    calls.append(Call(faiVault, ['%s(address)(uint256)' % ('pendingFTS'), wallet], [['%s_pending' % (faiVault), from_wei ]]))
    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    #print(stakes)
    for stake in stakes:
        if 'staked' in stake:
                if stakes[stake] > 0:
                    addPool = stake.split('_')
                    if addPool[0] == '0xE24146585E882B6b59ca9bFaaaFfED201E4E5491':
                        want = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
                        pending = 0
                    elif addPool[0] == '0x066807c7B22c6c0a7fa370A2cA812e5Fc22DBef6':
                        want = '0x10a450A21B79c3Af78fb4484FF46D3E647475db4'
                        pending = stakes['%s_pending' % addPool[0]]
                    else:
                        want = stakes['%s_want' % addPool[0]]
                        pending = 0      
                    if addPool[0] not in poolNest[poolKey]['userData']:
                        poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': want, 'pending' : pending }
                        poolIDs['%s_%s_want' % (poolKey, addPool[0])] = want


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getDYP(wallet):

    poolKey = '0xDYP'
    calls = []

    for pool in dypPools:
        calls.append(Call(pool, ['%s(address)(uint256)' % ('depositedTokens'), wallet], [['%s_staked' % (pool), from_wei ]]))
        calls.append(Call(pool, ['%s(address)(uint256)' % ('getPendingDivsEth'), wallet], [['%s_pending' % (pool), from_wei ]]))
        calls.append(Call(pool, 'trustedDepositTokenAddress()(address)', [['%s_want' % pool, None]]))

    
    stakes=Multicall(calls)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    rewarded = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
    rewardSym = 'WBNB'
    for stake in stakes:
        if 'staked' in stake:
                if stakes[stake] > 0:
                    addPool = stake.split('_')
                    want = stakes['%s_want' % addPool[0]]
                    pending = stakes['%s_pending' % addPool[0]]    
                    
                    if addPool[0] not in poolNest[poolKey]['userData']:
                        poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': want, 'pending' : pending, 'rewardToken' : rewarded, 'rewardSymbol' : rewardSym }
                        poolIDs['%s_%s_want' % (poolKey, addPool[0])] = want


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def getMerlinPools(wallet):

    poolKey = '0xMerlin'
    bunnyHop = '0xfF8B299da344AD8Ff399b4CBd3db01c0c7264bdf'
    calls = []

    for pool in magic:
        contract = pool
        calls.append(Call(bunnyHop, ['infoOfPool(address,address)((address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256))', contract, wallet], [['%s_userInfo' % (contract), parseMerlin]]))
        calls.append(Call(contract, ['rewardsToken()(address)'], [['%s_rewardToken' % (contract), None]]))
        calls.append(Call(contract, ['stakingToken()(address)'], [['%s_want' % (contract), None]]))
        #calls.append(Call(contract, ['priceShare()(uint256)'], [['%s_getPricePerFullShare' % (contract), from_wei]]))
                
    
    stakes=Multicall(calls)()

    filteredStakes = []

    #print(stakes)
    poolNest = {poolKey: 
    { 'userData': { } } }
    
    poolIDs = {}

    for stake in stakes:
        if 'userInfo' in stake:
            if stakes[stake]['userInfo']['staked'] > 0:
                #print(stake)
                addPool = stake.split('_')
                poolWant = addPool[0] + '_' + 'want'
                poolReward = addPool[0] + '_' + 'rewardToken'
                #pricePer = addPool[0] + '_' + 'getPricePerFullShare'
                #print(addPool[0], stakes[poolReward])
                #print(addPool[0],stakes[poolReward])
                try:
                    rewardSy = Call(stakes[poolReward], 'symbol()(string)', [['symbol', None]])()
                except:
                    rewardSy = {'symbol' : '?'}     
                if addPool[0] not in poolNest[poolKey]['userData']:
                    poolNest[poolKey]['userData'][addPool[0]] = stakes[stake]['userInfo']
                    poolIDs['%s_%s_want' % (poolKey, addPool[0])] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['want'] = stakes[poolWant]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardToken'] = stakes[poolReward]
                    poolNest[poolKey]['userData'][addPool[0]]['rewardSymbol'] = rewardSy['symbol']
                    #poolNest[poolKey]['userData'][addPool[0]]['getPricePerFullShare'] = stakes[pricePer]
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_eleven_hodls(wallet, eleven_hodls):

    poolKey = '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A'
    calls = []

    for eleven_token in eleven_hodls:
        if '11' in eleven_token['earnedToken'] and eleven_token['network'] == 'bsc' and eleven_token['earnedTokenAddress'] not in ['0x3Ed531BfB3FAD41111f6dab567b33C4db897f991', '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f', '0x0D5BaE8f5232820eF56D98c04B8F531d2742555F', '0xDF098493bB4eeE18BB56BE45DC43BD655a27E1A9', '0x27DD6E51BF715cFc0e2fe96Af26fC9DED89e4BE8', '0x025E2e9113dC1f6549C83E761d70E647c8CDE187']:
            pool_id = eleven_token['earnedTokenAddress']
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', from_wei]]))
    
    stakes=Multicall(calls)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_beefy_matic_stakes(wallet):

    poolKey = '0xBeefyMatic'
    calls = []

    for token in beefy_matic_pools:
        pool_id = token['earnedTokenAddress']
        if pool_id == '0xE71f3C11D4535a7F8c5FB03FDA57899B2C9c721F':
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', from_six]]))
        else:
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', from_wei]]))

    stakes=Multicall(calls, WEB3_NETWORKS['matic'])()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_beefy_style_stakes(wallet,vaults,farm_id,network):

    poolKey = farm_id
    calls = []

    for vault in vaults:
        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))

    stakes=Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_eleven_hodls_polygon(wallet, eleven_hodls):

    poolKey = '0xD109D9d6f258D48899D7D16549B89122B0536729'
    calls = []

    for eleven_token in eleven_hodls:
        if '11' in eleven_token['earnedToken'] and eleven_token['network'] == 'polygon' and eleven_token['earnedTokenAddress'] not in ['0x0FFb84A4c29147Bd745AAe0330f4F6f4Cb716c92','0x3Ed531BfB3FAD41111f6dab567b33C4db897f991', '0x5C0E7b820fCC7cC66b787A204B2B31cbc027843f', '0x0D5BaE8f5232820eF56D98c04B8F531d2742555F', '0xDF098493bB4eeE18BB56BE45DC43BD655a27E1A9', '0x27DD6E51BF715cFc0e2fe96Af26fC9DED89e4BE8', '0x025E2e9113dC1f6549C83E761d70E647c8CDE187']:
            pool_id = eleven_token['earnedTokenAddress']
            calls.append(Call(pool_id, ['balanceOf(address)(uint256)', wallet], [[f'{pool_id}_staked', None]]))
    
    stakes=Multicall(calls, WEB3_NETWORKS['matic'])()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for stake in stakes:
        if stakes[stake] > 1:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                
                wanted_token = addPool[0]
                
                if wanted_token.lower() in ['0x4f22aaf124853fdaed264746e9d7b21b2df86b90'.lower(),'0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'.lower(), '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'.lower(), '0x299FA358763037657Bea14825CD06ff390C2a634'.lower()]:
                    staked_value = from_custom(stakes[stake], 6)
                elif wanted_token.lower() in ['0x62b728ced61313f17c8b784740aa0fc20a8cffe7'.lower(),'0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6'.lower(), '0xF84BD51eab957c2e7B7D646A3427C5A50848281D'.lower(), '0xa599e42a39dea9230a8164dec8316c2522c9ccd7'.lower()]:
                    staked_value = from_custom(stakes[stake], 8)
                elif wanted_token.lower() in ['0x033d942A6b495C4071083f4CDe1f17e986FE856c'.lower()]:
                    staked_value = from_custom(stakes[stake], 4)
                else:
                    staked_value = from_wei(stakes[stake])
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: staked_value, 'want': addPool[0] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = addPool[0]
            else:    
                poolNest[poolKey]['userData'][addPool[0]].update({addPool[1]: stakes[stake]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_nuts(wallet):

    poolKey = '0xSquirrel'
    calls = []

    for pool in nuts:
        calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (pool['stakedFunction']), wallet], [['%s_staked' % (pool['contract']), from_wei]]))
        for i, reward in enumerate(pool['rewards']):
            calls.append(Call(pool['contract'], ['%s(address)(uint256)' % (reward['rewardFunction']), wallet], [['%s_pending_%s_%s' % (pool['contract'], reward['symbol'], reward['rewardToken']), from_wei]]))

    stakes=Multicall(calls)()

    filteredStakes = []


    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    poolCheck = {x['contract'] : x for x in nuts}

    #print(stakes)
    for stake in stakes:
        if stakes[stake] > 0:
            addPool = stake.split('_')       
            if addPool[0] not in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData'][addPool[0]] = {addPool[1]: stakes[stake], 'want': poolCheck[addPool[0]]['stakeToken'], 'gambitRewards' : [] }
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = poolCheck[addPool[0]]['stakeToken']
            else:
                if 'pending' in addPool[1]:     
                    poolNest[poolKey]['userData'][addPool[0]]['gambitRewards'].append({addPool[1]: stakes[stake], 'symbol' : addPool[2], 'token' : addPool[3]})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_adamant_funds(wallet):

    poolKey = '0xAdamant'
    calculator = '0x80d8dad3753887731BA8f92AEe84Df371B6A7790'
    minter = '0xAAE758A2dB4204E1334236Acd6E6E73035704921'
    strat_vaults_calls = []
    
    addy_mints = Call(minter, 'addyPerProfitEth()(uint256)', None, WEB3_NETWORKS['matic'])()
    
    # for deployer in adamant_deployers:
    #         contract = deployer['address']
    #         loop_over = deployer['poolLength']
    #         for lp in range(0,loop_over):
    #             strat_vaults_calls.append(Call(contract, ['deployedVaults(uint256)((address,address))', lp], [[f'{contract}_{lp}_addresses', None]]))
    
    # strat_vaults = Multicall(strat_vaults_calls, WEB3_NETWORKS['matic'])()
    # strat_vaults['0x3253e956a0e70a6b65D170511A84e93e16848dae_0_addresses'] = ('0x3253e956a0e70a6b65d170511a84e93e16848dae', '0xdf70e065ec14ea9a85cf99ec776bf83271ad11a9')
    # strat_vaults['0xD06D816DAae530f5Aa94903e89501f20BEBA6fB2_0_addresses'] = ('0x6eaf123d49f4e233f8283a69bd59a2443650f322', '0x9dd816c8966f0cdcf9c05ceed830163ff46080ff')
    # strat_vaults['0xD06D816DAae530f5Aa94903e89501f20BEBA6fB2_1_addresses'] = ('0x92c7277240e9ac0e82df455e0c808622664a79c3', '0xc872df0159b062c05c99ce6d3ef482980fb2a6a4')

    adamant_user_info = []
    strat_vaults = json.loads(requests.get('https://raw.githubusercontent.com/eepdev/vaults/main/current_vaults.json').text)
    for item in strat_vaults:
        strategy = item['strategyAddress']
        vault = item['vaultAddress']

        adamant_user_info.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        adamant_user_info.append(Call(vault, ['getPendingReward(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
        adamant_user_info.append(Call(vault, ['getRewardMultiplier()(uint256)'], [[f'{vault}_multiplier', None]]))
        adamant_user_info.append(Call(strategy, ['want()(address)'], [[f'{vault}_want', None]]))
    



    user_data = Multicall(adamant_user_info, WEB3_NETWORKS['matic'])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    

    for each in user_data:
        if 'staked' in each:
            if user_data[each] > 0:
                breakdown = each.split('_')
                staked = user_data[each]
                pending = user_data[f'{breakdown[0]}_pending']
                want_token = user_data[f'{breakdown[0]}_want']
                reward_multi = user_data[f'{breakdown[0]}_multiplier']
                reward_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

                extra_data = Multicall(
                    
                [Call(breakdown[0], ['getRatio()(uint256)'], [['getPricePerFullShare', from_wei]]),
                Call(calculator,['valueOfAsset(address,uint256)(uint256)', reward_token, pending], [['real_pending', None]])], WEB3_NETWORKS['matic'])()

                ppfs = extra_data['getPricePerFullShare']
                actual_staked = staked * ppfs
                actual_pending = extra_data['real_pending']
                 

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : actual_staked, 'pending': (from_wei((actual_pending * addy_mints)) * reward_multi) / 1000 }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

    addy_eth = get_addy_eth(wallet, addy_mints)
    if addy_eth is not None:
        poolIDs.update(addy_eth[0])
        poolNest['0xAdamant']['userData'].update(addy_eth[1]['0xAdamant']['userData'])

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_addy_eth(wallet, minting_rate=None):

    poolKey = '0xAdamant'
    
    adamant_user_info = []

    vault = '0xF7661EE874Ec599c2B450e0Df5c40CE823FEf9d3'

    adamant_user_info.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
    adamant_user_info.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', None]]))
    adamant_user_info.append(Call(vault, ['stakingToken()(address)'], [[f'{vault}_want', None]]))
    
    user_data = Multicall(adamant_user_info, WEB3_NETWORKS['matic'])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}
    
    for each in user_data:
        if 'staked' in each:
            if user_data[each] > 0:
                breakdown = each.split('_')
                staked = user_data[each]
                pending = user_data[f'{breakdown[0]}_pending']
                want_token = user_data[f'{breakdown[0]}_want']
                actual_pending = from_wei(pending * minting_rate)
                 

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending': actual_pending }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_quickswap_style(wallet, vaults, farm_id, network, want_function=None):
    
    if want_function is None:
        want_function = 'stakingToken'
    else:
        want_function = want_function

    poolKey = farm_id
    calls = []

    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(vault, [f'{want_function}()(address)'], [[f'{vault}_want', None]]))
    
    stakes=Multicall(calls, network)()

    filteredStakes = []

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                pending = stakes[f'{breakdown[0]}_pending']
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending': pending }
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_quickswap_style_multi(wallet, vaults, farm_id, network):
    
    poolKey = farm_id
    calls = []

    for vault in vaults:

        calls.append(Call(vault, ['balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        #calls.append(Call(vault, ['earned(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(vault, ['stakingToken()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, ['bothTokensEarned(address)(address[])', wallet], [[f'{vault}_rewardtokens', None]]))
    
    stakes=Multicall(calls, network)()

    reward_calls = []

    for each in stakes:
        if 'rewardtokens' in each:
            for i, token in enumerate(stakes[each]):
                vault = each.split('_')[0]
                reward_calls.append(Call(vault, ['earned(address,address)(uint256)', wallet, token], [[f'{vault}_{i}_{token}_pending', from_wei]]))
                reward_calls.append(Call(token, 'symbol()(string)', [[f'{vault}_{i}_{token}_symbol', None]]))


    rewards=Multicall(reward_calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_tokens = stakes[f'{breakdown[0]}_rewardtokens']
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i, rtoken in enumerate(reward_tokens):
                    reward_address = rtoken
                    reward_key = f'{breakdown[0]}_{i}_{rtoken}'
                    pending_amount = rewards[f'{reward_key}_pending']
                    symbol = rewards[f'{reward_key}_symbol']
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append({'pending': pending_amount, 'symbol' : symbol, 'token' : reward_address})
                    
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_vault_style(wallet, vaults, farm_id, network, _pps=None, _stake=None, _strict=None, want_token=None):

    if _pps == None:
        pps = 'getRatio'
    else:
        pps = _pps
    
    if _stake is None:
        stake = 'balanceOf'
    else:
        stake = _stake

    if _strict is None:
        strict = False
    else:
        strict = _strict
    
    if want_token is None:
        want_token = 'token'
    else:
        want_token = want_token

    poolKey = farm_id
    calls = []
    for vault in vaults:
        if vault == '0x992Ae1912CE6b608E0c0d2BF66259ab1aE62A657':
            calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', from_custom, 9]]))
        else:
            calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', None]]))
        
        if vault in ['0xa6Fc07819eE785C120aB765981b313D71b4FF406']:
            calls.append(Call(vault, [f'wmatic()(address)'], [[f'{vault}_want', None]]))
        elif vault in ['0x929e9dEfF1070bA346FB45EB841F035dCC29D131','0x5cD44E5Aa00b8D77c8c7102E530d947AB86c9551','0xA0FfC3b52c315B00ea3DaFbC3094059D46aA5Daf','0x2bffD2442C4509c32Cc4bcACC4aC85B89A0076BA','0x6F5be5d7Ecdd948dB34C111C06AEa1E2fE2D2c2F','0xCf2CF4B53B62022F81Ad73cAe04E433936eca6c0']:
            calls.append(Call(vault, [f'want()(address)'], [[f'{vault}_want', None]]))
        else:
            calls.append(Call(vault, [f'{want_token}()(address)'], [[f'{vault}_want', None]]))
        
        calls.append(Call(vault, [f'{pps}()(uint256)'], [[f'{vault}_getPricePerFullShare', from_wei]]))
    
    stakes=Multicall(calls, network, _strict=strict)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    token_decimals = template_helpers.get_token_list_decimals(vaults,farms[farm_id]['network'],False)

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                token_decimal = 18 if breakdown[0] not in token_decimals else token_decimals[breakdown[0]]
                staked = from_custom(stakes[each], token_decimal)
                want_token = stakes[f'{breakdown[0]}_want']
                price_per = stakes[f'{breakdown[0]}_getPricePerFullShare']
                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'getPricePerFullShare' : price_per, 'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_pancake_bunny_clones(wallet, vaults, network_id, dashboard_contract, calculator, farm_id, native_symbol, _decode=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        if _decode is None:
            decode = 'address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256'
        else:
            decode = 'address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256'

        for vault in vaults:
                calls.append(Call(dashboard_contract, ['profitOfPool(address,address)((uint256,uint256))', vault, wallet], [[f'{vault}_pendings', parse_profit_of_pool]]))
                calls.append(Call(dashboard_contract, [f'infoOfPool(address,address)(({decode}))', vault, wallet], [[f'{vault}_userinfo', parse_pancake_bunny_info]]))
                calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'rewardsToken()(address)'], [[f'{vault}_rewardtoken', None]]))


        stakes=Multicall(calls, network)()

        filteredStakes = []

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'userinfo' in each:
                if stakes[each]['balance'] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]['principal']
                    want_token = stakes[f'{breakdown[0]}_want']
                    pendings = stakes[f'{breakdown[0]}_pendings']
                    reward_token = '0xD016cAAe879c42cB0D74BB1A265021bf980A7E96' if stakes[f'{breakdown[0]}_rewardtoken'] == '0x6b70f0136a7e2bd1fa945566b82b208760632b2e' else stakes[f'{breakdown[0]}_rewardtoken']

                    try:
                        staked_symbol = Call(reward_token, 'symbol()(string)', None, network)()
                    except:
                        reward_token = Call(reward_token, [f'rewardsToken()(address)'], [[f'rewardtoken', None]], network)()['rewardtoken']
                        staked_symbol = Call(reward_token, 'symbol()(string)', None, network)()

                    staked_single_price = Call(calculator, ['valueOfAsset(address,uint256)((uint256,uint256))', reward_token, one_token], [[f'prices', parse_profit_of_pool]], network)()

                    if breakdown[0] in ['0x4Ad69DC9eA7Cc01CE13A37F20817baC4bF0De1ba','0x7a526d4679cDe16641411cA813eAf7B33422501D']:
                        poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : [{'pending': pendings[0], 'symbol' : native_symbol, 'token' : farms[poolKey]['rewardToken']}]}
                    else:
                        poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : [{'pending': pendings[1], 'symbol' : native_symbol, 'token' : farms[poolKey]['rewardToken']}, {'pending': pendings[0], 'symbol' : staked_symbol, 'token' : reward_token, 'valueOfAsset' : staked_single_price['prices'][1]}]}
                        
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_syrup_pools(wallet, pools, network_id, farm_id, staked=None, reward=None, pending_reward=None, user_info=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        staked = 'stakedToken' if staked is None else staked
        reward = 'rewardToken' if reward is None else reward
        pending_reward = 'pendingReward' if pending_reward is None else pending_reward
        user_info = 'userInfo' if user_info is None else user_info

        for pool in pools:
            calls.append(Call(pool, [f'{user_info}(address)(uint256)', wallet], [[f'{pool}_staked', from_wei]]))
            calls.append(Call(pool, [f'{pending_reward}(address)(uint256)', wallet], [[f'{pool}_pending', None]]))
            calls.append(Call(pool, [f'{staked}()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'{reward}()(address)'], [[f'{pool}_rewardtoken', None]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pendings = stakes[f'{breakdown[0]}_pending']
                    reward_token = stakes[f'{breakdown[0]}_rewardtoken']

                    reward_calls = []
                    reward_calls.append(Call(reward_token, 'symbol()(string)', [[f'symbol', None]]))
                    reward_calls.append(Call(reward_token, 'decimals()(uint256)', [[f'decimal', None]]))

                    reward_data=Multicall(reward_calls, network)()

                    reward_symbol = reward_data['symbol']
                    reward_decimal = reward_data['decimal']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : from_custom(pendings, reward_decimal), 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'rewardDecimal' : reward_decimal}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_adamant_stakes(wallet, farm_id):
    
    poolKey = farm_id
    staking_contract = '0x920f22E1e5da04504b765F8110ab96A20E6408Bd'
    addy_rewards = setPool(reward_abi, '0x920f22E1e5da04504b765F8110ab96A20E6408Bd', 'matic')
    wallet = Web3.toChecksumAddress(wallet)

    stakes= Call(staking_contract, ['totalBalance(address)(uint256)', wallet], [[f'totalBalance', from_wei]], WEB3_NETWORKS['matic'])()


    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}


    if stakes['totalBalance'] > 0:

        staked = stakes['totalBalance']
        reward_tokens = addy_rewards.claimableRewards(wallet).call()
        want_token = '0xc3FdbadC7c795EF1D6Ba111e06fF8F16A20Ea539'

        poolNest[poolKey]['userData'][staking_contract] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, staking_contract)] = want_token

        for i, rtoken in enumerate(reward_tokens):
            if rtoken[1] > 0: 
                reward_address = rtoken[0]
                pending_amount = from_wei(rtoken[1])
                symbol = Call(reward_address, 'symbol()(string)', [[f'symbol', None]], WEB3_NETWORKS['matic'])()['symbol']
                poolNest[poolKey]['userData'][staking_contract]['gambitRewards'].append({'pending': pending_amount, 'symbol' : symbol, 'token' : reward_address})
                    
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_apeswap(wallet, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        mini_ape = '0x54aff400858Dcac39797a81894D9920f16972D1D'
        mini_complex = '0x1F234B1b83e21Cb5e2b99b4E498fe70Ef2d6e3bf'
        pool_length = Call(mini_ape, [f'poolLength()(uint256)'],None,network)()
        

        for pid in range(0,pool_length):
            calls.append(Call(mini_ape, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}_staked', from_wei]]))
            calls.append(Call(mini_ape, [f'pendingBanana(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pending', from_wei]]))
            calls.append(Call(mini_ape, [f'lpToken(uint256)(address)', pid], [[f'{pid}_want', None]]))
            calls.append(Call(mini_complex, [f'pendingToken(uint256,address)(uint256)', pid, wallet], [[f'{pid}_complexp', from_wei]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pending = stakes[f'{breakdown[0]}_pending']
                    complex = stakes[f'{breakdown[0]}_complexp']
                    reward_token = '0x5d47baba0d66083c52009271faf3f50dcc01023c'
                    native_symbol = 'BANANA'
                    complex_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'
                    staked_symbol = 'WMATIC'


                    poolNest[poolKey]['userData'][int(breakdown[0])] = {'want': want_token, 'staked' : staked, 'gambitRewards' : [{'pending': pending, 'symbol' : native_symbol, 'token' : reward_token}, {'pending': complex, 'symbol' : staked_symbol, 'token' : complex_token}]}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_single_masterchef(wallet,farm_id,network_id,farm_data):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        if 'poolFunction' not in farm_data:
            pool_function = 'poolLength'
        else:
            pool_function = farm_data['poolFunction']
        
        pool_length = Call(farm_data['masterChef'], [f'{pool_function}()(uint256)'],None,network)() 
        staked_function = farm_data['stakedFunction']
        pending_function = farm_data['pendingFunction']
        reward_token = farm_data['rewardToken']
        reward_symbol = farm_data['rewardSymbol']
        if 'wantFunction' not in farm_data:
            want_function = 'poolInfo'
        else:
            want_function = farm_data['wantFunction']

        for pid in range(0,pool_length):
            calls.append(Call(farm_data['masterChef'], [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', from_wei]]))
            calls.append(Call(farm_data['masterChef'], [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_pending', from_wei]]))
            calls.append(Call(farm_data['masterChef'], [f'{want_function}(uint256)(address)', pid], [[f'{pid}ext_want', None]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pending = stakes[f'{breakdown[0]}_pending']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_acryptos_style_boosts(wallet, vaults, farm_id, network, caller, pfunc):

    poolKey = farm_id
    calls = []

    for vault in vaults:
        calls.append(Call(caller, [f'userInfo(address,address)(uint256)',vault,wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(caller, [f'{pfunc}(address,address)(uint256)',vault,wallet], [[f'{vault}_pending', from_wei]]))
    
    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = breakdown[0]
                pending = stakes[f'{breakdown[0]}_pending']
                poolNest[poolKey]['userData'][f'{breakdown[0]}-BOOST'] = {'want': want_token, 'staked' : staked, 'pending'  : pending}
                poolIDs['%s_%s_want' % (poolKey, f'{breakdown[0]}-BOOST')] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_pyq_triple_staking(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'stakes(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
                calls.append(Call(vault, [f'lqtyToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'getPendingETHGain(address)(uint256)', wallet], [[f'{vault}_pendingETH', from_wei]]))
                calls.append(Call(vault, [f'getPendingLQTYGain(address)(uint256)', wallet], [[f'{vault}_pendingLQTY', from_wei]]))
                calls.append(Call(vault, [f'getPendingLUSDGain(address)(uint256)', wallet], [[f'{vault}_pendingLUSD', from_wei]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]

                    reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingETH'], 'symbol' : 'WMATIC', 'token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'}
                    reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingLUSD'], 'symbol' : 'PUSD', 'token' : '0x9af3b7dc29d3c4b1a5731408b6a9656fa7ac3b72'}
                    reward_token_2 = {'pending': stakes[f'{breakdown[0]}_pendingLQTY'], 'symbol' : 'PYQ', 'token' : '0x5a3064cbdccf428ae907796cf6ad5a664cd7f3d8'}

                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_2)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

def get_pyq_double_staking(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'getCompoundedLUSDDeposit(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
                calls.append(Call(vault, [f'lusdToken()(address)'], [[f'{vault}_want', None]]))
                calls.append(Call(vault, [f'getDepositorETHGain(address)(uint256)', wallet], [[f'{vault}_pendingETH', from_wei]]))
                calls.append(Call(vault, [f'getDepositorLQTYGain(address)(uint256)', wallet], [[f'{vault}_pendingLQTY', from_wei]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]

                    reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingETH'], 'symbol' : 'WMATIC', 'token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'}
                    reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingLQTY'], 'symbol' : 'PYQ', 'token' : '0x5a3064cbdccf428ae907796cf6ad5a664cd7f3d8'}

                    want_token = stakes[f'{breakdown[0]}_want']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

def get_pyq_trove(wallet, vaults, farm_id, network_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]
        one_token = 1 * 10 ** 18

        for vault in vaults:
                calls.append(Call(vault, [f'getTroveColl(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
                calls.append(Call(vault, [f'getTroveDebt(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : 'PUSD', 'token' : '0x9af3b7dc29d3c4b1a5731408b6a9656fa7ac3b72'}
                    want_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

            if len(poolIDs) > 0:
                return poolIDs, poolNest    
            else:
                return None

def get_mai_graph(wallet):
    url = 'https://api.thegraph.com/subgraphs/name/gallodasballo/mai-finance-quick'
    obj = """{
    vaults(where: {account: "%s"}) {
    id
    account {
      id
    }
    deposited
    borrowed
        }
    }"""
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    vaults = json.loads(requests.post(url, json={'query': obj % (wallet.lower()), 'variables': None}, headers=headers).text)['data']['vaults']
    
    staked = 0
    pending = 0

    for each in vaults:
        staked += from_wei(int(each['deposited']))
        pending += from_wei(int(each['borrowed']))

    return {'VAULTS_staked' : staked, 'VAULTS_pending' : pending}

def get_mai_cvault(wallet, farm_id):
        poolKey = farm_id

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        stakes = get_mai_graph(wallet)

        if stakes['VAULTS_staked'] > 0:
            staked = stakes['VAULTS_staked']
            reward_token_0 = {'pending': stakes['VAULTS_pending'], 'symbol' : 'miMATIC', 'token' : '0xa3Fa99A148fA48D14Ed51d610c367C61876997F1'.lower()}
            want_token = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'

            poolNest[poolKey]['userData']['VAULTS'] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
            poolIDs['%s_%s_want' % (poolKey, 'VAULTS')] = want_token

            poolNest[poolKey]['userData']['VAULTS']['gambitRewards'].append(reward_token_0)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_wault_pools(wallet, pools, network_id, farm_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for pool in pools:
            calls.append(Call(pool, [f'userInfo(address)(uint256)', wallet], [[f'{pool}_staked', from_wei]]))
            calls.append(Call(pool, [f'pendingRewards(address)(uint256)', wallet], [[f'{pool}_pending', from_wei]]))
            calls.append(Call(pool, [f'pool()(address)'], [[f'{pool}_want', None]]))
            calls.append(Call(pool, [f'rewardToken()(address)'], [[f'{pool}_rewardtoken', None]]))


        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    pendings = stakes[f'{breakdown[0]}_pending']
                    reward_token = stakes[f'{breakdown[0]}_rewardtoken']
                    reward_symbol = Call(reward_token, 'symbol()(string)', [[f'symbol', None]], network)()['symbol']

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pendings, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_farmhero_staking(wallet,vault,network,farm_id):

    calls = []
    poolKey = farm_id

    calls.append(Call(vault, [f'totalBalance(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
    calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes = Multicall(calls,WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']
                w3_instance = setPool(multi_fee_v2,vault,network)
                reward_tokens = w3_instance.claimableRewards(wallet).call()

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i, rtoken in enumerate(reward_tokens):
                    reward_address = rtoken[0]
                    if rtoken[1] > 1:
                        pending_amount = from_wei(rtoken[1])
                        symbol = Call(reward_address, [f'symbol()(string)'], [[f'symbol', None]],WEB3_NETWORKS[network])()['symbol']
                        poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append({'pending': pending_amount, 'symbol' : symbol, 'token' : reward_address})

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_fh_pools(wallet,list_of_pools,network,farm_id,stake_func=None,reward_func=None):
    
    poolKey = farm_id

    if stake_func is None:
        stake_func = 'stakeToken'
    
    if reward_func is None:
        reward_func = 'rewardToken'

    
    calls = []
    for pool in list_of_pools:
        calls.append(Call(pool, ['balanceOf(address)(uint256)', wallet], [[f'{pool}_staked', from_wei]]))
        calls.append(Call(pool, [f'earned(address)(uint256)', wallet], [[f'{pool}_pending', from_wei]]))
        calls.append(Call(pool, [f'{stake_func}()(address)'], [[f'{pool}_want', None]]))
        calls.append(Call(pool, [f'{reward_func}()(address)'], [[f'{pool}_rewardtoken', None]]))

    stakes = Multicall(calls,WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_token = stakes[f'{breakdown[0]}_rewardtoken']
                try:
                    reward_token_want = Call(reward_token, 'want()(address)', [[f'want', None]], WEB3_NETWORKS[network])()['want']
                    reward_token_pps = Call(reward_token, 'getPricePerFullShare()(uint256)', [[f'pps', from_wei]], WEB3_NETWORKS[network])()['pps']
                    reward_token_symbol = Call(reward_token_want, 'symbol()(string)', [[f'symbol', None]], WEB3_NETWORKS[network])()['symbol']
                    reward_token = reward_token_want
                except:
                    reward_token_symbol = Call(reward_token, 'symbol()(string)', [[f'symbol', None]], WEB3_NETWORKS[network])()['symbol']
                    reward_token_pps =  1
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'] * reward_token_pps, 'symbol' : reward_token_symbol, 'token' : reward_token}
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_quickswap_lps(wallet,farm_id):

    poolKey = farm_id

    liquidityPositions = call_graph('https://api.thegraph.com/subgraphs/name/sameepsi/quickswap03', {'operationName' : 'liquidityPositions', 'query' : quickswap_lps.query, 'variables' : {'user': wallet.lower()}})

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for lp in liquidityPositions['data']['liquidityPositions']:
        if float(lp['liquidityTokenBalance']) > 0:
                staked = float(lp['liquidityTokenBalance'])
                want_token = lp['pair']['id']

                poolNest[poolKey]['userData'][f'QSLP{want_token}'] = {'want': want_token, 'staked' : staked, 'pending' : 0}
                poolIDs['%s_%s_want' % (poolKey, f'QSLP{want_token}')] = want_token
                    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_aperocket_space_pool(wallet,vaults,rewardtoken,network,farm_id,profit_offset):
    
    calls = []
    poolKey = farm_id
    
    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'SPACE()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'profitOf(address)((uint256,uint256,uint256))', wallet], [[f'{vault}_pending', parse_spacepool, profit_offset]]))

    stakes = Multicall(calls,WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_token = rewardtoken['token']
                reward_token_symbol = rewardtoken['symbol']
                reward_token_decimal = rewardtoken['decimal']
                reward_token_0 = {'pending': from_custom(stakes[f'{breakdown[0]}_pending'],reward_token_decimal), 'symbol' : reward_token_symbol, 'token' : reward_token}
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_balancer_user_pools(wallet,pools,network_id,farm_id):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for pool in pools:
            calls.append(Call(pool, [f'balanceOf(address)(uint256)', wallet], [[f'{pool}_staked', from_wei]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = breakdown[0]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : 0}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                
        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_pickle_chef(wallet,farm_id,network_id,chef,rewarder):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]
    pool_length = Call(chef, [f'poolLength()(uint256)'],None,network)() 

    for pid in range(0,pool_length):
        calls.append(Call(chef, [f'userInfo(uint256,address)(uint256)', pid, wallet], [[f'{pid}_staked', from_wei]]))
        calls.append(Call(chef, [f'pendingPickle(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pendingPickle', from_wei]]))
        calls.append(Call(rewarder, [f'pendingToken(uint256,address)(uint256)', pid, wallet], [[f'{pid}_pendingMatic', from_wei]]))
        calls.append(Call(chef, [f'lpToken(uint256)(address)', pid], [[f'{pid}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                pid = int(breakdown[0])
                staked = stakes[each]
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingPickle'], 'symbol' : 'PICKLE', 'token' : '0x2b88ad57897a8b496595925f43048301c37615da'}
                reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingMatic'], 'symbol' : 'WMATIC', 'token' : '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][pid] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][pid]['gambitRewards'].append(reward_token_0)
                poolNest[poolKey]['userData'][pid]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_curve_gauage(wallet,farm_id,network_id,gauages,rewards=None):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    if rewards is None:
        rewards = ['0x172370d5Cd63279eFa6d502DAB29171933a610AF', '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270']

    for guage in gauages:
        calls.append(Call(guage, [f'balanceOf(address)(uint256)', wallet], [[f'{guage}_staked', from_wei]]))
        for i,each in enumerate(rewards):
            calls.append(Call(guage, [f'claimable_reward_write(address,address)(uint256)', wallet,each], [[f'{guage}_pending{i}', from_wei]]))
        calls.append(Call(guage, [f'lp_token()(address)'], [[f'{guage}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()
    print(stakes)
    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                for i,each in enumerate(rewards):
                    symbol = Call(each, [f'symbol()(string)'], _w3=network)()
                    reward_gambit = {'pending': stakes[f'{breakdown[0]}_pending{i}'], 'symbol' : symbol, 'token' : each}

                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_gambit)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_telx_single(wallet,farm_id,network_id,vaults):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'earned(address)(uint256)', wallet], [[f'{vault}_pending', from_wei]]))
        calls.append(Call(vault, [f'rewardsToken()(address)'], [[f'{vault}_rewardToken', None]]))
        calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_token = stakes[f'{breakdown[0]}_rewardToken']
                reward_symbol = Call(reward_token, [f'symbol()(string)'], _w3=network)()
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pending'], 'symbol' : reward_symbol, 'token' : reward_token}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_telx_double(wallet,farm_id,network_id,vaults):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    for vault in vaults:
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'earnedA(address)(uint256)', wallet], [[f'{vault}_pendingA', from_wei]]))
        calls.append(Call(vault, [f'earnedB(address)(uint256)', wallet], [[f'{vault}_pendingB', from_wei]]))
        calls.append(Call(vault, [f'rewardsTokenA()(address)'], [[f'{vault}_rewardTokenA', None]]))
        calls.append(Call(vault, [f'rewardsTokenB()(address)'], [[f'{vault}_rewardTokenB', None]]))
        calls.append(Call(vault, [f'stakingToken()(address)'], [[f'{vault}_want', None]]))

    stakes=Multicall(calls, network,_strict=False)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_tokenA = stakes[f'{breakdown[0]}_rewardTokenA']
                reward_tokenB = stakes[f'{breakdown[0]}_rewardTokenB']
                reward_symbolA = Call(reward_tokenA, [f'symbol()(string)'], _w3=network)()
                reward_symbolB = Call(reward_tokenB, [f'symbol()(string)'], _w3=network)()
                reward_token_0 = {'pending': stakes[f'{breakdown[0]}_pendingA'], 'symbol' : reward_symbolA, 'token' : reward_tokenA}
                reward_token_1 = {'pending': stakes[f'{breakdown[0]}_pendingB'], 'symbol' : reward_symbolB, 'token' : reward_tokenB}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_blackswan_stakes(wallet):
    
    poolKey = '0xBlackSwan'
    calls = []
    swan_lake = '0xE420CC7F8F0df0f145d146e9FDC8a4237660Eecb'
    distribution_pool = '0xbCf0734600AC0AcC1BaD85f62c0BE82BBC8Ca3B5'

    calls.append(Call(distribution_pool,['balanceOf(address)(uint256)', wallet], [[f'{distribution_pool}_staked', from_custom, 6]]))
    calls.append(Call(distribution_pool,['takeWithAddress(address)(uint256)', wallet], [[f'{distribution_pool}_pending', from_wei]]))
    calls.append(Call(distribution_pool,['token()(address)'], [[f'{distribution_pool}_want', None]]))
    calls.append(Call(swan_lake,['balanceOf(address)(uint256)', wallet], [[f'{swan_lake}_staked', from_wei]]))
    calls.append(Call(swan_lake,['_takeWithAddress(address)((uint256,uint256))', wallet], [[f'{swan_lake}_pending', None]]))
    calls.append(Call(swan_lake,['token()(address)'], [[f'{swan_lake}_want', None]]))

    stakes = Multicall(calls,WEB3_NETWORKS['matic'])()
    
    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                reward_tokenA = '0xab7589dE4C581Db0fb265e25a8e7809D84cCd7E8'
                reward_symbolA = 'SWAN'
                reward_pendingA = stakes[f'{distribution_pool}_pending'] if breakdown[0] == distribution_pool else from_wei(stakes[f'{swan_lake}_pending'][1])
                reward_token_0 = {'pending': reward_pendingA , 'symbol' : reward_symbolA, 'token' : reward_tokenA}
                
                if breakdown[0] == swan_lake:
                    reward_tokenB = '0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'
                    reward_symbolB = 'SWAN-LP'
                    reward_pendingB = from_wei(stakes[f'{swan_lake}_pending'][0])
                    reward_token_1 = {'pending': reward_pendingB, 'symbol' : reward_symbolB, 'token' : reward_tokenB}

                want_token = stakes[f'{breakdown[0]}_want']

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)
                if breakdown[0] == swan_lake:
                    poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_1)

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_feeder_style(wallet, vaults, network, farm_id):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for vault in vaults:
        calls.append(Call(vault, [f'userInfo(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'token()(address)'], [[f'{vault}_want', None]]))
        calls.append(Call(vault, [f'depositedTokenBalance(bool)(uint256)',False], [[f'{vault}_depositedTokenBalance', from_wei]]))
        calls.append(Call(vault, [f'totalShares()(uint256)'], [[f'{vault}_totalShares', from_wei]]))

    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = stakes[f'{breakdown[0]}_want']
                depositedTokenBalance = stakes[f'{breakdown[0]}_depositedTokenBalance']
                totalShares = stakes[f'{breakdown[0]}_totalShares']

                if want_token == '0x0000000000000000000000000000000000000000':
                    want_token = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked/totalShares * depositedTokenBalance, 'vault_receipt' : breakdown[0], 'contractAddress' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_sfeed(wallet,staking_token,receipt_token,network,farm_id):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for vault in staking_token:
        calls.append(Call(receipt_token, [f'balanceOf(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))
        calls.append(Call(vault, [f'balanceOf(address)(uint256)', receipt_token], [[f'{vault}_totalDepositedFeeds', from_wei]]))
        calls.append(Call(receipt_token, [f'totalSupply()(uint256)'], [[f'{vault}_totalSFeedTokens', from_wei]]))

    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = breakdown[0]
                virtual_price = stakes[f'{breakdown[0]}_totalDepositedFeeds'] / stakes[f'{breakdown[0]}_totalSFeedTokens']           

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'contractAddress' : receipt_token, 'getPricePerFullShare' : virtual_price}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

def get_vault_style_no_want(wallet, vaults, farm_id, network, _pps=None, _stake=None, _strict=None, want_token=None, pps_decimal=None):

    if _pps == None:
        pps = 'getRatio'
    else:
        pps = _pps
    
    if _stake is None:
        stake = 'balanceOf'
    else:
        stake = _stake

    if _strict is None:
        strict = False
    else:
        strict = _strict
    
    if want_token is None:
        want_token = 'token'
    else:
        want_token = want_token

    if pps_decimal is None:
        pps_decimal = 18
    else:
        pps_decimal = pps_decimal

    poolKey = farm_id
    calls = []
    for vault in vaults:
        calls.append(Call(vault, [f'{stake}(address)(uint256)', wallet], [[f'{vault}_staked', from_wei]]))        
        calls.append(Call(vault, [f'{pps}()(uint256)'], [[f'{vault}_getPricePerFullShare', from_custom, pps_decimal]]))
    
    stakes=Multicall(calls, network, _strict=strict)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'staked' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                staked = stakes[each]
                want_token = want_token
                price_per = stakes[f'{breakdown[0]}_getPricePerFullShare']
                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'getPricePerFullShare' : price_per, 'vault_receipt' : breakdown[0]}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_lending_protocol(wallet,lending_vaults,farm_id,network):

    poolKey = farm_id
    calls = []

    for vault in lending_vaults:
        vault_address = vault['address']
        calls.append(Call(vault_address, [f'getAccountSnapshot(address)((uint256,uint256,uint256,uint256))', wallet], [[f'{vault_address}_accountSnapshot', None ]]))
        
    stakes=Multicall(calls, WEB3_NETWORKS[network])()

    poolNest = {poolKey: 
    { 'userData': { }
     } }

    poolIDs = {}

    hash_map = {x['address'] : x for x in lending_vaults}

    for stake in stakes:
        if stakes[stake][1] > 0 or stakes[stake][2] > 0:
            addPool = stake.split('_')
            if addPool[0] not in poolNest[poolKey]['userData']:

                snapshot =  stakes[stake]
                underlying = hash_map[addPool[0]]['want']
                underlying_decimal = hash_map[addPool[0]]['decimal']           
                collat = from_custom(snapshot[1], underlying_decimal)
                collat_rate = hash_map[addPool[0]]['collat_rate']
                borrow = from_custom(snapshot[2], underlying_decimal)
                rate = from_wei(snapshot[3])
                poolNest[poolKey]['userData'][addPool[0]] = {'staked' : collat * rate, 'want': underlying, 'borrowed' : borrow, 'rate' : collat_rate}
                poolIDs['%s_%s_want' % (poolKey, addPool[0])] = underlying


    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None

def get_just_pending(wallet,contracts,network,farm_id,reward_method,reward_token):

    poolKey = farm_id
    network = WEB3_NETWORKS[network]
    calls = []
    for contract in contracts:
        calls.append(Call(contract, [f'{reward_method}(address)(uint256)', wallet], [[f'{contract}_pending', from_wei]]))

    stakes=Multicall(calls, network)()

    poolNest = {poolKey: 
    { 'userData': { } } }

    poolIDs = {}

    for each in stakes:
        if 'pending' in each:
            if stakes[each] > 0:
                breakdown = each.split('_')
                pending = stakes[each]
                want_token = reward_token

                poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : 0, 'pending' : pending}
                poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
    
    if len(poolIDs) > 0:
        return poolIDs, poolNest
    else:
        return None

def get_moneypot(wallet, rewards, farm_id, network_id, contract, token_pair=None):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        for i,reward in enumerate(rewards):
            reward_address = reward['address']
            calls.append(Call(contract, [f'pendingTokenRewardsAmount(address,address)(uint256)', reward['address'], wallet], [[f'{reward_address}_{i}', from_wei]]))
        calls.append(Call(token_pair, [f'balanceOf(address)(uint256)', wallet], [[f'{token_pair}', from_wei]]))

        stakes=Multicall(calls, network)()

        print(stakes)

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        want_token = token_pair

        poolNest[poolKey]['userData'][contract] = {'want': token_pair, 'staked' : stakes[token_pair], 'gambitRewards' : []}
        poolIDs['%s_%s_want' % (poolKey, contract)] = want_token

        for i in range(0,len(rewards)):
            token = rewards[i]['address']
            token_id = f'{token}_{i}'
            pending = stakes[token_id]

            if pending > 0:
                reward_token_data = {'pending': pending, 'symbol' : rewards[i]['symbol'], 'token' : token}
                poolNest[poolKey]['userData'][contract]['gambitRewards'].append(reward_token_data)

        # for i,reward in enumerate(rewards):
        #     token = reward['address']
        #     token_id = f'{token}_{i}'
        #     pending = stakes[token_id]
        #     print(pending)
        #     if pending > 0:
        #         reward_token_data = {'pending': pending, 'symbol' : reward['symbol'], 'token' : reward['address']}
        #         poolNest[poolKey]['userData'][contract]['gambitRewards'].append(reward_token_data)

        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

def get_zombie_masterchef(wallet,farm_id,network_id,chef):
        poolKey = farm_id
        calls = []
        network = WEB3_NETWORKS[network_id]

        pool_function = 'poolLength'
        pool_length = Call(chef, [f'{pool_function}()(uint256)'],None,network)() 
        
        staked_function = 'userInfo'
        pending_function = 'pendingZombie'
        reward_token = '0x50ba8bf9e34f0f83f96a340387d1d3888ba4b3b5'
        reward_symbol = 'ZMBE'
        want_function = 'poolInfo'

        for pid in range(0,pool_length):
            calls.append(Call(chef, [f'{staked_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_staked', from_wei]]))
            calls.append(Call(chef, [f'{pending_function}(uint256,address)(uint256)', pid, wallet], [[f'{pid}ext_pending', from_wei]]))
            calls.append(Call(chef, [f'{want_function}(uint256)((address,uint256,uint256,uint256,uint256,bool,bool,address,address,uint256,uint256,uint256,uint256))', pid], [[f'{pid}ext_want', parser.parse_zombie_pool]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']['lp_token']
                    pending = stakes[f'{breakdown[0]}_pending']
                    zombie_override = True if stakes[f'{breakdown[0]}_want']['is_grave'] and stakes[f'{breakdown[0]}_want']['requires_rug'] else False

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'pending' : pending, 'rewardToken' : reward_token, 'rewardSymbol' : reward_symbol, 'zombieOverride' : zombie_override, 'contractAddress' : chef}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token
                


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None

### Prices
async def async_get_request(session, url, token, decimal, shareAmount, quote_decimal):
    try:
        timeout = ClientTimeout(total=5)
        async with session.get(url, headers={'Content-Type': 'application/json'}) as response:
            content = await response.json()
        # print(content)
        #return { 'token' : token, 'price' : (int(content['bestResult']['routes'][0]['amount']) / (10**18)) / 100 }
        try: 
            return { 'token' : token, 'price' : (int(content['toTokenAmount']) / (10**quote_decimal)) / shareAmount }
        except:
            print('Oracle Error', token, content)
            return { 'token' : token, 'price' : 0 }
    except:
        print('Failed', token)
        return {'token' : token, 'price' : .01 }

async def multiCallPrice(loopOver):
    tasks = []
    timeout = ClientTimeout(total=40)

    network_ids={'bsc' : '56', 'matic' : '137', 'kcc' : '321', 'eth' : '1'}

    async with ClientSession(timeout=timeout) as session:
        for token in loopOver:
            
            #Catch Native Tokens
            if token['token'].lower() == '0x3Ed531BfB3FAD41111f6dab567b33C4db897f991'.lower():
                tkn = '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0'
            elif token['token'].lower() == '0x15B9462d4Eb94222a7506Bc7A25FB27a2359291e'.lower():
                tkn = '0x42f6f551ae042cbe50c739158b4f0cac0edb9096'
            elif token['token'].lower() in fulcrmCheck:
                tkn = fulcrmCheck[token['token'].lower()]['loanToken']
            elif token['token'].lower() == '-':
                tkn = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'.lower()
            elif token['token'].lower() in alpacas:
                tkn = alpacas[token['token'].lower()]
            elif token['token'].lower() == '0x62445168cf24b9cbeda1ba716196e05399b0da7c':
                tkn = '0xE0B58022487131eC9913C1F3AcFD8F74FC6A6C7E'
            elif token['token'].lower() == '0x2612F31fD829578F3f9c8DF1c4793C15340520FE':
                tkn = '0x6f6350d5d347aa8f7e9731756b60b774a7acf95b'
            else:
                tkn = token['token']

            if tkn.lower() in ['0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c'.lower(), '0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6'.lower(), '0x24834BBEc7E39ef42f4a75EAF8E5B6486d3F0e57'.lower(), '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'.lower()]:
                shareAmount = 1
            elif tkn.lower() in ['0xc581b735a1688071a1746c968e0798d642ede491'.lower()]:
                shareAmount = 1000
            else:
                shareAmount = 100

            tkndecimal = shareAmount * 10 ** token['decimal']
            
            network = network_ids[token['network']]
            quote_decimal = 18

            if token['network'] == 'bsc':
                quote_token = '0xe9e7cea3dedca5984780bafc599bd69add087d56'
            elif token['network'] == 'matic':
                quote_token = '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'
            elif token['network'] == 'eth':
                quote_token = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
                quote_decimal = 6

            if tkn.lower() in ['0xe9e7cea3dedca5984780bafc599bd69add087d56'.lower(), '0x7343b25c4953f4c57ed4d16c33cbedefae9e8eb9'.lower()] :
                url = f'https://api.1inch.exchange/v3.0/{network}/quote?fromTokenAddress={tkn}&toTokenAddress=0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3&amount={tkndecimal}'
                #url = 'https://pathfinder-bsc-56.1inch.exchange/v1.0/quote?fromTokenAddress=%s&toTokenAddress=0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3&amount=%s&gasPrice=5000000000' % (tkn, tkndecimal)
            elif tkn.lower() in ['0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'.lower()]:
                url = f'https://api.1inch.exchange/v3.0/{network}/quote?fromTokenAddress={tkn}&toTokenAddress=0xc2132D05D31c914a87C6611C10748AEb04B58e8F&amount={tkndecimal}'
            elif tkn.lower() in ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'.lower()]:
                url = f'https://api.1inch.exchange/v3.0/{network}/quote?fromTokenAddress={tkn}&toTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&amount={tkndecimal}'
            elif tkn.lower() in ['0xc168e40227e4ebd8c1cae80f7a55a4f0e6d66c97'.lower(), '0x24834BBEc7E39ef42f4a75EAF8E5B6486d3F0e57'.lower()]:
                url = f'https://api.1inch.exchange/v3.0/{network}/quote?fromTokenAddress={tkn}&toTokenAddress={quote_token}&amount={tkndecimal}&protocols=DFYN'
            else:
                url = f'https://api.1inch.exchange/v3.0/{network}/quote?fromTokenAddress={tkn}&toTokenAddress={quote_token}&amount={tkndecimal}'
                #url = 'https://pathfinder-bsc-56.1inch.exchange/v1.0/quote?fromTokenAddress=%s&toTokenAddress=0xe9e7cea3dedca5984780bafc599bd69add087d56&amount=%s&gasPrice=5000000000' % (tkn, tkndecimal)

            task = asyncio.ensure_future(async_get_request(session, url, token['token'], token['decimal'], shareAmount, quote_decimal))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return(responses)

def setPool(abi, address, network=None):
    if network == None:
        w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))
    else:
        w3 = WEB3_NETWORKS[network]['connection']
    contract = w3.eth.contract(address=address, abi=abi)
    poolFunctions = contract.functions
    return(poolFunctions)

def getURNprice():
    Web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
    router = setPool(uraniumABI, '0xF4EE46Ac2BA83121F79c778ed0D950ffF11a18Ed')
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress('0x670De9f45561a2D02f283248F65cbd26EAd861C8'), Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')]).call()
    return from_wei(price[1])

def getPHBprice():
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=red-pulse&vs_currencies=usd')
    data = json.loads(r.text)

    return data['red-pulse']['usd']

def getJetValue():
    calls = []

    fuelContract = '0x2090c8295769791ab7a3cf1cc6e0aa19f35e441a'
    jetContract = '0xf6488205957f0b4497053d6422F49e27944eE3Dd'


    calls.append(Call(fuelContract, ['%s(address)(uint256)' % ('balanceOf'), jetContract], [['fuelShare', from_wei]]))
    calls.append(Call(jetContract, ['%s()(uint256)' % ('totalSupply')], [['jetShare', from_wei]])) 
       
    stakes=Multicall(calls)()

    jetMultipler = stakes['fuelShare'] / stakes['jetShare']

    return jetMultipler

def getDiamondPrices(symbol):
    url = 'https://api.diamondhand.fi/token/info'
    obj = {"tokens":[symbol]}
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    x = requests.post(url, data=json.dumps(obj), headers=headers)
    
    return from_custom(int(json.loads(x.text)[0]['price']), 6 )

def getWaultPrices():
    r = requests.get('https://api.wault.finance/realtimeData.js?ts=%s' % (round(time.time())))
    r = r.text[19:]
    r = json.loads(r)
    return r

def getxGMTprice():

    GMT_READER = Web3.toChecksumAddress('0xCcD9623e3A54024F74bc989f14d461Fb309287Fe')
    PCS_V2_FACTORY = Web3.toChecksumAddress('0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73')
    callTOKENS = [Web3.toChecksumAddress('0xe304ff0983922787Fd84BC9170CD21bF78B16B10'),Web3.toChecksumAddress('0x85E76cbf4893c1fbcB34dCF1239A91CE2A4CF5a7')]

    router = setPool(gambitABI, GMT_READER)
    price = router.getPairInfo(PCS_V2_FACTORY, callTOKENS).call()
    return price[1] / price[0]

def getwSwap(token):
    #Web3.toChecksumAddress('0xD48745E39BbED146eEC15b79cBF964884F9877c2')
    router = setPool(json.loads(wSwapABI), Web3.toChecksumAddress('0xD48745E39BbED146eEC15b79cBF964884F9877c2'))
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')]).call()
    return from_wei(price[1])

def getCGprice(tokenID):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={tokenID}&vs_currencies=usd'
    r = requests.get(url)
    r = json.loads(r.text)

    return r[tokenID]['usd']

def getPCSV1(token):
    router = setPool(pcsRouter, Web3.toChecksumAddress('0x05ff2b0db69458a0750badebc4f9e13add608c7f'))
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')]).call()
    return from_wei(price[1])

def getPCSV2(token):
    router = setPool(pcs2Router, Web3.toChecksumAddress('0x10ED43C718714eb63d5aA57B78B54704E256024E'))
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')]).call()
    return from_wei(price[1])

def get_jet_swap(token):
    router = setPool(jetsRouter, Web3.toChecksumAddress('0xBe65b8f75B9F20f4C522e0067a3887FADa714800'))
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')]).call()
    return from_wei(price[1])

def get_bi_swap(token):
    router = setPool(biswap_router, Web3.toChecksumAddress('0x3a6d8cA21D1CF76F653A67577FA0D27453350dD8'))
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0x55d398326f99059fF775485246999027B3197955')]).call()
    return from_wei(price[1])

def get_firebird_swap(token):
    # router = setPool(firebird_abi, Web3.toChecksumAddress('0xF6fa9Ea1f64f1BBfA8d71f7f43fAF6D45520bfac'), 'matic')
    # price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063')]).call()
    r = requests.get('https://api.firebird.finance/api/coin-stat/hope')
    r = json.loads(r.text)

    # return from_wei(price[1])
    return r['data']['polygon']['price']

def get_four_belt():
    r = requests.get('https://s.belt.fi/status/A_beltTokenList.json')
    r = json.loads(r.text)
    price = [{x['address'] : x['price']} for x in r if x['address'] == '0x9cb73F20164e399958261c289Eb5F9846f4D1404']
    
    return price[0]

def get_crv_vp():
    price = Call('0x445FE580eF8d70FF569aB36e80c647af338db351', 'get_virtual_price()(uint256)', [['price', from_wei]], WEB3_NETWORKS['matic'])()
    return price['price']

def get_dnd_price(token_list):
    post_data = {"tokens": token_list}
    heads = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json;charset=UTF-8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1"
  }
    r = requests.post('https://api.iron.finance/token/info', headers=heads, data=json.dumps(post_data))

    return json.loads(r.text)

def getwSwap_matic(token):
        
    router = setPool(json.loads(wSwapABI), Web3.toChecksumAddress('0x3a1D87f206D12415f5b0A33E786967680AAb4f6d'), 'matic')
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063')]).call()
    return from_wei(price[1])

def get_poly_wault():
    r = requests.get('https://polyapi.wault.finance/realtimeData.js?ts=%s' % (round(time.time())))
    r = r.text[19:]
    r = json.loads(r)

    price_data = {'0x4c4bf319237d98a30a929a96112effa8da3510eb' : r['wexPrice'], '0x3053ad3b31600074e9A90440770f78D5e8Fc5A54'.lower() : r['waultxPrice']}
    return price_data

def ape_router_matic(token):
    router = setPool(pcsRouter, '0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607', 'matic')
    native_price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress('0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'), Web3.toChecksumAddress('0x2791bca1f2de4661ed88a30c99a7a9449aa84174')]).call()
    price = router.getAmountsOut(1 * 10 ** 18, [Web3.toChecksumAddress(token), Web3.toChecksumAddress('0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270')]).call()
    return from_custom(price[1], 18) * from_custom(native_price[1], 6)

def get_atricryptos_price(network=None, _id=None, out_decimal=None, input_types=None):

    if network is None:
        network = 'matic'

    if _id is None:
        _id = '0x751B1e21756bDbc307CBcC5085c042a0e9AaEf36'

    if out_decimal is None:
        out_decimal = 18
    
    if input_types is None:
        input_types = 'uint256,uint256'

    calls = []

    calls.append(Call(_id, [f'calc_withdraw_one_coin({input_types})(uint256)', 1000000000000000000, 0], [[f'token_price', from_custom, out_decimal]]))
    if network == 'matic':
        calls.append(Call('0x445fe580ef8d70ff569ab36e80c647af338db351', [f'get_virtual_price()(uint256)'], [[f'virtual_price', from_wei]]))

    stakes=Multicall(calls, WEB3_NETWORKS[network])()
    if 'virtual_price' in stakes:
        vp = stakes['virtual_price']
    else:
        vp = 1
    return stakes['token_price'] * vp

def get_blackswan_lp():
    x = [] 
    x.append(Call('0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46', [f'getReserves()((uint112,uint112))'], [[f'reserves', None]]))
    x.append(Call('0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46','totalSupply()(uint256)', [['totalSupply', from_wei]]))

    multi = Multicall(x,WEB3_NETWORKS['matic'])()
    userPct = 1 / multi['totalSupply']
    lpval = (userPct * multi['reserves'][0] / (10**6))

    return lpval

### eventHandler
def get_or_create_eventloop():
    #asyncio.set_event_loop_policy(aiogevent.EventLoopPolicy())
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def getWallet(wallet):
    headers = {'X-API-KEY': 'YBQYWtO5vkwOEuU1FTFUP2j5Mz0jMBwLe'}
    url = 'https://graphql.bitquery.io/'
    r = requests.post(url, json={'query': query, 'variables': variables % (wallet)}, headers=headers)
    
    if r.status_code == 200:
        response = json.loads(r.text)
        cleanData = response['data']['ethereum']['address'][0]['balances']
        wBalances = [x for x in cleanData if x['value'] > 0]
    else:
        raise Exception('Query failed and return code is {}'.format(r.status_code))

    tokens = []

    for d in wBalances:
        tokens += [{'token' : d['currency']['address'], 'decimal' : d['currency']['decimals']} ]

    # loop = get_or_create_eventloop()
    # future = asyncio.ensure_future(multiCallPrice(tokens))
    # prices = loop.run_until_complete(future)

    #prices = await multiCallPrice(tokens)

    prices = {x['token'] : x['price'] for x in prices}

    for i,token in enumerate(wBalances):
        wBalances[i]['totalAmount'] = token['value'] * prices[token['currency']['address']]

    grandTotal = sum(d['totalAmount'] for d in wBalances if d['totalAmount'] > 1)

    return wBalances, grandTotal

### Run From Flask
async def runFlask(selectedPools, wallet):

    ##Add Layered Farms

    ##BlueSwap
    if '0xb04381026F5D4AAf0487aC4336F16E133FA5FB0a' in selectedPools:
        selectedPools += ['0xBDd7E57634eEdAfBb61a12744dd249EBAB69CAB9', '0xbadb507006b72a94F3529e79B3F5a12e0E6A95F3']
    
    ##HyruleSwap
    if '0x76bd7145b99FDF84064A082BF86A33198C6e9D09' in selectedPools:
        selectedPools += ['0xd1b3d8ef5ac30a14690fbd05cf08905e1bf7d878']
    
    ##Sponge
    if '0x303961805A22d76Bac6B2dE0c33FEB746d82544B' in selectedPools:
        selectedPools += ['0xED955AE44A5632A0163B72e2f5e1474FB814034F']
    
    ##PolyCat
    if '0x4ce9Ae2f5983e19AebF5b8Bae4460f2B9EcE811a' in selectedPools:
        selectedPools += ['0xBdA1f897E851c7EF22CD490D2Cf2DAce4645A904']

    ##Iron Poly
    if '0x65430393358e55A658BcdE6FF69AB28cF1CbB77a' in selectedPools:
        selectedPools += ['0xb444d596273C66Ac269C33c30Fbb245F4ba8A79d', '0xa37DD1f62661EB18c338f18Cf797cff8b5102d8e']

    ##PolyWhale
    if '0x34bc3D36845d8A7cA6964261FbD28737d0d6510f' in selectedPools:
        selectedPools += ['0x0c23DCc118313ceB45a029CE0A4AB744eA4928ef']

    ##Tako
    if '0x4448336BA564bd620bE90d55078e397c26492a43' in selectedPools:
        selectedPools += ['0x8399B18A8f951a84e98366013EcE47F9bcb6D1f5']

    ##Tako Poly
    if '0xB19300246e19929a617C4260189f7B759597B8d8' in selectedPools:
        selectedPools += ['0xB19300246e19929a617C4260189f7B759597B8d8']
    
    ##SafeDollar Poly
    if '0x69E7Bbe85db0364397378364458952bEcB886920' in selectedPools:
        selectedPools += ['0x17684f4d5385FAc79e75CeafC93f22D90066eD5C', '0x029D14479B9497B95CeD7DE6DAbb023E31b4a1C3']

    ##PolyPup
    if '0xCc7E7c9FC775D25176e9Bfc5A400EdAc212aa81C' in selectedPools:
        selectedPools += ['0x9DcB2D5e7b5212fAF98e4a152827fd76bD55f68b']

    #KSwap
    if '0xaEBa5C691aF30b7108D9C277d6BB47347387Dc13' in selectedPools:
        selectedPools += ['0x5E6D7c01824C64C4BC7f2FF42C300871ce6Ff555','0x1FcCEabCd2dDaDEa61Ae30a2f1c2D67A05fDDa29']

    #JSwap
    if '0x83C35EA2C32293aFb24aeB62a14fFE920C2259ab' in selectedPools:
        selectedPools += ['0x4e864E36Bb552BD1Bf7bcB71A25d8c96536Af7e3', '0x0B29065f0C5B9Db719f180149F0251598Df2F1e4']


    poolLen = await getPoolLengths(selectedPools, wallet)
    #print(poolLen)
    stakes = await getOnlyStaked(poolLen, wallet)
    #print(stakes)
    pendingWants = await getPendingWant(stakes, wallet)

    
    if '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A' in selectedPools:
        eleNRV = getElevenNerve(wallet)
        
        if eleNRV is not None:
            pendingWants[0].update(eleNRV[0])
            pendingWants[1]['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'].update(eleNRV[1]['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'])
    
    if '0xHorizon' in selectedPools:
        horizon = getHorizonStakes(wallet)
        pendingWants[0].update(horizon[0])
        pendingWants[1]['0xHorizon']['userData'].update(horizon[1]['0xHorizon']['userData'])

    if '0xIronFinance' in selectedPools:
        iron = getIronFinance(wallet, get_iron_vaults(), '0xIronFinance', WEB3_NETWORKS['bsc'])
        if iron is not None:
            pendingWants[0].update(iron[0])
            pendingWants[1]['0xIronFinance']['userData'].update(iron[1]['0xIronFinance']['userData'])

    if '0xDiamondHands' in selectedPools:
        diamond = getDiamondHands(wallet)
        if diamond is not None:
            pendingWants[0].update(diamond[0])
            pendingWants[1]['0xDiamondHands']['userData'].update(diamond[1]['0xDiamondHands']['userData'])

    if '0xd56339F80586c08B7a4E3a68678d16D37237Bd96' in selectedPools:
        vSafe = getValueSafes(wallet)
        if vSafe is not None:
            pendingWants[0].update(vSafe[0])
            pendingWants[1]['0xd56339F80586c08B7a4E3a68678d16D37237Bd96']['userData'].update(vSafe[1]['0xd56339F80586c08B7a4E3a68678d16D37237Bd96']['userData'])
    
    if '0xE9a8b6ea3e7431E6BefCa51258CB472Df2Dd21d4' in selectedPools:
        firebird_ext = get_user_firebird_vaults(wallet)
        if firebird_ext is not None:
            pendingWants[0].update(firebird_ext[0])
            pendingWants[1]['0xE9a8b6ea3e7431E6BefCa51258CB472Df2Dd21d4']['userData'].update(firebird_ext[1]['0xE9a8b6ea3e7431E6BefCa51258CB472Df2Dd21d4']['userData'])

    if '0xPancakeBunny' in selectedPools:
        bunny_bsc = get_pancake_bunny_clones(wallet, get_pancakebunny_pools('bsc'), 'bsc', '0xb3c96d3c3d643c2318e4cdd0a9a48af53131f5f4', '0xf5bf8a9249e3cc4cb684e3f23db9669323d4fb7d', '0xPancakeBunny', 'BUNNY', 'ten')

        if bunny_bsc is not None:
            pendingWants[0].update(bunny_bsc[0])
            pendingWants[1]['0xPancakeBunny']['userData'].update(bunny_bsc[1]['0xPancakeBunny']['userData'])

    if '0xMerlin' in selectedPools:
        merlins = getMerlinPools(wallet)
        if merlins is not None:
            pendingWants[0].update(merlins[0])
            pendingWants[1]['0xMerlin']['userData'].update(merlins[1]['0xMerlin']['userData'])

    if '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A' in selectedPools:
        elevens = get_eleven_hodls(wallet, get_ele_tokens())
        if elevens is not None:
            pendingWants[0].update(elevens[0])
            pendingWants[1]['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'].update(elevens[1]['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A']['userData'])

        farm_id = '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A'
        
        extension = get_vault_style_no_want(wallet,['0x3Ed531BfB3FAD41111f6dab567b33C4db897f991'],'0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', WEB3_NETWORKS['bsc'], 'tokensPerShare', want_token='0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0', pps_decimal=12)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56' in selectedPools:
        jetMultipler = getJetValue()
        jetFuels = getFuelVaults(wallet)
        if jetFuels is not None:
            pendingWants[0].update(jetFuels[0])
            pendingWants[1]['0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56']['userData'].update(jetFuels[1]['0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56']['userData'])

    if '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D' in selectedPools:
        farm_id = '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D'
        waulton = getWaultLocked(wallet)
        if waulton is not None:
            pendingWants[0].update(waulton[0])
            pendingWants[1]['0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D']['userData'].update(waulton[1]['0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D']['userData'])

        extension = get_syrup_pools(wallet,get_wault_pool_contracts(),'bsc', '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D',staked='pool',pending_reward='pendingRewards')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xe87DE2d5BbB4aF23c665Cf7331eC744B020883bB' in selectedPools:
        apo = getApoyield(wallet)
        if apo is not None:
            pendingWants[0].update(apo[0])
            pendingWants[1]['0xe87DE2d5BbB4aF23c665Cf7331eC744B020883bB']['userData'].update(apo[1]['0xe87DE2d5BbB4aF23c665Cf7331eC744B020883bB']['userData'])      

    if '0xGambit' in selectedPools:
        gam = getGambits(wallet)
        if gam is not None:
            pendingWants[0].update(gam[0])
            pendingWants[1]['0xGambit']['userData'].update(gam[1]['0xGambit']['userData'])

    if '0xSquirrel' in selectedPools:
        sql = get_nuts(wallet)
        if sql is not None:
            pendingWants[0].update(sql[0])
            pendingWants[1]['0xSquirrel']['userData'].update(sql[1]['0xSquirrel']['userData'])
    
    if '0xAdamant' in selectedPools:
        addy = get_adamant_funds(wallet)
        if addy is not None:
            pendingWants[0].update(addy[0])
            pendingWants[1]['0xAdamant']['userData'].update(addy[1]['0xAdamant']['userData'])
        
        addy_staking = get_adamant_stakes(wallet, '0xAdamant')
        if addy_staking is not None:
            pendingWants[0].update(addy_staking[0])
            pendingWants[1]['0xAdamant']['userData'].update(addy_staking[1]['0xAdamant']['userData'])

    if '0xAcryptos' in selectedPools:
        acrypt_vaults = get_acryptos_vaults()

        acryptos = get_vault_style(wallet, acrypt_vaults, '0xAcryptos', WEB3_NETWORKS['bsc'], 'getPricePerFullShare')

        if acryptos is not None:
            pendingWants[0].update(acryptos[0])
            pendingWants[1]['0xAcryptos']['userData'].update(acryptos[1]['0xAcryptos']['userData'])

        acryptos = get_acryptos_style_boosts(wallet,get_acryptos_vaults(),'0xAcryptos',WEB3_NETWORKS['bsc'],'0xb1fa5d3c0111d8E9ac43A19ef17b281D5D4b474E', 'pendingSushi')
        
        if acryptos is not None:
            pendingWants[0].update(acryptos[0])
            pendingWants[1]['0xAcryptos']['userData'].update(acryptos[1]['0xAcryptos']['userData']) 

    if '0xFortress' in selectedPools:
        fort = getFortress(wallet)
        if fort is not None:
            #print(fort[1])
            pendingWants[0].update(fort[0])
            pendingWants[1]['0xFortress']['userData'].update(fort[1]['0xFortress']['userData'])

    if '0xDYP' in selectedPools:
        dyps = getDYP(wallet)
        if dyps is not None:
            #print(fort[1])
            pendingWants[0].update(dyps[0])
            pendingWants[1]['0xDYP']['userData'].update(dyps[1]['0xDYP']['userData'])

    if '0xQuickSwap' in selectedPools:
        qs_stakes = get_quickswap_style(wallet, qs_vaults, '0xQuickSwap', WEB3_NETWORKS['matic'])
        
        if qs_stakes is not None:
            pendingWants[0].update(qs_stakes[0])
            pendingWants[1]['0xQuickSwap']['userData'].update(qs_stakes[1]['0xQuickSwap']['userData'])

        qs_lps = get_quickswap_lps(wallet,'0xQuickSwap')
        
        if qs_lps is not None:
            pendingWants[0].update(qs_lps[0])
            pendingWants[1]['0xQuickSwap']['userData'].update(qs_lps[1]['0xQuickSwap']['userData'])

    if '0xDFYN' in selectedPools:
        dfyn_stakes = get_quickswap_style(wallet, dfyn_regular, '0xDFYN', WEB3_NETWORKS['matic'])
        dfyn_duals = get_quickswap_style_multi(wallet, dfyn_dual_vaults, '0xDFYN', WEB3_NETWORKS['matic'])
        
        if dfyn_stakes is not None:
            pendingWants[0].update(dfyn_stakes[0])
            pendingWants[1]['0xDFYN']['userData'].update(dfyn_stakes[1]['0xDFYN']['userData'])
        
        if dfyn_duals is not None:
            pendingWants[0].update(dfyn_duals[0])
            pendingWants[1]['0xDFYN']['userData'].update(dfyn_duals[1]['0xDFYN']['userData'])

    if '0xTaodao' in selectedPools:
        tao = getTaoDao(wallet)
        if tao is not None:
            pendingWants[0].update(tao[0])
            pendingWants[1]['0xTaodao']['userData'].update(tao[1]['0xTaodao']['userData'])

    if '0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0' in selectedPools:
        pop = getPop(wallet)
        if pop is not None:
            pendingWants[0].update(pop[0])
            pendingWants[1]['0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0']['userData'].update(pop[1]['0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0']['userData'])

    if '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' in selectedPools:
        bingoBoard = getbingoBoard(wallet)
        if bingoBoard is not None:
            pendingWants[0].update(bingoBoard[0])
            pendingWants[1]['0x97bdB4071396B7f60b65E0EB62CE212a699F4B08']['userData'].update(bingoBoard[1]['0x97bdB4071396B7f60b65E0EB62CE212a699F4B08']['userData'])
    
    if '0xBeefy' in selectedPools:
        beeflp = requests.get('https://api.beefy.finance/lps')
        beefsingle = requests.get('https://api.beefy.finance/prices')

        beefyPrices = { **json.loads(beeflp.text), **json.loads(beefsingle.text) }
        boosted = getBeefyBoosts(wallet)

        if boosted is not None:
            pendingWants[0].update(boosted[0])
            pendingWants[1]['0xBeefy']['userData'].update(boosted[1]['0xBeefy']['userData'])

    if '0xBeefyMatic' in selectedPools:
        beefy_matic = get_beefy_matic_stakes(wallet)
        
        if beefy_matic is not None:
            pendingWants[0].update(beefy_matic[0])
            pendingWants[1]['0xBeefyMatic']['userData'].update(beefy_matic[1]['0xBeefyMatic']['userData'])

        farm_id = '0xBeefyMatic'
        extension = get_fh_pools(wallet, get_beefy_boosts_poly(), 'matic', '0xBeefyMatic', stake_func='stakedToken')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xBeefyFantom' in selectedPools:
        beefy_fantom = get_beefy_style_stakes(wallet,get_beefy_fantom_pools(),'0xBeefyFantom','ftm')
        
        if beefy_fantom is not None:
            pendingWants[0].update(beefy_fantom[0])
            pendingWants[1]['0xBeefyFantom']['userData'].update(beefy_fantom[1]['0xBeefyFantom']['userData'])

    if '0xBeefyAVAX' in selectedPools:
        beefy_avax = get_beefy_style_stakes(wallet,get_beefy_avax_pools(),'0xBeefyAVAX','avax')
        
        if beefy_avax is not None:
            pendingWants[0].update(beefy_avax[0])
            pendingWants[1]['0xBeefyAVAX']['userData'].update(beefy_avax[1]['0xBeefyAVAX']['userData'])

    if '0xD109D9d6f258D48899D7D16549B89122B0536729' in selectedPools:
        
        farm_id = '0xD109D9d6f258D48899D7D16549B89122B0536729'
        
        eleven_polygon = get_eleven_hodls_polygon(wallet, get_ele_tokens())

        
        if eleven_polygon is not None:
            pendingWants[0].update(eleven_polygon[0])
            pendingWants[1]['0xD109D9d6f258D48899D7D16549B89122B0536729']['userData'].update(eleven_polygon[1]['0xD109D9d6f258D48899D7D16549B89122B0536729']['userData'])

        extension = get_vault_style_no_want(wallet,['0x0FFb84A4c29147Bd745AAe0330f4F6f4Cb716c92'],'0xD109D9d6f258D48899D7D16549B89122B0536729', WEB3_NETWORKS['matic'], 'tokensPerShare', want_token='0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0', pps_decimal=12)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x6275518a63e891b1bC54FEEBBb5333776E32fAbD' in selectedPools:
        kogevaults = get_vault_style(wallet, ast.literal_eval(pull_koge_vaults()), '0x6275518a63e891b1bC54FEEBBb5333776E32fAbD', WEB3_NETWORKS['matic'])
        if kogevaults is not None:
            pendingWants[0].update(kogevaults[0])
            pendingWants[1]['0x6275518a63e891b1bC54FEEBBb5333776E32fAbD']['userData'].update(kogevaults[1]['0x6275518a63e891b1bC54FEEBBb5333776E32fAbD']['userData'])

    if '0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d' in selectedPools:
        polycrystal = get_vault_style(wallet, ['0x5BaDd6C71fFD0Da6E4C7D425797f130684D057dd'], '0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d', WEB3_NETWORKS['matic'], 'getPricePerFullShare', 'userInfo')
        if polycrystal is not None:
            pendingWants[0].update(polycrystal[0])
            pendingWants[1]['0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d']['userData'].update(polycrystal[1]['0xeBCC84D2A73f0c9E23066089C6C24F4629Ef1e6d']['userData'])

    if '0x4F1818Ff649498a2441aE1AD29ccF55a8E1C6250' in selectedPools:
        hyperjumps = get_vault_style(wallet, hyperjump_vault_list, '0x4F1818Ff649498a2441aE1AD29ccF55a8E1C6250', WEB3_NETWORKS['bsc'], 'getPricePerFullShare')
        if hyperjumps is not None:
            pendingWants[0].update(hyperjumps[0])
            pendingWants[1]['0x4F1818Ff649498a2441aE1AD29ccF55a8E1C6250']['userData'].update(hyperjumps[1]['0x4F1818Ff649498a2441aE1AD29ccF55a8E1C6250']['userData'])

    if '0x90Df158ff7c31aD1d81ddDb1D8ab9d0eCBCeDa20' in selectedPools:
        hyperjumps = get_vault_style(wallet, [x['earnedTokenAddress'] for x in get_hyperjump_vaults_ftm()], '0x90Df158ff7c31aD1d81ddDb1D8ab9d0eCBCeDa20', WEB3_NETWORKS['ftm'], 'getPricePerFullShare')
        if hyperjumps is not None:
            pendingWants[0].update(hyperjumps[0])
            pendingWants[1]['0x90Df158ff7c31aD1d81ddDb1D8ab9d0eCBCeDa20']['userData'].update(hyperjumps[1]['0x90Df158ff7c31aD1d81ddDb1D8ab9d0eCBCeDa20']['userData'])

    if '0xAutoShark' in selectedPools:
        sharks = get_pancake_bunny_clones(wallet, get_autoshark_vaults('bsc'), 'bsc', '0xa5251abdb5218699F09360DF17967C0e2ffA6655', '0x41B471F347a7C2C8e6cb7F4F59C570C6D9c69a3C', '0xAutoShark', 'JAWS')

        if sharks is not None:
            pendingWants[0].update(sharks[0])
            pendingWants[1]['0xAutoShark']['userData'].update(sharks[1]['0xAutoShark']['userData'])

    if '0xAutoSharkMatic' in selectedPools:
        sharks = get_pancake_bunny_clones(wallet, get_autoshark_vaults('poly'), 'matic', '0xA96CeA606D206310e4ffaa65577D316D49043cDF', '0xd9bAfd0024d931D103289721De0D43077e7c2B49', '0xAutoSharkMatic', 'JAWS')

        if sharks is not None:
            pendingWants[0].update(sharks[0])
            pendingWants[1]['0xAutoSharkMatic']['userData'].update(sharks[1]['0xAutoSharkMatic']['userData'])

    if '0xPancakeBunnyMatic' in selectedPools:
        bunny_matic = get_pancake_bunny_clones(wallet, get_pancakebunny_pools('matic'), 'matic','0xFA71FD547A6654b80c47DC0CE16EA46cECf93C02', '0xe3b11c3bd6d90cfebbb4fb9d59486b0381d38021', '0xPancakeBunnyMatic', 'polyBUNNY', 'ten')

        if bunny_matic is not None:
            pendingWants[0].update(bunny_matic[0])
            pendingWants[1]['0xPancakeBunnyMatic']['userData'].update(bunny_matic[1]['0xPancakeBunnyMatic']['userData'])

    if '0xApeRocket' in selectedPools:
        aperock = get_pancake_bunny_clones(wallet, get_aperocket_vaults(), 'bsc', '0xe64AA77B1719eFf35D6740cB99200a193B8d6c97', '0x5D6086f8aae9DaEBAC5674E8F3b867D5743171D3', '0xApeRocket', 'SPACE')

        if aperock is not None:
            pendingWants[0].update(aperock[0])
            pendingWants[1]['0xApeRocket']['userData'].update(aperock[1]['0xApeRocket']['userData'])

        spacepool = get_aperocket_space_pool(wallet,['0xd79dc49Ed716832658ec28FE93dd733e0DFB8d58'],{'token' : '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c', 'symbol' : 'WBNB', 'decimal' : 18}, 'bsc', '0xApeRocket', 2)

        if spacepool is not None:
            pendingWants[0].update(spacepool[0])
            pendingWants[1]['0xApeRocket']['userData'].update(spacepool[1]['0xApeRocket']['userData'])

    if '0xApeRocketMatic' in selectedPools:
        aperock = get_pancake_bunny_clones(wallet, get_aperocket_vaults_matic(), 'matic', '0x6e44fe8d084734cE65DF0d458ACAaB3C20c95937', '0xBE53cB783ff5d63979De124924960e2F193625B2', '0xApeRocketMatic', 'pSPACE')

        if aperock is not None:
            pendingWants[0].update(aperock[0])
            pendingWants[1]['0xApeRocketMatic']['userData'].update(aperock[1]['0xApeRocketMatic']['userData'])

        spacepool = get_aperocket_space_pool(wallet,['0xBa56A30ec2Ee2B4C3c7EE75e0CFEbcD1b22dE8cd'],{'token' : '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619', 'symbol' : 'WETH', 'decimal' : 18}, 'matic', '0xApeRocketMatic', 2)

        if spacepool is not None:
            pendingWants[0].update(spacepool[0])
            pendingWants[1]['0xApeRocketMatic']['userData'].update(spacepool[1]['0xApeRocketMatic']['userData'])

    if '0xApeSwapMatic' in selectedPools:
        apeswaps = get_apeswap(wallet, '0xApeSwapMatic', 'matic')

        if apeswaps is not None:
            pendingWants[0].update(apeswaps[0])
            pendingWants[1]['0xApeSwapMatic']['userData'].update(apeswaps[1]['0xApeSwapMatic']['userData'])

    if '0xBalancer' in selectedPools:
        user_balancer = get_balancer_user_pools(wallet, get_balancer_pools(), 'matic', '0xBalancer')

        if user_balancer is not None:
            pendingWants[0].update(user_balancer[0])
            pendingWants[1]['0xBalancer']['userData'].update(user_balancer[1]['0xBalancer']['userData'])

    if '0x2DC11B394BD0f1CC6AC0a269cfe3CC0b333601B4' in selectedPools:
        apolyyeld = get_vault_style(wallet, ['0xc49bc7118a73Ca6CB36Bfa454FD40eCAE079a463'], '0x2DC11B394BD0f1CC6AC0a269cfe3CC0b333601B4', WEB3_NETWORKS['matic'], 'getPricePerFullShare', 'userInfo')
        if apolyyeld is not None:
            pendingWants[0].update(apolyyeld[0])
            pendingWants[1]['0x2DC11B394BD0f1CC6AC0a269cfe3CC0b333601B4']['userData'].update(apolyyeld[1]['0x2DC11B394BD0f1CC6AC0a269cfe3CC0b333601B4']['userData'])

    if '0x058451C62B96c594aD984370eDA8B6FD7197bbd4' in selectedPools:
        panther_jungles = ['0x3B5Ed7B0F8bf5D2b485352e15A416092Ca741C2c', '0xf31cbe0b2bb2e704310c90a6f74300b3d4627ce8', '0x85ff09374D1f59288b6978EB9254377a51BE0B7c']
        jungles = get_syrup_pools(wallet, panther_jungles, 'bsc', '0x058451C62B96c594aD984370eDA8B6FD7197bbd4')

        if jungles is not None:
            pendingWants[0].update(jungles[0])
            pendingWants[1]['0x058451C62B96c594aD984370eDA8B6FD7197bbd4']['userData'].update(jungles[1]['0x058451C62B96c594aD984370eDA8B6FD7197bbd4']['userData'])       

    if '0xf6E62b59DbD8C8395321F886bd06eCf04f57C088' in selectedPools:
        stables = get_single_masterchef(wallet, '0xf6E62b59DbD8C8395321F886bd06eCf04f57C088', 'bsc', farms['0xbb131Ee18cbBEf03bB554F935F9FECed65B67488'])

        if stables is not None:
            pendingWants[0].update(stables[0])
            pendingWants[1]['0xf6E62b59DbD8C8395321F886bd06eCf04f57C088']['userData'].update(stables[1]['0xf6E62b59DbD8C8395321F886bd06eCf04f57C088']['userData'])

    if '0xIronPoly' in selectedPools:
        stables = get_single_masterchef(wallet, '0xIronPoly', 'matic', farms['0x1fD1259Fa8CdC60c6E8C86cfA592CA1b8403DFaD'])

        if stables is not None:
            pendingWants[0].update(stables[0])
            pendingWants[1]['0xIronPoly']['userData'].update(stables[1]['0xIronPoly']['userData'])      

    if '0xF4168CD3C00799bEeB9a88a6bF725eB84f5d41b7' in selectedPools:
        thor = get_syrup_pools(wallet,thunder_pools,'bsc','0xF4168CD3C00799bEeB9a88a6bF725eB84f5d41b7')

        if thor is not None:
            pendingWants[0].update(thor[0])
            pendingWants[1]['0xF4168CD3C00799bEeB9a88a6bF725eB84f5d41b7']['userData'].update(thor[1]['0xF4168CD3C00799bEeB9a88a6bF725eB84f5d41b7']['userData'])      

    if '0xPYQ' in selectedPools:

        pyq_trove = get_pyq_trove(wallet, ['0xA2A065DBCBAE680DF2E6bfB7E5E41F1f1710e63b'], '0xPYQ', 'matic')

        if pyq_trove is not None:
            pendingWants[0].update(pyq_trove[0])
            pendingWants[1]['0xPYQ']['userData'].update(pyq_trove[1]['0xPYQ']['userData'])

        pyq_stake = get_pyq_triple_staking(wallet, ['0xf2F4326E96cCC834216A7F95b96BD51239880048'], '0xPYQ', 'matic')

        if pyq_stake is not None:
            pendingWants[0].update(pyq_stake[0])
            pendingWants[1]['0xPYQ']['userData'].update(pyq_stake[1]['0xPYQ']['userData'])

        pyq_stake = get_pyq_double_staking(wallet, ['0x445098d74B6eB4f3BCF20865989b777ee405a48C'], '0xPYQ', 'matic')

        if pyq_stake is not None:
            pendingWants[0].update(pyq_stake[0])
            pendingWants[1]['0xPYQ']['userData'].update(pyq_stake[1]['0xPYQ']['userData'])
        
        pyq_farms = get_quickswap_style(wallet, pyq_farm_list, '0xPYQ', WEB3_NETWORKS['matic'], 'uniToken')

        if pyq_farms is not None:
            pendingWants[0].update(pyq_farms[0])
            pendingWants[1]['0xPYQ']['userData'].update(pyq_farms[1]['0xPYQ']['userData'])

    if '0x574Fe4E8120C4Da1741b5Fd45584de7A5b521F0F' in selectedPools:
        mai_vault = get_mai_cvault(wallet, '0x574Fe4E8120C4Da1741b5Fd45584de7A5b521F0F')

        if mai_vault is not None:
            pendingWants[0].update(mai_vault[0])
            pendingWants[1]['0x574Fe4E8120C4Da1741b5Fd45584de7A5b521F0F']['userData'].update(mai_vault[1]['0x574Fe4E8120C4Da1741b5Fd45584de7A5b521F0F']['userData'])      

    if '0xC8Bd86E5a132Ac0bf10134e270De06A8Ba317BFe' in selectedPools:
        wault_poly_pools = get_wault_pools(wallet,['0x33f7FC6cf0E6878B59232F7CC30f8A62d1831274'],'matic','0xC8Bd86E5a132Ac0bf10134e270De06A8Ba317BFe')

        if wault_poly_pools is not None:
            pendingWants[0].update(wault_poly_pools[0])
            pendingWants[1]['0xC8Bd86E5a132Ac0bf10134e270De06A8Ba317BFe']['userData'].update(wault_poly_pools[1]['0xC8Bd86E5a132Ac0bf10134e270De06A8Ba317BFe']['userData'])

    if '0x8e5860DF653A467D1cC5b6160Dd340E8D475724E' in selectedPools:
        farm_hero_vested = get_farmhero_staking(wallet,farmhero.matic_staking,'matic','0x8e5860DF653A467D1cC5b6160Dd340E8D475724E')

        if farm_hero_vested is not None:
            pendingWants[0].update(farm_hero_vested[0])
            pendingWants[1]['0x8e5860DF653A467D1cC5b6160Dd340E8D475724E']['userData'].update(farm_hero_vested[1]['0x8e5860DF653A467D1cC5b6160Dd340E8D475724E']['userData']) 

        farm_hero_pools = get_fh_pools(wallet,farmhero.matic_pools,'matic','0x8e5860DF653A467D1cC5b6160Dd340E8D475724E')

        if farm_hero_pools is not None:
            pendingWants[0].update(farm_hero_pools[0])
            pendingWants[1]['0x8e5860DF653A467D1cC5b6160Dd340E8D475724E']['userData'].update(farm_hero_pools[1]['0x8e5860DF653A467D1cC5b6160Dd340E8D475724E']['userData']) 

    if '0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D' in selectedPools:
        farm_hero_vested = get_farmhero_staking(wallet,farmhero.bsc_staking,'bsc','0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D')

        if farm_hero_vested is not None:
            pendingWants[0].update(farm_hero_vested[0])
            pendingWants[1]['0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D']['userData'].update(farm_hero_vested[1]['0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D']['userData']) 

        farm_hero_pools = get_fh_pools(wallet,farmhero.bsc_pools,'bsc','0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D')

        if farm_hero_pools is not None:
            pendingWants[0].update(farm_hero_pools[0])
            pendingWants[1]['0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D']['userData'].update(farm_hero_pools[1]['0xDAD01f1d99191a2eCb78FA9a007604cEB8993B2D']['userData'])

    if '0xDb457E7fA88C9818f6134afD673941fCE777F92F' in selectedPools:
        farm_hero_vested = get_farmhero_staking(wallet,farmhero.oke_staking,'oke','0xDb457E7fA88C9818f6134afD673941fCE777F92F')

        if farm_hero_vested is not None:
            pendingWants[0].update(farm_hero_vested[0])
            pendingWants[1]['0xDb457E7fA88C9818f6134afD673941fCE777F92F']['userData'].update(farm_hero_vested[1]['0xDb457E7fA88C9818f6134afD673941fCE777F92F']['userData']) 

        farm_hero_pools = get_fh_pools(wallet,farmhero.oke_pools,'oke','0xDb457E7fA88C9818f6134afD673941fCE777F92F')

        if farm_hero_pools is not None:
            pendingWants[0].update(farm_hero_pools[0])
            pendingWants[1]['0xDb457E7fA88C9818f6134afD673941fCE777F92F']['userData'].update(farm_hero_pools[1]['0xDb457E7fA88C9818f6134afD673941fCE777F92F']['userData'])  

    if '0x0d17C30aFBD4d29EEF3639c7B1F009Fd6C9f1F72' in selectedPools:
        farm_id = '0x0d17C30aFBD4d29EEF3639c7B1F009Fd6C9f1F72'
        extension = get_vault_style(wallet,evm.poolext.boneswap.vaults,farm_id,WEB3_NETWORKS['matic'],'getPricePerFullShare','userInfo')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,evm.poolext.boneswap.pools,'matic',farm_id,'stakeToken')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])  

    if '0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9' in selectedPools:
        farm_id = '0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9'
        ape_pools = get_apeswap_pools()
        extension = get_syrup_pools(wallet,ape_pools[0],'bsc','0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9','stakeToken')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,ape_pools[1],'bsc','0x5c8D727b265DBAfaba67E050f2f739cAeEB4A6F9','STAKE_TOKEN','REWARD_TOKEN')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x73feaa1ee314f8c655e354234017be2193c9e24e' in selectedPools:
        farm_id = '0x73feaa1ee314f8c655e354234017be2193c9e24e'
        cake_pools = get_pcs_pools()
        extension = get_syrup_pools(wallet,cake_pools[0],'bsc',farm_id)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,cake_pools[1],'bsc','0x73feaa1ee314f8c655e354234017be2193c9e24e','syrup')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_vault_style(wallet,['0xa80240Eb5d7E05d3F250cF000eEc0891d00b51CC'],'0x73feaa1ee314f8c655e354234017be2193c9e24e',WEB3_NETWORKS['bsc'], 'getPricePerFullShare', 'userInfo')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xPickle' in selectedPools:
        farm_id = '0xPickle'

        extension = get_pickle_chef(wallet,farm_id,'matic','0x20B2a3fc7B13cA0cCf7AF81A68a14CB3116E8749','0xE28287544005094be096301E5eE6E2A6E6Ef5749')


        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_vault_style(wallet,get_pickle_addresses('polygon'),farm_id,WEB3_NETWORKS['matic'])

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xCurvePolygon' in selectedPools:
        farm_id = '0xCurvePolygon'

        extension = get_curve_gauage(wallet,'0xCurvePolygon','matic', evm.poolext.curve.polygon_gauges)


        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xCurveFTM' in selectedPools:
        farm_id = '0xCurveFTM'

        extension = get_curve_gauage(wallet,'0xCurveFTM','ftm', evm.poolext.curve.ftm_gauges, ['0x1E4F97b9f9F913c46F1632781732927B9019C68b'])


        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xTelx' in selectedPools:
        farm_id = '0xTelx'

        extension = get_telx_single(wallet,'0xTelx','matic',telx.single)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_telx_double(wallet,'0xTelx','matic',telx.double)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xHarvester' in selectedPools:
        farm_id = '0xHarvester'

        extension = get_single_masterchef(wallet, '0xHarvester', 'matic', farms['0xb49036Fb35b4E1572509f301e1b0fd0113771ffa'])

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xBlackSwan' in selectedPools:
        farm_id = '0xBlackSwan'

        extension = get_blackswan_stakes(wallet)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x6CB1Cdbae9a20413e37aF1491507cd5faE2DdD3e' in selectedPools:
        farm_id = '0x6CB1Cdbae9a20413e37aF1491507cd5faE2DdD3e'

        extension = get_single_masterchef(wallet, farm_id, 'bsc', farms['0x2937c747Bc64B9E4DeBe5E7A4bA9bEAE33B91126'])

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,['0x8052D595E75c2E6e452bd2302aa1E66eAdBE2b42','0xDbd85332d6f6Edd1b66ba0594355aAAA140c1F07', '0x5e5964dfcbe523387cb86f7fbd283f64acd6c21a'],'bsc',farm_id,staked='stakeToken',reward='rewardToken',pending_reward='pendingReward')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xPaprBSC' in selectedPools:
        farm_id = '0xPaprBSC'

        extension = get_vault_style(wallet,get_paprprintr_vaults(56),'0xPaprBSC', WEB3_NETWORKS['bsc'], 'getPricePerFullShare', _strict=True)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,papr.bsc_natives+papr.bsc_pools,'bsc','0xPaprBSC','trustedDepositTokenAddress','trustedRewardTokenAddress','getEstimatedPendingDivs', 'depositedTokens')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,papr.bsc_printer,'bsc','0xPaprBSC','share','cash','earned', 'balanceOf')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xPaprMatic' in selectedPools:
        farm_id = '0xPaprMatic'

        extension = get_vault_style(wallet,get_paprprintr_vaults(137),'0xPaprMatic', WEB3_NETWORKS['matic'], 'getPricePerFullShare', _strict=True)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,papr.matic_natives,'matic',farm_id,'trustedDepositTokenAddress','trustedRewardTokenAddress','getEstimatedPendingDivs', 'depositedTokens')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,papr.matic_printer,'matic',farm_id,'share','cash','earned', 'balanceOf')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xPaprKCC' in selectedPools:
        farm_id = '0xPaprKCC'

        extension = get_vault_style(wallet,get_paprprintr_vaults(321),'0xPaprKCC', WEB3_NETWORKS['kcc'], 'getPricePerFullShare', _strict=True)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x1948abC5400Aa1d72223882958Da3bec643fb4E5' in selectedPools:
        farm_id = '0x1948abC5400Aa1d72223882958Da3bec643fb4E5'
        
        extension = get_syrup_pools(wallet,dino.pools,'matic',farm_id,'DINO','REWARD','pendingReward')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xUniswapETH' in selectedPools:
        farm_id = '0xUniswapETH'
        
        extension = uniswapv3.get_uniswap_v3_positions(wallet,'eth','0xc36442b4a4522e871399cd717abdd847ab11fe88','0x1F98431c8aD98523631AE4a59f267346ea31F984', farm_id)
        
        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xSuperFarm' in selectedPools:
        farm_id = '0xSuperFarm'
        
        extension = get_syrup_pools(wallet,get_superfarm_pools(),'bsc','0xSuperFarm','_inToken','_rewardToken','pendingReward','_userInfo')

        
        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,['0x8C73dC245D2626311dD28319793893460B358F3c'],'bsc','0xSuperFarm','STAKED_TOKEN','REWARD_TOKEN','getTotalRewardsBalance','balanceOf')
        
        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xPandaSwap' in selectedPools:
        farm_id = '0xPandaSwap'
        
        extension =  get_syrup_pools(wallet,pandaswap.farms,'oke',farm_id,'lpt','sharetoken','earned','balanceOf')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xd90A8878a2277879600AA2cba0CADC7E1a11354D' in selectedPools:
        farm_id = '0xd90A8878a2277879600AA2cba0CADC7E1a11354D'
        
        extension =  get_feeder_style(wallet,feeder.auto_staking,'bsc','0xd90A8878a2277879600AA2cba0CADC7E1a11354D')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension =  get_sfeed(wallet,['0x67d66e8Ec1Fd25d98B3Ccd3B19B7dc4b4b7fC493'],'0xEb9902A19Fa1286c8832bF44e9B18E89f682f614','bsc',farm_id)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78' in selectedPools:
        farm_id = '0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78'
        
        extension =  get_syrup_pools(wallet,polygonfarm.pools,'matic','0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78','poolInfo','rewardToken','pendingReward','userInfo')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_vault_style(wallet,['0x8e6C2827d234b16C3B496deD77a0f6b7e3Cf27ee'],'0x9A2C85eFBbE4DD93cc9a9c925Cea4A2b59c0db78',WEB3_NETWORKS['matic'], 'getPricePerFullShare', 'userInfo')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xdA30Aae916417C9Ad8DE97Bb1d59395f2Dd905e4' in selectedPools:
        farm_id = '0xdA30Aae916417C9Ad8DE97Bb1d59395f2Dd905e4'
        
        extension = get_vault_style(wallet,['0xdcfd912b50904B4d5745DfFe0D4d7a5097c82849'],farm_id,WEB3_NETWORKS['matic'], 'getPricePerFullShare', 'userInfo')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xIronLend' in selectedPools:
        farm_id = '0xIronLend'
        
        extension = get_lending_protocol(wallet,ironlend.vaults,'0xIronLend','matic')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])


        extension = get_just_pending(wallet,['0x942D581a01887B4CB45B2EAA64E2bD6D50D1f99A'],'matic','0xIronLend','calculateReward','0x4A81f8796e0c6Ad4877A51C86693B0dE8093F2ef')

    if '0xBenqi' in selectedPools:
        farm_id = '0xBenqi'
        
        extension = get_lending_protocol(wallet,benqi.vaults,'0xBenqi','avax')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xElevenOKE' in selectedPools:
        farm_id = '0xElevenOKE'
        
        extension = get_vault_style(wallet, get_ele_tokens('okexchain'), '0xElevenOKE', WEB3_NETWORKS['oke'], 'getPricePerFullShare')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xRugZombie' in selectedPools:
        farm_id = '0xRugZombie'

        extension = get_zombie_masterchef(wallet, '0xRugZombie', 'bsc', '0x590Ea7699A4E9EaD728F975efC573f6E34a5dC7B')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

        extension = get_syrup_pools(wallet,rugzombie.pools,'bsc',farm_id)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x29e6b6acb00ef1cdfebdc5a2d3731f791b85b207' in selectedPools:
        farm_id = '0x29e6b6acb00ef1cdfebdc5a2d3731f791b85b207'

        extension = get_syrup_pools(wallet,['0xd38cE88CAf05FFDb193Ba95fce552c5129E42C89'],'bsc',farm_id)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x8A4f4c7F4804D30c718a76B3fde75f2e0cFd8712' in selectedPools:
        farm_id = '0x8A4f4c7F4804D30c718a76B3fde75f2e0cFd8712'

        extension = get_moneypot(wallet,[{'address' : '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', 'symbol' : 'WBNB'}, {'address' : '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56', 'symbol' : 'BUSD'}], '0x8A4f4c7F4804D30c718a76B3fde75f2e0cFd8712', 'bsc', '0xAD07Cf266C99d0cC379D4f460F0FF27b81314238', '0x0c0bf2bd544566a11f59dc70a8f43659ac2fe7c2')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x4e22399070aD5aD7f7BEb7d3A7b543e8EcBf1d85' in selectedPools:
        farm_id = '0x4e22399070aD5aD7f7BEb7d3A7b543e8EcBf1d85'

        extension = get_vault_style(wallet,jetswapvaults.matic_to_list,'0x4e22399070aD5aD7f7BEb7d3A7b543e8EcBf1d85', WEB3_NETWORKS['matic'], 'getPricePerFullShare')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0x63d6EC1cDef04464287e2af710FFef9780B6f9F5' in selectedPools:
        farm_id = '0x63d6EC1cDef04464287e2af710FFef9780B6f9F5'

        extension = get_vault_style(wallet,jetswapvaults.bsc_to_list,'0x63d6EC1cDef04464287e2af710FFef9780B6f9F5', WEB3_NETWORKS['bsc'], 'getPricePerFullShare')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xStadiumArcadium' in selectedPools:
        farm_id = '0xStadiumArcadium'

        extension = farm_templates.get_multireward_masterchef(wallet,'0xStadiumArcadium','matic',ext_masterchef.stadium_farm_info)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xConvexETH' in selectedPools:
        farm_id = '0xConvexETH'

        extension = farm_templates.get_convex(wallet,'0xConvexETH','eth','0xF403C135812408BFbE8713b5A23a04b3D48AAE31')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xMoonPot' in selectedPools:
        farm_id = '0xMoonPot'

        extension = farm_templates.get_moonpot_contracts(wallet,'0xMoonPot','bsc',moonpot.moonpot_contracts)

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xBb3f43008e277543353588Ca2A4941F12e3CaCC0' in selectedPools:
        farm_id = '0xBb3f43008e277543353588Ca2A4941F12e3CaCC0'

        extension = get_single_masterchef(wallet, farm_id, 'matic', farms['0x6A08491e01b36D116c332C87253a78e6480f7f6D'])

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xPNG' in selectedPools:
        farm_id = '0xPNG'

        extension = get_quickswap_style(wallet,png.staking_rewards,farm_id,WEB3_NETWORKS['avax'])

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xTraderJoe' in selectedPools:
        farm_id = '0xTraderJoe'

        extension = farm_templates.get_traderjoe_masterchef(wallet, '0xTraderJoe', 'avax', '0xd6a4F121CA35509aF06A0Be99093d08462f53052')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    if '0xYak' in selectedPools:
        farm_id = '0xYak'

        extension = farm_templates.get_vault_style_custom_pps(wallet, yak.vaults, '0xYak', 'avax')

        if extension is not None:
            pendingWants[0].update(extension[0])
            pendingWants[1][farm_id]['userData'].update(extension[1][farm_id]['userData'])

    #print(pendingWants)
    if len(pendingWants[0]) < 1:
        return {}
    #print(pendingWants)
    lastReturn = get_token_data(pendingWants)

    
    #print(lastReturn)
    if '0xF3ca45633B2b2C062282ab38de74EAd2B76E8800' in selectedPools:
        moneyPot = getMoneyPot(wallet)
        lastReturn['0xF3ca45633B2b2C062282ab38de74EAd2B76E8800']['userData']['moneyPot'] = moneyPot

    tokens = []
    ftm_tokens = []
    kcc_tokens = []
    oke_tokens = []
    harmony_tokens = []
    avax_tokens = []

    for d in lastReturn:
        if farms[d]['network'] in INCH_SUPPORTED:
            tokens += [{'token' : x['token0'], 'decimal' : x['tkn0d'], 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'token0' in x]
            
            for x in lastReturn[d]['userData'].values():
                if 'gambitRewards' in x:
                    for rewards in x['gambitRewards']:
                        decimal = rewards['decimal'] if 'decimal' in rewards else 18
                        tokens += [{'token' : rewards['token'], 'decimal' : decimal, 'network' : farms[d]['network']}]
                elif 'rewardDecimal' in x and 'rewardToken' in x:
                    tokens += [{'token' : x['rewardToken'], 'decimal' : x['rewardDecimal'], 'network' : farms[d]['network']}]
                elif 'rewardToken' in x:
                    tokens += [{'token' : x['rewardToken'], 'decimal' : 18, 'network' : farms[d]['network']}]
                if 'slot0' in x:
                    tokens += [{'token' : x['token1'], 'decimal' : x['tkn1d'], 'network' : farms[d]['network']}]


                if 'balancerTokens' in x:
                    for i,balancer in enumerate(x['balancerTokens']):
                        tokens += [{'token' : balancer, 'decimal' : x['balancerDecimals'][i], 'network' : farms[d]['network']}]

                        
                
        elif farms[d]['network'] == 'ftm':
            ftm_tokens += [{'token' : x['token0'], 'decimal' : x['tkn0d'], 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'token0' in x]
            ftm_tokens += [{'token' : x['rewardToken'], 'decimal' : 18, 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'rewardToken' in x]
            for x in lastReturn[d]['userData'].values():
                if 'gambitRewards' in x:
                    for rewards in x['gambitRewards']:
                        ftm_tokens += [{'token' : rewards['token'], 'decimal' : 18, 'network' : farms[d]['network']}]

        elif farms[d]['network'] == 'kcc':
            kcc_tokens += [{'token' : x['token0'], 'decimal' : x['tkn0d'], 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'token0' in x]
            kcc_tokens += [{'token' : x['rewardToken'], 'decimal' : 18, 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'rewardToken' in x]
            for x in lastReturn[d]['userData'].values():
                if 'gambitRewards' in x:
                    for rewards in x['gambitRewards']:
                        kcc_tokens += [{'token' : rewards['token'], 'decimal' : 18, 'network' : farms[d]['network']}]

        elif farms[d]['network'] == 'oke':
            oke_tokens += [{'token' : x['token0'], 'decimal' : x['tkn0d'], 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'token0' in x]
            oke_tokens += [{'token' : x['rewardToken'], 'decimal' : 18, 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'rewardToken' in x]
            for x in lastReturn[d]['userData'].values():
                if 'gambitRewards' in x:
                    for rewards in x['gambitRewards']:
                        oke_tokens += [{'token' : rewards['token'], 'decimal' : 18, 'network' : farms[d]['network']}]

        elif farms[d]['network'] == 'harmony':
            harmony_tokens += [{'token' : x['token0'], 'decimal' : x['tkn0d'], 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'token0' in x]
            harmony_tokens += [{'token' : x['rewardToken'], 'decimal' : 18, 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'rewardToken' in x]
            for x in lastReturn[d]['userData'].values():
                if 'gambitRewards' in x:
                    for rewards in x['gambitRewards']:
                        harmony_tokens += [{'token' : rewards['token'], 'decimal' : 18, 'network' : farms[d]['network']}]

        elif farms[d]['network'] == 'avax':
            avax_tokens += [{'token' : x['token0'], 'decimal' : x['tkn0d'], 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'token0' in x]
            avax_tokens += [{'token' : x['rewardToken'], 'decimal' : 18, 'network' : farms[d]['network']} for x in lastReturn[d]['userData'].values() if 'rewardToken' in x]
            for x in lastReturn[d]['userData'].values():
                if 'gambitRewards' in x:
                    for rewards in x['gambitRewards']:
                        avax_tokens += [{'token' : rewards['token'], 'decimal' : 18, 'network' : farms[d]['network']}]

    tokens += [{'token' : '0xe9e7cea3dedca5984780bafc599bd69add087d56', 'decimal' : 18, 'network' : 'bsc'}, {'token' : '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', 'decimal' : 18, 'network' : 'bsc' }, {'token' : '0x2090c8295769791ab7A3CF1CC6e0AA19F35e441A', 'decimal' : 18, 'network' : 'bsc'}]
    
    if '0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A' in selectedPools:
        tokens += [{'token' : '0x42f6f551ae042cbe50c739158b4f0cac0edb9096', 'decimal' : 18, 'network' : 'bsc'}]

    for d in selectedPools:
        if farms[d]['network'] in INCH_SUPPORTED:
            tokens += [{'token' : farms[d]['rewardToken'], 'decimal' : farms[d]['decimal'], 'network' : farms[d]['network']}]
        elif farms[d]['network'] == 'ftm':
            ftm_tokens += [{'token' : farms[d]['rewardToken'], 'decimal' : farms[d]['decimal'], 'network' : farms[d]['network']}]
        elif farms[d]['network'] == 'kcc':
            kcc_tokens += [{'token' : farms[d]['rewardToken'], 'decimal' : farms[d]['decimal'], 'network' : farms[d]['network']}]
        elif farms[d]['network'] == 'oke':
            oke_tokens += [{'token' : farms[d]['rewardToken'], 'decimal' : farms[d]['decimal'], 'network' : farms[d]['network']}]
        elif farms[d]['network'] == 'harmony':
            harmony_tokens += [{'token' : farms[d]['rewardToken'], 'decimal' : farms[d]['decimal'], 'network' : farms[d]['network']}]
        elif farms[d]['network'] == 'avax':
            avax_tokens += [{'token' : farms[d]['rewardToken'], 'decimal' : farms[d]['decimal'], 'network' : farms[d]['network']}]            

    if '0xBeefy' in selectedPools:
        for d in bBoostsCheck:
            tokens += [{'token' : bBoostsCheck[d]['earnedTokenAddress'], 'decimal' : bBoostsCheck[d]['earnedTokenDecimals'], 'network' : 'bsc'}]
    if '0x97bdB4071396B7f60b65E0EB62CE212a699F4B08' in selectedPools:
        tokens += [{'token' : '0x579A6277a6c2c63a5b25006F63Bce5DC8D9c25e7', 'decimal' : 18, 'network' : 'bsc'}]

    tokentemp = [i for n, i in enumerate(tokens) if i not in tokens[n + 1:]]

    #Pull Prices
    # loop = get_or_create_eventloop()
    # future = asyncio.ensure_future(multiCallPrice(tokentemp))
    # prices = loop.run_until_complete(future)

    prices = await multiCallPrice(tokentemp)
    prices = {x['token'] : x['price'] for x in prices}

    if '0xF3ca45633B2b2C062282ab38de74EAd2B76E8800' in selectedPools:
        prices.update({'0x670De9f45561a2D02f283248F65cbd26EAd861C8' : getURNprice() })
    
    prices['0x85e76cbf4893c1fbcb34dcf1239a91ce2a4cf5a7'] = 1
    prices['0x85E76cbf4893c1fbcB34dCF1239A91CE2A4CF5a7'] = 1
    prices['0x8f3cf7ad23cd3cadbd9735aff958023239c6a063'] = 1

    if '0xe304ff0983922787Fd84BC9170CD21bF78B16B10' in prices:
        prices['0xe304ff0983922787Fd84BC9170CD21bF78B16B10'] = getxGMTprice()

    if '0x34ea3f7162e6f6ed16bd171267ec180fd5c848da' in prices:
        prices['0x34ea3f7162e6f6ed16bd171267ec180fd5c848da'] = int(get_dnd_price(['DND'])[0]['price']) / 1e6
    
    if '0x6ff2d9e5891a7a7c554b80e0d1b791483c78bce9' in prices:
        prices.update({'0x6ff2d9e5891a7a7c554b80e0d1b791483c78bce9': getCGprice('wault-finance-old')})
    if '0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21' in prices:
        prices.update({'0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21': getwSwap('0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21')})
    if '0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90' in prices:
        prices['0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90'] = getwSwap('0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90')
    if '0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4' in prices:
        prices['0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4'] = coingecko_by_address_network('0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4', 'polygon-pos')['0x16eccfdbb4ee1a85a33f3a9b21175cd7ae753db4']['usd']

    if '0x62ee12e4fe74a815302750913c3c796bca23e40e' in prices:
        prices['0x62ee12e4fe74a815302750913c3c796bca23e40e'] = getPCSV1('0x62ee12e4fe74a815302750913c3c796bca23e40e')

    if '0xef6f50fe05f4ead7805835fd1594406d31b96ed8' in prices:
        prices['0xef6f50fe05f4ead7805835fd1594406d31b96ed8'] = getPCSV2('0xef6f50fe05f4ead7805835fd1594406d31b96ed8')  

    if '0x0487b824c8261462f88940f97053e65bdb498446' in prices:
        prices['0x0487b824c8261462f88940f97053e65bdb498446'] = get_jet_swap('0x0487b824c8261462f88940f97053e65bdb498446') 

    if '0x965f527d9159dce6288a2219db51fc6eef120dd1' in prices:
        prices['0x965f527d9159dce6288a2219db51fc6eef120dd1'] = get_bi_swap('0x965f527d9159dce6288a2219db51fc6eef120dd1')

    if '0xd78C475133731CD54daDCb430F7aAE4F03C1E660' in prices:
        prices['0xd78C475133731CD54daDCb430F7aAE4F03C1E660'] = get_firebird_swap('0xd78C475133731CD54daDCb430F7aAE4F03C1E660')

    if '0xdd97ab35e3c0820215bc85a395e13671d84ccba2' in prices:
        prices['0xdd97ab35e3c0820215bc85a395e13671d84ccba2'] = Call('0x41B471F347a7C2C8e6cb7F4F59C570C6D9c69a3C', ['valueOfAsset(address,uint256)((uint256,uint256))', '0xdd97ab35e3c0820215bc85a395e13671d84ccba2', 1 * 10 ** 18], [['price', parse_profit_of_pool]])()['price'][1]

    if '0x1f546ad641b56b86fd9dceac473d1c7a357276b7' in prices:
        prices['0x1f546ad641b56b86fd9dceac473d1c7a357276b7'] = Call('0x41B471F347a7C2C8e6cb7F4F59C570C6D9c69a3C', ['valueOfAsset(address,uint256)((uint256,uint256))', '0x1f546ad641b56b86fd9dceac473d1c7a357276b7', 1 * 10 ** 18], [['price', parse_profit_of_pool]])()['price'][1]

    if '0x76bf0c28e604cc3fe9967c83b3c3f31c213cfe64' in prices:
        prices['0x76bf0c28e604cc3fe9967c83b3c3f31c213cfe64'] = ape_router_matic('0x76bf0c28e604cc3fe9967c83b3c3f31c213cfe64')

    if '0x5d47baba0d66083c52009271faf3f50dcc01023c' in prices:
        prices['0x5d47baba0d66083c52009271faf3f50dcc01023c'] = ape_router_matic('0x5d47baba0d66083c52009271faf3f50dcc01023c')

    if '0xcd734b1f9b0b976ddc46e507d0aa51a4216a1e98' in prices:
        prices['0xcd734b1f9b0b976ddc46e507d0aa51a4216a1e98'] = getPCSV2('0xcd734b1f9b0b976ddc46e507d0aa51a4216a1e98')

    if '0x63041a8770c4cfe8193d784f3dc7826eab5b7fd2' in prices:
        prices['0x63041a8770c4cfe8193d784f3dc7826eab5b7fd2'] = Call('0x41B471F347a7C2C8e6cb7F4F59C570C6D9c69a3C', ['valueOfAsset(address,uint256)((uint256,uint256))', '0x63041a8770c4cfe8193d784f3dc7826eab5b7fd2', 1 * 10 ** 18], [['price', parse_profit_of_pool]])()['price'][1]

    if '0x72b7d61e8fc8cf971960dd9cfa59b8c829d91991' in prices:
        prices['0x72b7d61e8fc8cf971960dd9cfa59b8c829d91991'] = get_price_from_router('0x72b7d61e8fc8cf971960dd9cfa59b8c829d91991','bsc',routers.BSCRouter.PLANET,True)

    if any(i in prices for i in ['0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25', '0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25'.lower()]):
        x = get_price_from_router('0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25','matic',routers.MATICRouter.JETSWAP,True)
        prices['0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25'] = x
        prices['0x845E76A8691423fbc4ECb8Dd77556Cb61c09eE25'.lower()] = x

    if '0xddb3bd8645775f59496c821e4f55a7ea6a6dc299' in prices:
        x = get_price_from_router('0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95','bsc',routers.BSCRouter.APESWAP,True)
        prices['0xddb3bd8645775f59496c821e4f55a7ea6a6dc299'] = x
        prices['0x603c7f932ed1fc6575303d8fb018fdcbb0f39a95'] = x

    if '0xd016caae879c42cb0d74bb1a265021bf980a7e96' in prices:
        x = get_price_from_router('0xd016caae879c42cb0d74bb1a265021bf980a7e96','matic',routers.MATICRouter.APESWAP,True,bypass_token='0x7ceb23fd6bc0add59e62ac25578270cff1b9f619')
        prices['0xd016caae879c42cb0d74bb1a265021bf980a7e96'] = x
        prices['0xD016cAAe879c42cB0D74BB1A265021bf980A7E96'] = x

    if '0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46' in prices:
        prices['0xD3293BdE855033c77B7919da40ABD1DF9EB5eB46'] = get_blackswan_lp()

    if '0x7d5bc7796fd62a9a27421198fc3c349b96cdd9dc' in prices:
        x = get_price_from_router('0x7d5bc7796fd62a9a27421198fc3c349b96cdd9dc','bsc',routers.BSCRouter.MELSWAP)
        prices['0x7d5bc7796fd62a9a27421198fc3c349b96cdd9dc'] = x
        prices['0x7d5bc7796fd62a9a27421198fc3c349b96cdd9dc'] = x

    if '0xc623d9e8bf6812852a7aeded140d479095cfd941' in prices:
        prices['0xc623d9e8bf6812852a7aeded140d479095cfd941'] = get_price_from_router('0xc623d9e8bf6812852a7aeded140d479095cfd941', 'bsc', routers.BSCRouter.PCS_V2,native=True)

    if '0xb5389a679151c4b8621b1098c6e0961a3cfee8d4' in prices:
        prices['0xb5389a679151c4b8621b1098c6e0961a3cfee8d4'] = get_price_from_router('0xb5389a679151c4b8621b1098c6e0961a3cfee8d4', 'bsc', routers.BSCRouter.PCS_V2,native=True)

    if '0x2c449ba613873e7b980faf2b686207d7bd205541' in prices:
        prices['0x2c449ba613873e7b980faf2b686207d7bd205541'] = get_price_from_router('0x2c449ba613873e7b980faf2b686207d7bd205541', 'bsc', routers.BSCRouter.COBRA, native=True)

    if '0xa649325aa7c5093d12d6f98eb4378deae68ce23f' in prices:
        prices['0xa649325aa7c5093d12d6f98eb4378deae68ce23f'] = get_price_from_router('0xa649325aa7c5093d12d6f98eb4378deae68ce23f', 'matic', routers.MATICRouter.APESWAP, native=True)

    if '0x56e344be9a7a7a1d27c854628483efd67c11214f' in prices:
        x = get_price_from_router('0x56e344be9a7a7a1d27c854628483efd67c11214f', 'bsc', routers.BSCRouter.SHIB, native=True)
        prices['0x56e344be9a7a7a1d27c854628483efd67c11214f'] = x
        prices['0x0c0bf2bd544566a11f59dc70a8f43659ac2fe7c2'] = x
        




    if any(i in prices for i in ['0x4c4bf319237d98a30a929a96112effa8da3510eb', '0x3053ad3b31600074e9A90440770f78D5e8Fc5A54'.lower()]):
        prices.update(get_poly_wault())
    
    if len(ftm_tokens) > 0:
        prices = {**prices, **fantom_router_prices(ftm_tokens,['SPOOKY', 'HYPER', 'SPIRIT', 'WAKA', 'PAINT'])}

    if len(kcc_tokens) > 0:
        prices = {**prices, **kcc_router_prices(kcc_tokens,['KUSWAP', 'KOFFEE', 'KANDY', 'BONE'])}

    if len(oke_tokens) > 0:
        prices = {**prices, **oke_router_prices(oke_tokens,['PANDA', 'CHERRY', 'KSWAP'])}

    if len(harmony_tokens) > 0:
        prices = {**prices, **harmony_router_prices(harmony_tokens,['SUSHI', 'VENOM'])}

    if len(avax_tokens) > 0:
        prices = {**prices, **avax_router_prices(avax_tokens,['PNG', 'JOE', 'SUSHI'])}

    #print(prices)
    finalResponse = lastReturn
    #print(finalResponse)
    for f in lastReturn:
        farmAdd = f
        rewardToken = farms[f]['rewardToken']
        farm_network = farms[f]['network']

        for x in lastReturn[f]['userData']:
            try:
                if 'boostedReward' in lastReturn[f]['userData'][x]:
                    rewardToken = lastReturn[f]['userData'][x]['boostedReward']
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pending'] * beefyPrices[rewardToken], 2)
                elif 'pendingNerve' in lastReturn[f]['userData'][x]:
                    finalResponse[f]['userData'][x]['pendingNRVAmount'] = round((finalResponse[f]['userData'][x]['pendingNerve'] * finalResponse[f]['userData'][x]['nerveMultipler']) * prices['0x42f6f551ae042cbe50c739158b4f0cac0edb9096'.lower()], 2)
                    finalResponse[f]['userData'][x]['pendingELE'] = round(finalResponse[f]['userData'][x]['pending'] * prices[rewardToken], 2)
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pendingELE'] + finalResponse[f]['userData'][x]['pendingNRVAmount'], 2)
                elif x == 'bingoBoard':
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices['0x579A6277a6c2c63a5b25006F63Bce5DC8D9c25e7'], 2)
                elif 'rewardToken' in lastReturn[f]['userData'][x]:
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[lastReturn[f]['userData'][x]['rewardToken']], 2)
                elif 'gambitRewards' in lastReturn[f]['userData'][x]:
                    finalResponse[f]['userData'][x]['pendingAmount'] = 0
                    for i, gr in enumerate(lastReturn[f]['userData'][x]['gambitRewards']):
                        if 'valueOfAsset' in finalResponse[f]['userData'][x]['gambitRewards'][i]:
                            finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount'] = gr['pending'] * gr['valueOfAsset']
                        else:
                            finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount'] = gr['pending'] * prices[gr['token']]
                        if x not in ['0xA2A065DBCBAE680DF2E6bfB7E5E41F1f1710e63b', 'VAULTS']:
                            finalResponse[f]['userData'][x]['pendingAmount'] += finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount']

                else:
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[rewardToken], 2)
                
                if 'pendingNerve' in lastReturn[f]['userData'][x]:
                    finalResponse[f]['userData'][x]['pendingNRVAmount'] = round((finalResponse[f]['userData'][x]['pendingNerve'] * finalResponse[f]['userData'][x]['nerveMultipler']) * prices['0x42f6f551ae042cbe50c739158b4f0cac0edb9096'.lower()], 2)
                
                if 'pendingBunny' in lastReturn[f]['userData'][x]:
                    finalResponse[f]['userData'][x]['pendingBunnyAmount'] = round(finalResponse[f]['userData'][x]['pendingBunny'] * prices['0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51'.lower()], 2)
                    finalResponse[f]['userData'][x]['pendingRewardAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[lastReturn[f]['userData'][x]['rewardToken']], 2)
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pendingBunnyAmount'] + finalResponse[f]['userData'][x]['pendingRewardAmount'], 2)

                if 'pendingMerlin' in lastReturn[f]['userData'][x]:
                    finalResponse[f]['userData'][x]['pendingMerlinAmount'] = round(finalResponse[f]['userData'][x]['pendingMerlin'] * prices['0xda360309c59cb8c434b28a91b823344a96444278'.lower()], 2)
                    finalResponse[f]['userData'][x]['pendingRewardAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[lastReturn[f]['userData'][x]['rewardToken']], 2)
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pendingMerlinAmount'] + finalResponse[f]['userData'][x]['pendingRewardAmount'], 2)

            except:

                finalResponse[f]['userData'][x]['pendingAmount'] = 0
                finalResponse[f]['userData'][x]['pending'] = 0
            try:
                    finalResponse[f]['userData'][x].update(getEBalances(lastReturn[f]['userData'][x]['staked'],
                     lastReturn[f]['userData'][x]['totalSupply'],
                     lastReturn[f]['userData'][x]['reserves'],
                     lastReturn[f]['userData'][x]['token0'],
                     lastReturn[f]['userData'][x]['tkn0d'],
                     lastReturn[f]['userData'][x]['tkn1d'],
                     lastReturn[f]['userData'][x]['pricePer'],
                     lastReturn[f]['userData'][x]['e11token'],
                     prices))

                    finalResponse[f]['userData'][x]['tokenPair'] = '%s/%s' % (lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s'])
            except KeyError:
                try:
                    if 'getPricePerFullShare' in lastReturn[f]['userData'][x]:
                        stakedAmount = lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getPricePerFullShare']
                    else:
                        stakedAmount = lastReturn[f]['userData'][x]['staked']

                    finalResponse[f]['userData'][x].update(getLPBalances(stakedAmount,
                    lastReturn[f]['userData'][x]['totalSupply'],
                    lastReturn[f]['userData'][x]['reserves'],
                    lastReturn[f]['userData'][x]['token0'],
                    lastReturn[f]['userData'][x]['tkn0d'],
                    lastReturn[f]['userData'][x]['tkn1d'],
                    prices))

                    finalResponse[f]['userData'][x]['tokenPair'] = '%s/%s' % (lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s'])
                    
                    if 'getPricePerFullShare' in lastReturn[f]['userData'][x]:
                        finalResponse[f]['userData'][x]['elevenBalance'] = '(%s)' % (finalResponse[f]['userData'][x]['lpTotal'])
                        finalResponse[f]['userData'][x]['lpTotal'] = round(lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getPricePerFullShare'], 4)

                except KeyError:

                    if x == 'moneyPot':
                        finalResponse[f]['userData'][x]['lpPrice'] = lastReturn[f]['userData'][x]['u235balance'] * prices['0x670De9f45561a2D02f283248F65cbd26EAd861C8']
                        finalResponse[f]['userData'][x]['BUSD_total'] = lastReturn[f]['userData'][x]['BUSD_pending'] * prices['0xe9e7cea3dedca5984780bafc599bd69add087d56']
                        finalResponse[f]['userData'][x]['WBNB_total'] = lastReturn[f]['userData'][x]['WBNB_pending'] * prices['0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c']
                        finalResponse[f]['userData'][x]['pendingAmount'] = finalResponse[f]['userData'][x]['WBNB_total'] + finalResponse[f]['userData'][x]['BUSD_total']
                    
                    else:

                        if lastReturn[f]['userData'][x]['token0'].lower() == '0x670De9f45561a2D02f283248F65cbd26EAd861C8'.lower():
                            quotePrice = getURNprice()
                        elif lastReturn[f]['userData'][x]['token0'].lower() in ['0x86aFa7ff694Ab8C985b79733745662760e454169'.lower(), '0x049d68029688eAbF473097a2fC38ef61633A3C7A'.lower(), '0x10a450A21B79c3Af78fb4484FF46D3E647475db4'.lower(), '0x7C9e73d4C71dae564d41F78d56439bB4ba87592f'.lower(), '0x02dA7035beD00ae645516bDb0c282A7fD4AA7442'.lower()]:
                            quotePrice = 1
                        elif lastReturn[f]['userData'][x]['token0'].lower() == '0xdff88a0a43271344b760b58a35076bf05524195c'.lower():
                            quotePrice = getPHBprice()
                        elif lastReturn[f]['userData'][x]['token0'].lower() == '0x28060854AC19391dF6C69Df430cAba4506181d56'.lower():
                            quotePrice = prices['0xee814f5b2bf700d2e843dc56835d28d095161dd9']
                        elif lastReturn[f]['userData'][x]['token0'].lower() == '0xf6488205957f0b4497053d6422F49e27944eE3Dd'.lower():
                            quotePrice = prices['0x2090c8295769791ab7A3CF1CC6e0AA19F35e441A'] * getJetValue()
                        elif lastReturn[f]['userData'][x]['token0'].lower() == '0x9cb73F20164e399958261c289Eb5F9846f4D1404'.lower():
                            quotePrice = float(get_four_belt()['0x9cb73F20164e399958261c289Eb5F9846f4D1404'])
                        elif lastReturn[f]['userData'][x]['token0'].lower() == '0x92d5ebf3593a92888c25c0abef126583d4b5312e'.lower():
                            quotePrice = get_atricryptos_price('ftm', '0x92d5ebf3593a92888c25c0abef126583d4b5312e',6,'uint256,int128')
                        elif 'zombieOverride' in lastReturn[f]['userData'][x]:
                            if lastReturn[f]['userData'][x]['zombieOverride'] is True:
                                quotePrice = prices['0x50ba8bf9e34f0f83f96a340387d1d3888ba4b3b5']
                            else:
                                quotePrice = prices[lastReturn[f]['userData'][x]['token0']] if lastReturn[f]['userData'][x]['token0'] in prices else 0.1
                        else:
                            quotePrice = prices[lastReturn[f]['userData'][x]['token0']] if lastReturn[f]['userData'][x]['token0'] in prices else 0.1

                        if 'curve_pool_token' in lastReturn[f]['userData'][x]:
                            if lastReturn[f]['userData'][x]['curve_pool_token'] == '0x8096ac61db23291252574d49f036f0f9ed8ab390':
                                quotePrice = get_atricryptos_price()

                        singleStake = lastReturn[f]['userData'][x]['staked']

                        if 'e11token' in finalResponse[f]['userData'][x]:
                            if lastReturn[f]['userData'][x]['e11token'].lower() == '0xAcD7B3D9c10e97d0efA418903C0c7669E702E4C0'.lower():
                                fullStake = from_custom(lastReturn[f]['userData'][x]['pricePer'], 12) * singleStake
                            else:
                                fullStake = from_wei(lastReturn[f]['userData'][x]['pricePer']) * singleStake

                                if 'virtualPrice' in lastReturn[f]['userData'][x]:
                                    fullStake = fullStake * lastReturn[f]['userData'][x]['virtualPrice']
                            

                            finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                            
                            if lastReturn[f]['userData'][x]['e11token'].lower() == '0xdaf66c0b7e8e2fc76b15b07ad25ee58e04a66796'.lower():
                                inchBNBPrice = beefyPrices['1inch-1inch-bnb']

                                finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * inchBNBPrice, 2)
                            
                            else:    
                                finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                        
                        elif 'fulcrumToken' in finalResponse[f]['userData'][x]:
                            fullStake = lastReturn[f]['userData'][x]['fulcrumToken'] * singleStake
                            finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                            finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                        elif 'swap' in finalResponse[f]['userData'][x]:
                            if 'pricePer' in finalResponse[f]['userData'][x]:
                                singleStake = singleStake * from_wei(finalResponse[f]['userData'][x]['pricePer'])
                            fullStake = singleStake * finalResponse[f]['userData'][x]['virtualPrice']
                            finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                            finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                        elif 'curve_pool_token' in finalResponse[f]['userData'][x]:
                            fullStake = singleStake * finalResponse[f]['userData'][x]['virtualPrice']
                            if 'getRatio' in finalResponse[f]['userData'][x]:
                                fullStake = fullStake * finalResponse[f]['userData'][x]['getRatio']
                            if 'getPricePerFullShare' in finalResponse[f]['userData'][x]:
                                fullStake = fullStake * finalResponse[f]['userData'][x]['getPricePerFullShare']
                            finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                            finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)                            
                        elif 'getPricePerFullShare' in finalResponse[f]['userData'][x]:
                            fullStake = singleStake * finalResponse[f]['userData'][x]['getPricePerFullShare']
                            finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                            finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                        elif 'getRatio' in finalResponse[f]['userData'][x]:
                            fullStake = singleStake * finalResponse[f]['userData'][x]['getRatio']
                            finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                            finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                        elif 'balancerBalances' in finalResponse[f]['userData'][x]:
                            finalResponse[f]['userData'][x].update(get_balancer_ratio(finalResponse[f]['userData'][x], prices))
                        elif 'slot0' in finalResponse[f]['userData'][x]:
                            finalResponse[f]['userData'][x].update(uniswapv3.get_uniswap_v3_balance(finalResponse[f]['userData'][x], farm_network, prices))
                            finalResponse[f]['userData'][x]['tokenPair'] = '%s/%s' % (lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s'])
                            for i, gr in enumerate(lastReturn[f]['userData'][x]['uniswapFee']):
                                finalResponse[f]['userData'][x]['uniswapFee'][i]['pendingAmount'] = gr['pending'] * prices[gr['token']]
                                finalResponse[f]['userData'][x]['pendingAmount'] += finalResponse[f]['userData'][x]['uniswapFee'][i]['pendingAmount']
                        else:
                            finalResponse[f]['userData'][x]['lpPrice'] = round(singleStake * quotePrice, 2)
                            if 'borrowed' in finalResponse[f]['userData'][x]:
                                finalResponse[f]['userData'][x]['borrowedUSD'] = finalResponse[f]['userData'][x]['borrowed'] * quotePrice
                        if 'tokenPair' not in finalResponse[f]['userData'][x]:
                            finalResponse[f]['userData'][x]['tokenPair'] = lastReturn[f]['userData'][x]['tkn0s']
        try:
            pending_user_amount = sum(d['pendingAmount'] for d in finalResponse[f]['userData'].values() if d)
            finalResponse[f]['poolTotal'] = sum(d['lpPrice'] for d in finalResponse[f]['userData'].values() if d)
            finalResponse[f]['pendingTotal'] = pending_user_amount if pending_user_amount > 0 else 0
            finalResponse[f]['total'] = finalResponse[f]['poolTotal'] + finalResponse[f]['pendingTotal'] if finalResponse[f]['pendingTotal'] >= 0 else finalResponse[f]['poolTotal']
        except:
            finalResponse[f]['poolTotal'] = 0
            finalResponse[f]['pendingTotal'] = 0
            finalResponse[f]['total'] = 0
        
        if f == '0xFortress':
            mintedFAI = Call("0x67340Bd16ee5649A37015138B3393Eb5ad17c195", ['%s(address)(uint256)' % ('mintedFAIs'), wallet], [['mint', from_wei ]])()
            finalResponse[f]['mintedFAI'] = mintedFAI['mint']
        
        if 'type' in farms[f]:
            finalResponse[f]['type'] = farms[f]['type']
            if farms[f]['type'] == 'lending':
                finalResponse[f]['availableLimit'] = sum(d['lpPrice'] * d['rate'] for d in finalResponse[f]['userData'].values() if 'rate' in d)
                finalResponse[f]['totalBorrowed'] = sum(d['borrowedUSD'] for d in finalResponse[f]['userData'].values() if 'borrowedUSD' in d)

    
    #print(finalResponse)
    return finalResponse

#runFlask(['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', '0x0895196562C7868C5Be92459FaE7f877ED450452', '0xd56339F80586c08B7a4E3a68678d16D37237Bd96', '0x7f7Bf15B9c68D23339C31652C8e860492991760d', '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56'], '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f')

# import pprofile
# prof = pprofile.Profile()
# with prof():
#     runFlask(['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', '0x0895196562C7868C5Be92459FaE7f877ED450452', '0xd56339F80586c08B7a4E3a68678d16D37237Bd96', '0x7f7Bf15B9c68D23339C31652C8e860492991760d', '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56'], '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f')
# prof.dump_stats("profiler_stats.txt")

# import pprofile
# profiler = pprofile.StatisticalProfile()
# statistical_profiler_thread = pprofile.StatisticalThread(
#     profiler=profiler,
# )
# with statistical_profiler_thread:
#     runFlask(['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', '0x7f7Bf15B9c68D23339C31652C8e860492991760d', '0x86f4bC1EBf2C209D12d3587B7085aEA5707d4B56', '0x69C77Aca910851E61a64b855116888F1c5eD3B75', '0x22fB2663C7ca71Adc2cc99481C77Aaf21E152e2D'], '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f')

# profiler.dump_stats("profiler_stats.txt")


