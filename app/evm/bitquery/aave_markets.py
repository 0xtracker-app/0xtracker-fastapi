aave_markets = '''query Main($lendingPool: String!) {\n  protocolData(lendingPoolAddressProvider: $lendingPool) {\n    reserves {\n      underlyingAsset\n      symbol\n      decimals\n      aTokenAddress\n      variableDebtTokenAddress\n      baseLTVasCollateral\n    }\n  }\n}\n'''