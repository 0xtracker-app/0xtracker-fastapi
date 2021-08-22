import asyncio
from aiohttp import ClientSession, ClientTimeout
from farms import farms
from poolext.fulcrumpools import pools as fulcrumpools
from poolext.alpacaTokens import alpacas
from new import getxGMTprice, getDiamondPrices, getWaultPrices, getCGprice, getwSwap, getPCSV1, getPCSV2, get_jet_swap
fulcrmCheck = {x['address'].lower() : x for x in fulcrumpools}



def getPrices(tokenList):
    loop = get_or_create_eventloop()
    future = asyncio.ensure_future(multiCallPrice(tokenList))
    prices = loop.run_until_complete(future)
    prices = {x['token'] : x['price'] for x in prices}
    
    prices['0x85e76cbf4893c1fbcb34dcf1239a91ce2a4cf5a7'] = 1
    prices['0x85E76cbf4893c1fbcB34dCF1239A91CE2A4CF5a7'] = 1
    prices['0xe304ff0983922787Fd84BC9170CD21bF78B16B10'] = getxGMTprice()
    try:
        prices.update({'0x34ea3f7162e6f6ed16bd171267ec180fd5c848da': getDiamondPrices('DND')})
    except:
        prices.update({'0x34ea3f7162e6f6ed16bd171267ec180fd5c848da': 0.1})
    try:
        waultPrices = getWaultPrices()
        prices.update({'0x6ff2d9e5891a7a7c554b80e0d1b791483c78bce9': getCGprice('wault-finance-old')})
        prices.update({'0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21': getwSwap('0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21')})
        prices['0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90'] = getwSwap('0xa9c41a46a6b3531d28d5c32f6633dd2ff05dfb90')
    except:
        prices.update({'0x6ff2d9e5891a7a7c554b80e0d1b791483c78bce9': .01})
        prices.update({'0xb64e638e60d154b43f660a6bf8fd8a3b249a6a21': .01})

    if '0x62ee12e4fe74a815302750913c3c796bca23e40e' in prices:
        prices['0x62ee12e4fe74a815302750913c3c796bca23e40e'] = getPCSV1('0x62ee12e4fe74a815302750913c3c796bca23e40e')

    if '0xef6f50fe05f4ead7805835fd1594406d31b96ed8' in prices:
        prices['0xef6f50fe05f4ead7805835fd1594406d31b96ed8'] = getPCSV2('0xef6f50fe05f4ead7805835fd1594406d31b96ed8')  

    if '0x0487b824c8261462f88940f97053e65bdb498446' in prices:
        prices['0x0487b824c8261462f88940f97053e65bdb498446'] = get_jet_swap('0x0487b824c8261462f88940f97053e65bdb498446') 

    return prices

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

async def async_get_request(session, url, token, decimal, shareAmount):
    #print(token)
    async with session.get(url, headers={'Content-Type': 'application/json'}) as response:
        content = await response.json()
    # print(content)
    #return { 'token' : token, 'price' : (int(content['bestResult']['routes'][0]['amount']) / (10**18)) / 100 }
    try: 
        return { 'token' : token, 'price' : (int(content['toTokenAmount']) / (10**18)) / shareAmount }
    except:
        print('Oracle Error', token, content)
        return { 'token' : token, 'price' : 0 }

async def multiCallPrice(loopOver):
    tasks = []
    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    network_ids={'bsc' : '56', 'matic' : '137', 'kcc' : '321'}
    async with ClientSession() as session:
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
            else:
                tkn = token['token']

            if tkn.lower() == '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c'.lower():
                shareAmount = 1
            else:
                shareAmount = 100
                        
            tkndecimal = shareAmount * 10 ** token['decimal']

            network = network_ids[token['network']]

            if token['network'] == 'bsc':
                quote_token = '0xe9e7cea3dedca5984780bafc599bd69add087d56'
            elif token['network'] == 'matic':
                quote_token = '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'         

            if tkn.lower() in ['0xe9e7cea3dedca5984780bafc599bd69add087d56'.lower(), '0x7343b25c4953f4c57ed4d16c33cbedefae9e8eb9'.lower()] :
                url = f'https://api.1inch.exchange/v3.0/{network}/quote?fromTokenAddress={tkn}&toTokenAddress=0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3&amount={tkndecimal}'
                #url = 'https://pathfinder-bsc-56.1inch.exchange/v1.0/quote?fromTokenAddress=%s&toTokenAddress=0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3&amount=%s&gasPrice=5000000000' % (tkn, tkndecimal)
            else:
                url = f'https://api.1inch.exchange/v3.0/{network}/quote?fromTokenAddress={tkn}&toTokenAddress={quote_token}&amount={tkndecimal}'
                #url = 'https://pathfinder-bsc-56.1inch.exchange/v1.0/quote?fromTokenAddress=%s&toTokenAddress=0xe9e7cea3dedca5984780bafc599bd69add087d56&amount=%s&gasPrice=5000000000' % (tkn, tkndecimal)
 
            task = asyncio.ensure_future(async_get_request(session, url, token['token'], token['decimal'], shareAmount))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return(responses)
