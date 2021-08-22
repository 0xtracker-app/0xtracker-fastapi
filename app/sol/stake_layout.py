from enum import IntEnum

from construct import Bytes, Padding, Int64ul, Int8ul, Int64sl, Int16ul, Octet, BytesInteger
from construct import BitsInteger, BitsSwapped, BitStruct, Const, Flag
from construct import Struct
from solana._layouts.shared import PUBLIC_KEY_LAYOUT


# Fusion Pools Layout
STAKE_INFO_LAYOUT_V4 = Struct(
    "state" / Int64ul,
    "nonce" / Int64ul,
    "poolLpTokenAccount" / Bytes(32),
    "poolRewardTokenAccount" / Bytes(32),
    "totalReward" / Int64ul,
    "perShare" / BytesInteger(16,swapped=True),
    "perBlock" / Int64ul,
    "option" / Int8ul,
    "poolRewardTokenAccountB" / Bytes(32),
    Padding(7),
    "totalRewardB" / Int64ul,
    "perShareB" / BytesInteger(16,swapped=True),
    "perBlockB" / Int64ul,
    "lastBlock" / Int64ul,
    "owner" / Bytes(32)
)

# RAY Yield Farming
STAKE_INFO_LAYOUT = Struct(
    "state" / Int64ul,
    "nonce" / Int64ul,
    "poolLpTokenAccount" / Bytes(32),
    "poolRewardTokenAccount" / Bytes(32),
    "owner" / Bytes(32),
    "feeOwner" / Bytes(32),
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
    "market" / Bytes(32),
    "owner" / Bytes(32),
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
  "stakerOwner" / Bytes(32),
  "depositBalance" / Int64ul,
  "rewardDebt" / Int64ul
)

USER_STAKE_INFO_ACCOUNT_LAYOUT_V4 = Struct(
  "state" / Int64ul,
  "poolId" / Bytes(32),
  "stakerOwner" / Bytes(32),
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