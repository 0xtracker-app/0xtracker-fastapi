async def get_valkyrie_staking(wallet, session, vaults, farm_id, mongodb, network):
    poolKey = farm_id
    cosmos = CosmosNetwork(wallet)
    net_config = cosmos.all_networks[network]

    staking = await asyncio.gather(*[queries.get_osmosis_locked_staking(net_config, session), queries.get_osmosis_unlocked_staking(net_config, session)])

    poolNest = {
        poolKey: {
            'userData': {},
            }
        }

    poolIDs = {}

    for i,each in enumerate(staking[0]['coins']):

            staked_position = {'staked' : 0, 'gambitRewards' : [], 'network' : 'cosmos'}
            want_token = each['denom']
            staked_position.update(await TokenMetaData(address=want_token, mongodb=mongodb, network=net_config, session=session).lookup())
            staked_position['want'] = want_token
            staked_position['staked'] = helpers.from_custom(each['amount'], 18)
        
            poolNest[poolKey]['userData'][want_token] = staked_position
            poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

    for i,each in enumerate(staking[1]['coins']):

            want_token = each['denom']

            if want_token in poolNest[poolKey]['userData']:
                poolNest[poolKey]['userData']['want'] += helpers.from_custom(each['amount'], 18)
            else:
                staked_position = {'staked' : 0, 'gambitRewards' : [], 'network' : 'cosmos'}
                staked_position.update(await TokenMetaData(address=want_token, mongodb=mongodb, network=net_config, session=session).lookup())
                staked_position['want'] = want_token
                staked_position['staked'] = helpers.from_custom(each['amount'], 18)
        
                poolNest[poolKey]['userData'][want_token] = staked_position
                poolIDs['%s_%s_want' % (poolKey, want_token)] = want_token

    if len(poolIDs) > 0:
        return poolIDs, poolNest    
    else:
        return None