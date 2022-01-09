from .helpers import from_custom
import time

def get_balancer_ratio(token_data,quote_price):

    userPct = token_data['staked'] / token_data['total_shares']

    lp_values = []
    
    for i, each in enumerate(token_data['reserves']):
        lpvalue = (userPct * int(each)) / (10**token_data['token_decimals'][i])
        lp_values.append(lpvalue)
    
    lp_price = 0

    for i,lp_balance in enumerate(lp_values):
        token_address = token_data['all_tokens'][i]
        token_price = quote_price[token_address]
        lp_price += lp_balance * token_price

    return {'lpTotal': '/'.join([str(round(x,2)) for x in lp_values]), 'lpPrice' : lp_price, 'lpBalances' : lp_values, 'actualStaked' : token_data['staked']}

async def calculate_prices(lastReturn, prices, wallet, mongo_client, farm_configuraiton):

    finalResponse = lastReturn
    
    for f in lastReturn:
        for x in lastReturn[f]['userData']:
            if 'gambitRewards' in lastReturn[f]['userData'][x]:
                finalResponse[f]['userData'][x]['pendingAmount'] = 0
                for i, gr in enumerate(lastReturn[f]['userData'][x]['gambitRewards']):
                        finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount'] = gr['pending'] * prices[gr['token']]
                        finalResponse[f]['userData'][x]['pendingAmount'] += finalResponse[f]['userData'][x]['gambitRewards'][i]['pendingAmount']


            if 'token1' in lastReturn[f]['userData'][x]:
                    
                    lastReturn[f]['userData'][x].update(get_balancer_ratio(lastReturn[f]['userData'][x], prices))

                    finalResponse[f]['userData'][x]['tokenPair'] = '%s/%s' % (lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s'])
                    finalResponse[f]['userData'][x]['tokenSymbols'] = [lastReturn[f]['userData'][x]['tkn0s'], lastReturn[f]['userData'][x]['tkn1s']]
                   
            else:
                    quotePrice = prices[lastReturn[f]['userData'][x]['token0']] if lastReturn[f]['userData'][x]['token0'] in prices else 0.1
                    singleStake = lastReturn[f]['userData'][x]['staked']
                    
                    finalResponse[f]['userData'][x]['actualStaked'] = singleStake
                    finalResponse[f]['userData'][x]['lpPrice'] = round(singleStake * quotePrice, 2)
                    finalResponse[f]['userData'][x]['lpTotal'] = singleStake
                    
                    if 'tokenPair' not in finalResponse[f]['userData'][x]:
                        finalResponse[f]['userData'][x]['tokenPair'] = lastReturn[f]['userData'][x]['tkn0s']
                        finalResponse[f]['userData'][x]['tokenSymbols'] = [lastReturn[f]['userData'][x]['tkn0s']]

                    if 'borrowed' in finalResponse[f]['userData'][x]:
                        finalResponse[f]['userData'][x]['borrowedUSD'] = finalResponse[f]['userData'][x]['borrowed'] * quotePrice

        try:
            pending_user_amount = sum(d['pendingAmount'] for d in finalResponse[f]['userData'].values() if d)
            finalResponse[f]['poolTotal'] = sum(d['lpPrice'] for d in finalResponse[f]['userData'].values() if d)
            finalResponse[f]['pendingTotal'] = pending_user_amount if pending_user_amount > 0 else 0
            finalResponse[f]['total'] = finalResponse[f]['poolTotal'] + finalResponse[f]['pendingTotal'] if finalResponse[f]['pendingTotal'] >= 0 else finalResponse[f]['poolTotal']
        except:
            finalResponse[f]['poolTotal'] = 0
            finalResponse[f]['pendingTotal'] = 0
            finalResponse[f]['total'] = 0


        if 'type' in farm_configuraiton:
            finalResponse[f]['type'] = farm_configuraiton['type']
            if farm_configuraiton['type'] == 'lending':
                finalResponse[f]['availableLimit'] = sum(d['lpPrice'] * d['rate'] for d in finalResponse[f]['userData'].values() if 'rate' in d)
                finalResponse[f]['totalBorrowed'] = sum(d['borrowedUSD'] for d in finalResponse[f]['userData'].values() if 'borrowedUSD' in d)

        if finalResponse[f]['total'] > 0:
            mongo_client.xtracker['user_data'].update_one({'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : f, 'farm_network' : 'terra'}, { "$set": {'wallet' : wallet.lower(), 'timeStamp' : int(time.time()), 'farm' : f, 'farmNetwork' : 'terra', 'dollarValue' : finalResponse[f]['total']} }, upsert=True)
        
    return finalResponse