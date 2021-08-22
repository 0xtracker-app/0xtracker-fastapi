from os import replace
from platform import dist
from types import MethodDescriptorType
from gevent import monkey
from grequests import request
monkey.patch_all() # we need to patch very early
from eth_utils import address
from oracles import coingecko_by_address_network, get_price_from_router, kcc_router_prices
from toolz.itertoolz import last
from poolext.pancakebunny import bunnies
from poolext.gambit import gambits
from poolext.taodao import dao
from poolext.pancakepools import pancakePools
from poolext.fortress import forts
from poolext.dyp import dypPools
from poolext.merlin import magic
from poolext.squirrel import nuts
from poolext.adamant import adamant_deployers
from poolext.kogefarm import koge_vaults
from poolext.aperocket import ape_rockets
from poolext.pancake_bunny_matic import bunny_matic_vaults
import poolext.feeder as feeder
import poolext.pandaswap as pandaswap
import poolext.superfarm as superfarm
import poolext.curve
import poolext.telx as telx
import poolext.paprprintr as papr
import poolext.polygonfarm as polygonfarm
import poolext.ironlend as ironlend
import abi.traderjoe
from abi.add_rewards import reward_abi
from abi.balancer_vault import balancer_vault_abi
from abi.farmhero import multi_fee_v2
import bitquery.quickswap_lps
import bitquery.balancer_pools
from multicall import Call, Multicall
import multicall.parsers as parsers
from web3 import Web3
from farms import farms
import abi.uni_nft as uniNFT
import requests
import hjson
import json
from networks import WEB3_NETWORKS, SCAN_APIS
from new import from_wei, get_apeswap_pools, get_curve_gauage, get_ele_tokens, get_syrup_pools, get_vault_style, getLP, get_single_masterchef, from_custom, setPool, get_balancer_token, getSingle, get_pancake_bunny_clones,parseAccountSnapshot
from abi.wswap import wSwapABI
from abi.gambit import gambitABI
from abi.pcs1 import pcsRouter
from abi.jets import jetsRouter
from routers import router
import abi.adamant
import time
import asyncio
import routers
import requests
import hjson
from aiohttp import ClientSession, ClientTimeout
from pymongo import MongoClient
import datetime
import cloudscraper
from thegraph import call_graph
import re
import math
import decimal
import farm_templates
import template_helpers

DUST_FILTER = 0.00000000001
pool = '0xEDfcB78e73f7bA6aD2D829bf5D462a0924da28eD'
wallet = '0x6afbe7482cf93d7f4e0dca2eb6a86ceb3bbad3c5'
client = MongoClient('mongodb+srv://xtracker:FkIIpyj3hdUWpuEl@cluster0.wrato.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mongo = client.xtracker
tokenDB = mongo.full_tokens

# owner = Web3.toChecksumAddress('0x55f8742e649f02816f972ffe6bcde17c61ee2bc4')
# owner_address = Web3.solidityKeccak(['address'],[owner])

# print(owner_address)

WEB3_PROVIDER = Web3(Web3.HTTPProvider('https://speedy-nodes-nyc.moralis.io/64498953ccdea0710b4b8304/bsc/mainnet/archive'))

approval_filter = WEB3_PROVIDER.eth.filter({
    "fromBlock" : 9862051,
    "topics": ["0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
               "0x00000000000000000000000055f8742e649f02816f972ffe6bcde17c61ee2bc4"]
    })


# x = WEB3_PROVIDER.eth.get_filter_logs(approval_filter.filter_id)

# print(x)

def get_curve_gauage(wallet,farm_id,network_id,gauages,rewards=None):
    poolKey = farm_id
    calls = []
    network = WEB3_NETWORKS[network_id]

    if rewards is None:
        rewards = ['0x172370d5Cd63279eFa6d502DAB29171933a610AF', '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270']

    for guage in gauages:
        calls.append(Call(guage, [f'balanceOf(address)(uint256)', wallet], [[f'{guage}_staked', from_wei]]))
        for i,each in enumerate(rewards):
            calls.append(Call(guage, [f'claimable_reward(address,address)(uint256)', wallet,each], [[f'{guage}_pending{i}', from_wei]]))
            
        calls.append(Call(guage, [f'claimable_tokens(address)(uint256)', wallet], [[f'{guage}_pendingtokens', from_wei]]))
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


# for each in poolext.curve.eth_gauges_1:
#     # x = get_curve_gauage('0xbb49444efe86b167d1cc35c79a9eb39110dbd5e3','farm','eth',[each],['0xd533a949740bb3306d119cc777fa900ba034cd52'])
#     # print(x)

#     try:
#         x = get_curve_gauage('0x7eb510a2d3316dd2cdca937a95ec81cdf140a98d','farm','eth',[each],['0xd533a949740bb3306d119cc777fa900ba034cd52'])

#     except:
#         print(each,' failed')


def get_moonpot_contracts(wallet,farm_id,network_id,contracts):
        poolKey = farm_id

        network = WEB3_NETWORKS[network_id]

        reward_calls = []
        for each in contracts:
            reward_calls.append(Call(each['contract'], [f'rewardTokenLength()(uint256)'], [[each['contract'], None]]))

        reward_lengths = Multicall(reward_calls, network)()

        calls = []
        for each in contracts:
            pot_contract = each['contract']
            token_function = each['token_function']
            reward_length = reward_lengths[pot_contract]
            calls.append(Call(pot_contract, [f'userTotalBalance(address)(uint256)',wallet], [[f'{pot_contract}_staked', from_wei]]))
            calls.append(Call(pot_contract, [f'{token_function}()(address)'], [[f'{pot_contract}_want', None]]))
            for i in range(0,reward_length):
                calls.append(Call(pot_contract, [f'earned(address,uint256)(uint256)', wallet, i], [[f'{pot_contract}pending{i}', None]]))
                calls.append(Call(pot_contract, [f'rewardInfo(uint256)(address)', i], [[f'{pot_contract}rewardaddress{i}', None]]))

        stakes=Multicall(calls, network)()

        poolNest = {poolKey: 
        { 'userData': { } } }

        poolIDs = {}

        reward_symbols_decimals = template_helpers.get_token_list_decimals_symbols([stakes[x] for x in stakes if 'rewardaddress' in x],network_id)

        for each in stakes:
            if 'staked' in each:
                if stakes[each] > 0:
                    breakdown = each.split('_')
                    staked = stakes[each]
                    want_token = stakes[f'{breakdown[0]}_want']
                    wanted_decimal = 18
                    pot_contract = breakdown[0]
                    reward_length = reward_lengths[pot_contract]

                    poolNest[poolKey]['userData'][breakdown[0]] = {'want': want_token, 'staked' : staked, 'gambitRewards' : []}
                    poolIDs['%s_%s_want' % (poolKey, breakdown[0])] = want_token

                    for i in range(0,reward_length):
                        if f'{pot_contract}pending{i}' in stakes:
                            pending_reward = stakes[f'{breakdown[0]}pending{i}']
                            pending_reward_contract = stakes[f'{breakdown[0]}rewardaddress{i}']
                            pending_reward_symbol = reward_symbols_decimals[f'{pending_reward_contract}_symbol']
                            pending_reward_decimal = reward_symbols_decimals[f'{pending_reward_contract}_decimals']
                            if pending_reward > 0:
                                reward_token_0 = {'pending': from_custom(pending_reward, pending_reward_decimal), 'symbol' : pending_reward_symbol, 'token' : pending_reward_contract}
                                poolNest[poolKey]['userData'][breakdown[0]]['gambitRewards'].append(reward_token_0)


        if len(poolIDs) > 0:
            return poolIDs, poolNest    
        else:
            return None


moonpot_contracts = [{'contract': '0x35ebb629b6e65Cb7705B5E0695982D206898f195', 'token_function': 'stakeToken'}, {
    'contract': '0x30d55CE74E2dcd1B0Ff37214a6978FCFc06aA499', 'token_function': 'underlying'}]


def get_lending_protocol(wallet,lending_vaults,farm_id,network):

    poolKey = farm_id
    calls = []

    for vault in lending_vaults:

        vault_address = vault['address']
        print(vault_address)
        calls.append(Call(vault_address, [f'getAccountSnapshot(address)((uint256,uint256,uint256,uint256))', wallet], [[f'{vault_address}_accountSnapshot', None ]]))
        
        stakes=Multicall(calls, WEB3_NETWORKS[network])()

import poolext.benqi as benqi

get_lending_protocol(wallet,benqi.vaults,'0xBenqi','avax')

