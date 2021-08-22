query = "query liquidityPositions($user: Bytes!) {\n  liquidityPositions(where: {user: $user}) {\n    pair {\n      id\n      reserve0\n      reserve1\n      reserveUSD\n      token0 {\n        id\n        symbol\n        derivedETH\n        __typename\n      }\n      token1 {\n        id\n        symbol\n        derivedETH\n        __typename\n      }\n      totalSupply\n      __typename\n    }\n    liquidityTokenBalance\n    __typename\n  }\n}\n"


{"operationName":"liquidityPositions",}