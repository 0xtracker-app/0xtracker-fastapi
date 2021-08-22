from multicall import Call, Multicall
from web3 import Web3
from farms import farms
import requests
import hjson
import json
from new import from_wei, getSingle, ellCheck, from_custom, setPool, beefyCheck, fulcrmCheck, catchENRV
import time
from pymongo import MongoClient
import priceHelper
import datetime

client = MongoClient('mongodb+srv://xtracker:FkIIpyj3hdUWpuEl@cluster0.wrato.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mongo = client.xtracker
poolWantDB = mongo.poolInfo
farmInfoDB = mongo.farmInfo
tokenDB = mongo.tokens
WEB3_NETWORKS = {'bsc': { 'connection' : Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/')), 'id' : 56}, 'matic':  {'connection' : Web3(Web3.HTTPProvider('https://polygon-mainnet.infura.io/v3/d09c293e2cc14290ada8169d29e9b65f')), 'id' : 137}, 'ftm' : {'connection' : Web3(Web3.HTTPProvider('https://rpc.ftm.tools/')), 'id': 250}, 'kcc' : {'connection' : Web3(Web3.HTTPProvider('https://rpc-mainnet.kcc.network')), 'id': 321}}

def parseReserves(value):
    return [str(value[0]), str(value[1])]

def parsePoolInfo(data):
    return {'want': data[0], 'allocPoint' : data[1]}

def parsePoolInfoX(data):
    return {'want': data[1], 'allocPoint' : data[2]}

def parsePoolInfoICE(data):
    return {'want': data[0], 'allocPoint' : data[4]}

def getLP(token, farm_id):

    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]

    try:
        return getSwap(token, farm_id)
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

        return {**lpPool, **lpTokens()}

def getSingle(token, farm_id):

        network = farms[farm_id]['network']
        network_chain = WEB3_NETWORKS[network]
        
        if token in catchENRV:
            token = catchENRV[token]['tokenAddress']
        
        try:
            return getSwap(token, farm_id)
        except:
            try:
                return getBeltToken(token, farm_id)
            except:
                try:
                    return getGrowToken(token, farm_id)
                except:
                    single = Multicall([
                        Call(token, 'symbol()(string)', [['tkn0s', None]]),
                        Call(token, 'decimals()(uint8)', [['tkn0d', None]]),
                    ], network_chain)

                    add = {'token0' : token}

                    return {**add, **single()}

def getSwap(token, farm_id):
    
    network = farms[farm_id]['network']
    network_chain = WEB3_NETWORKS[network]
    
    swap = Multicall([
            Call(token, 'swap()(address)', [['swap', None]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
        ], network_chain)

    swap=swap()

    if token in ['0x55088b82748ac28e31e0677241dbbe0a663d7e40', '0xe7419b94082a87c04ffb298805ec07f745d9d216']:
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


    belt = Multicall([
            Call(token, 'getPricePerFullShare()(uint256)', [['getPricePerFullShare', from_wei]]),
            Call(token, 'symbol()(string)', [['tkn0s', None]]),
            Call(token, 'token()(address)', [['token0', None]])
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
        return {**wrappedCalls, **{'getPricePerFullShare': (grow['growTotalReserve'] / grow['growTotalSupply'])}}
    except:
        wrappedCalls = getSingle(grow['reserveToken'], farm_id)
        return {**wrappedCalls, **{'getPricePerFullShare': (grow['growTotalReserve'] / grow['growTotalSupply'])}}

def singleLP(token, prices):
    if 'token1' not in token:
        return {'price' : prices[token['token0']]}
    else:
        return getLPBalances(token, prices)

def getLPBalances(lp, prices):

    quotePrice = prices[lp['token0']]

    userPct = 1 / lp['totalSupply']
    lp1val = (userPct * int(lp['reserves'][0])) / (10**lp['tkn0d'])

    return {'price' : (lp1val * quotePrice) * 2}

def runJob():
    for farm in farms:
        if 'perBlock' in farms[farm]:
            print(farm)
            perBlockFunction = farms[farm]['perBlock']
            chef = farms[farm]['masterChef']
            rewardToken = farms[farm]['rewardToken']
            network = farms[farm]['network']
            network_chain = WEB3_NETWORKS[network]

            rewardDecimal = Call(rewardToken, 'decimals()(uint8)', None, network_chain)()

            rewardPerBlock = Call(chef, ['%s()(uint256)' % (perBlockFunction)], None, network_chain)() / 10 ** rewardDecimal

            totalAllocPoints = Call(chef, ['%s()(uint256)' % ('totalAllocPoint')], [['totalAllocPoint', None ]], network_chain)()
            
            if chef == '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7':
                poolLength = Call(chef, ['%s()(uint256)' % ('getRewardsLength')], [['poolLength', None ]], network_chain)()
            else:
                poolLength = Call(chef, ['%s()(uint256)' % ('poolLength')], [['poolLength', None ]], network_chain)()

            
            data = {'chef' : farm, 'rewardPerBlock' : rewardPerBlock, 'totalAllocPoints' : totalAllocPoints['totalAllocPoint'], 'poolLength' : poolLength['poolLength'], 'rewardToken' : rewardToken, 'rewardDecimal' : rewardDecimal, 'timestamp' : currentTime, 'network': network}
            farmInfoDB.update_one({'chef' : farm}, { "$set": data }, upsert=True)

            rng = 1 if farm in ['0x0895196562C7868C5Be92459FaE7f877ED450452'] else 0
            end = 3 if farm in [''] else poolLength['poolLength']
            for i in range(rng, end):
                if farm == '0xd1b3d8ef5ac30a14690fbd05cf08905e1bf7d878' and i == 2:
                    continue
                elif farm == '0x0895196562C7868C5Be92459FaE7f877ED450452' and i == 331:
                    continue
                elif farm == '0x95030532D65C7344347E61Ab96273B6B110385F2' and i == 43:
                    continue
                else:
                    if farm == '0xF1F8E3ff67E386165e05b2B795097E95aaC899F0':
                        poolInfo = Call(farm, ['poolInfo(uint256)((uint256,address,uint256,uint256,uint256))', i], [['poolInfo', parsePoolInfoX]], network_chain)()
                    elif farm in ['0x05200cB2Cee4B6144B2B2984E246B52bB1afcBD0', '0xbf513aCe2AbDc69D38eE847EFFDaa1901808c31c']:
                        poolInfo = Call(farm, ['poolInfo(uint256)((address,uint256,uint256,uint256,uint256))', i], [['poolInfo', parsePoolInfoICE]], network_chain)()
                    elif farm == '0x036DB579CA9A04FA676CeFaC9db6f83ab7FbaAD7':
                        poolInfo = Call(farm, ['rewardsInfo(uint256)((address,uint256,uint256,uint256))', i], [['poolInfo', parsePoolInfo]], network_chain)()
                    else:
                        poolInfo = Call(farm, ['poolInfo(uint256)((address,uint256,uint256,uint256))', i], [['poolInfo', parsePoolInfo]], network_chain)()
                
                wanted = poolInfo['poolInfo']['want']
                try:
                    decimalWant = Call(wanted, 'decimals()(uint8)', None, network_chain)()
                except:
                    decimalWant = 18
                try:
                    ttl = Call(wanted, ['balanceOf(address)(uint256)', farm], None, network_chain)() / 10 ** decimalWant
                except:
                    ttl = 0
                data = {'key': '%s_%s' % (farm, i), 'poolInfo' : poolInfo['poolInfo'], 'farm' : farm, 'poolIndex' : i, 'ttl' : ttl, 'timestamp' : currentTime, 'network': network}
                print(data)
                poolWantDB.update_one({'key' : '%s_%s' % (farm, i)}, { "$set": data }, upsert=True)

currentTime = datetime.datetime.utcnow()
start_time = datetime.datetime.now()

runJob()

distinctWants = poolWantDB.distinct("poolInfo.want")

for token in distinctWants:
    record = poolWantDB.find_one({'poolInfo.want' : token})
    farm = record['key'].split('_')[0]
    farm_network = farms[farm]['network']
    print(farm)

    try:
        data = {**getLP(token, farm), **{'tokenID' : token}, **{'timestamp' : currentTime, 'network' : farm_network}}
        tokenDB.update_one({'tokenID' : token}, { "$set": data }, upsert=True)
    except:
        try:
            data = {**getSingle(token, farm), **{'tokenID' : token}, **{'timestamp' : currentTime, 'network' : farm_network}}
            tokenDB.update_one({'tokenID' : token}, { "$set": data }, upsert=True)
        except Exception as error:
            print(str(error), token)
        
distinctTokens = tokenDB.distinct("token0")
fetchList = [{'token' : d, 'decimal' : tokenDB.find_one({'token0' : d})['tkn0d'], 'network' : tokenDB.find_one({'token0' : d})['network']} for d in distinctTokens ]

allPrices = priceHelper.getPrices(fetchList)



for each in tokenDB.find():
    query = { "tokenID": each['tokenID'] }
    newvalues = { "$set": singleLP(each, allPrices) }

    tokenDB.update_one(query, newvalues)
    print(newvalues)
    
end_time = datetime.datetime.now()
print('Duration: {}'.format(end_time - start_time))

