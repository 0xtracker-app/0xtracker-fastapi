from enum import IntEnum

from construct import Bytes, Padding, Int64ul, Int8ul, Int64sl, Int16ul, Octet, BytesInteger, Int64un, Int16un
from construct import BitsInteger, BitsSwapped, BitStruct, Const, Flag, Computed
from construct import Struct
from solana._layouts.shared import PUBLIC_KEY_LAYOUT
from base64 import b64decode, b64encode
from base58 import b58decode
from solana.publickey import PublicKey
# from borsh_construct import CStruct, Int8ul, Int64ul, U128


def decode_byte_string(byte_string: str, encoding: str = "base64") -> bytes:
    """Decode a encoded string from an RPC Response."""
    b_str = str.encode(byte_string)
    if encoding == "base64":
        return b64decode(b_str)
    if encoding == "base58":
        return b58decode(b_str)

    raise NotImplementedError(f"{encoding} decoding not currently supported.")

def convert_public_key(hash):
    return str(PublicKey(hash))

# Fusion Pools Layout
STAKE_INFO_LAYOUT_V4 = Struct(
    "state" / Int64ul,
    "nonce" / Int64ul,
    "poolLpTokenAccount" / PUBLIC_KEY_LAYOUT,
    "poolRewardTokenAccount" / PUBLIC_KEY_LAYOUT,
    "totalReward" / Int64ul,
    "perShare" / BytesInteger(16,swapped=True),
    "perBlock" / Int64ul,
    "option" / Int8ul,
    "poolRewardTokenAccountB" / PUBLIC_KEY_LAYOUT,
    Padding(7),
    "totalRewardB" / Int64ul,
    "perShareB" / BytesInteger(16,swapped=True),
    "perBlockB" / Int64ul,
    "lastBlock" / Int64ul,
    "owner" / PUBLIC_KEY_LAYOUT
    
)

# RAY Yield Farming
STAKE_INFO_LAYOUT = Struct(
    "state" / Int64ul,
    "nonce" / Int64ul,
    "poolLpTokenAccount" / PUBLIC_KEY_LAYOUT,
    "poolRewardTokenAccount" / PUBLIC_KEY_LAYOUT,
    "owner" / PUBLIC_KEY_LAYOUT,
    "feeOwner" / PUBLIC_KEY_LAYOUT,
    "feeY" / Int64ul,
    "feeX" / Int64ul,
    "totalReward" / Int64ul,
    "rewardPerShareNet" / BytesInteger(16,swapped=True),
    "lastBlock" / Int64ul,
    "rewardPerBlock" / Int64ul
)

# Serum Open Orders Book
ACCOUNT_FLAGS_LAYOUT = BitsSwapped(  # Swap to little endian
    BitStruct(
        "initialized" / Flag,
        "market" / Flag,
        "open_orders" / Flag,
        "request_queue" / Flag,
        "event_queue" / Flag,
        "bids" / Flag,
        "asks" / Flag,
        Const(0, BitsInteger(57)),  # Padding
    )
)

# Serum Open Orders Book
OPEN_ORDERS_LAYOUT = Struct(
    Padding(5),
    "account_flags" / ACCOUNT_FLAGS_LAYOUT,
    "market" / PUBLIC_KEY_LAYOUT,
    "owner" / PUBLIC_KEY_LAYOUT,
    "base_token_free" / Int64ul,
    "base_token_total" / Int64ul,
    "quote_token_free" / Int64ul,
    "quote_token_total" / Int64ul,
    "free_slot_bits" / Bytes(16),
    "is_bid_bits" / Bytes(16),
    "orders" / Bytes(16)[128],
    "client_ids" / Int64ul[128],
    "referrer_rebate_accrued" / Int64ul,
    Padding(7),
)

USER_STAKE_INFO_ACCOUNT_LAYOUT = Struct(
  "state" / Int64ul,
  "poolId" / PUBLIC_KEY_LAYOUT,
  "stakerOwner" / PUBLIC_KEY_LAYOUT,
  "depositBalance" / Int64ul,
  "rewardDebt" / Int64ul,
)

USER_STAKE_INFO_ACCOUNT_LAYOUT_V4 = Struct(
  "state" / Int64ul,
  "poolId" / PUBLIC_KEY_LAYOUT,
  "stakerOwner" / PUBLIC_KEY_LAYOUT,
  "depositBalance" / Int64ul,
  "rewardDebt" / Int64ul,
  "rewardDebtB" / Int64ul
)

SOLFARM_RAYDIUM_VAULT_LAYOUT = Struct(
  "blob" / Octet,
  "authority" / PUBLIC_KEY_LAYOUT,
  "token_program"  / PUBLIC_KEY_LAYOUT,
  "pda_token_account" / PUBLIC_KEY_LAYOUT,
  "pda" / PUBLIC_KEY_LAYOUT,
  "nonce" / Int8ul,
  "info_nonce" / Int8ul,
  "reward_a_nonce" / Int8ul,
  "reward_b_nonce" / Int8ul,
  "swap_to_nonce" / Int8ul,
  "total_vault_balance" / Int64ul,
  "info_account" / PUBLIC_KEY_LAYOUT,
  "lp_token_account" / PUBLIC_KEY_LAYOUT,
  "lp_token_mint" / PUBLIC_KEY_LAYOUT,
  "reward_a_account" / PUBLIC_KEY_LAYOUT,
  "reward_b_account" / PUBLIC_KEY_LAYOUT,
  "swap_to_account" / PUBLIC_KEY_LAYOUT,
  "total_vlp_shares" / Int64ul
)

SOLFARM_RAYDIUM_USER_BALANCE_LAYOUT = Struct(
  "blob" / Octet,
  "owner" / PUBLIC_KEY_LAYOUT,
  "amount" / Int64ul
)

SOLFARM_SABER_VAULT_LAYOUT = Struct(
  "blob" / Octet,
  "authority" / PUBLIC_KEY_LAYOUT,
  "saber_farm_program"  / PUBLIC_KEY_LAYOUT,
  "saber_farm_landlord" / PUBLIC_KEY_LAYOUT,
  "saber_farm_plot" / PUBLIC_KEY_LAYOUT,
  "lp_token_mint" / PUBLIC_KEY_LAYOUT,
  "saber_farm_plot_farmer" / PUBLIC_KEY_LAYOUT,
  "saber_farm_plot_farmer_nonce" / Int8ul,
  "pda_signer" / PUBLIC_KEY_LAYOUT,
  "vault_pda_signer_nonce" / Int8ul,
  "vault_account_nonce" / Int8ul,
  "controller_fee" / Int64ul,
  "platform_fee" / Int64ul,
  "vault_fee" / Int64ul,
  "entrance_fee" / Int64ul,
  "withdrawal_fee" / Int64ul,
  "fee_recipient" / PUBLIC_KEY_LAYOUT,
  "fee_authority" / PUBLIC_KEY_LAYOUT,
  "compound_authority" / PUBLIC_KEY_LAYOUT,
  "total_vault_balance" / Int64ul,
  "total_vlp_shares" / Int64ul
)

SOLFARM_SABER_USER_BALANCE_LAYOUT = Struct(
  "owner" / PUBLIC_KEY_LAYOUT,
  "vault" / PUBLIC_KEY_LAYOUT,
  "shares" / Int64ul,
  "amount" / Int64ul,
  "last_deposit_time" / Int64ul,
)

SABER_FARMER = Struct(
  "authority" / PUBLIC_KEY_LAYOUT,
  "plot_key" / PUBLIC_KEY_LAYOUT,
  "token_vault" / PUBLIC_KEY_LAYOUT,
  "wages_earned" / Int64ul,
  "wages_per_token_paid" / Int64ul
)

SABER_PLOT = Struct(
    'landlord_key' / PUBLIC_KEY_LAYOUT,
    'token_mint_key'/ PUBLIC_KEY_LAYOUT,
    'token_mint_decimals' / Int8ul,
    'famine_ts' / Int64sl,
    'last_update_ts' / Int64sl,
    'rewards_per_tokens_stored' / Int64ul,
    'daily_rewards_rate' / Int64ul,
    'rewards_share' / Int64ul,
    'total_tokens_deposited' / Int64ul,
)

SABER_LANDLORD = Struct(
    'base' / PUBLIC_KEY_LAYOUT,
    'bump' / Int8ul,
    'authority'/ PUBLIC_KEY_LAYOUT,
    'pending_authority'/ PUBLIC_KEY_LAYOUT,
    'num_plots' / Int16ul,
    'daily_rewards_rate' / Int64ul,
    'total_rewards_shares' / Int64ul,
    'mint_proxy_program'/ PUBLIC_KEY_LAYOUT,
    'rewards_token_mint'/ PUBLIC_KEY_LAYOUT
)

RAYDIUM_AMM_V4 = Struct(
  "status" / Int64ul,
  "nonce" / Int64ul,
  "orderNum" / Int64ul,
  "depth" / Int64ul,
  "coinDecimals" / Int64ul,
  "pcDecimals" / Int64ul,
  "state" / Int64ul,
  "resetFlag" / Int64ul,
  "minSize" / Int64ul,
  "volMaxCutRatio" / Int64ul,
  "amountWaveRatio" / Int64ul,
  "coinLotSize" / Int64ul,
  "pcLotSize" / Int64ul,
  "minPriceMultiplier" / Int64ul,
  "maxPriceMultiplier" / Int64ul,
  "systemDecimalsValue" / Int64ul,
  ## Fees
  "minSeparateNumerator" / Int64ul,
  "minSeparateDenominator" / Int64ul,
  "tradeFeeNumerator" / Int64ul,
  "tradeFeeDenominator" / Int64ul,
  "pnlNumerator" / Int64ul,
  "pnlDenominator" / Int64ul,
  "swapFeeNumerator" / Int64ul,
  "swapFeeDenominator" / Int64ul,
  ## OutPutData
  "needTakePnlCoin" / Int64ul,
  "needTakePnlPc" / Int64ul,
  "totalPnlPc" / Int64ul,
  "totalPnlCoin" / Int64ul,
  "poolTotalDepositPc" / BytesInteger(16, signed=False, swapped=True),
  "poolTotalDepositCoin" / BytesInteger(16, signed=False, swapped=True),
  "swapCoinInAmount" / BytesInteger(16, signed=False, swapped=True),
  "swapPcOutAmount" / BytesInteger(16, signed=False, swapped=True),
  "swapCoin2PcFee" / Int64ul,
  "swapPcInAmount" / BytesInteger(16, signed=False, swapped=True),
  "swapCoinOutAmount" / BytesInteger(16, signed=False, swapped=True),
  "swapPc2CoinFee" / Int64ul,

  'rawpoolCoinTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'rawpoolPcTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'rawcoinMintAddress'/ PUBLIC_KEY_LAYOUT,
  'rawpcMintAddress'/ PUBLIC_KEY_LAYOUT,
  'rawlpMintAddress'/ PUBLIC_KEY_LAYOUT,
  'rawammOpenOrders'/ PUBLIC_KEY_LAYOUT,
  'rawserumMarket'/ PUBLIC_KEY_LAYOUT,
  'rawserumProgramId'/ PUBLIC_KEY_LAYOUT,
  'rawammTargetOrders'/ PUBLIC_KEY_LAYOUT,
  'rawpoolWithdrawQueue'/ PUBLIC_KEY_LAYOUT,
  'rawpoolTempLpTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'rawammOwner'/ PUBLIC_KEY_LAYOUT,
  'rawpnlOwner'/ PUBLIC_KEY_LAYOUT,
  'poolCoinTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolCoinTokenAccount)),
  'poolPcTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolPcTokenAccount)),
  'coinMintAddress' / Computed(lambda this: convert_public_key(this.rawcoinMintAddress)),
  'pcMintAddress' / Computed(lambda this: convert_public_key(this.rawpcMintAddress)),
  'lpMintAddress' / Computed(lambda this: convert_public_key(this.rawlpMintAddress)),
  'ammOpenOrders' / Computed(lambda this: convert_public_key(this.rawammOpenOrders)),
  'serumMarket' / Computed(lambda this: convert_public_key(this.rawserumMarket)),
  'serumProgramId' / Computed(lambda this: convert_public_key(this.rawserumProgramId)),
  'ammTargetOrders' / Computed(lambda this: convert_public_key(this.rawammTargetOrders)),
  'poolWithdrawQueue' / Computed(lambda this: convert_public_key(this.rawpoolWithdrawQueue)),
  'poolTempLpTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolTempLpTokenAccount)),
  'ammOwner' / Computed(lambda this: convert_public_key(this.rawammOwner)),
  'pnlOwner' / Computed(lambda this: convert_public_key(this.rawpnlOwner)),
)

RAYDIUM_AMM_V3 = Struct(
  "status" / Int64ul,
  "nonce" / Int64ul,
  "orderNum" / Int64ul,
  "depth" / Int64ul,
  "coinDecimals" / Int64ul,
  "pcDecimals" / Int64ul,
  "state" / Int64ul,
  "resetFlag" / Int64ul,
  "fee" / Int64ul,
  "min_separate" / Int64ul,
  "minSize" / Int64ul,
  "volMaxCutRatio" / Int64ul,
  "pnlRatio" / Int64ul,
  "amountWaveRatio" / Int64ul,
  "coinLotSize" / Int64ul,
  "pcLotSize" / Int64ul,
  "minPriceMultiplier" / Int64ul,
  "maxPriceMultiplier" / Int64ul,
  "needTakePnlCoin" / Int64ul,
  "needTakePnlPc" / Int64ul,
  "totalPnlX" / Int64ul,
  "totalPnlY" / Int64ul,
  "poolTotalDepositPc" / Int64ul,
  "poolTotalDepositCoin" / Int64ul,
  "systemDecimalsValue" / Int64ul,
  'rawpoolCoinTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'rawpoolPcTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'rawcoinMintAddress'/ PUBLIC_KEY_LAYOUT,
  'rawpcMintAddress'/ PUBLIC_KEY_LAYOUT,
  'rawlpMintAddress'/ PUBLIC_KEY_LAYOUT,
  'rawammOpenOrders'/ PUBLIC_KEY_LAYOUT,
  'rawserumMarket'/ PUBLIC_KEY_LAYOUT,
  'rawserumProgramId'/ PUBLIC_KEY_LAYOUT,
  'rawammTargetOrders'/ PUBLIC_KEY_LAYOUT,
  'rawammQuantities'/ PUBLIC_KEY_LAYOUT,
  'rawpoolWithdrawQueue'/ PUBLIC_KEY_LAYOUT,
  'rawpoolTempLpTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'rawammOwner'/ PUBLIC_KEY_LAYOUT,
  'rawpnlOwner'/ PUBLIC_KEY_LAYOUT,
  'rawsrmTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'poolCoinTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolCoinTokenAccount)),
  'poolPcTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolPcTokenAccount)),
  'coinMintAddress' / Computed(lambda this: convert_public_key(this.rawcoinMintAddress)),
  'pcMintAddress' / Computed(lambda this: convert_public_key(this.rawpcMintAddress)),
  'lpMintAddress' / Computed(lambda this: convert_public_key(this.rawlpMintAddress)),
  'ammOpenOrders' / Computed(lambda this: convert_public_key(this.rawammOpenOrders)),
  'serumMarket' / Computed(lambda this: convert_public_key(this.rawserumMarket)),
  'serumProgramId' / Computed(lambda this: convert_public_key(this.rawserumProgramId)),
  'ammTargetOrders' / Computed(lambda this: convert_public_key(this.rawammTargetOrders)),
  'ammQuantities' / Computed(lambda this: convert_public_key(this.rawammQuantities)),
  'poolWithdrawQueue' / Computed(lambda this: convert_public_key(this.rawpoolWithdrawQueue)),
  'poolTempLpTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolTempLpTokenAccount)),
  'ammOwner' / Computed(lambda this: convert_public_key(this.rawammOwner)),
  'pnlOwner' / Computed(lambda this: convert_public_key(this.rawpnlOwner)),
  'srmTokenAccount'/ Computed(lambda this: convert_public_key(this.rawsrmTokenAccount))
)

RAYDIUM_AMM = Struct(
  "status" / Int64ul,
  "nonce" / Int64ul,
  "orderNum" / Int64ul,
  "depth" / Int64ul,
  "coinDecimals" / Int64ul,
  "pcDecimals" / Int64ul,
  "state" / Int64ul,
  "resetFlag" / Int64ul,
  "fee" / Int64ul,
  "minSize" / Int64ul,
  "volMaxCutRatio" / Int64ul,
  "pnlRatio" / Int64ul,
  "amountWaveRatio" / Int64ul,
  "coinLotSize" / Int64ul,
  "pcLotSize" / Int64ul,
  "minPriceMultiplier" / Int64ul,
  "maxPriceMultiplier" / Int64ul,
  "needTakePnlCoin" / Int64ul,
  "needTakePnlPc" / Int64ul,
  "totalPnlX" / Int64ul,
  "totalPnlY" / Int64ul,
  "systemDecimalsValue" / Int64ul,
  'poolCoinTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'poolPcTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'coinMintAddress'/ PUBLIC_KEY_LAYOUT,
  'pcMintAddress'/ PUBLIC_KEY_LAYOUT,
  'lpMintAddress'/ PUBLIC_KEY_LAYOUT,
  'ammOpenOrders'/ PUBLIC_KEY_LAYOUT,
  'serumMarket'/ PUBLIC_KEY_LAYOUT,
  'serumProgramId'/ PUBLIC_KEY_LAYOUT,
  'ammTargetOrders'/ PUBLIC_KEY_LAYOUT,
  'ammQuantities'/ PUBLIC_KEY_LAYOUT,
  'poolWithdrawQueue'/ PUBLIC_KEY_LAYOUT,
  'poolTempLpTokenAccount'/ PUBLIC_KEY_LAYOUT,
  'ammOwner'/ PUBLIC_KEY_LAYOUT,
  'pnlOwner'/ PUBLIC_KEY_LAYOUT,
  'poolCoinTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolCoinTokenAccount)),
  'poolPcTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolPcTokenAccount)),
  'coinMintAddress' / Computed(lambda this: convert_public_key(this.rawcoinMintAddress)),
  'pcMintAddress' / Computed(lambda this: convert_public_key(this.rawpcMintAddress)),
  'lpMintAddress' / Computed(lambda this: convert_public_key(this.rawlpMintAddress)),
  'ammOpenOrders' / Computed(lambda this: convert_public_key(this.rawammOpenOrders)),
  'serumMarket' / Computed(lambda this: convert_public_key(this.rawserumMarket)),
  'serumProgramId' / Computed(lambda this: convert_public_key(this.rawserumProgramId)),
  'ammTargetOrders' / Computed(lambda this: convert_public_key(this.rawammTargetOrders)),
  'ammQuantities' / Computed(lambda this: convert_public_key(this.rawammQuantities)),
  'poolWithdrawQueue' / Computed(lambda this: convert_public_key(this.rawpoolWithdrawQueue)),
  'poolTempLpTokenAccount' / Computed(lambda this: convert_public_key(this.rawpoolTempLpTokenAccount)),
  'ammOwner' / Computed(lambda this: convert_public_key(this.rawammOwner)),
  'pnlOwner' / Computed(lambda this: convert_public_key(this.rawpnlOwner)),
)

DEPOSIT_SCHEMA =  Struct(
    "depositReserve" / PUBLIC_KEY_LAYOUT,
    "depositedAmount" / Int64ul,
    "marketValue" / BytesInteger(16, signed=False, swapped=True),
    "padding" / Padding(32),
    "depositReserveKey" / Computed(lambda this: convert_public_key(this.depositReserve))
)

BORROW_SCHEMA = Struct(
    "borrowReserve" / PUBLIC_KEY_LAYOUT,
    "cumulativeBorrowRateWads" / BytesInteger(16, signed=False, swapped=True),
    "borrowAmountWads" / BytesInteger(16, signed=False, swapped=True),
    "marketValue" / BytesInteger(16, signed=False, swapped=True),
    "padding" / Padding(32),
    "borrowReserveKey" / Computed(lambda this: convert_public_key(this.borrowReserve))
)


SOLEND_OBLIGATION = Struct(
  'version' / Int8ul,
  'slot' / Int64ul,
  'stale' / Int8ul,
  'lendingMarket' / PUBLIC_KEY_LAYOUT,
  'owner' / PUBLIC_KEY_LAYOUT,
  'depositedValue' / BytesInteger(16, signed=False, swapped=True),
  'borrowedValue' / BytesInteger(16, signed=False, swapped=True),
  'allowedBorrowValue' / BytesInteger(16, signed=False, swapped=True),
  'unhealthyBorrowValue' / BytesInteger(16, signed=False, swapped=True),
  Padding(64),
  'depositsLen' / Int8ul,
  'borrowsLen' / Int8ul,
  "deposits" / DEPOSIT_SCHEMA[lambda this: this.depositsLen],
  "borrows" / BORROW_SCHEMA[lambda this: this.borrowsLen],
  "lendingMarketKey" / Computed(lambda this: convert_public_key(this.lendingMarket)),
  "ownerKey" / Computed(lambda this: convert_public_key(this.owner))
)

RESERVE_SCHEMA = Struct(
    "version" / Int8ul,
    "slot" / Int64ul,
    "stale" / Int8ul,
    "lendingMarket" / PUBLIC_KEY_LAYOUT,
    "liquidityMintPubkey" / PUBLIC_KEY_LAYOUT,
    "liquidityMintDecimals" / Int8ul,
    "liquiditySupplyPubkey" / PUBLIC_KEY_LAYOUT,
    "pythOracle" / PUBLIC_KEY_LAYOUT,
    "switchboardOracle" / PUBLIC_KEY_LAYOUT,
    "availableAmount" / Int64ul,
    "borrowedAmountWads" / BytesInteger(16, signed=False, swapped=True),
    "cumulativeBorrowRateWads" / BytesInteger(16, signed=False, swapped=True),
    "marketPrice" / BytesInteger(16, signed=False, swapped=True),
    "collateralMintPubkey" / PUBLIC_KEY_LAYOUT,
    "collateralMintTotalSupply" / Int64ul,
    "collateralSupplyPubkey" / PUBLIC_KEY_LAYOUT,
    "optimalUtilizationRate" / Int8ul,
    "loanToValueRatio" / Int8ul,
    "liquidationBonus" / Int8ul,
    "liquidationThreshold" / Int8ul,
    "minBorrowRate" / Int8ul,
    "optimalBorrowRate" / Int8ul,
    "maxBorrowRate" / Int8ul,
    "borrowFeeWad" / Int64ul,
    "flashLoanFeeWad" / Int64ul,
    "hostFeePercentage" / Int8ul,
    "depositLimit" / Int64ul,
    "borrowLimit" / Int64ul,
    "feeReceiver" / PUBLIC_KEY_LAYOUT,
    "lendingMarketKey" / Computed(lambda this: convert_public_key(this.lendingMarket)),
    "liquidityMintPubkeyKey" / Computed(lambda this: convert_public_key(this.liquidityMintPubkey)),
    "liquiditySupplyPubkeyKey" / Computed(lambda this: convert_public_key(this.liquiditySupplyPubkey)),
    "pythOracleKey" / Computed(lambda this: convert_public_key(this.pythOracle)),
    "switchboardOracleKey" / Computed(lambda this: convert_public_key(this.switchboardOracle)),
    "collateralMintPubkeyKey" / Computed(lambda this: convert_public_key(this.collateralMintPubkey)),
    "collateralSupplyPubkeyKey" / Computed(lambda this: convert_public_key(this.collateralSupplyPubkey)),
    "feeReceiverKey" / Computed(lambda this: convert_public_key(this.feeReceiver))
)

# DEPOSIT_SCHEMA =  CStruct(
#     "depositReserve" / PUBLIC_KEY_LAYOUT,
#     "depositedAmount" / Int64ul,
#     "marketValue" / U128,
#     "padding" / Padding(32)
# )

# BORROW_SCHEMA = CStruct(
#     "borrowReserve" / PUBLIC_KEY_LAYOUT,
#     "cumulativeBorrowRateWads" / U128,
#     "borrowAmountWads" / U128,
#     "marketValue" / U128,
#     "padding" / Padding(32)
# )

# ACCOUNT_SCHEMA = CStruct(
#     "version" / Int8ul,
#     "slot" / Int64ul,
#     "stale" / Int8ul,
#     "lendingMarket"/ PUBLIC_KEY_LAYOUT,
#     "owner" / PUBLIC_KEY_LAYOUT,
#     "depositedValue" / U128,
#     "borrowedValue" / U128,
#     "allowedBorrowValue" / U128,
#     "unhealthyBorrowValue" / U128,
#     "padding" / Padding(64),
#     "depositsLen" / Int8ul,
#     "borrowsLen" / Int8ul,
#     "deposits" / DEPOSIT_SCHEMA[lambda this: this.depositsLen],
#     "borrows" / BORROW_SCHEMA[lambda this: this.borrowsLen]
# )

# LIQUIDATION_TRANSACTION_SCHEMA = CStruct(
#     "instruction" / Int8ul,
#     "liquidityAmount" / Int64ul
# )