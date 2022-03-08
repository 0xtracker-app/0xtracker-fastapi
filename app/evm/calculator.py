from .multicall import Multicall, Call, parsers
from . import uniswapv3
import time
import os
from ..db.schemas import UserRecord
from ..db.crud import create_user_history
from datetime import datetime, timezone

def getLPBalances(staked, totalSupply, reserves, token0, tkn0d, tkn1d, prices):

    quotePrice = prices[token0.lower()]
    userPct = staked / totalSupply
    lp1val = (userPct * int(reserves[0])) / (10**tkn0d)
    lp2val = (userPct * int(reserves[1])) / (10**tkn1d)

    return {'lpTotal': '%s/%s' % (round(lp1val, 2), round(lp2val, 2)), 'lpPrice' : round((lp1val * quotePrice) * 2, 2), 'lpBalances' : [lp1val, lp2val], 'actualStaked' : staked}

def getEBalances(staked, totalSupply, reserves, token0, tkn0d, tkn1d, pricePer, eToken, prices):

    quotePrice = prices[token0.lower()]

    #Check for E11
    if token0.lower() == '0xAcD7B3D9c10e97d0efA418903C0c7669E702E4C0'.lower():
        actualStaked = staked * (pricePer / (10**12))
    else:
        actualStaked = staked * parsers.from_wei(pricePer)

    userPct = actualStaked / totalSupply
    lp1val = (userPct * int(reserves[0])) / (10**tkn0d)
    lp2val = (userPct * int(reserves[1])) / (10**tkn1d)

    return {'lpTotal': round(actualStaked, 4), 'lpPrice' : round((lp1val * quotePrice) * 2, 2), 'elevenBalance' : '(%s/%s)' % (round(lp1val, 2), round(lp2val, 2)), 'lpBalances' : [lp1val, lp2val], 'actualStaked' : actualStaked}

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
        token_price = quote_price[token_address.lower()]
        lp_price += lp_balance * token_price

    return {'lpTotal': '/'.join([str(round(x,2)) for x in lp_values]), 'lpPrice' : lp_price, 'actualStaked' : token_data['staked'], 'tokenSymbols' : token_data['balancerSymbols'], 'lpBalances' : lp_values, 'tokenPair' : "/".join(token_data['balancerSymbols'])}

def get_bancor_ratio(token_data,quote_price):

    userPct = token_data['staked'] / token_data['totalSupply']

    lp_multiplier = 1 / token_data['bancorWeights'][0]

    lp_values = []
    
    for i, each in enumerate(token_data['bancorBalances']):
        lpvalue = (userPct * int(each)) / (10**token_data['bancorDecimals'][i])
        lp_values.append(lpvalue)
    
    lp_price = 0

    for i,lp_balance in enumerate(lp_values):
        token_address = token_data['bancorTokens'][i]
        token_price = quote_price[token_address.lower()]
        lp_price += lp_balance * token_price

    return {'lpTotal': '/'.join([str(round(x,2)) for x in lp_values]), 'lpPrice' : lp_price, 'actualStaked' : token_data['staked'], 'tokenSymbols' : token_data['bancorSymbols'], 'lpBalances' : lp_values, 'tokenPair' : "/".join(token_data['bancorSymbols'])}
    

async def calculate_prices(lastReturn, prices, farm_data, wallet, mongo_client, pdb):

    finalResponse = lastReturn
    rewardToken = farm_data['rewardToken']
    farm_network = farm_data['network']
    
    for f in lastReturn:
        farmAdd = f

        for x in lastReturn[f]['userData']:

            if 'pendingNerve' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingNRVAmount'] = round((finalResponse[f]['userData'][x]['pendingNerve'] * finalResponse[f]['userData'][x]['nerveMultipler']) * prices['0x42f6f551ae042cbe50c739158b4f0cac0edb9096'.lower()], 2)
                finalResponse[f]['userData'][x]['pendingELE'] = round(finalResponse[f]['userData'][x]['pending'] * prices[rewardToken.lower()], 2)
                finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pendingELE'] + finalResponse[f]['userData'][x]['pendingNRVAmount'], 2)

            if x == 'bingoBoard':
                if 'pending' in finalResponse[f]['userData'][x]:
                    finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices['0x579A6277a6c2c63a5b25006F63Bce5DC8D9c25e7'.lower()], 2)

            if 'rewardToken' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[lastReturn[f]['userData'][x]['rewardToken'].lower()], 2)

            elif 'gambitRewards' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingAmount'] = 0
                for i, gr in enumerate(lastReturn[f]['userData'][x]['gambitRewards']):
                    if 'valueOfAsset' in finalResponse[f]['userData'][x]['gambitRewards'][i]:
                        finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount'] = gr['pending'] * gr['valueOfAsset']
                    else:
                        finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount'] = gr['pending'] * prices[gr['token'].lower()]
                    if x not in ['0xA2A065DBCBAE680DF2E6bfB7E5E41F1f1710e63b', 'VAULTS']:
                        finalResponse[f]['userData'][x]['pendingAmount'] += finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount']

            elif 'pendingNerve' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingNRVAmount'] = round((finalResponse[f]['userData'][x]['pendingNerve'] * finalResponse[f]['userData'][x]['nerveMultipler']) * prices['0x42f6f551ae042cbe50c739158b4f0cac0edb9096'.lower()], 2)
            
            elif 'pendingBunny' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingBunnyAmount'] = round(finalResponse[f]['userData'][x]['pendingBunny'] * prices['0xc9849e6fdb743d08faee3e34dd2d1bc69ea11a51'.lower()], 2)
                finalResponse[f]['userData'][x]['pendingRewardAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[lastReturn[f]['userData'][x]['rewardToken'].lower()], 2)
                finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pendingBunnyAmount'] + finalResponse[f]['userData'][x]['pendingRewardAmount'], 2)

            elif 'pendingMerlin' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingMerlinAmount'] = round(finalResponse[f]['userData'][x]['pendingMerlin'] * prices['0xda360309c59cb8c434b28a91b823344a96444278'.lower()], 2)
                finalResponse[f]['userData'][x]['pendingRewardAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[lastReturn[f]['userData'][x]['rewardToken'].lower()], 2)
                finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pendingMerlinAmount'] + finalResponse[f]['userData'][x]['pendingRewardAmount'], 2)
            
            elif 'pending' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingAmount'] = round(finalResponse[f]['userData'][x]['pending'] * prices[rewardToken.lower()], 2)
            else:
                finalResponse[f]['userData'][x]['pendingAmount'] = 0
                finalResponse[f]['userData'][x]['pending'] = 0


            if 'e11token' in lastReturn[f]['userData'][x]:
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
                    finalResponse[f]['userData'][x]['tokenSymbols'] = [lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s']]
            if 'reserves' in lastReturn[f]['userData'][x]:

                    if 'getPricePerFullShare' in lastReturn[f]['userData'][x]:
                        stakedAmount = lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getPricePerFullShare']
                    elif 'getRatio' in finalResponse[f]['userData'][x]:
                        stakedAmount = lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getRatio']
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
                    finalResponse[f]['userData'][x]['tokenSymbols'] = [lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s']]
                    
                    if 'getPricePerFullShare' in lastReturn[f]['userData'][x]:
                        finalResponse[f]['userData'][x]['elevenBalance'] = '(%s)' % (finalResponse[f]['userData'][x]['lpTotal'])
                        finalResponse[f]['userData'][x]['lpTotal'] = round(lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getPricePerFullShare'], 4)
                        finalResponse[f]['userData'][x]['actualStaked'] = lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getPricePerFullShare']
                    
                    if 'getRatio' in lastReturn[f]['userData'][x]:
                        finalResponse[f]['userData'][x]['elevenBalance'] = '(%s)' % (finalResponse[f]['userData'][x]['lpTotal'])
                        finalResponse[f]['userData'][x]['lpTotal'] = round(lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getRatio'], 4)
                        finalResponse[f]['userData'][x]['actualStaked'] = lastReturn[f]['userData'][x]['staked'] * lastReturn[f]['userData'][x]['getRatio']
                   
            else:
                    # if lastReturn[f]['userData'][x]['token0'].lower() in ['0x86aFa7ff694Ab8C985b79733745662760e454169'.lower(), '0x049d68029688eAbF473097a2fC38ef61633A3C7A'.lower(), '0x10a450A21B79c3Af78fb4484FF46D3E647475db4'.lower(), '0x7C9e73d4C71dae564d41F78d56439bB4ba87592f'.lower(), '0x02dA7035beD00ae645516bDb0c282A7fD4AA7442'.lower()]:
                    #     quotePrice = 1
                    # elif lastReturn[f]['userData'][x]['token0'].lower() == '0xdff88a0a43271344b760b58a35076bf05524195c'.lower():
                    #     quotePrice = getPHBprice()
                    # elif lastReturn[f]['userData'][x]['token0'].lower() == '0x28060854AC19391dF6C69Df430cAba4506181d56'.lower():
                    #     quotePrice = prices['0xee814f5b2bf700d2e843dc56835d28d095161dd9']
                    # elif lastReturn[f]['userData'][x]['token0'].lower() == '0xf6488205957f0b4497053d6422F49e27944eE3Dd'.lower():
                    #     quotePrice = prices['0x2090c8295769791ab7A3CF1CC6e0AA19F35e441A'] * getJetValue()
                    # elif lastReturn[f]['userData'][x]['token0'].lower() == '0x9cb73F20164e399958261c289Eb5F9846f4D1404'.lower():
                    #     quotePrice = float(get_four_belt()['0x9cb73F20164e399958261c289Eb5F9846f4D1404'])
                    # elif lastReturn[f]['userData'][x]['token0'].lower() == '0x92d5ebf3593a92888c25c0abef126583d4b5312e'.lower():
                    #     quotePrice = get_atricryptos_price('ftm', '0x92d5ebf3593a92888c25c0abef126583d4b5312e',6,'uint256,int128')
                    if 'zombieOverride' in lastReturn[f]['userData'][x]:
                        if lastReturn[f]['userData'][x]['zombieOverride'] is True:
                            quotePrice = prices['0x50ba8bf9e34f0f83f96a340387d1d3888ba4b3b5'.lower()]
                        else:
                            quotePrice = prices[lastReturn[f]['userData'][x]['token0'].lower()] if lastReturn[f]['userData'][x]['token0'].lower() in prices else 0.1
                    else:
                        quotePrice = prices[lastReturn[f]['userData'][x]['token0'].lower()] if lastReturn[f]['userData'][x]['token0'].lower() in prices else 0.1

                    # if 'curve_pool_token' in lastReturn[f]['userData'][x]:
                    #     if lastReturn[f]['userData'][x]['curve_pool_token'] == '0x8096ac61db23291252574d49f036f0f9ed8ab390':
                    #         quotePrice = get_atricryptos_price()

                    singleStake = lastReturn[f]['userData'][x]['staked']

                    if 'e11token' in finalResponse[f]['userData'][x]:
                        if lastReturn[f]['userData'][x]['e11token'].lower() == '0xAcD7B3D9c10e97d0efA418903C0c7669E702E4C0'.lower():
                            fullStake = parsers.from_custom(lastReturn[f]['userData'][x]['pricePer'], 12) * singleStake
                        else:
                            fullStake = parsers.from_wei(lastReturn[f]['userData'][x]['pricePer']) * singleStake

                            if 'virtualPrice' in lastReturn[f]['userData'][x]:
                                fullStake = fullStake * lastReturn[f]['userData'][x]['virtualPrice']
                        

                        finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                        finalResponse[f]['userData'][x]['actualStaked'] = fullStake
                        
                        # if lastReturn[f]['userData'][x]['e11token'].lower() == '0xdaf66c0b7e8e2fc76b15b07ad25ee58e04a66796'.lower():
                        #     inchBNBPrice = beefyPrices['1inch-1inch-bnb']

                        #     finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * inchBNBPrice, 2)
                        
                        # else:    
                        #     finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)

                        finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                    elif 'fulcrumToken' in finalResponse[f]['userData'][x]:
                        fullStake = lastReturn[f]['userData'][x]['fulcrumToken'] * singleStake
                        finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                        finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                        finalResponse[f]['userData'][x]['actualStaked'] = fullStake
                    elif 'swap' in finalResponse[f]['userData'][x]:
                        if 'pricePer' in finalResponse[f]['userData'][x]:
                            singleStake = singleStake * parsers.from_wei(finalResponse[f]['userData'][x]['pricePer'])
                        fullStake = singleStake * finalResponse[f]['userData'][x]['virtualPrice']
                        finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                        finalResponse[f]['userData'][x]['actualStaked'] = fullStake
                        finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                    elif 'curve_pool_token' in finalResponse[f]['userData'][x]:
                        fullStake = singleStake * finalResponse[f]['userData'][x]['virtualPrice']
                        if 'getRatio' in finalResponse[f]['userData'][x]:
                            fullStake = fullStake * finalResponse[f]['userData'][x]['getRatio']
                        if 'getPricePerFullShare' in finalResponse[f]['userData'][x]:
                            fullStake = fullStake * finalResponse[f]['userData'][x]['getPricePerFullShare']
                        finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                        finalResponse[f]['userData'][x]['actualStaked'] = fullStake
                        finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)                            
                    elif 'getPricePerFullShare' in finalResponse[f]['userData'][x]:
                        fullStake = singleStake * finalResponse[f]['userData'][x]['getPricePerFullShare']
                        finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                        finalResponse[f]['userData'][x]['actualStaked'] = fullStake
                        finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                    elif 'getRatio' in finalResponse[f]['userData'][x]:
                        fullStake = singleStake * finalResponse[f]['userData'][x]['getRatio']
                        finalResponse[f]['userData'][x]['lpTotal'] = round(fullStake, 4)
                        finalResponse[f]['userData'][x]['actualStaked'] = fullStake
                        finalResponse[f]['userData'][x]['lpPrice'] = round(fullStake * quotePrice, 2)
                    elif 'balancerBalances' in finalResponse[f]['userData'][x]:
                        finalResponse[f]['userData'][x].update(get_balancer_ratio(finalResponse[f]['userData'][x], prices))
                    elif 'bancorBalances' in finalResponse[f]['userData'][x]:
                        finalResponse[f]['userData'][x].update(get_bancor_ratio(finalResponse[f]['userData'][x], prices))
                    
                    elif 'slot0' in finalResponse[f]['userData'][x]:
                        finalResponse[f]['userData'][x].update(uniswapv3.get_uniswap_v3_balance(finalResponse[f]['userData'][x], farm_network, prices))
                        finalResponse[f]['userData'][x]['tokenPair'] = '%s/%s' % (lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s'])
                        finalResponse[f]['userData'][x]['tokenSymbols'] = [lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s']]
                        for i, gr in enumerate(lastReturn[f]['userData'][x]['uniswapFee']):
                            finalResponse[f]['userData'][x]['uniswapFee'][i]['pendingAmount'] = gr['pending'] * prices[gr['token'].lower()]
                            finalResponse[f]['userData'][x]['pendingAmount'] += finalResponse[f]['userData'][x]['uniswapFee'][i]['pendingAmount']
                    else:
                        finalResponse[f]['userData'][x]['actualStaked'] = singleStake
                        finalResponse[f]['userData'][x]['lpPrice'] = round(singleStake * quotePrice, 2)

                        if 'borrowed' in finalResponse[f]['userData'][x]:
                            finalResponse[f]['userData'][x]['borrowedUSD'] = finalResponse[f]['userData'][x]['borrowed'] * quotePrice

                    if 'tokenPair' not in finalResponse[f]['userData'][x]:
                        finalResponse[f]['userData'][x]['tokenPair'] = lastReturn[f]['userData'][x]['tkn0s']
                        finalResponse[f]['userData'][x]['tokenSymbols'] = [lastReturn[f]['userData'][x]['tkn0s']]
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
            mintedFAI = await Call("0x67340Bd16ee5649A37015138B3393Eb5ad17c195", ['%s(address)(uint256)' % ('mintedFAIs'), wallet], [['mint', parsers.from_wei ]])()
            finalResponse[f]['mintedFAI'] = mintedFAI['mint']
        
        if 'type' in farm_data:
            finalResponse[f]['type'] = farm_data['type']
            if farm_data['type'] == 'lending':
                finalResponse[f]['availableLimit'] = sum(d['lpPrice'] * d['rate'] for d in finalResponse[f]['userData'].values() if 'rate' in d)
                finalResponse[f]['totalBorrowed'] = sum(d['borrowedUSD'] for d in finalResponse[f]['userData'].values() if 'borrowedUSD' in d)

        if finalResponse[f]['total'] > 0 and os.getenv('USER_WRITE', 'True') == 'True':
            create_user_history(pdb, UserRecord(timestamp=datetime.fromtimestamp(int(time.time()), tz=timezone.utc), farm=f, farm_network=farm_network, wallet=wallet.lower(), dollarvalue=finalResponse[f]['total'], farmnetwork=farm_network ))
            #mongo_client.xtracker['user_data'].update_one({'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : f, 'farm_network' : farm_network}, { "$set": {'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : f, 'farmNetwork' : farm_network, 'dollarValue' : finalResponse[f]['total']} }, upsert=True)
            
    return finalResponse
