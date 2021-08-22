from solana.publickey import PublicKey

def get_pending_rewards(deposit_balance, per_share, decimal, reward_debit, reward_decimal):

    raw_rewards = deposit_balance * per_share / decimal - reward_debit

    return round(from_custom(raw_rewards,reward_decimal),6)

def from_custom(value, decimal):
    return value / (10**decimal)

def public_key_hex(key):
    return bytes(PublicKey(key))

##Wrappers for human readable layouts
def saber_farmer_wrapper(struct):
    data = {
        'authority' : PublicKey(struct.authority),
        'plot_key' : PublicKey(struct.plot_key),
        'token_vault' : PublicKey(struct.token_vault),
        'wages_earned' : struct.wages_earned,
        'wages_per_token_paid' : struct.wages_per_token_paid   
    }
    return data

def standard_account_wrapper(struct):
    data = {
        'mint' : PublicKey(struct.mint),
        'owner' : PublicKey(struct.owner),
        'amount' : struct.amount,
        'delegate_option' : struct.delegate_option,
        'delegate' : PublicKey(struct.delegate),
        'state' : struct.state,
        'is_native_option' : struct.is_native_option,
        'is_native' : struct.is_native,
        'delegated_amount' : struct.delegated_amount,
        'close_authority_option' : struct.close_authority_option,
        'close_authority' : PublicKey(struct.close_authority)
    }
    return data