abi = [
    
    """function getProtocolData (address primaryMarketAddress, address exchangeAddress, address pancakePairAddress, address feeDistributorAddress, address account) view returns (
        uint256 blockNumber,
        uint256 blockTimestamp,
        tuple (
            tuple (
                uint256 underlyingToken,
                uint256 quoteToken,
                uint256 tokenM,
                uint256 tokenA,
                uint256 tokenB,
                uint256 chess
            ) balance,
            tuple (
                uint256 primaryMarketUnderlying,
                tuple (
                    uint256 quoteToken,
                    uint256 tokenM,
                    uint256 tokenA,
                    uint256 tokenB
                ) exchange,
                uint256 votingEscrowChess
            ) allowance
        ) wallet,
        tuple (
            bool isFundActive,
            bool isPrimaryMarketActive,
            bool isExchangeActive,
            uint256 fundActivityStartTime,
            uint256 exchangeActivityStartTime,
            uint256 currentDay,
            uint256 currentWeek,
            uint256 dailyProtocolFeeRate,
            uint256 totalShares,
            uint256 totalUnderlying,
            uint256 rebalanceSize,
            uint256 currentInterestRate,
            tuple (
                uint256 ratioM,
                uint256 ratioA2M,
                uint256 ratioB2M,
                uint256 ratioAB,
                uint256 timestamp
            ) lastRebalance
        ) fund,
        tuple (
            uint256 currentCreatingUnderlying,
            uint256 currentRedeemingShares,
            tuple (
                uint256 day,
                uint256 creatingUnderlying,
                uint256 redeemingShares,
                uint256 createdShares,
                uint256 redeemedUnderlying,
                uint256 version
            ) account
        ) primaryMarket,
        tuple (
            tuple (
                uint256 tokenM,
                uint256 tokenA,
                uint256 tokenB
            ) totalDeposited,
            uint256 weightedSupply,
            uint256 workingSupply,
            tuple (
                tuple (
                    uint256 tokenM,
                    uint256 tokenA,
                    uint256 tokenB
                ) available,
                tuple (
                    uint256 tokenM,
                    uint256 tokenA,
                    uint256 tokenB
                ) locked,
                uint256 weightedBalance,
                uint256 workingBalance,
                tuple (
                    uint256 veProportion,
                    uint256 amount,
                    uint256 unlockTime
                ) veSnapshot,
                bool isMaker,
                uint256 chessRewards
            ) account
        ) exchange,
        tuple (
            uint256 chessTotalSupply,
            uint256 chessRate,
            tuple (
                uint256 chessBalance,
                uint256 totalSupply,
                int256 tradingWeekTotalSupply,
                tuple (
                    uint256 amount,
                    uint256 unlockTime
                ) account
            ) votingEscrow,
            tuple (
                uint256 tradingWeekTotalSupply,
                tuple (
                    uint256 amount,
                    uint256 unlockTime,
                    uint256 weight
                ) account
            ) interestRateBallot,
            tuple ( 
                tuple (
                    uint256 claimableRewards,
                    uint256 currentBalance,
                    uint256 amount,
                    uint256 unlockTime
                ) account,
                uint256 currentRewards,
                uint256 currentSupply,
                uint256 tradingWeekTotalSupply,
                tuple[3] (
                    uint256 timestamp,
                    uint256 veSupply,
                    uint256 rewards
                ) historicalRewards
            ) feeDistributor
        ) governance,
        tuple (
            uint112 reserve0,
            uint112 reserve1,
            address token0,
            address token1
        ) pair
    )`,
    `function getUnsettledTrades (address exchangeAddress, address account, uint256[] epochs) view returns (
        tuple[] (
            tuple(uint256 frozenQuote, uint256 effectiveQuote, uint256 reservedBase) takerBuy,
            tuple(uint256 frozenBase, uint256 effectiveBase, uint256 reservedQuote) takerSell,
            tuple(uint256 frozenBase, uint256 effectiveBase, uint256 reservedQuote) makerBuy,
            tuple(uint256 frozenQuote, uint256 effectiveQuote, uint256 reservedBase) makerSell
        ) unsettledTradeM,
        tuple[] (
            tuple(uint256 frozenQuote, uint256 effectiveQuote, uint256 reservedBase) takerBuy,
            tuple(uint256 frozenBase, uint256 effectiveBase, uint256 reservedQuote) takerSell,
            tuple(uint256 frozenBase, uint256 effectiveBase, uint256 reservedQuote) makerBuy,
            tuple(uint256 frozenQuote, uint256 effectiveQuote, uint256 reservedBase) makerSell
        ) unsettledTradeA,
        tuple[] (
            tuple(uint256 frozenQuote, uint256 effectiveQuote, uint256 reservedBase) takerBuy,
            tuple(uint256 frozenBase, uint256 effectiveBase, uint256 reservedQuote) takerSell,
            tuple(uint256 frozenBase, uint256 effectiveBase, uint256 reservedQuote) makerBuy,
            tuple(uint256 frozenQuote, uint256 effectiveQuote, uint256 reservedBase) makerSell
        ) unsettledTradeB
    )"""
]