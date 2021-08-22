from hexbytes import HexBytes
from eth_abi import decode_abi
from web3 import Web3
import json
import requests
import time
import os
from dotenv import load_dotenv
from elevenpools import pools
import sqlite3
from farms import farms
import cloudscraper
import asyncio
from aiohttp import ClientSession
from web3.providers.base import JSONBaseProvider
from web3.providers import HTTPProvider
from eth_abi import decode_abi
import psycopg2

##UI Entry
#wallet = '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f'
#address = Web3.toChecksumAddress('0x1ac6c0b955b6d7acb61c9bdf3ee98e0689e07b8a')

w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))

load_dotenv()
bscscanAPI = os.getenv("bscscanAPI")
pcsFactory = '0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F'
WBNB = Web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c')
BUSD = Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')
abiDB = psycopg2.connect(os.getenv("DATABASE_URL"))
BEP20_ABI = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'
bsc_node_address = "https://bsc-dataseed1.binance.org/"
DUST_FILTER = 0.00000000001 * 1e18

def setPool(abi, address):
    try:
        contract = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
    except:
        contract = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=BEP20_ABI)
    poolFunctions = contract.functions
    return(poolFunctions)

def poolInfo(id, pool):
    return pool.poolInfo(id).call()

def pendingRewards(id, pending, pool, wallet):
    return pool[pending](id, wallet).call()

def getABI(contract):
    scraper = cloudscraper.create_scraper()
    try:
        print('Using BSCSCan')
        r = scraper.get('https://api.bscscan.com/api?module=contract&action=getabi&address=%s&apikey=%s' % (contract, bscscanAPI))
        r = json.loads(r.text)
        r = r['result']
    except:
        print('Using BEP20')
        r = BEP20_ABI

    return r

def userStaked(id, wlt, pool):
    staked = pool.stakedWantTokens(id, wlt).call()
    return staked / (10**18)

def totalSupply(pool):
    total = pool.totalSupply().call()
    return total

def getReserves(pool):
    return pool.getReserves().call()

def getBNBprice():
    pcs = setPool(abiRoute(pcsFactory), pcsFactory)
    bnbPrice = pcs.getAmountsOut(1 * 10 ** 18, [WBNB, BUSD]).call()
    #return Web3.fromWei(bnbPrice[1], 'ether')
    return bnbPrice[1] / (10**18)

def getTokenInfobsc(token):
    r = requests.get('https://api.bscscan.com/api?module=token&action=tokeninfo&contractaddress=%s&apikey=%s' % (token,bscscanAPI))
    return json.loads(r.text)

def getDecimals(pool):
    try:
        return pool.decimals().call()
    except:
        return 18

def getPrice(token):

    
    if token == '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c':
        return getBNBprice()
    else:
        BNB = WBNB
        if token == '0x3Ed531BfB3FAD41111f6dab567b33C4db897f991':
            token = '0xacd7b3d9c10e97d0efa418903c0c7669e702e4c0'
        elif token == '0x15B9462d4Eb94222a7506Bc7A25FB27a2359291e':
            token = '0x42f6f551ae042cbe50c739158b4f0cac0edb9096'
        
        tkn = Web3.toChecksumAddress(token)
        pcs = setPool(abiRoute(pcsFactory), pcsFactory)
        tknPool = setPool(abiRoute(token), tkn)
        tkndecimal = 1 * 10 ** getDecimals(tknPool)

        try:
            print('Using 1INCH')
            print(token)
            url = 'https://pathfinder-bsc-56.1inch.exchange/v1.0/quotes?deepLevel=1&mainRouteParts=20&parts=40&virtualParts=40&fromTokenAddress=%s&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount=%s&gasPrice=10000000000&protocolWhiteList=WBNB,BURGERSWAP,PANCAKESWAP,VENUS,JULSWAP,BAKERYSWAP,BSC_ONE_INCH_LP,ACRYPTOS,BSC_DODO,APESWAP,SPARTAN,BELTSWAP,VSWAP,VPEGSWAP,HYPERSWAP,BSC_DODO_V2,SWAPSWIPE,ELLIPSIS_FINANCE,NERVE&protocols=WBNB,BURGERSWAP,PANCAKESWAP,VENUS,JULSWAP,BAKERYSWAP,BSC_ONE_INCH_LP,ACRYPTOS,BSC_DODO,APESWAP,SPARTAN,BELTSWAP,VSWAP,VPEGSWAP,HYPERSWAP,BSC_DODO_V2,SWAPSWIPE,ELLIPSIS_FINANCE,NERVE&deepLevels=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1&mainRoutePartsList=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1&partsList=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1&virtualPartsList=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1' % (token, tkndecimal)
            r = requests.get(url)
            r = json.loads(r.text)
            r = r['bestResult']['routes'][0]['amount']
            tokenPrice = int(r) / (10**18) #/ (10**tknPool.decimals().call())

        except:
            print('Using PCS Factory')
            pair = [tkn, BNB]
            amountIn = 1 * 10 ** getDecimals(tknPool)
            tokenAmounts = pcs.getAmountsOut(amountIn, pair).call()
            tokenPrice = tokenAmounts[1] / (10**18)

        return tokenPrice * getBNBprice()

def userInfo(id, wlt, pool, poolFunction):
    r = pool[poolFunction](id, wlt).call()
    if type(r) is int:
        return r
    else:
        return r[0]

def checkStakes(masterchef, wlt):

    abi = abiRoute(masterchef)
    pool = w3.eth.contract(address=masterchef, abi=abi)
    length = pool.functions.poolLength().call()

    pendingFunction = findPending(masterchef)
    stakedFunction = farms[masterchef]['stakedFunction']

    loop = get_or_create_eventloop()
    future = asyncio.ensure_future(buildCallsTwo(bsc_node_address, range(0, length), wlt, pool, abi, masterchef, stakedFunction))
    userPools = loop.run_until_complete(future)

    active = []
    for i, x in enumerate(userPools):
        if x[0] > DUST_FILTER:
            
            active.append({'id': i, 'stake': x[0] / (10**18) })

    loop = get_or_create_eventloop()
    future = asyncio.ensure_future(buildCallsOne(bsc_node_address, [x['id'] for x in active], pool, abi, masterchef, 'poolInfo'))
    wantTokens = loop.run_until_complete(future)

    for i, x in enumerate(wantTokens):
        active[i]['want'] = Web3.toChecksumAddress(x[0])

    loop = get_or_create_eventloop()
    future = asyncio.ensure_future(buildCallsTwo(bsc_node_address, [x['id'] for x in active], wlt, pool, abi, masterchef, pendingFunction[0]))
    pendingTokens = loop.run_until_complete(future)

    for i, x in enumerate(pendingTokens):
            active[i]['pending'] = x[0] / (10**18)

    loop = get_or_create_eventloop()
    future = asyncio.ensure_future(buildCallsNone(bsc_node_address, [x['want'] for x in active], 'symbol'))
    symbols = loop.run_until_complete(future)

    for i, x in enumerate(symbols):
            active[i]['type'] = x[0]

    for i, symbol in enumerate(active):
        

        if symbol['type'] in ['Cake-LP', 'APE-LP', 'Many-LP']:
            lpPool = setPool(abiRoute(symbol['want']), Web3.toChecksumAddress(symbol['want']))
            reserves = getReserves(lpPool)
            active[i]['token'] = [ { 'address' : lpPool.token0().call(), 'reserve' : reserves[0] } , { 'address' : lpPool.token1().call(), 'reserve' : reserves[1]} ]
            active[i]['totalSupply'] = totalSupply(lpPool) / (10**18)
        else:
            active[i]['token'] = [symbol['want']]

    return active

def tokenSymbol(token):
    tkn = Web3.toChecksumAddress(token)
    tknPool = setPool(abiRoute(token), tkn)
    return tknPool.symbol().call()

def toWei(amount):
    return Web3.toWei(amount, 'ether')

def findPending(address):
    contract = w3.eth.contract(address=address, abi=abiRoute(address))
    funcs = contract.all_functions()

    possiblePending = []
    for each in funcs:
        if 'pending' in type(each).__name__ :
            possiblePending.append(type(each).__name__)

    return possiblePending

def getElevenLP(lpContract, staked):

    print(lpContract)
    contract = setPool(abiRoute(lpContract), lpContract)

    token1 = Web3.toChecksumAddress(contract.token0().call())
    token2 = Web3.toChecksumAddress(contract.token1().call())
    totalSupply = contract.totalSupply().call() / (10**18)
    reserves = contract.getReserves().call()

    tk0 = setPool(abiRoute(token1), token1)
    tk1 = setPool(abiRoute(token2), token2)

    dec0 = getDecimals(tk0)
    dec1 = getDecimals(tk1)

    userPct = staked / totalSupply
    
    lp1 = (userPct * reserves[0]) / (10**dec0)
    lp2 = (userPct * reserves[1]) / (10**dec1)

    if token2 in [BUSD]:
        return [lp2 * 2, round(lp1, 2), round(lp2, 2)]
    else:
        return [(lp1 * getPrice(token1)) * 2, round(lp1, 2), round(lp2, 2)]
        
def getAllStakes(selectedFarms,wallet):
    
    userPools = []
    for x, address in enumerate(selectedFarms):
        # print(x)
        userPools.append( {'name' : farms[address]['name'], 'userData' : []} )
        # print(address)
        allStakes = checkStakes(Web3.toChecksumAddress(address), Web3.toChecksumAddress(wallet))

        rewardPrice = getPrice(farms[address]['rewardToken'])
        

        for stake in allStakes:
            
            userStake = {
            }

            userStake['pending'] = round(stake['pending'], 4)
            userStake['pendingAmount'] = round(stake['pending'], 4) * rewardPrice
            
            if len(stake['token']) == 2:
                
                token0 = setPool(abiRoute(stake['token'][0]['address']), stake['token'][0]['address'])
                
                token1 = setPool(abiRoute(stake['token'][1]['address']), stake['token'][1]['address'])

                    
                dec0 = getDecimals(token0)
                dec1 = getDecimals(token1)

                userStake['tokenPair'] = token0.symbol().call() + '/' + token1.symbol().call()
                print(userStake['tokenPair'])
                userStake['staked'] = round ( stake['stake'], 4)
                
                userPct = stake['stake'] / stake['totalSupply']
                lp1val = ( userPct * stake['token'][0]['reserve']) / (10**dec0)
                lp2val = (userPct * stake['token'][1]['reserve']) / (10**dec1)

                userStake['lpTotal'] = str(round ( lp1val, 2)) + ' / ' + str(round( lp2val, 2 ))
                
                if stake['token'][0]['address'] in [BUSD]:
                    userStake['lpPrice'] = lp2val * 2
                else:
                    userStake['lpPrice'] = (lp1val * getPrice(stake['token'][0]['address'])) * 2
            else:
                contract = setPool(abiRoute(stake['token'][0]), stake['token'][0])
                dec = getDecimals(contract)
                symbol = contract.symbol().call()

                allContracts = {x['tokenDescription'] : x for x in pools}

                userStake['tokenPair'] = symbol
                print(symbol)
                if symbol in [x['tokenDescription'] for x in pools]:
                    #print(allContracts[symbol])
                    contract = setPool(abiRoute(allContracts[symbol]['tokenAddress']), Web3.toChecksumAddress(allContracts[symbol]['tokenAddress']))
                    
                    lpMulti = contract.getPricePerFullShare().call() / (10**18)
                    userStake['staked'] = round( stake['stake'], 4 )
                    userStake['lpTotal'] = round( stake['stake'] * lpMulti, 4)

                    lpContract = Web3.toChecksumAddress(contract.token().call())
                    
                    if 'token2' in allContracts[symbol]:
                        e11 = getElevenLP(lpContract, stake['stake'] * lpMulti)
                        userStake['lpPrice'] = e11[0]
                        userStake['elevenBalance'] = '(%s/%s)' % (e11[1], e11[2]) 
                    else:
                        userStake['lpPrice'] =  getPrice(allContracts[symbol]['token1']) * (stake['stake'] * lpMulti)

                else:
                    print(stake['token'][0])
                    if stake['token'][0] == '0x3Ed531BfB3FAD41111f6dab567b33C4db897f991':
                        #print(stake['stake'], (contract.tokensPerShare().call() / (10**12))) 
                        contract = setPool(abiRoute(stake['token'][0]), Web3.toChecksumAddress(stake['token'][0]))
                        userStake['staked'] = round( stake['stake'], 4 )
                        userStake['lpTotal'] = round(stake['stake'] * (contract.tokensPerShare().call() / (10**12)), 4)
                        userStake['lpPrice'] = getPrice(stake['token'][0]) * userStake['lpTotal']
                    else:
                        userStake['staked'] = round( stake['stake'], 4 )
                        userStake['lpPrice'] = getPrice(stake['token'][0]) * userStake['staked']
            
            userPools[x]['userData'].append(userStake)
        
        userPools[x]['total'] = sum(d['lpPrice'] for d in userPools[x]['userData'] if d) + sum(d['pendingAmount'] for d in userPools[x]['userData'] if d)
        print(userPools)
    return userPools

def abiRoute(contract):
    cursor = abiDB.cursor()
    cursor.execute('SELECT * FROM public."ABI" WHERE contract=%s', (contract,))
    results = cursor.fetchall()

    if len(results) == 0:
        abi = getABI(contract)
        cursor.execute('INSERT INTO public."ABI" VALUES(%s,%s)', (contract, abi))
        abiDB.commit()
        return abi
    else:
        return results[0][1]

def getABItypes(abi, function):
    for fields in abi:
        #print(fields)
        if 'name' in fields:
            if(fields['name'] == function):
                functionName = fields['name']
                #print(functionName)
                functionInputs = []
                for inputs in fields['outputs']:
                    functionInputs.append(inputs['type'])
    return functionInputs

async def async_make_request(session, url, method, params):
    base_provider = JSONBaseProvider()
    request_data = base_provider.encode_rpc_request(method, params)
    async with session.post(url, data=request_data,
                        headers={'Content-Type': 'application/json'}) as response:
        content = await response.read()
    response = base_provider.decode_rpc_response(content)
    return response

async def async_get_request(session, url):
    async with session.get(url, headers={'Content-Type': 'application/json'}) as response:
        content = await response.json()
        r = int(content['bestResult']['routes'][0]['amount']) / (10**18)
    return r

async def buildCallsTwo(node_address, loopOver, functionArgs, contract, abi, master, functionName):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for pool in loopOver:
            to = master
            data = contract.encodeABI(fn_name=functionName, args=[pool ,functionArgs] )
            task = asyncio.ensure_future(async_make_request(session, node_address,
                                                            'eth_call',[{'to' : to , 'data' : data}, 'latest']))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        functionTypes = getABItypes(json.loads(abi), functionName)
        
        r = []
        for each in responses:
            try:
                r.append(decode_abi(functionTypes, HexBytes(each['result'])))
            except:
                r.append((0,))
       
        return r

async def buildCallsOne(node_address, loopOver, contract, abi, master, functionName):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for pool in loopOver:
            to = master
            data = contract.encodeABI(fn_name=functionName, args=[pool] )
            task = asyncio.ensure_future(async_make_request(session, node_address,
                                                            'eth_call',[{'to' : to , 'data' : data}, 'latest']))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        functionTypes = getABItypes(json.loads(abi), functionName)
        
        r = []
        for each in responses:
            r.append(decode_abi(functionTypes, HexBytes(each['result'])))
        
        return r

async def buildCallsNone(node_address, loopOver, functionName):
    tasks = []
    if len(loopOver) == 0:
        return []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for pool in loopOver:
            address = Web3.toChecksumAddress(pool)
            to = address
            abi = abiRoute(address)
            pool = w3.eth.contract(address=address, abi=abi)
            
            data = pool.encodeABI(fn_name=functionName)
            task = asyncio.ensure_future(async_make_request(session, node_address,
                                                            'eth_call',[{'to' : to , 'data' : data}, 'latest']))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        functionTypes = getABItypes(json.loads(abi), functionName)
        
        r = []
        for each in responses:
            r.append(decode_abi(functionTypes, HexBytes(each['result'])))
        
        return r

async def buildGetPrice(loopOver):
    tasks = []
    BNBquote = getBNBprice()
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for token in loopOver:
            tknPool = setPool(abiRoute(token), token)
            tkndecimal = 1 * 10 ** getDecimals(tknPool)
            url = 'https://pathfinder-bsc-56.1inch.exchange/v1.0/quotes?deepLevel=1&mainRouteParts=20&parts=40&virtualParts=40&fromTokenAddress=%s&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount=%s&gasPrice=10000000000&protocolWhiteList=WBNB,BURGERSWAP,PANCAKESWAP,VENUS,JULSWAP,BAKERYSWAP,BSC_ONE_INCH_LP,ACRYPTOS,BSC_DODO,APESWAP,SPARTAN,BELTSWAP,VSWAP,VPEGSWAP,HYPERSWAP,BSC_DODO_V2,SWAPSWIPE,ELLIPSIS_FINANCE,NERVE&protocols=WBNB,BURGERSWAP,PANCAKESWAP,VENUS,JULSWAP,BAKERYSWAP,BSC_ONE_INCH_LP,ACRYPTOS,BSC_DODO,APESWAP,SPARTAN,BELTSWAP,VSWAP,VPEGSWAP,HYPERSWAP,BSC_DODO_V2,SWAPSWIPE,ELLIPSIS_FINANCE,NERVE&deepLevels=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1&mainRoutePartsList=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1&partsList=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1&virtualPartsList=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1' % (token, tkndecimal)
            task = asyncio.ensure_future(async_get_request(session, url, BNBquote))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print(responses)

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
# test = testRun('0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f')

# for each in test:
#     print(each[0])

#print(checkStakes('0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f'))

#getAllStakes(['0x1ac6C0B955B6D7ACb61c9Bdf3EE98E0689e07B8A', '0x7f7Bf15B9c68D23339C31652C8e860492991760d', '0x2EBe8CDbCB5fB8564bC45999DAb8DA264E31f24E', '0x0895196562C7868C5Be92459FaE7f877ED450452'], '0x72Dc7f18ff4B59143ca3D21d73fA6e40D286751f',)
#print(getPrice('0xC7d0CE2961396d02059f06e8DF7Dd37E6809d478'))
##print( findPending('0x2EBe8CDbCB5fB8564bC45999DAb8DA264E31f24E') )

# prices = ['0xa86d305A36cDB815af991834B46aD3d7FbB38523', '0xbda8d53fe0f164915b46cd2ecffd94254b6086a2' ]

# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(buildGetPrice(prices))
# allPrices = loop.run_until_complete(future)

# for each in prices:
#     print(getPrice(each))
